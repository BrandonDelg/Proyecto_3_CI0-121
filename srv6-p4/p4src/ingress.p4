control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action insert_srh_route_a(egressSpec_t port) {
        hdr.srh.setValid();
        hdr.segment_list[0].setValid();
        hdr.segment_list[1].setValid();

        hdr.srh.next_header = hdr.ipv6.nextHdr; 
        hdr.srh.hdr_ext_len = 4;
        hdr.srh.routing_type = SRH_ROUTING_TYPE;
        hdr.srh.segments_left = 1;

        hdr.segment_list[0].addr = R4_ADDR;
        hdr.segment_list[1].addr = R2_ADDR;

        hdr.ipv6.dstAddr = hdr.segment_list[1].addr;
        hdr.ipv6.nextHdr = IPV6_ROUTING_HEADER; 

        standard_metadata.egress_spec = port;
    }

    action insert_srh_route_b(egressSpec_t port) {
        hdr.srh.setValid();
        hdr.segment_list[0].setValid();
        hdr.segment_list[1].setValid();

        hdr.srh.next_header = hdr.ipv6.nextHdr;
        hdr.srh.hdr_ext_len = 4;
        hdr.srh.routing_type = SRH_ROUTING_TYPE;
        hdr.srh.segments_left = 1;

        hdr.segment_list[0].addr = R4_ADDR;
        hdr.segment_list[1].addr = R3_ADDR;

        hdr.ipv6.dstAddr = hdr.segment_list[1].addr;
        hdr.ipv6.nextHdr = IPV6_ROUTING_HEADER;

        standard_metadata.egress_spec = port;
    }

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
            if (!hdr.srh.isValid()) {
                srv6_policy.apply();
            }
            
            if (hdr.srh.isValid()) {
                srv6_transit_table.apply();
            }

            ipv6_forward.apply();
        }
    }
}