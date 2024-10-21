import socket
import sys

HOST = 'localhost'
PORT = 38000
BUFFER_SIZE = 1024

# Store the player's name after registration
player_name = None

# Send command to the tracker
def driver(command):
    global player_name

    # Only prefix with player name if not registering
    if player_name and not command.startswith("REGISTER"):
        command = f"{player_name} {command}"
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(command.encode(), (HOST, PORT))
        response, _ = sock.recvfrom(BUFFER_SIZE)
        return response.decode()

def main():
    global player_name

    command = " ".join(sys.argv[1:])
    
    # Set player_name when registering
    if command.startswith("REGISTER"):
        parts = command.split()
        if len(parts) >= 2:
            player_name = parts[1]
    
    response = driver(command)
    
    print(f"Output: {response}")

if __name__ == "__main__":
    main()
