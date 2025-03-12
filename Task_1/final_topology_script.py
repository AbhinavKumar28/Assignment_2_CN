from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep
import argparse

def create_network(option, cc_scheme, link_loss):
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)

    c0 = net.addController('c0')

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    h7 = net.addHost('h7')

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, s2, bw=100)
    net.addLink(h3, s2)
    net.addLink(s2, s3, bw=50, loss=(link_loss if 'd' in option else 0))
    net.addLink(h4, s3)
    net.addLink(h5, s3)
    net.addLink(s3, s4, bw=100)
    net.addLink(h6, s4)
    net.addLink(h7, s4)

    net.start()

    # Ensure all links are active before applying specific configurations
    net.configLinkStatus('s1', 's2', 'up')
    net.configLinkStatus('s2', 's3', 'up')
    net.configLinkStatus('s3', 's4', 'up')
    # net.configLinkStatus('s2', 's4', 'up')
    net.pingAll()

    h7.cmd('iperf3 -s &')
    h7.cmd('sleep 5')

    # iperf_cmd_normal = lambda host, duration: host.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t {duration} -C {cc_scheme} &')

    # iperf_cmd = iperf_cmd_normal

    if option == 'a':
        h1.cmd('tcpdump -i h1-eth0 -w a_reno_3.pcap &')
        result = h1.cmd(f'iperf3 -c {h7.IP()} -p 5201 -b 10M -P 10 -t 150 -C reno')
        print("result")
    elif option == 'b':
        iperf_cmd(h1, 150)
        sleep(15)
        iperf_cmd(h3, 120)
        sleep(15)
        iperf_cmd(h4, 90)
    elif option == 'c1':
        net.configLinkStatus('s1', 's2', 'down')
        iperf_cmd(h3, 150)
    elif option == 'c2a':
        iperf_cmd(h1, 150)
        iperf_cmd(h2, 150)
    elif option == 'c2b':
        iperf_cmd(h1, 150)
        iperf_cmd(h3, 150)
    elif option == 'c2c':
        iperf_cmd(h1, 150)
        iperf_cmd(h3, 150)
        iperf_cmd(h4, 150)
    elif option == 'd1':
        net.configLinkStatus('s1', 's2', 'down')
        iperf_cmd(h3, 150)
    elif option == 'd2a':
        iperf_cmd(h1, 150)
        iperf_cmd(h2, 150)
    elif option == 'd2b':
        iperf_cmd(h1, 150)
        iperf_cmd(h3, 150)
    elif option == 'd2c':
        iperf_cmd(h1, 150)
        iperf_cmd(h3, 150)
        iperf_cmd(h4, 150)
    # CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser()
    parser.add_argument('--option', type=str, required=True, help='Experiment option (a, b, c1, c2a, c2b, c2c, d1, d2)')
    parser.add_argument('--cc', type=str, default='cubic', help='Congestion control scheme (htcp, reno, bic)')
    parser.add_argument('--loss', type=int, default=0, help='Link loss percentage for S2-S3 (only applicable for d1, d2)')
    args = parser.parse_args()
    create_network(args.option, args.cc, args.loss)
