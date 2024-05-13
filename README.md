# sni-finder
Developed to analyze PCAP (Packet Capture) files precisely to extract and display domain names in the Server Name Indication (SNI) field from TLS network traffic. 

The script utilizes pyshark to parse the PCAP files, argparse to specify the PCAP file path via the command line, and the PrettyTable library to neatly format and present the results.

Argument example:
```
python3 sni_finder.py /path/to/pcap/file.pcap
```

Output example:
```
+--------------+-------------+----------------+------------------+-------------------+
|  Source IP   | Source Port | Destination IP | Destination Port |      TLS SNI      |
+--------------+-------------+----------------+------------------+-------------------+
| 192.168.65.3 |    46638    | 104.16.125.34  |       443        | enabled.tls13.com |
+--------------+-------------+----------------+------------------+-------------------+
```
