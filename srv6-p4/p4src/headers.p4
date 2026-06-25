typedef bit<48> macAddr_t;
typedef bit<9>  egressSpec_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv6_t {
    bit<4>    version;
    bit<8>    trafficClass;
    bit<20>   flowLabel;
    bit<16>   payloadLen;
    bit<8>    nextHdr;
    bit<8>    hopLimit;
    bit<128>  srcAddr;
    bit<128>  dstAddr;
}

header srh_t {
    bit<8> next_header;
    bit<8> hdr_ext_len;
    bit<8> routing_type;
    bit<8> segments_left;
}

header segment_t {
    bit<128> addr;
}

struct headers {
    ethernet_t ethernet;
    ipv6_t     ipv6;
    srh_t      srh;
    segment_t  segment_list[4];
}

struct metadata {
}

const bit<128> R2_ADDR = 0x20260000000000000000000000000002; // 2026::2
const bit<128> R3_ADDR = 0x20260000000000000000000000000003; // 2026::3
const bit<128> R4_ADDR = 0x20260000000000000000000000000004; // 2026::4

const bit<16> ETHERTYPE_IPV6 = 0x86dd;
const bit<8>  IPV6_ROUTING_HEADER = 43;
const bit<8>  SRH_ROUTING_TYPE = 4;