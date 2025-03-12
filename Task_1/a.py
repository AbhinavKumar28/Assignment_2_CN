from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np

# Load the pcap file
pcap_file = "D:\ComputerNetworks\Assignment 2\a_reno.pcap"  # Replace with your actual file
packets = rdpcap(pcap_file)

# Extract TCP packets
tcp_packets = [pkt for pkt in packets if pkt.haslayer(TCP)]

# Variables for analysis
start_time = packets[0].time
end_time = packets[-1].time
duration = end_time - start_time

# Throughput Calculation (bps)
time_intervals = np.linspace(int(start_time), int(end_time)+1, num=100)
throughput = []

for t in time_intervals:
    bytes_transferred = sum(len(pkt) for pkt in tcp_packets if pkt.time <= t)
    throughput.append((bytes_transferred * 8) / (t - start_time + 1))  # bps

# Goodput Calculation
useful_data = sum(len(pkt[TCP].payload) for pkt in tcp_packets if pkt[TCP].payload)
goodput = useful_data * 8 / duration  # in bps

# Packet Loss Rate Calculation
seq_numbers = set()
total_packets = len(tcp_packets)
for pkt in tcp_packets:
    seq_numbers.add(pkt[TCP].seq)

unique_seq_numbers = len(seq_numbers)
packet_loss_rate = ((total_packets - unique_seq_numbers) / total_packets) * 100

# Maximum Window Size Achieved
max_window_size = max(pkt[TCP].window for pkt in tcp_packets)

# Plot Throughput
plt.figure(figsize=(10, 5))
plt.plot(time_intervals - start_time, throughput, label="Throughput (bps)")
plt.xlabel("Time (s)")
plt.ylabel("Throughput (bps)")
plt.title("TCP Throughput Over Time")
plt.legend()
plt.grid()
plt.show()

# Print Results
# print(f"Goodput: {goodput / 1e6:.2f} Mbps")
print(f"Goodput: {float(goodput) / 1e6:.2f} Mbps")
print(f"Packet Loss Rate: {packet_loss_rate:.2f}%")
print(f"Maximum Window Size: {max_window_size} bytes")
