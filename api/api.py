import time, os
import sqlite3 as sql
import scapy.all as scapy
import geoip2.database
from flask import Flask, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

from utils import *

# configure flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*30
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.txt', '.pcap']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SQL_DB'] = 'database/sql_db.db'
app.config['GEO_DB_CITY'] = 'database/GeoLite2-City_20210928/GeoLite2-City.mmdb'


# ensure that there is at least one table in the database
# if there is not, create one
# set the current table correctly
sql_connection = sql.connect(app.config['SQL_DB'])
cursor=sql_connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
initial_table_names = [x[0] for x in cursor.fetchall()]
cursor.close()
sql_connection.close()
if not len(initial_table_names) >= 1:
    # create a default table
    table_name =  "first_table"
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()
    cursor.execute("""
    CREATE TABLE """ + santitize_table_name(table_name) + """ (
        id INTEGER PRIMARY KEY,
        inet_layer TEXT NOT NULL,
        transport_layer TEXT NOT NULL,
        src TEXT NOT NULL,
        dest TEXT NOT NULL,
        src_country TEXT,
        src_city TEXT, 
        src_lat FLOAT,
        src_long FLOAT,
        dest_country TEXT,
        dest_city TEXT,
        dest_lat FLOAT,
        dest_long FLOAT
    )
    """)
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

    app.config['CURRENT_TABLE'] = table_name
else:
    app.config['CURRENT_TABLE'] = initial_table_names[0]





