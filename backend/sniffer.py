import time
from scapy.all import sniff, IP, TCP, UDP

def process_packet(packet):
    """
    Callback function that runs every time a network packet is captured.
    Extracts key features from OSI Layer 3 (IP) and Layer 4 (TCP/UDP).
    """
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        pkt_size = len(packet)
        proto = "OTHER"

        if TCP in packet:
            proto = "TCP"
        elif UDP in packet:
            proto = "UDP"

        packet_data = {
            "timestamp": time.time(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": proto,
            "length": pkt_size
        }

        print(f"[{proto}] {src_ip} -> {dst_ip} | Size: {pkt_size} bytes")
        return packet_data

def start_sniffing(packet_count=10):
    """
    Starts listening to network interfaces.
    Requires administrator privileges.
    """
    print(f"Starting network sniffing for {packet_count} packets...")
    sniff(prn=process_packet, count=packet_count, store=False)

if __name__ == "__main__":
    # Test run: capture 10 live packets
    start_sniffing(packet_count=10)