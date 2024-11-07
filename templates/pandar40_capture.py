import socket
import numpy as np

# Pandar40P's IP and data port
LIDAR_IP = "192.168.1.201"
LIDAR_PORT = 2368  # Default data port for Pandar40P

# Create a UDP socket to receive data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", LIDAR_PORT))  # Bind to all IP addresses on the specified port

print("Listening for data from Pandar40P on 192.168.1.201:2368...")

try:
    while True:
        data, addr = sock.recvfrom(1206)  # Each data packet is typically 1206 bytes
        point_data = np.frombuffer(data, dtype=np.uint8)  # Convert to a numpy array
        print("Received data packet:", point_data)  # Print data for inspection
except KeyboardInterrupt:
    print("Data capture interrupted by user.")
finally:
    sock.close()