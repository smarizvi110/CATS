# app_sender.py
import time
import config
from transport_sender import TransportSender

def main():
    sender_transport = TransportSender()
    sender_transport.start()

    print("Application Sender starting...")
    try:
        msg_counter = 0
        for i in range(10): # Send a mix of data
            # Send a burst of low-priority data
            for j in range(3):
                low_prio_msg = f"LOW_PRIO_DATA_CHUNK_{msg_counter}".encode('latin-1')
                print(f"[App Sender] Sending low priority: {low_prio_msg.decode('latin-1')}")
                sender_transport.send_data(low_prio_msg, config.LOW_PRIORITY)
                msg_counter += 1
                time.sleep(0.02) # Slight app-level delay

            # Send one high-priority message
            high_prio_msg = f"HIGH_PRIO_IMPORTANT_MESSAGE_{i}".encode('latin-1')
            print(f"[App Sender] Sending HIGH priority: {high_prio_msg.decode('latin-1')}")
            sender_transport.send_data(high_prio_msg, config.HIGH_PRIORITY)
            
            time.sleep(config.PACING_INTERVAL * 2) # Let some ACKs potentially flow

        print("Application Sender: All initial data queued. Waiting for a bit...")
        time.sleep(5) # Keep sender alive to process ACKs and potential resends

    except KeyboardInterrupt:
        print("Application Sender interrupted.")
    finally:
        print("Application Sender stopping transport...")
        sender_transport.stop()
        print("Application Sender finished.")

if __name__ == "__main__":
    main()