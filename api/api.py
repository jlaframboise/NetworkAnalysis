"""
This file will comprise the main api for the flask application.
It contains:
1. initialization code
2. GET endpoints
3. POST endpoints
4. DELETE endpoints
5. Tests

This flask api will serve as the backend for a React.js application. 
It will use an sqlite3 database. 

"""


from sqlite3.dbapi2 import Error
import time
import os
import sqlite3 as sql
import scapy.all as scapy
import geoip2.database
from flask import Flask, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

from utils import *

# configure flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*30
app.config['UPLOAD_EXTENSIONS'] = ['.pcap']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SQL_DB'] = 'database/sql_db.db'
app.config['GEO_DB_CITY'] = 'database/GeoLite2-City_20210928/GeoLite2-City.mmdb'


######## Setup Database ########################################################

# ensure that there is at least one table in the database
# if there is not, create one
# set the current table correctly
def init_db():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    initial_table_names = [x[0] for x in cursor.fetchall()]
    cursor.close()
    sql_connection.close()
    if not len(initial_table_names) >= 1:
        # create a default table
        table_name = "first_table"
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

init_db()


######## GET requests #########################################################

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/count_packets')
def get_packet_count():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM """ + app.config['CURRENT_TABLE'] + """
    """)
    record = cursor.fetchone()
    cursor.close()
    sql_connection.close()
    return {'packet_count': record[0]}


@app.route('/transport_layer_freqs')
def get_transport_layer_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT transport_layer, COUNT(*)
    FROM """ + app.config['CURRENT_TABLE'] + """
    GROUP BY transport_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}


@app.route('/inet_layer_freqs')
def get_inet_layer_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT inet_layer, COUNT(*)
    FROM """ + app.config['CURRENT_TABLE'] + """
    GROUP BY inet_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"dist": record}


@app.route('/src_freqs')
def get_src_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT 
        src, 
        COUNT(src) AS `value_count`
    FROM 
        """ + app.config['CURRENT_TABLE'] + """
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
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT 
        dest, 
        COUNT(dest) AS `value_count`
    FROM 
        """ + app.config['CURRENT_TABLE'] + """
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
    cursor = sql_connection.cursor()

    cursor.execute("""
    SELECT 
        src_country, 
        COUNT(src_country) AS `value_count`
    FROM 
        """ + app.config['CURRENT_TABLE'] + """
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
    cursor = sql_connection.cursor()

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
    cursor = sql_connection.cursor()
    if limit is None:
        cursor.execute("""
        SELECT * 
        FROM """ + app.config['CURRENT_TABLE'])
    else:
        # use query parameters to avoid sql injection vulnerabilities
        cursor.execute("""
        SELECT * 
        FROM """ + app.config['CURRENT_TABLE'] + """ 
        LIMIT ?""", [limit])
    records = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"packets": records}


@app.route('/get_table_names', methods=['GET'])
def get_table_names():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"table_names": record}


@app.route('/get_current_table_name', methods=['GET'])
def get_current_table_name():
    return {'table_name': app.config['CURRENT_TABLE']}


######## POST requests ########################################################

@app.route('/create_table', methods=['POST'])
def create_table():
    table_name = request.form['table_name']
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
    return {'status': 'table created'}


