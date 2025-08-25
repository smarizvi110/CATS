# segment.py
import json

SEGMENT_TYPE_DATA = "DATA"
SEGMENT_TYPE_ACK = "ACK"

class Segment:
    def __init__(self, type, priority, seq_num, payload=b'', ack_num=None):
        self.type = type
        self.priority = priority # Only relevant for DATA segments
        self.seq_num = seq_num   # For DATA segments
        self.ack_num = ack_num   # For ACK segments
        self.payload = payload

    def to_bytes(self):
        data = {
            "type": self.type,
            "priority": self.priority,
            "seq_num": self.seq_num,
            "ack_num": self.ack_num,
            "payload": self.payload.decode('latin-1') # Assuming payload can be string-like
        }
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def from_bytes(byte_data):
        try:
            data = json.loads(byte_data.decode('utf-8'))
            payload_bytes = data.get("payload", "").encode('latin-1')
            return Segment(
                type=data.get("type"),
                priority=data.get("priority"),
                seq_num=data.get("seq_num"),
                payload=payload_bytes,
                ack_num=data.get("ack_num")
            )
        except json.JSONDecodeError:
            print("Error decoding segment")
            return None
        except Exception as e:
            print(f"Error creating segment from bytes: {e}")
            return None

    def __str__(self):
        if self.type == SEGMENT_TYPE_DATA:
            return f"Segment(DATA, Prio:{self.priority}, Seq:{self.seq_num}, Size:{len(self.payload)})"
        elif self.type == SEGMENT_TYPE_ACK:
            return f"Segment(ACK, AckNum:{self.ack_num})"
        return "Segment(Unknown)"