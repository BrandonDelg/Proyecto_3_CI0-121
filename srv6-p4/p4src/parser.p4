control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        packet.extract(hdr.ethernet);

        transition select(hdr.ethernet.etherType) {
            ETHERTYPE_IPV6: parse_ipv6;
            default: accept;
        }
    }

    state parse_ipv6 {
        packet.extract(hdr.ipv6);

        // Si el campo nextHdr indica Routing Header, se interpreta como SRH.
        // En caso contrario, el paquete IPv6 se acepta sin SRH.
        transition select(hdr.ipv6.nextHdr) {
            IPV6_ROUTING_HEADER: parse_srh;
            default: accept;
        }
    }

    state parse_srh {
        packet.extract(hdr.srh);
        transition parse_segment_0;
    }

    state parse_segment_0 {
        // Primer segmento de la lista corresponde al destino final del camino SRv6.
        packet.extract(hdr.segment_list[0]);
        transition parse_segment_1;
    }

    state parse_segment_1 {
        // Segundo segmento de la lista corresponde al primer router que debe visitar el paquete.
        packet.extract(hdr.segment_list[1]);
        transition accept;
    }
}