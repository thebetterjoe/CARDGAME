import socket
#creating data structures and hosting
players = {}  
games = []  

HOST = 'localhost' 
PORT = 31337
BUFFER_SIZE = 1024

#creating the socket and running the tracker on our local host with 31337 port (#pwn.college)
def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Tracker is running on {HOST}:{PORT}")
    return sock


#registering a player, 
def register_player(data, addr):
        parts = data.split()  

        if len(parts) != 5 or parts[0].upper() != "REGISTER":
            return "That command does not exist"
        
        player_name, ip, t_port, p_port = parts[1], parts[2], int(parts[3]), int(parts[4])

        if player_name in players:
            return f"Error Player {player_name} already exists"

        players[player_name] = (ip, t_port, p_port)

        return f"SUCCESS {player_name} registered"
    

#querying the players
def query_players():
    result = f"{len(players)} Players registered:\n"
    for player, (ip, t_port, p_port) in players.items():
        result += f"{player} at {ip}:{t_port}/{p_port}\n"
    
    return result.strip()

#querying the games
def query_games():    
    result = f"{len(games)} current Games:\n"
    
    
    for game in games:
        result += f"{game}\n"
    
    return result.strip()

#deregistering a player
def deregister_player(data):
    
        parts = data.split()  
        player_name = parts[1]

        if player_name not in players:
            return f"Error Player {player_name} does not exist"

        del players[player_name]
        return f"SUCCESS {player_name} de-registered"
    


#function to process whatever user input is given
def process_message(message, addr):
    parts = message.split(maxsplit=1)

    if len(parts) < 2:
        return "Error"

    player_name, command = parts

    if command.startswith("REGISTER"):
        return register_player(command, addr)
    elif command.startswith("QUERY_PLAYERS"):
        return query_players()
    elif command.startswith("QUERY_GAMES"):
        return query_games()
    elif command.startswith("DE_REGISTER"):
        return deregister_player(command)
    else:
        return f"Error"


def main():
    sock = create_socket()

    while True:
        message, addr = sock.recvfrom(BUFFER_SIZE)
        message = message.decode()
        response = process_message(message, addr)

        print(f"Received {addr}: {message}")
        print(f"Sending response: {response}")

        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()

