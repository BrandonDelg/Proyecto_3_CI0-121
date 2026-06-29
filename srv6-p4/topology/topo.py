import time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.node import Switch

class P4SwitchBMv2(Switch):
    def __init__(self, name, dpid=None, **kwargs):
        Switch.__init__(self, name, **kwargs)
        self.dpid = dpid

    def start(self, controllers):
        pass

    def stop(self):
        self.cmd('killall simple_switch_grpc')
        Switch.stop(self)

class SRv6Topo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='2026::11/64', mac='00:00:00:00:00:11')
        h2 = self.addHost('h2', ip='2026::42/64', mac='00:00:00:00:00:42')

        r1 = self.addSwitch('r1', cls=P4SwitchBMv2)
        r2 = self.addSwitch('r2', cls=P4SwitchBMv2)
        r3 = self.addSwitch('r3', cls=P4SwitchBMv2)
        r4 = self.addSwitch('r4', cls=P4SwitchBMv2)

        self.addLink(
            h1,
            r1,
            addr1='00:00:00:00:00:11',
            addr2='00:00:00:00:01:01'
        )

        self.addLink(
            r1,
            r2,
            addr1='00:00:00:00:12:01',
            addr2='00:00:00:00:12:02'
        )

        self.addLink(
            r1,
            r3,
            addr1='00:00:00:00:13:01',
            addr2='00:00:00:00:13:03'
        )

        self.addLink(
            r2,
            r4,
            addr1='00:00:00:00:24:02',
            addr2='00:00:00:00:24:04'
        )

        self.addLink(
            r3,
            r4,
            addr1='00:00:00:00:34:03',
            addr2='00:00:00:00:34:04'
        )

        self.addLink(
            r4,
            h2,
            addr1='00:00:00:00:04:42',
            addr2='00:00:00:00:00:42'
        )

def setup_hosts(net):
    h1 = net.get('h1')
    h2 = net.get('h2')

    # IPv6 addresses
    h1.cmd('ip -6 addr add 2026::11/64 dev h1-eth0')
    h2.cmd('ip -6 addr add 2026::42/64 dev h2-eth0')

    h1.cmd('ip -6 neigh replace 2026::42 lladdr 00:00:00:00:01:01 dev h1-eth0')
    h2.cmd('ip -6 neigh replace 2026::11 lladdr 00:00:00:00:04:42 dev h2-eth0')


if __name__ == '__main__':
    setLogLevel('info')
    topo = SRv6Topo()
    net = Mininet(topo=topo, controller=None)
    net.start()

    print("*** Topologia SRv6 levantada con MAC fijas ***")

    setup_hosts(net)

    time.sleep(2)

    CLI(net)
    net.stop()