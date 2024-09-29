import socket
import sys

HOST = 'localhost'
PORT = 31337
BUFFER_SIZE = 1024

# Store the player's name after registration
player_name = None

#player is assigned to the terminal after created
def driver(command):
    global player_name
    if player_name:
        command = f"{player_name} {command}"
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(command.encode(), (HOST, PORT))
        response, _ = sock.recvfrom(BUFFER_SIZE)
        return response.decode()

def main():
    global player_name

    command = " ".join(sys.argv[1:])
    
    if command.startswith("REGISTER"):
        parts = command.split()
        player_name = parts[1]
    
    response = driver(command)
    
    print(f"Output: {response}")

if __name__ == "__main__":
    main()
