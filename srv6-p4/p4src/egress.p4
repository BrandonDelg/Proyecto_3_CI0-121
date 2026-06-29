control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    action srv6_egress_decap(bit<128> final_dst) {
        if (hdr.srh.isValid() && hdr.srh.segments_left == 0) {
            hdr.ipv6.nextHdr = hdr.srh.next_header;
            hdr.ipv6.payloadLen = hdr.ipv6.payloadLen - 40;
            hdr.ipv6.dstAddr = final_dst;

            hdr.srh.setInvalid();
            hdr.segment_list[0].setInvalid();
            hdr.segment_list[1].setInvalid();
        }
    }

    table srv6_egress_table {
        key = {
            hdr.ipv6.dstAddr : exact;
        }

        actions = {
            srv6_egress_decap;
            NoAction;
        }

        size = 256;
        default_action = NoAction();
    }

    apply {
        srv6_egress_table.apply();
    }
}