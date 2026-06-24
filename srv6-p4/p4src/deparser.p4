/*
    Deparser del switch.

    Su función es reconstruir el paquete antes de enviarlo por el puerto
    de salida, los encabezados se emiten en el mismo orden en que deben
    aparecer dentro del paquete.
*/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv6);
        packet.emit(hdr.srh);
        packet.emit(hdr.segment_list);
    }
}