import models.conection as conection
from .Agente import Agente
from bson import Binary

db = conection.connect_mongodb()

if 'agentes' not in db.list_collection_names():
    db.create_collection('agentes')

# Creación de indices
db.agentes.create_index('idAgente', unique=True)

def insertar_agente(agente):
    try:
        collection = db['agentes']
        agente = Agente.crear_desde_dict(agente)
        
        # Convertir UUIDs a Binary para MongoDB
        agente_dict = agente.model_dump(by_alias=True)
        agente_dict['idAgente'] = Binary.from_uuid(agente_dict['idAgente'])
        agente_dict['idEmpresa'] = Binary.from_uuid(agente_dict['idEmpresa'])
        
        collection.insert_one(agente_dict)
    except Exception as e:
        raise e