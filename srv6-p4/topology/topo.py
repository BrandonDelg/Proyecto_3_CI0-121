# from mininet.net import Mininet
# from mininet.cli import CLI
# from mininet.node import OVSSwitch
# from mininet.log import setLogLevel
# from mininet.topo import Topo

# class SRv6Topo(Topo):

#     def build(self):

#         h1 = self.addHost('h1')
#         h2 = self.addHost('h2')

#         r1 = self.addSwitch('r1')
#         r2 = self.addSwitch('r2')
#         r3 = self.addSwitch('r3')
#         r4 = self.addSwitch('r4')

#         self.addLink(h1, r1)
#         self.addLink(r1, r2)
#         self.addLink(r1, r3)
#         self.addLink(r2, r4)
#         self.addLink(r3, r4)
#         self.addLink(r4, h2)


# if __name__ == '__main__':
#     setLogLevel('info')

#     topo = SRv6Topo()
#     net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
#     net.start()
#     CLI(net)
#     net.stop()

import time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.node import Switch

# Creamos una clase limpia para obligar a Mininet a levantar el binario P4 correcto
class P4SwitchBMv2(Switch):
    def __init__(self, name, dpid=None, **kwargs):
        Switch.__init__(self, name, **kwargs)
        self.dpid = dpid

    def start(self, controllers):
        # Mapeamos los IDs numéricos para gRPC
        device_id = self.name.replace('r', '')
        grpc_port = 50050 + int(device_id)
        
        # Construimos los argumentos de interfaces físicas de Mininet
        port_args = ""
        for idx, intf in enumerate(self.intfList()):
            if not intf.IP():
                port_args += f"-i {idx+1}:{intf.name} "

        # Ejecutamos el software switch de P4
        cmd = (f"simple_switch_grpc --device-id {device_id} {port_args} "
               f"--thrift-port {9090+int(device_id)} --log-console -- "
               f"--grpc-server-addr 127.0.0.1:{grpc_port} &")
        
        print(f"*** Lanzando BMv2 para {self.name}: {cmd}")
        self.cmd(cmd)

    def stop(self):
        self.cmd('killall simple_switch_grpc')
        Switch.stop(self)

class SRv6Topo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='2026::11/64')
        h2 = self.addHost('h2', ip='2026::42/64')

        # Usamos nuestra clase custom BMv2
        r1 = self.addSwitch('r1', cls=P4SwitchBMv2)
        r2 = self.addSwitch('r2', cls=P4SwitchBMv2)
        r3 = self.addSwitch('r3', cls=P4SwitchBMv2)
        r4 = self.addSwitch('r4', cls=P4SwitchBMv2)

        # Ojo al orden de los links para heredar el mapeo de puertos exacto (1, 2, 3)
        self.addLink(h1, r1)  # r1-eth1 (Puerto 1)
        self.addLink(r1, r2)  # r1-eth2 (Puerto 2) -> r2-eth1 (Puerto 1)
        self.addLink(r1, r3)  # r1-eth3 (Puerto 3) -> r3-eth1 (Puerto 1)
        self.addLink(r2, r4)  # r2-eth2 (Puerto 2) -> r4-eth1 (Puerto 1)
        self.addLink(r3, r4)  # r3-eth2 (Puerto 2) -> r4-eth2 (Puerto 2)
        self.addLink(r4, h2)  # r4-eth3 (Puerto 3)

if __name__ == '__main__':
    setLogLevel('info')
    topo = SRv6Topo()
    net = Mininet(topo=topo, controller=None)
    net.start()
    
    print("*** Esperando que levanten los servidores gRPC...")
    time.sleep(2)
    
    CLI(net)
    net.stop()