@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/count_packets')
def get_packet_count():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM """+ app.config['CURRENT_TABLE'] + """
    """)
    record = cursor.fetchone()
    cursor.close()
    sql_connection.close()
    return {'packet_count': record[0]}

@app.route('/transport_layer_freqs')
def get_transport_layer_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT transport_layer, COUNT(*)
    FROM """+ app.config['CURRENT_TABLE'] + """
    GROUP BY transport_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}

@app.route('/inet_layer_freqs')
def get_inet_layer_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT inet_layer, COUNT(*)
    FROM """+ app.config['CURRENT_TABLE'] + """
    GROUP BY inet_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}

@app.route('/src_freqs')
def get_src_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT 
        src, 
        COUNT(src) AS `value_count`
    FROM 
        """+ app.config['CURRENT_TABLE'] + """
    GROUP BY 
        src
    ORDER BY
        `value_count` DESC
    LIMIT 10
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}

@app.route('/dest_freqs')
def get_dest_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT 
        dest, 
        COUNT(dest) AS `value_count`
    FROM 
        """+ app.config['CURRENT_TABLE'] + """
    GROUP BY 
        dest
    ORDER BY
        `value_count` DESC
    LIMIT 10
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}


@app.route('/country_freqs')
def get_country_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT 
        src_country, 
        COUNT(src_country) AS `value_count`
    FROM 
        """+ app.config['CURRENT_TABLE'] + """
    GROUP BY 
        src_country
    ORDER BY
        `value_count` DESC
    LIMIT 10
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}


# test that the sql is accessible
@app.route('/sql_version', methods=['GET'])
def get_version():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("select sqlite_version()")
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"sql version": record}

# get packets from sql database
@app.route('/packets', methods=['GET'])
def get_packets():
    limit = request.args.get('packet_limit')
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()
    if limit is None:
        cursor.execute("""
        SELECT * 
        FROM """+ app.config['CURRENT_TABLE'])
    else:
        # use query parameters to avoid sql injection vulnerabilities
        cursor.execute("""
        SELECT * 
        FROM """+ app.config['CURRENT_TABLE'] + """ 
        LIMIT ?""", [limit])
    records = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"packets": records}






@app.route('/create_table', methods=['POST'])
def create_table():
    table_name =  request.form['table_name']
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()
    cursor.execute("""
    CREATE TABLE """ + santitize_table_name(table_name) + """ (
        id INTEGER PRIMARY KEY,
        inet_layer TEXT NOT NULL,
        transport_layer TEXT NOT NULL,
        src TEXT NOT NULL,
        dest TEXT NOT NULL,
        src_country TEXT,
        src_city TEXT, 
        src_lat FLOAT,
        src_long FLOAT,
        dest_country TEXT,
        dest_city TEXT,
        dest_lat FLOAT,
        dest_long FLOAT
    )
    """)
    sql_connection.commit()
    cursor.close()
    sql_connection.close()
    return {'status':'table created I think. '}

@app.route('/get_table_names', methods=['GET'])
def get_table_names():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"table_names": record}

@app.route('/get_current_table_name', methods=['GET'])
def get_current_table_name():
    return {'table_name': app.config['CURRENT_TABLE']}

@app.route('/set_current_table', methods=['POST'])
def set_table():
    new_table_name =  request.form['table_name']
    app.config['CURRENT_TABLE'] = santitize_table_name(new_table_name)
    return {'status':'table set I think. ', 'new_table_name':app.config['CURRENT_TABLE']}

@app.route('/delete_current_table', methods=['DELETE'])
def delete_current_table():
    
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    table_names = [x[0] for x in table_names]
    print(table_names)

    if len(table_names)<2:
        return {'status': 'can not delete table if no other tables exist'}
    else:
        cursor.execute("DROP TABLE " + app.config['CURRENT_TABLE'])
        table_names = [x for x in table_names if x !=app.config['CURRENT_TABLE']]
        app.config['CURRENT_TABLE'] = table_names[0]

    print(table_names)
    print(app.config['CURRENT_TABLE'])
    
    sql_connection.commit()
    cursor.close()
    sql_connection.close()
    
    return {'status':'Deleted table'}


# upload a file
@app.route('/upload', methods=['POST'])
def upload_packet():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return {'status': "successful file upload!"}

# upload a pcap file, sniff it, store it in sql db
@app.route('/add_pcap', methods=['POST'])
def upload_pcap():
    # upload file
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        fpath_out = os.path.join(app.config['UPLOAD_PATH'], filename)
        print(fpath_out)
        uploaded_file.save(fpath_out)
        packets = scapy.sniff(offline=fpath_out)

        # parse packets
        with geoip2.database.Reader(app.config['GEO_DB_CITY']) as reader:
            parsed_packets = parse_packets(packets, geo_reader=reader)

        # save to db
        sql_connection = sql.connect(app.config['SQL_DB'])
        cursor = sql_connection.cursor()
        cursor.executemany("""INSERT INTO """+ app.config['CURRENT_TABLE'] + """ (inet_layer, transport_layer, src, dest, src_country, src_city, src_lat, src_long, dest_country, dest_city, dest_lat, dest_long)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", parsed_packets)
        sql_connection.commit()
        cursor.close()
        sql_connection.close()
    else:
        return {'status': "failed"}


    return {'status': "successful pcap upload!", "data":parsed_packets}



# sniff packets at the server if allowed
# return results
@app.route('/sniff', methods=['GET', 'POST'])
def sniff():
    try:
        packets = scapy.sniff(count=10, iface="enp39s0", filter="ip", timeout=10)
    except PermissionError:
        return {"status":"The server does not have privilege to sniff packets. \
        Run the server as sudo or psudo only if running locally. "}

    # parse packets
    with geoip2.database.Reader(app.config['GEO_DB_CITY']) as reader:
        parsed_packets = parse_packets(packets, geo_reader=reader)

    # save to db
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()
    cursor.executemany("""INSERT INTO """+ app.config['CURRENT_TABLE'] + """ (inet_layer, transport_layer, src, dest, src_country, src_city, src_lat, src_long, dest_country, dest_city, dest_lat, dest_long)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", parsed_packets)
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

    return {"status": f"Succeeded in sniffing and adding {len(parsed_packets)} packets. "}


