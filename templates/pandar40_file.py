import socket
import numpy as np
import struct

# Pandar40P’s IP and port
LIDAR_IP = "192.168.1.201"
LIDAR_PORT = 2368
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", LIDAR_PORT))

# PCD header for point cloud data
pcd_header = """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA ascii
"""

points = []

try:
    print("Capturing data...")
    while True:
        data, addr = sock.recvfrom(1206)
        
        # Adjust this parsing based on the exact data structure
        point_data = np.frombuffer(data, dtype=np.uint8)
        
        # Skip header if necessary, e.g., if there's an 8-byte header
        start_offset = 8
        for i in range(start_offset, len(point_data), 12):  # 12 bytes per XYZ point
            try:
                x, y, z = struct.unpack('fff', point_data[i:i+12])
                points.append(f"{x} {y} {z}")
            except struct.error:
                # Break if remaining bytes are less than 12
                break

except KeyboardInterrupt:
    print("Saving captured data to .pcd file...")
finally:
    sock.close()

# Write points to PCD file
num_points = len(points)
with open("pandar40_capture2.pcd", "w") as f:
    f.write(pcd_header.format(num_points, num_points))
    f.write("\n".join(points))