import os
import json
import requests

STEAM_API_KEY = os.environ["STEAM_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STEAM_ID = "76561199562409289"
STATE_FILE = "status.json"

def get_status():
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": STEAM_ID
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    players = response.json()["response"]["players"]
    return int(players[0]["personastate"]) if players else 0

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }, timeout=20).raise_for_status()

def main():
    current = get_status()

    try:
        with open(STATE_FILE, "r") as f:
            previous = json.load(f)["status"]
    except FileNotFoundError:
        previous = current

    if previous == 0 and current > 0:
        send_telegram(
            "🟢 Znajomy właśnie pojawił się online na Steamie!\n"
            f"https://steamcommunity.com/profiles/{STEAM_ID}/"
        )

    with open(STATE_FILE, "w") as f:
        json.dump({"status": current}, f)

    print(f"Status: {current}")

if __name__ == "__main__":
    main()
