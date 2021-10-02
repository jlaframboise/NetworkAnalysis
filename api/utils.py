import scapy.all as scapy

def parse_packets(packets):
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

    return data_for_db