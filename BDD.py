import requests

# URL de base du serveur
BASE_URL = "http://10.111.6.64:3000"

# Fonction pour enregistrer une partie
def save_game(player_name, score):
    try:
        response = requests.post(
            f"{BASE_URL}/save-game",
            json={"player_name": player_name, "score": score}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}
    except Exception as e:
        return {"error": str(e)}

# Fonction pour récupérer toutes les parties
def get_games():
    try:
        response = requests.get(f"{BASE_URL}/get-games")
        if response.status_code == 200:
            return response.json().get("games", [])
        else:
            return {"error": response.json()}
    except Exception as e:
        return {"error": str(e)}
