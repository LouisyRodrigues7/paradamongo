import requests

CHANNELS = {
    "regras": {
        "id": 3096396,
        "read_key": "OUNIMVOOQHLNG8J3"
    },
    "parada1": {
        "id": 3096316,
        "read_key": "9CGNRNFKB4SB7364"
    },
    "parada2": {
        "id": 3102167,
        "read_key": "K6WYZH8LQQX47G2D"
    }
}

def read_from_thingspeak(tipo, results=8000):
    """Lê múltiplos feeds de um canal ThingSpeak"""
    channel = CHANNELS[tipo]
    url = f"https://api.thingspeak.com/channels/{channel['id']}/feeds.json"
    params = {
        "api_key": channel["read_key"],
        "results": results
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("feeds", [])
        else:
            print(f"⚠️ Erro ao ler canal {tipo}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ Erro de conexão com canal {tipo}: {e}")
        return []
