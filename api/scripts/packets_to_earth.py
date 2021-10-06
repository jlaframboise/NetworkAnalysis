"""
A program to read in a packet capture file
(from something like Wireshark) and generate a 
kml file that can be imported into Google Earth to
visualize the packet locations. 

Jacob Laframboise

"""


from collections import Counter
from prettytable import PrettyTable
from scapy.all import IP, rdpcap
import geoip2.database


def ip_to_kml(ip, reader):
    """
    A function to take in an ip address, and return 
    a few lines of kml representing the longitude and
    latitude of the point. 

    The reader passed in is of type geoip2.database.Reader
    and this is used to find the location information from
    the ip address
    """
    try:
        response = reader.city(ip)
        longitude = response.location.longitude
        latitude = response.location.latitude
        kml = (
            "<Placemark>\n"
            "<name>%s</name>\n"
            "<Point>\n"
            "<coordinates>%6f,%6f</coordinates>\n"
            "</Point>\n"
            "</Placemark>\n"
        ) % (ip, longitude, latitude)
        return kml
    except:
        # the ip was not found in the database
        return None


def ips_to_line_kml(ip1, ip2, reader):
    """
    This function takes multiple ip addresses, 
    and a geoip2.databse.Reader object and 
    retrieves location information about both addresses. 

    It returns kml for a connecting line between the points. 
    """

    res1 = reader.city(ip1)
    long1 = res1.location.longitude
    lat1 = res1.location.latitude

    res2 = reader.city(ip2)
    long2 = res2.location.longitude
    lat2 = res2.location.latitude

    kml = (
        "<Placemark>\n"
        "<name>%s connecting to %s</name>\n"
        "<LineString>\n"
        "<extrude>1</extrude>\n"
        "<tessellate>1</tessellate>\n"
        "<altitudeMode>relativeToGround</altitudeMode>\n"
        "<coordinates>\n"
        "%6f,%6f,50 %6f,%6f,50\n"
        "</coordinates>\n"
        "</LineString>\n"
        "</Placemark>\n"
    ) % (ip1, ip2, long1, lat1, long2, lat2)

    return kml


def packet_to_kml(packet, reader):
    """
    A function to take in a packet, and a 
    geoip2.databse.Reader object and it will
    try to use the reader to get location information
    on the source and destination ip address. 

    If it succeeds with location information, 
    it creates a kml entry for this point. 

    If both points are found in the database, 
    then it will also create a kml line connecting
    the points. 
    """

    try:
        src_ip = packet[IP].src
        src_kml = ip_to_kml(src_ip, reader)
    except:
        src_kml = None
    try:
        dest_ip = packet[IP].dest
        dest_kml = ip_to_kml(dest_ip, reader)
    except:
        dest_kml = None

    if src_kml is not None and dest_kml is not None:
        connect_kml = ips_to_line_kml(src_ip, dest_ip, reader)
        print("Added connection")
    else:
        connect_kml = None

    return src_kml, dest_kml, connect_kml


if __name__ == '__main__':
    print("Reading packets and generating kml...")

    # setup geo database and read packets.
    geoDataPath = '/home/jacob/Documents/GeoLite2-City_20210928/GeoLite2-City.mmdb'
    fname = "gov-websites-cap1.pcapng"
    packets = rdpcap(fname)

    kmls = ""
    with geoip2.database.Reader(geoDataPath) as reader:
        for packet in packets:
            src_kml, dest_kml, connect_kml = packet_to_kml(packet, reader)
            if src_kml is not None:
                kmls = kmls + src_kml
            if dest_kml is not None:
                kmls = kmls + dest_kml
            if connect_kml is not None:
                kmls = kmls + connect_kml

    # add in extra kml lines to top and bottom of document
    kml_header = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
        "<Document>\n"
    )
    kml_footer = (
        "</Document>\n"
        "</kml>\n"
    )

    kml_doc = kml_header + kmls + kml_footer

    print("Kml generated! Writing to file...")

    # write the kml document to file for import into
    # Google Earth
    f = open("kml_out.kml", 'w')
    f.write(kml_doc)
    f.close()

    print("Complete. ")
