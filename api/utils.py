import scapy.all as scapy

def santitize_table_name(table_name_input):
    return ''.join( chr for chr in table_name_input if chr.isalnum() or chr=="_" )

def parse_packets(packets, geo_reader=None):
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

            if geo_reader is not None:
                try:
                    response=geo_reader.city(src)
                    src_city=response.city.name
                    src_country=response.country.name
                    src_long = response.location.longitude
                    src_lat = response.location.latitude
                except:
                    # the ip was not found in the database
                    src_city=src_country=src_long=src_lat=None
                try:
                    response=geo_reader.city(dest)
                    dest_city=response.city.name
                    dest_country=response.country.name
                    dest_long = response.location.longitude
                    dest_lat = response.location.latitude
                except:
                    # the ip was not found in the database
                    dest_city=dest_country=dest_long = dest_lat = None
                values = ("IP", transport_layer_type, str(src), str(dest), src_country, src_city, src_lat, src_long, dest_country, dest_city, dest_lat, dest_long)
            else:
                values = ("IP", transport_layer_type, str(src), str(dest))
            data_for_db.append(values)

        except IndexError:
            print("skipped packet with no IP layer")

    return data_for_db