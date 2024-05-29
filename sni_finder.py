import pyshark
from prettytable import PrettyTable
import argparse


def extract_tls_sni(packet):
    try:
        tls_layer = packet.tls
        sni = tls_layer.handshake_extensions_server_name
        return sni
    except AttributeError:
        return None


def main(pcap_file):
    capture = pyshark.FileCapture(pcap_file)

    table = PrettyTable()
    table.field_names = ["Source IP", "Source Port", "Destination IP", "Destination Port", "TLS SNI"]

    for packet in capture:
        if 'IP' in packet and 'TCP' in packet and 'TLS' in packet:
            sni = extract_tls_sni(packet)
            if sni is not None:
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst
                src_port = packet.tcp.srcport
                dst_port = packet.tcp.dstport
                table.add_row([src_ip, src_port, dst_ip, dst_port, sni])

    capture.close()

    print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract TLS SNI field from a PCAP file.')
    parser.add_argument('pcap_file', type=str, help='The path to the PCAP file to analyze.')
    args = parser.parse_args()

    main(args.pcap_file)
