import models.conection as conection
from pydantic import BaseModel
from typing import Type, Union
from .Agente import Agente
from .Empresa import Empresa
from .Cliente import Cliente
from .Ticket import Ticket
from bson import Binary
from uuid import UUID

class MongoModel:
    db = conection.connect_mongodb()

    # Creación de colecciones si no existen
    collections = ['agentes', 'empresas', 'clientes', 'tickets']
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)

    # Creación de índices
    db.agentes.create_index('idAgente', unique=True)
    db.empresas.create_index('idEmpresa', unique=True)
    db.clientes.create_index('idCliente', unique=True)
    db.tickets.create_index('idTicket', unique=True)

    @classmethod
    def insertar_agente(cls, agente):
        cls._insertar_documento('agentes', agente, Agente)

    @classmethod
    def insertar_empresa(cls, empresa):
        cls._insertar_documento('empresas', empresa, Empresa)

    @classmethod
    def insertar_cliente(cls, cliente):
        cls._insertar_documento('clientes', cliente, Cliente)

    @classmethod
    def insertar_ticket(cls, ticket):
        cls._insertar_documento('tickets', ticket, Ticket)

    @classmethod
    def _insertar_documento(cls, collection_name: str, data: dict, model_class: Type[Union[Agente, Empresa, Cliente, Ticket]]):
        try:
            collection = cls.db[collection_name]
            data = model_class.crear_desde_dict(data)

            # Convertir UUIDs a Binary para MongoDB
            data_dict = data.model_dump(by_alias=True)
            for key, value in data_dict.items():
                if isinstance(value, UUID):
                    data_dict[key] = Binary.from_uuid(value)

            collection.insert_one(data_dict)
        except Exception as e:
            raise e
