control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    action srv6_egress_decap() {
        if (hdr.srh.isValid() && hdr.srh.segments_left == 0) {
            hdr.ipv6.nextHdr = hdr.srh.next_header;

            hdr.srh.setInvalid();
            hdr.segment_list[0].setInvalid();
            hdr.segment_list[1].setInvalid();
            hdr.segment_list[2].setInvalid();
            hdr.segment_list[3].setInvalid();
        }
    }

    apply {
        srv6_egress_decap();
    }
}