from pymongo import MongoClient

# Conexão com o cluster (já criado por você)
MONGO_URI = "mongodb+srv://paradauser:1234@iotproject.9hsgy6i.mongodb.net/?retryWrites=true&w=majority&appName=IotProject"
DB_NAME = "IotProject"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Coleções separadas
col_paradas = db["paradas"]
col_regras = db["regras"]

def salvar_parada(dado):
    """Salva documento de uma parada (1 ou 2)"""
    col_paradas.insert_one(dado)

def salvar_regra(dado):
    """Salva documento de regras"""
    col_regras.insert_one(dado)
