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

topos = {'srv6': SRv6Topo}