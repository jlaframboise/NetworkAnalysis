from scapy import data
import scapy.all as scapy
import sys
import re

print(scapy.IP)

# read packets from pcap file
# packets = scapy.sniff(offline="gov-websites-cap1.pcap")

# sniff packets live ( run with psudo)
packets = scapy.sniff(count=1000, iface="enp39s0", filter="ip")
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
    



print(data_for_db)

import sqlite3 as sql

sql_connection = sql.connect('sql_db.db')
cursor=sql_connection.cursor()
print("Connected to db")


sql_create_table_query="""
CREATE TABLE ip_packets (
    id INTEGER PRIMARY KEY,
    inet_layer TEXT NOT NULL,
    transport_layer TEXT,
    src TEXT,
    dest TEXT
)
"""


# cursor = sql_connection.cursor()
# cursor.execute(sql_create_table_query)
# sql_connection.commit()
# print("Table created")
# cursor.close()


cursor = sql_connection.cursor()
cursor.executemany('''INSERT INTO ip_packets (inet_layer, transport_layer, src, dest)
VALUES (?, ?, ?, ?)''', data_for_db)
sql_connection.commit()
cursor.close()
