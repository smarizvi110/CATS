# config.py
RECEIVER_IP = "127.0.0.1"
RECEIVER_PORT = 12345
SENDER_PORT = 12346 # For ACKs

MAX_SEGMENT_PAYLOAD_SIZE = 100  # Bytes
HIGH_PRIORITY = 0
LOW_PRIORITY = 1

# Simulated Bottleneck: Send one segment every X seconds
PACING_INTERVAL = 0.1  # Seconds

# Simple ACK timeout (for demo purposes, not full retransmission)
ACK_TIMEOUT = 0.5 # Seconds