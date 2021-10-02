import time, os
import sqlite3 as sql
import scapy.all as scapy
from flask import Flask, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

from utils import *


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*30
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.txt', '.pcap']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SQL_DB'] = 'database/sql_db.db'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/count_packets')
def get_packet_count():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM ip_packets
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
    FROM ip_packets
    GROUP BY transport_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"transport_layer_dist": record}

@app.route('/inet_layer_freqs')
def get_inet_layer_freqs():
    sql_connection = sql.connect(app.config['SQL_DB'])
    cursor=sql_connection.cursor()

    cursor.execute("""
    SELECT inet_layer, COUNT(*)
    FROM ip_packets
    GROUP BY inet_layer
    """)
    record = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"inet_layer_dist": record}


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
        parsed_packets = parse_packets(packets)

        # save to db
        sql_connection = sql.connect(app.config['SQL_DB'])
        cursor = sql_connection.cursor()
        cursor.executemany('''INSERT INTO ip_packets (inet_layer, transport_layer, src, dest)
        VALUES (?, ?, ?, ?)''', parsed_packets)
        sql_connection.commit()
        cursor.close()
        sql_connection.close()
    else:
        return {'status': "failed"}


    return {'status': "successful pcap upload!", "data":parsed_packets}




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
        FROM ip_packets""")
    else:
        # use query parameters to avoid sql injection vulnerabilities
        cursor.execute("""
        SELECT * 
        FROM ip_packets 
        LIMIT ?""", [limit])
    records = cursor.fetchall()
    cursor.close()
    sql_connection.close()
    return {"packets": records}

# sniff packets at the server if allowed
# return results
@app.route('/sniff', methods=['GET'])
def sniff():
    try:
        packets = scapy.sniff(count=10, iface="enp39s0", filter="ip")
    except PermissionError:
        return {"status":"The server does not have privilege to sniff packets. \
        Run the server as sudo or psudo only if running locally. "}

    data_for_db = []
    for i in range(len(packets)):
        # print(f"{i}", end='\t')
        packet = packets[i]
        layers = packet.layers()
        try:
            ip_packet = packet[scapy.IP]
            src = ip_packet.src
            dest = ip_packet.dst
            next_layer = ip_packet.payload
            transport_layer_type = str(type(next_layer))
            if "TCP" in transport_layer_type:
                transport_layer_type = "TCP"
            elif "UDP" in transport_layer_type:
                transport_layer_type = "UDP"
            values = ("IP", transport_layer_type, str(src), str(dest))
            data_for_db.append(values)

        except IndexError:
            print("skipped packet with no IP layer")
    return {"packet_values":data_for_db}


