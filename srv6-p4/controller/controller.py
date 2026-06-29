import os
import argparse
import p4runtime_sh.shell as shell
from p4runtime_sh.shell import FwdPipeConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P4INFO = os.path.join(BASE_DIR, "build", "srv6.p4info.txtpb")
P4BIN = os.path.join(BASE_DIR, "build", "srv6.json")

pipe_config = FwdPipeConfig(P4INFO, P4BIN)

H1_ADDR = "2026::11"
H2_ADDR = "2026::42"
R2_ADDR = "2026::2"
R3_ADDR = "2026::3"
R4_ADDR = "2026::4"

MAC_H1 = "00:00:00:00:00:11"
MAC_H2 = "00:00:00:00:00:42"

MAC_R1_DESDE_R2 = "00:00:00:00:12:01"
MAC_R1_DESDE_R3 = "00:00:00:00:13:01"
MAC_R4_DESDE_R2 = "00:00:00:00:24:04"
MAC_R4_DESDE_R3 = "00:00:00:00:34:04"


def instalar_reglas(addr, device, reglas):
    shell.setup(
        grpc_addr=addr,
        device_id=device,
        election_id=(device, 1),
        config=pipe_config,
        verbose=False
    )

    for regla in reglas:
        entrada = shell.TableEntry(regla["table"])

        if regla["table"] == "MyIngress.ipv6_forward":
            entrada.match["hdr.ipv6.dstAddr"] = regla["match"] + "/128"
        else:
            entrada.match["hdr.ipv6.dstAddr"] = regla["match"]

        entrada.action = shell.Action(regla["action"])

        if "params" in regla:
            for clave, valor in regla["params"].items():
                entrada.action[clave] = valor

        entrada.insert()
        print("Regla insertada:", regla["table"], regla["match"])

    shell.teardown()


def reglas_r1(ruta):
    if ruta == "A":
        accion = "MyIngress.insert_srh_route_a"
        puerto = "2"
    else:
        accion = "MyIngress.insert_srh_route_b"
        puerto = "3"

    return [
        {
            "table": "MyIngress.srv6_policy",
            "match": H2_ADDR,
            "action": accion,
            "params": {"port": puerto}
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": H1_ADDR,
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": MAC_H1, "port": "1"}
        }
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ruta", choices=["A", "B"], required=True)
    args = parser.parse_args()

    instalar_reglas("127.0.0.1:50051", 1, reglas_r1(args.ruta))

    instalar_reglas("127.0.0.1:50052", 2, [
        {
            "table": "MyIngress.srv6_transit_table",
            "match": R2_ADDR,
            "action": "MyIngress.srv6_transit"
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": R4_ADDR,
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": MAC_R4_DESDE_R2, "port": "2"}
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": H1_ADDR,
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": MAC_R1_DESDE_R2, "port": "1"}
        }
    ])

    instalar_reglas("127.0.0.1:50053", 3, [
        {
            "table": "MyIngress.srv6_transit_table",
            "match": R3_ADDR,
            "action": "MyIngress.srv6_transit"
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": R4_ADDR,
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": MAC_R4_DESDE_R3, "port": "2"}
        },
        {
            "table": "MyIngress.ipv6_forward",
            "match": H1_ADDR,
            "action": "MyIngress.set_nhop",
            "params": {"dst_mac": MAC_R1_DESDE_R3, "port": "1"}
        }
    ])

    instalar_reglas("127.0.0.1:50054", 4, [
    {
        "table": "MyEgress.srv6_egress_table",
        "match": R4_ADDR,
        "action": "MyEgress.srv6_egress_decap",
        "params": {"final_dst": H2_ADDR}
    },
    {
        "table": "MyIngress.ipv6_forward",
        "match": R4_ADDR,
        "action": "MyIngress.set_nhop",
        "params": {"dst_mac": MAC_H2, "port": "3"}
    },
    {
        "table": "MyIngress.ipv6_forward",
        "match": H1_ADDR,
        "action": "MyIngress.set_nhop",
        "params": {"dst_mac": "00:00:00:00:24:02", "port": "1"}
    }
])

    print("Control plane configurado.")
    print("Ruta seleccionada:", args.ruta)


if __name__ == "__main__":
    main()