from pymongo import MongoClient

MONGO_URI = "mongodb+srv://louisy_atlas:xPVmpWj4nHF@iotproject.9hsgy6i.mongodb.net/?retryWrites=true&w=majority&appName=IotProject"
DB_NAME = "IotProject"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def salvar_em_colecao(nome_colecao, documento):
    """Salva documentos em coleções dinâmicas por parada."""
    colecao = db[nome_colecao]
    colecao.insert_one(documento)

def salvar_regra(documento):
    """Salva regras em coleção fixa."""
    col_regras = db["regras"]
    col_regras.insert_one(documento)
