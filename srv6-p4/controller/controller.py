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

        t.match["hdr.ipv6.dstAddr"] = r["match"]
        t.action = shell.Action(r["action"])

        if "params" in r:
            for k, v in r["params"].items():
                t.action[k] = str(v)

        t.insert()

    shell.teardown()


def main():

    print("=== PROGRAMANDO R1 ===")
    program_switch("127.0.0.1:50051", 1, [
        {
            "table": "ipv6_forward",
            "match": "2001:1::1",
            "action": "set_nhop",
            "params": {
                "dst_mac": "a6:3e:eb:77:e4:be",
                "port": "1"
            }
        }
    ])

    print("=== PROGRAMANDO R2 (SRv6 transit) ===")
    program_switch("127.0.0.1:50052", 2, [
        {
            "table": "srv6_transit_table",
            "match": "2001:2::1",
            "action": "srv6_transit"
        },
        {
            "table": "ipv6_forward",
            "match": "2001:4::1",
            "action": "set_nhop",
            "params": {
                "dst_mac": "1e:a1:5c:42:fe:ee",
                "port": "2"
            }
        }
    ])

    print("=== PROGRAMANDO R3 (SRv6 transit) ===")
    program_switch("127.0.0.1:50053", 3, [
        {
            "table": "srv6_transit_table",
            "match": "2001:3::1",
            "action": "srv6_transit"
        },
        {
            "table": "ipv6_forward",
            "match": "2001:4::1",
            "action": "set_nhop",
            "params": {
                "dst_mac": "06:9e:5e:f7:74:9f",
                "port": "2"
            }
        }
    ])

    print("=== PROGRAMANDO R4 ===")
    program_switch("127.0.0.1:50054", 4, [
        {
            "table": "ipv6_forward",
            "match": "2001:4::1",
            "action": "set_nhop",
            "params": {
                "dst_mac": "aa:bb:cc:dd:ee:ff",
                "port": "3"
            }
        }
    ])

    print("TODO PROGRAMADO")
    input("ENTER para salir")


if __name__ == "__main__":
    main()