from datetime import datetime
from thingspeak_handler import read_from_thingspeak
from mongo_handler import salvar_em_colecao, salvar_regra

def parse_feed(feed, parada_nome, canal_id):
    """Transforma feed do ThingSpeak em documento limpo e legível."""
    
    if not feed:
        return None

    try:
        timestamp = datetime.strptime(feed["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        timestamp = datetime.utcnow()

    return {
        "timestamp": timestamp,
        "parada": parada_nome,
        "canal": canal_id,

        "visual": int(feed.get("field1", 0)),
        "fisico": int(feed.get("field3", 0)),
    }

def main():
    print("📡 Iniciando sincronização ThingSpeak → MongoDB...")

    # ---------------- REGRAS ----------------
    print("🔹 Baixando regras...")
    feeds_regras = read_from_thingspeak("regras", results=8000)
    print(f"🔹 {len(feeds_regras)} registros encontrados.")

    for feed in feeds_regras:
        try:
            regra_doc = {
                "timestamp": feed.get("created_at"),
                "f1": feed.get("field1"),
                "f2": feed.get("field2"),
                "f3": feed.get("field3")
            }
            salvar_regra(regra_doc)
        except Exception as e:
            print("Erro salvando regra:", e)

    # ---------------- PARADA 1 ----------------
    print("🔹 Baixando dados da Parada P001...")
    feeds_p1 = read_from_thingspeak("parada1", results=8000)
    print(f"🔹 {len(feeds_p1)} registros encontrados.")

    for feed in feeds_p1:
        doc = parse_feed(feed, "P001", 3096316)
        if doc:
            salvar_em_colecao("parada_P001_logs", doc)

    # ---------------- PARADA 2 ----------------
    print("🔹 Baixando dados da Parada P002...")
    feeds_p2 = read_from_thingspeak("parada2", results=8000)
    print(f"🔹 {len(feeds_p2)} registros encontrados.")

    for feed in feeds_p2:
        doc = parse_feed(feed, "P002", 3102167)
        if doc:
            salvar_em_colecao("parada_P002_logs", doc)

    print("✅ Sincronização finalizada!")
    print("📌 Dados organizados em coleções separadas por parada.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ Execução interrompida pelo usuário.")
