import asyncio
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.sniffer import process_packet
from backend.ml_engine import TrafficAnomalyDetector
from scapy.all import sniff, IP, TCP, UDP

app = FastAPI(title="NetShield AI Security Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = TrafficAnomalyDetector()

@app.get("/")
def root():
    return {"status": "NetShield AI Backend Running", "system": "Active"}

@app.websocket("/ws/traffic")
async def websocket_traffic_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Dashboard client connected via WebSocket.")

    # Get the main event loop for safe thread scheduling
    loop = asyncio.get_running_loop()

    def packet_callback(packet):
        if IP in packet:
            pkt_size = len(packet)
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = "TCP" if TCP in packet else ("UDP" if UDP in packet else "OTHER")
            
            ai_result = detector.predict(packet_length=pkt_size, packet_rate=1)

            telemetry = {
                "timestamp": time.strftime("%H:%M:%S"),
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": proto,
                "length": pkt_size,
                "status": ai_result["status"],
                "is_anomaly": ai_result["is_anomaly"],
                "score": round(ai_result["score"], 4)
            }

            # Schedule thread-safe async push to WebSocket client
            asyncio.run_coroutine_threadsafe(
                websocket.send_json(telemetry),
                loop
            )

    try:
        # Run Scapy sniffer in a background executor thread
        await loop.run_in_executor(
            None, 
            lambda: sniff(prn=packet_callback, store=False)
        )
    except WebSocketDisconnect:
        print("Dashboard client disconnected.")