control MyIngress(
    inout headers hdr,
    inout metadata meta,
    inout standard_metadata_t standard_metadata)
{

    action srv6_transit() {
        if (hdr.srh.segments_left > 0) {

            hdr.srh.segments_left =
                hdr.srh.segments_left - 1;

            hdr.ipv6.dstAddr =
                hdr.segment_list[hdr.srh.segments_left].addr;
        }
    }

    action set_nhop(
        macAddr_t dst_mac,
        egressSpec_t port)
    {
        hdr.ethernet.dstAddr = dst_mac;

        standard_metadata.egress_spec = port;
    }

    action drop() {
        mark_to_drop(standard_metadata);
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
        }

        size = 1024;
    }

    apply {
        srv6_transit_table.apply();
        ipv6_forward.apply();
    }
}