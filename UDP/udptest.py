import socket

# Configure UDP server
udp_server_ip = '0.0.0.0'  # Listen on all available network interfaces
udp_server_port = 12345  # Choose a suitable port

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((udp_server_ip, udp_server_port))

while True:
    # Receive UDP packet from ESP32
    data, address = udp_socket.recvfrom(1024)  # Adjust buffer size as needed
    print(f"Received from {address}: {data.decode()}")

    # Prepare a response
    response_data = "Response from Raspberry Pi"

    # Send the response back to the ESP32
    udp_socket.sendto(response_data.encode(), address)
