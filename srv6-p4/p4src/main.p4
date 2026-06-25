#include <core.p4>
#include <v1model.p4>

#include "headers.p4"
#include "parser.p4"
#include "ingress.p4"
#include "egress.p4"
#include "deparser.p4"

control MyVerifyChecksum(inout headers hdr, inout metadata meta) { apply {} }
control MyComputeChecksum(inout headers hdr, inout metadata meta) { apply {} }

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;