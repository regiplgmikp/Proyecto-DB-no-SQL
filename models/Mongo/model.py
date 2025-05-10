import models.conection as conection
from .Agente import Agente
from .Empresa import Empresa
from .Cliente import Cliente
from .Ticket import Ticket
from bson import Binary

db = conection.connect_mongodb()

if 'agentes' not in db.list_collection_names():
    db.create_collection('agentes')

if 'empresas' not in db.list_collection_names():
    db.create_collection('empresas')

if 'clientes' not in db.list_collection_names():
    db.create_collection('clientes')

if 'tickets' not in db.list_collection_names():
    db.create_collection('tickets')

# Creación de indices
# Agentes:
db.agentes.create_index('idAgente', unique=True)

# Empresas:
db.empresas.create_index('idEmpresa', unique=True)

# Clientes:
db.clientes.create_index('idCliente', unique=True)

# Clientes:
db.tickets.create_index('idTicket', unique=True)


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
        collection = db['empresas']
        empresa = Empresa.crear_desde_dict(empresa)
        
        # Convertir UUIDs a Binary para MongoDB
        empresa_dict = empresa.model_dump(by_alias=True)
        empresa_dict['idEmpresa'] = Binary.from_uuid(empresa_dict['idEmpresa'])
        
        collection.insert_one(empresa_dict)
    except Exception as e:
        raise e

def insertar_cliente(cliente):
    try:
        collection = db['clientes']
        cliente = Cliente.crear_desde_dict(cliente)
        
        # Convertir UUIDs a Binary para MongoDB
        cliente_dict = cliente.model_dump(by_alias=True)
        cliente_dict['idCliente'] = Binary.from_uuid(cliente_dict['idCliente'])
        cliente_dict['idEmpresa'] = Binary.from_uuid(cliente_dict['idEmpresa'])
        
        collection.insert_one(cliente_dict)
    except Exception as e:
        raise e

def insertar_ticket(ticket):
    try:
        collection = db['tickets']
        ticket = Ticket.crear_desde_dict(ticket)
        
        # Convertir UUIDs a Binary para MongoDB
        ticket_dict = ticket.model_dump(by_alias=True)
        ticket_dict['idTicket'] = Binary.from_uuid(ticket_dict['idTicket'])
        ticket_dict['idCliente'] = Binary.from_uuid(ticket_dict['idCliente'])
        ticket_dict["idAgente"] = Binary.from_uuid(ticket_dict["idAgente"]) if ticket_dict["idAgente"] is not None else None
        ticket_dict['idEmpresa'] = Binary.from_uuid(ticket_dict['idEmpresa'])
        
        collection.insert_one(ticket_dict)
    except Exception as e:
        raise e