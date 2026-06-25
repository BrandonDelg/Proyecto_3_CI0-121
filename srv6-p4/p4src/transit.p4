action srv6_transit() {

    if (hdr.srh.segments_left > 0) {

        hdr.srh.segments_left =
            hdr.srh.segments_left - 1;

        if (hdr.srh.segments_left == 0) {
            hdr.ipv6.dstAddr =
                hdr.segment_list[0].addr;
        }
    }
}

action set_nhop(
    macAddr_t dst_mac,
    egressSpec_t port)
{
    hdr.ethernet.dstAddr = dst_mac;
    standard_metadata.egress_spec = port;
}

table srv6_transit_table {

    key = {
        hdr.ipv6.dstAddr : exact;
    }

    actions = {
        srv6_transit;
        NoAction;
    }

    size = 256;
}

table ipv6_forward {

    key = {
        hdr.ipv6.dstAddr : lpm;
    }

    actions = {
        set_nhop;
        drop;
        NoAction;
    }

    size = 1024;
}