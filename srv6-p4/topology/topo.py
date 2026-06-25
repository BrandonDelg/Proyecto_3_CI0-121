from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch
from mininet.log import setLogLevel
from mininet.topo import Topo

class SRv6Topo(Topo):

    def build(self):

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        r1 = self.addSwitch('r1')
        r2 = self.addSwitch('r2')
        r3 = self.addSwitch('r3')
        r4 = self.addSwitch('r4')

        self.addLink(h1, r1)
        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r2, r4)
        self.addLink(r3, r4)
        self.addLink(r4, h2)


if __name__ == '__main__':
    setLogLevel('info')

    topo = SRv6Topo()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    net.start()
    CLI(net)
    net.stop()