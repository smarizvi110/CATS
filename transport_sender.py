# transport_sender.py
import socket
import time
import threading
from collections import deque

import config
from segment import Segment, SEGMENT_TYPE_DATA, SEGMENT_TYPE_ACK

class TransportSender:
    def __init__(self, local_ip="0.0.0.0", local_port=config.SENDER_PORT,
                 remote_ip=config.RECEIVER_IP, remote_port=config.RECEIVER_PORT):
        self.remote_addr = (remote_ip, remote_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((local_ip, local_port))
        self.sock.settimeout(0.1) # Non-blocking for ACK reception

        self.send_buffer_high = deque() # Queue for high priority segments
        self.send_buffer_low = deque()  # Queue for low priority segments
        
        self.next_seq_num = 0
        self.unacked_segments = {} # {seq_num: (segment, send_time, retries)}

        self.running = True
        self.ack_listener_thread = threading.Thread(target=self._listen_for_acks, daemon=True)
        self.pacing_thread = threading.Thread(target=self._pace_sending, daemon=True)

    def start(self):
        self.ack_listener_thread.start()
        self.pacing_thread.start()
        print(f"Sender transport started. Listening for ACKs on port {config.SENDER_PORT}")
        print(f"Sending to {self.remote_addr}")

    def stop(self):
        self.running = False
        if self.ack_listener_thread.is_alive():
            self.ack_listener_thread.join(timeout=1)
        if self.pacing_thread.is_alive():
            self.pacing_thread.join(timeout=1)
        self.sock.close()
        print("Sender transport stopped.")

    def send_data(self, app_data: bytes, priority: int):
        # Segmentation
        offset = 0
        while offset < len(app_data):
            payload_chunk = app_data[offset:offset + config.MAX_SEGMENT_PAYLOAD_SIZE]
            
            segment = Segment(type=SEGMENT_TYPE_DATA,
                              priority=priority,
                              seq_num=self.next_seq_num,
                              payload=payload_chunk)
            
            if priority == config.HIGH_PRIORITY:
                self.send_buffer_high.append(segment)
            else: # Low priority
                self.send_buffer_low.append(segment)
            
            # print(f"[Sender App->Transport] Queued: {segment} (Orig Data Size: {len(app_data)})")
            self.next_seq_num += 1
            offset += config.MAX_SEGMENT_PAYLOAD_SIZE

    def _listen_for_acks(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                ack_segment = Segment.from_bytes(data)
                if ack_segment and ack_segment.type == SEGMENT_TYPE_ACK:
                    # print(f"[Transport Sender] Received ACK: {ack_segment.ack_num}")
                    if ack_segment.ack_num in self.unacked_segments:
                        del self.unacked_segments[ack_segment.ack_num]
                        # print(f"[Transport Sender] Segment {ack_segment.ack_num} ACKed and removed.")
                    # else:
                        # print(f"[Transport Sender] Received duplicate/late ACK for {ack_segment.ack_num}")
            except socket.timeout:
                continue # Just to make the loop non-blocking
            except Exception as e:
                if self.running: # Avoid error messages during shutdown
                    print(f"Error in ACK listener: {e}")
                break

    def _pace_sending(self):
        while self.running:
            # Resend timed-out segments (very simple demo version)
            # A more robust system would have better retry logic
            now = time.time()
            for seq_num, (segment, send_time, retries) in list(self.unacked_segments.items()):
                if now - send_time > config.ACK_TIMEOUT:
                    if retries < 2: # Limit retries for demo
                        print(f"[Transport Sender] Timeout for segment {seq_num}. Resending (Attempt {retries+1})...")
                        self.sock.sendto(segment.to_bytes(), self.remote_addr)
                        self.unacked_segments[seq_num] = (segment, now, retries + 1)
                    else:
                        print(f"[Transport Sender] Max retries for segment {seq_num}. Giving up.")
                        del self.unacked_segments[seq_num]


            segment_to_send = None
            if self.send_buffer_high:
                segment_to_send = self.send_buffer_high.popleft()
            elif self.send_buffer_low:
                segment_to_send = self.send_buffer_low.popleft()

            if segment_to_send:
                try:
                    self.sock.sendto(segment_to_send.to_bytes(), self.remote_addr)
                    print(f"[Transport Sender->Network] Sent: {segment_to_send}")
                    self.unacked_segments[segment_to_send.seq_num] = (segment_to_send, time.time(), 0)
                except Exception as e:
                    print(f"Error sending segment: {e}")
            
            time.sleep(config.PACING_INTERVAL)