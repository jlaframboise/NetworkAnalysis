import sqlite3 as sql

sql_connection = sql.connect('sql_db.db')
cursor = sql_connection.cursor()
print("Connected to db")

cursor.execute("select sqlite_version()")
record = cursor.fetchall()
print(f"The sql verison is: {record}")
cursor.close()

sql_create_table_query = """
CREATE TABLE packets (
    id INTEGER PRIMARY KEY,
    iface_type TEXT NOT NULL,
    ip_version TEXT NOT NULL,
    type TEXT NOT NULL,
    src TEXT,
    dest TEXT
)
"""


# cursor = sql_connection.cursor()
# cursor.execute(sql_create_table_query)
# sql_connection.commit()
# print("Table created")
# cursor.close()


packet_data = [
    ('ETHER', 'IPv6', 'TCP', '192.168.0.250:56588', '35.201.71.192:https'),
    ('ETHER', 'IP', 'TCP', 'me', 'google'),
    ('ETHER', 'IPv6', 'TCP', 'me', 'shopify'),
    ('ETHER', 'IPv6', 'UDP', 'shopify', 'me'),
    ('ETHER', 'IP', 'UDP', 'me', 'skynet'),
]

insert_query = """
INSERT INTO packets (iface_type, ip_version, type, src, dest)
VALUES ('ETHER', 'IPv6', 'TCP', '192.168.0.250:56588', '35.201.71.192:https')
"""

cursor = sql_connection.cursor()
cursor.execute(insert_query)
sql_connection.commit()
cursor.close()


cursor = sql_connection.cursor()
cursor.executemany('''INSERT INTO packets (iface_type, ip_version, type, src, dest)
VALUES (?, ?, ?, ?, ?)''', packet_data)
sql_connection.commit()
cursor.close()

# def execute_query(connection, query):
#     cursor = connection.cursor()
#     cursor.execute(query)
#     connection.commit()
#     cursor.close()
