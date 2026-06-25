import p4runtime_sh.shell as shell
from p4runtime_sh.shell import FwdPipeConfig

P4INFO = "/home/brandondelg/Documents/Proyecto_3_CI0-121/srv6-p4/build/srv6.p4info.txtpb"
P4BIN  = "/home/brandondelg/Documents/Proyecto_3_CI0-121/srv6-p4/build/srv6.json"

pipe_config = FwdPipeConfig(P4INFO, P4BIN)

def program_switch(addr, device, rules):
    shell.setup(
        grpc_addr=addr,
        device_id=device,
        election_id=(device, 1),
        config=pipe_config,
        verbose=False
    )

    for r in rules:
        t = shell.TableEntry(r["table"])

        if r["table"] == "MyIngress.ipv6_forward":
            t.match["hdr.ipv6.dstAddr"] = f"{r['match']}/128"
        else:
            t.match["hdr.ipv6.dstAddr"] = r["match"]

        t.action = shell.Action(r["action"])

        if "params" in r:
            for k, v in r["params"].items():
                t.action[k] = str(v)

        t.insert()
        print(f"Regla insertada con éxito en tabla {r['table']}")

    shell.teardown()

def main():
    program_switch("127.0.0.1:50051", 1, [
        {
            "table": "MyIngress.srv6_policy",
            "match": "2026::4", 
            "action": "MyIngress.insert_srh_route_a",
            "params": {"port": "2"} 
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": "2026::2",
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": "a6:3e:eb:77:e4:be", "port": "2"}
        }
    ])

    program_switch("127.0.0.1:50052", 2, [
        {
            "table": "MyIngress.srv6_transit_table",
            "match": "2026::2",
            "action": "MyIngress.srv6_transit"
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": "2026::4",
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": "1e:a1:5c:42:fe:ee", "port": "2"}
        }
    ])

    program_switch("127.0.0.1:50053", 3, [
        {
            "table": "MyIngress.srv6_transit_table",
            "match": "2026::3",
            "action": "MyIngress.srv6_transit"
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": "2026::4",
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": "06:9e:5e:f7:74:9f", "port": "2"}
        }
    ])

    program_switch("127.0.0.1:50054", 4, [
        {
            "table": "MyIngress.ipv6_forward",
            "match": "2026::4",
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": "aa:bb:cc:dd:ee:ff", "port": "3"} 
        }
    ])

    input("Presioná ENTER para salir...")

if __name__ == "__main__":
    main()