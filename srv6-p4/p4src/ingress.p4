control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    // Acción auxiliar para descartar paquetes cuando no haya una regla válida.
    action drop() {
        mark_to_drop(standard_metadata);
    }

    // Inserta un SRH para enviar el paquete por la ruta A: R1 -> R2 -> R4.
    action insert_srh_route_a(egressSpec_t port) {

        // Se activan el SRH y los dos segmentos que se van a incluir.
        hdr.srh.setValid();
        hdr.segment_list[0].setValid();
        hdr.segment_list[1].setValid();

        // El campo Next Header de IPv6 se cambia a 43, que indica Routing Header.
        hdr.ipv6.nextHdr = IPV6_ROUTING_HEADER;


        /*
            Campos básicos del SRH simplificado.
            next_header = 59 indica que no se procesa otro encabezado superior.
            routing_type = 4 corresponde a Segment Routing Header.
            segments_left = 1 indica que todavía queda un segmento por visitar.
        */
        hdr.srh.next_header = NO_NEXT_HEADER;
        hdr.srh.hdr_ext_len = 4;
        hdr.srh.routing_type = SRH_ROUTING_TYPE;
        hdr.srh.segments_left = 1;

        // Ruta A: R1 -> R2 -> R4
        hdr.segment_list[0].addr = R4_ADDR;
        hdr.segment_list[1].addr = R2_ADDR;

        // Se actualiza el destino IPv6 al primer router intermedio de la ruta y se define el puerto de salida del switch.
        hdr.ipv6.dstAddr = hdr.segment_list[1].addr;
        standard_metadata.egress_spec = port;
    }

    //Misma lógica que el pasado pero para enviar el paquete por la ruta B: R1 -> R3 -> R4.
    action insert_srh_route_b(egressSpec_t port) {
        hdr.srh.setValid();
        hdr.segment_list[0].setValid();
        hdr.segment_list[1].setValid();

        hdr.ipv6.nextHdr = IPV6_ROUTING_HEADER;

        hdr.srh.next_header = NO_NEXT_HEADER;
        hdr.srh.hdr_ext_len = 4;
        hdr.srh.routing_type = SRH_ROUTING_TYPE;
        hdr.srh.segments_left = 1;

        // Ruta B: R1 -> R3 -> R4
        hdr.segment_list[0].addr = R4_ADDR;
        hdr.segment_list[1].addr = R3_ADDR;

        hdr.ipv6.dstAddr = hdr.segment_list[1].addr;
        standard_metadata.egress_spec = port;
    }

    /*
        Tabla de política SRv6.
        Según el destino IPv6 original, el control plane puede seleccionar si el paquete usará la ruta A o la ruta B.
    */
    table srv6_policy {
        key = {
            hdr.ipv6.dstAddr: exact;
        }

        actions = {
            insert_srh_route_a;
            insert_srh_route_b;
            drop;
            NoAction;
        }

        size = 1024;
        default_action = NoAction();
    }
    #include "transit.p4"
    apply {
        if (hdr.ipv6.isValid()) {
            srv6_policy.apply();
            if (hdr.srh.isValid()) {
                srv6_transit_table.apply();
            }

            ipv6_forward.apply();
        }
    }
}