from collections import Counter
from prettytable import PrettyTable
from scapy.all import *
import geoip2.database


fname = "cap1.pcapng"

packets = rdpcap(fname)
print(packets[0][IP].src)
srcIP=[]
destIP = []
for pkt in packets:
    if IP in pkt:
        try:
           srcIP.append(pkt[IP].src)
           destIP.append(pkt[IP].dest)
        except:
            pass

#print(srcIP)




geoDataPath = '/home/jacob/Projects/NetworkAnalysis/GeoLite2-City_20200915/GeoLite2-City.mmdb'

dest_cities = []
src_cities = []
with geoip2.database.Reader(geoDataPath) as reader:
    for i in destIP:
        try:
            response=reader.city(i)
            if response.city.name is not None:
                dest_cities.append(response.city.name)
        except:
            pass
    for i in srcIP:
        try:
            response=reader.city(i)
            if response.city.name is not None:
                src_cities.append(response.city.name)
        except:
            pass
        

print(dest_cities)
print(src_cities)