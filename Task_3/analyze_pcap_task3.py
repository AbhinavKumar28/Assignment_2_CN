from scapy.all import rdpcap, TCP,IP
import numpy as np

# Load the pcap file
pcap_file = "capture_nfdf.pcap"
packets = rdpcap(pcap_file)

# Initialize variables
total_bytes = 0  # For Throughput
useful_bytes = 0  # For Goodput
retransmitted_bytes = 0
packet_sizes = []
tcp_connections = {}  # To track unique connections (srcIP, dstIP, srcPort, dstPort)
retransmissions = 0
total_packets = 0

# Extract timestamps
start_time = packets[0].time
end_time = packets[-1].time
total_time = end_time - start_time  # Total duration of the capture

# Process each packet
for pkt in packets:
    if pkt.haslayer(TCP):
        total_packets += 1
        total_bytes += len(pkt)  # Count total bytes (including retransmissions)

        # Track max packet size
        packet_sizes.append(len(pkt))

        # Extract TCP sequence number
        seq_num = pkt[TCP].seq
        conn_tuple = (pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport)

        # Track unique connections
        if conn_tuple not in tcp_connections:
            tcp_connections[conn_tuple] = set()
        
        # Check for retransmissions (duplicate sequence numbers)
        if seq_num in tcp_connections[conn_tuple]:
            retransmissions += 1
            retransmitted_bytes += len(pkt[TCP].payload)
        else:
            useful_bytes += len(pkt[TCP].payload)  # Goodput only counts first-time data
            tcp_connections[conn_tuple].add(seq_num)

# Compute metrics
throughput = total_bytes / total_time  # Bytes per second
goodput = useful_bytes / total_time  # Only non-retransmitted payload
packet_loss_rate = (retransmissions / total_packets) * 100 if total_packets > 0 else 0
max_packet_size = max(packet_sizes) if packet_sizes else 0

# Print results
print(f"Total Duration: {total_time:.2f} sec")
print(f"Throughput: {throughput:.2f} bytes/sec")
print(f"Goodput: {goodput:.2f} bytes/sec")
print(f"Packet Loss Rate: {packet_loss_rate:.2f}%")
print(f"Maximum Packet Size: {max_packet_size} bytes")
