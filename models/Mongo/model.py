import models.conection as conection
from .Agente import Agente
from .Empresa import Empresa
from bson import Binary

db = conection.connect_mongodb()

if 'agentes' not in db.list_collection_names():
    db.create_collection('agentes')

# Creación de indices
# Agentes:
db.agentes.create_index('idAgente', unique=True)

# Empresas:
db.empresas.create_index('idEmpresa', unique=True)


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

def insertar_empresa(empresa):
    try:
        collection = db['agentes']
        empresa = Empresa.crear_desde_dict(empresa)
        
        # Convertir UUIDs a Binary para MongoDB
        empresa_dict = empresa.model_dump(by_alias=True)
        empresa_dict['iEmpresa'] = Binary.from_uuid(empresa_dict['idEmpresa'])
        
        collection.insert_one(empresa_dict)
    except Exception as e:
        raise e