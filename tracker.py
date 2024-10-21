import socket
import random

# Creating data structures and hosting
players = {}
games = []

HOST = 'localhost'
#port for my group 74#port for group 74- confused on why, im working from my house, not a public university IP but no prob
PORT = 38000
BUFFER_SIZE = 1024

# Creating the socket and running the tracker on our local host with port 3800
def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Tracker is running on {HOST}:{PORT}")
    return sock

# registering a player
def register_player(data, addr):
    parts = data.split()

    player_name, ip, t_port, p_port = parts[1], parts[2], int(parts[3]), int(parts[4])

    if player_name in players:
        return f"Error Player {player_name} already exists"

    players[player_name] = (ip, t_port, p_port, "free")

    return f"SUCCESS {player_name} registered"

# query the players
def query_players():
    result = f"{len(players)} Players registered:\n"
    for player_name, (ip, t_port, p_port, status) in players.items():
        result += f"Player: {player_name}, IP: {ip}, Tracker Port: {t_port}, Peer Port: {p_port}, Status: {status}\n"
    return result

# query ongoing games
def query_games():
    result = f"{len(games)} Games ongoing:\n"
    for game in games:
        game_id, dealer, players_in_game = game
        result += f"Game ID: {game_id}, Dealer: {dealer}, Players: {', '.join(players_in_game)}\n"
    return result

# start a game and have if constraints
def start_game(data):
    parts = data.split()

    if len(parts) != 4 or parts[0].upper() != "START":
        return "missing parameters"

    dealer, n, holes = parts[1], int(parts[2]), int(parts[3])

    # Validating dealer and number of players
    if dealer not in players:
        return "ERROR: Dealer not registered"
    
    # if num_holes < 1 or num_holes > 9:
    #     return "ERROR: Number of holes must be between 1 and 9"

    #it says players must be <= 3 so im assuming we cant have more than 3?
    if n < 1 or n > 3:
        return "ERROR: Number of players must be 1 ≤ n ≤ 3"

    available_players = [player for player in players if player != dealer and players[player][3] == "free"]
    if len(available_players) < n:
        return "ERROR: Not enough available players"

    selected_players = random.sample(available_players, n)
    game_id = len(games) + 1  

    #storing game information
    players_in_game = [dealer] + selected_players
    for player in players_in_game:
        players[player] = (*players[player][:3], "in-play")

    games.append((game_id, dealer, players_in_game))
    return f"SUCCESS: Game {game_id} started with dealer {dealer} and players {', '.join(selected_players)}"

# Ending  game
def end_game(data):
    parts = data.split()
    game_id, dealer = int(parts[1]), parts[2]

    # Validating game exists and dealer
    for game in games:
        if game[0] == game_id and game[1] == dealer:
            games.remove(game)
            for player in game[2]:
                players[player] = (*players[player][:3], "free")
            return f"SUCCESS: Game {game_id} ended successfully"
    
    return "ERROR"

# De-registering a player
def de_register(data):
    parts = data.split()
    player_name = parts[1]

    #make sure player is registered and not currently ingame
    if player_name not in players:
        return f"ERROR: Player {player_name} not registered"
    for game in games:
        if player_name in game[2]:
            return f"ERROR: Player {player_name} is in an ongoing game and cannot be de-registered"

    # Remove player
    del players[player_name]
    return f"SUCCESS: Player {player_name} de-registered successfully"

#steal card function
def steal_card(data):
    parts = data.split()
    stealing_player, target_player, card_position = parts[1], parts[2], int(parts[3])

    for game in games:
        if stealing_player in game[2] and target_player in game[2]:
            return f"SUCCESS: {stealing_player} stole {card_position} from {target_player}"
    
    return "ERROR"

# main function to parse incoming function requests
def main():
    sock = create_socket()
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        data = data.decode().strip()
        
        if data.startswith("REGISTER"):
            response = register_player(data, addr)
        elif data == "QUERY PLAYERS":
            response = query_players()
        elif data == "QUERY GAMES":
            response = query_games()
        elif data.startswith("START"):
            response = start_game(data)
        elif data.startswith("END"):
            response = end_game(data)
        elif data.startswith("DE-REGISTER"):
            response = de_register(data)
        elif data.startswith("STEAL"):
            response = steal_card(data)
        else:
            response = "Unknown command"
        
        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()
