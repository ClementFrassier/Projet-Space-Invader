import requests

# URL de base du serveur
BASE_URL = "http://10.111.6.64:3000"

# Base URL of the server
def save_game(player_name, score):
    """
    Save a player's game data to the server.

    Parameters:
        player_name (str): The name of the player to save.
        score (int): The score of the player.

    Returns:
        dict: 
            - If successful: The server's JSON response (e.g., success message or saved data).
            - If failed: A dictionary containing the error message.
    """
    try:
        # Send a POST request to the /save-game endpoint
        response = requests.post(
            f"{BASE_URL}/save-game",
            json={"player_name": player_name, "score": score}
        )
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}
    except Exception as e:
        return {"error": str(e)}

# Function to recover all games
def get_games():
    """
    Retrieve all saved game data from the server.

    Returns:
        list or dict:
            - If successful: A list of games retrieved from the server.
            - If failed: A dictionary containing the error message.
    """

    try:
        response = requests.get(f"{BASE_URL}/get-games")
        if response.status_code == 200:
            return response.json().get("games", [])
        else:
            return {"error": response.json()}
    except Exception as e:
        return {"error": str(e)}
