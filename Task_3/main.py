from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

class SimpleTopo(Topo):
    """Simple topology with two hosts and a switch"""
    def build(self):
        h1 = self.addHost('h1')  # Server
        h2 = self.addHost('h2')  # Client
        s1 = self.addSwitch('s1')
        
        self.addLink(h1, s1)
        self.addLink(h2, s1)

def configure_tcp_settings(h1, h2, nagle_enabled, delayed_ack_enabled):
    """Configure TCP_NODELAY and Delayed-ACK on the server and client."""
    
    # Set TCP_NODELAY (Nagle’s Algorithm)
    nagle_value = "0" if nagle_enabled else "1"
    h1.cmd(f"echo {nagle_value} > /proc/sys/net/ipv4/tcp_nodelay")
    h2.cmd(f"echo {nagle_value} > /proc/sys/net/ipv4/tcp_nodelay")
    
    # Set Delayed-ACK
    delayed_ack_value = "1" if delayed_ack_enabled else "0"
    h1.cmd(f"echo {delayed_ack_value} > /proc/sys/net/ipv4/tcp_delack_min")
    h2.cmd(f"echo {delayed_ack_value} > /proc/sys/net/ipv4/tcp_delack_min")

    print(f"[*] TCP_NODELAY = {nagle_value}, Delayed-ACK = {delayed_ack_value}")

def run_experiment(nagle_enabled, delayed_ack_enabled):
    """Sets up Mininet, configures TCP settings, starts the server, client, and captures traffic."""
    setLogLevel('info')  # Display Mininet logs
    net = Mininet(topo=SimpleTopo(), controller=Controller)
    
    net.start()
    
    h1 = net.get('h1')  # Server
    h2 = net.get('h2')  # Client
    
    # Configure TCP settings
    configure_tcp_settings(h1, h2, nagle_enabled, delayed_ack_enabled)
    
    print("[*] Starting TCP Server on h1")
    h1.cmd('python3 server.py &')  # Start server in background
    
    time.sleep(2)  # Allow the server to start
    
    print("[*] Capturing traffic on h1")
    h1.cmd('tcpdump -i h1-eth0 -w capture.pcap &')  # Capture packets

    print("[*] Starting TCP Client on h2")
    h2.cmd('python3 client.py')  # Start client
    
    print("[*] Stopping traffic capture")
    h1.cmd('kill %tcpdump')  # Stop packet capture
    
    print("[*] Experiment complete. Run Wireshark on 'capture.pcap' for analysis.")
    
    CLI(net)  # Open Mininet CLI for manual testing
    net.stop()

if __name__ == '__main__':
    # Change these values based on the test case you want to run
    nagle_enabled = False      # Set True to enable Nagle, False to disable
    delayed_ack_enabled = True # Set True to enable Delayed-ACK, False to disable
    
    run_experiment(nagle_enabled, delayed_ack_enabled)
