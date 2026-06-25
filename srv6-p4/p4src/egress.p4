// control MyEgress(
//     inout headers hdr,
//     inout metadata meta,
//     inout standard_metadata_t standard_metadata)
// {
//     action srv6_egress_decap() {
//         if (hdr.srh.isValid() && hdr.srh.segments_left == 0) {

//             /*
//              * Se restaura el nextHdr original del paquete.
//              * El SRH trae guardado cual era el siguiente encabezado.
//              */
//             hdr.ipv6.nextHdr = hdr.srh.next_header;

//             /*
//              * Se invalida el SRH para que el deparser no lo vuelva a emitir.
//              */
//             hdr.srh.setInvalid();

//             /*
//              * Se invalidan los segmentos de la lista.
//              */
//             hdr.segment_list[0].setInvalid();
//             hdr.segment_list[1].setInvalid();
//             hdr.segment_list[2].setInvalid();
//             hdr.segment_list[3].setInvalid();
//         }
//     }

//     apply {
//         srv6_egress_decap();
//     }
// }

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