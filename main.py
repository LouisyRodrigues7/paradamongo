from datetime import datetime
from thingspeak_handler import read_from_thingspeak
from mongo_handler import salvar_parada, salvar_regra

def parse_feed(feed, parada_nome, canal_id):
    """Converte feed do ThingSpeak em documento organizado"""
    if not feed:
        return None

    try:
        timestamp = datetime.strptime(feed["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        timestamp = datetime.utcnow()

    return {
        "timestamp": timestamp,
        "botao": feed.get("field1", "desconhecido"),
        "estado": feed.get("field2", "desconhecido"),
        "parada": parada_nome,
        "canal_thingspeak": canal_id
    }

def main():
    print("📡 Iniciando sincronização ThingSpeak → MongoDB...")

    # --- Regras ---
    print("🔹 Buscando regras...")
    feeds_regras = read_from_thingspeak("regras", results=8000)  # pegar todos registros
    print(f"🔹 {len(feeds_regras)} registros encontrados em regras.")
    for feed in feeds_regras:
        regra_doc = parse_feed(feed, "regras", 3096396)
        if regra_doc:
            salvar_regra(regra_doc)

    # --- Parada 1 ---
    print("🔹 Buscando parada_1...")
    feeds_p1 = read_from_thingspeak("parada1", results=8000)
    print(f"🔹 {len(feeds_p1)} registros encontrados em parada_1.")
    for feed in feeds_p1:
        parada1_doc = parse_feed(feed, "parada_1", 3096316)
        if parada1_doc:
            salvar_parada(parada1_doc)

    # --- Parada 2 ---
    print("🔹 Buscando parada_2...")
    feeds_p2 = read_from_thingspeak("parada2", results=8000)
    print(f"🔹 {len(feeds_p2)} registros encontrados em parada_2.")
    for feed in feeds_p2:
        parada2_doc = parse_feed(feed, "parada_2", 3102167)
        if parada2_doc:
            salvar_parada(parada2_doc)

    print("✅ Sincronização completa.")
    print("📌 Todos os dados do ThingSpeak foram salvos no MongoDB.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ Execução interrompida pelo usuário.")