@app.route('/set_current_table', methods=['POST'])
def set_table():
    new_table_name = request.form['table_name']
    app.config['CURRENT_TABLE'] = santitize_table_name(new_table_name)
    return {'status': 'table set', 'new_table_name': app.config['CURRENT_TABLE']}

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
        cursor.executemany("""
        INSERT INTO """ + app.config['CURRENT_TABLE'] + """ 
        (inet_layer, transport_layer, src, dest, src_country, src_city, src_lat, 
        src_long, dest_country, dest_city, dest_lat, dest_long)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", parsed_packets)
        sql_connection.commit()
        cursor.close()
        sql_connection.close()
    else:
        return {'status': "failed"}

    return {'status': "successful pcap upload!", "data": parsed_packets}


# sniff packets at the server if allowed
# return results
@app.route('/sniff', methods=['GET', 'POST'])
def sniff():
    try:
        packets = scapy.sniff(count=10, iface="enp39s0",
                              filter="ip", timeout=10)
    except PermissionError:
        return {"status": "The server does not have privilege to sniff packets. \
        Run the server as sudo or psudo only if running locally. "}

    # parse packets
    with geoip2.database.Reader(app.config['GEO_DB_CITY']) as reader:
        parsed_packets = parse_packets(packets, geo_reader=reader)

    # save to db
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()
    cursor.executemany("""INSERT INTO 
    """ + app.config['CURRENT_TABLE'] + """ 
    (inet_layer, transport_layer, src, dest, src_country, src_city, src_lat, 
    src_long, dest_country, dest_city, dest_lat, dest_long)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", parsed_packets)
    sql_connection.commit()
    cursor.close()
    sql_connection.close()

    return {"status": f"Succeeded in sniffing and adding {len(parsed_packets)} packets. "}


######## DELETE requests ######################################################


@app.route('/delete_current_table', methods=['DELETE'])
def delete_current_table():

    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor = sql_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    table_names = [x[0] for x in table_names]

    if len(table_names) < 2:
        return {'status': 'can not delete table if no other tables exist'}
    else:
        cursor.execute("DROP TABLE " + app.config['CURRENT_TABLE'])
        table_names = [x for x in table_names if x !=
                       app.config['CURRENT_TABLE']]
        app.config['CURRENT_TABLE'] = table_names[0]


    sql_connection.commit()
    cursor.close()
    sql_connection.close()

    return {'status': 'Deleted table'}


######## Tests ################################################################
run_tests = True

######## GET tests ##############################

def test_sql_version():
    print("Testing sql version")
    with app.test_client() as tc:
        try:
            res = tc.get("/sql_version").get_json()
            assert res is not None and int(res['sql version'][0][0][0]) >= 3
            return True
        except Error as e:
            print("Failed with error: " + e)
            return False


def test_get_packets():
    print("Testing get_packets")
    with app.test_client() as tc:
        try:
            res = tc.get("/packets").get_json()
            assert res is not None and res['packets'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_packet_count():
    print("Testing get_packet_count")
    with app.test_client() as tc:
        try:
            res = tc.get("/count_packets").get_json()
            assert res is not None and res['packet_count'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_transport_layer_freqs():
    print("Testing transport_layer_freqs")
    with app.test_client() as tc:
        try:
            res = tc.get("/transport_layer_freqs").get_json()
            assert res is not None and res['dist'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_inet_layer_freqs():
    print("Testing inet_layer_freqs")
    with app.test_client() as tc:
        try:
            res = tc.get("/inet_layer_freqs").get_json()
            assert res is not None and res['dist'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_src_freqs():
    print("Testing get_src_freqs")
    with app.test_client() as tc:
        try:
            res = tc.get("/src_freqs").get_json()
            assert res is not None and res['dist'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_dest_freqs():
    print("Testing get_dest_freqs")
    with app.test_client() as tc:
        try:
            res = tc.get("/dest_freqs").get_json()
            assert res is not None and res['dist'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_country_freqs():
    print("Testing get_country_freqs")
    with app.test_client() as tc:
        try:
            res = tc.get("/country_freqs").get_json()
            assert res is not None and res['dist'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_table_names():
    print("Testing get_table_names")
    with app.test_client() as tc:
        try:
            res = tc.get("/get_table_names").get_json()
            assert res is not None and res['table_names'] is not None
            return True
        except:
            print("Failed test")
            return False

def test_get_current_table_name():
    print("Testing get_current_table_name")
    with app.test_client() as tc:
        try:
            res = tc.get("/get_current_table_name").get_json()
            assert res is not None and res['table_name'] is not None
            return True
        except:
            print("Failed test")
            return False


######## POST tests ##############################

def test_create_table():
    print("Testing create_table")
    with app.test_client() as tc:
        try:
            res = tc.post("/create_table", data={
                'table_name': 'test_table_1'
            }).get_json()
            assert res is not None and res['status']=="table created"
            return True
        except:
            print("Failed test")
            return False


def test_set_table():
    print("Testing set_table")
    with app.test_client() as tc:
        try:
            res = tc.post("/set_current_table", data={
                'table_name': 'test_table_1'
            }).get_json()
            assert res is not None and res['status']=="table set"
            return True
        except:
            print("Failed test")
            return False

def test_delete_current_table():
    print("Testing delete_current_table")
    with app.test_client() as tc:
        try:
            res = tc.delete("/delete_current_table").get_json()
            assert res is not None and res['status']=="Deleted table"
            return True
        except:
            print("Failed test")
            return False



if run_tests:
    test_functions = [
        test_sql_version,
        test_get_packets,
        test_get_packet_count,
        test_get_transport_layer_freqs,
        test_get_inet_layer_freqs,
        test_get_src_freqs,
        test_get_dest_freqs,
        test_get_country_freqs,
        test_get_table_names,
        test_get_current_table_name,
        test_create_table,
        test_set_table,
        test_delete_current_table,
    ]
    test_results = []

    for f in test_functions:
        t_result = f()
        test_results.append(t_result)
        print(t_result)
    
    print(f"Passed {sum(test_results)} / {len(test_results)} tests. ")
    print("Failed tests: ")
    for i in range(len(test_results)):
        if not test_results[i]:
            print(test_functions[i])

