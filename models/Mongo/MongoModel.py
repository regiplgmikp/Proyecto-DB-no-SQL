import models.conection as conection
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
        return cls._insertar_documento('agentes', agente, Agente)

    @classmethod
    def obtener_agente_por_id(cls, idAgente: UUID):
        return cls._obtener_documento_por_id('agentes', idAgente, 'idAgente')

    @classmethod
    def insertar_empresa(cls, empresa):
        return cls._insertar_documento('empresas', empresa, Empresa)

    @classmethod
    def obtener_empresa_por_id(cls, idEmpresa: UUID):
        return cls._obtener_documento_por_id('empresas', idEmpresa, 'idEmpresa')

    @classmethod
    def insertar_cliente(cls, cliente):
        return cls._insertar_documento('clientes', cliente, Cliente)

    @classmethod
    def obtener_cliente_por_id(cls, idCliente: UUID):
        return cls._obtener_documento_por_id('clientes', idCliente, 'idCliente')

    @classmethod
    def insertar_ticket(cls, ticket):
        return cls._insertar_documento('tickets', ticket, Ticket)

    @classmethod
    def obtener_ticket_por_id(cls, idTicket: UUID):
        return cls._obtener_documento_por_id('tickets', idTicket, 'idTicket')

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
            return data # Si hay algún error en la insersión, no se llega a esta linea, solo si todo salio correctamente, se retorna la coleccion creada
        except Exception as e:
            raise e


    @classmethod
    def _obtener_documento_por_id(cls, collection_name: str, id_value: UUID, id_field: str):
        collection = cls.db[collection_name]
        documento = collection.find_one({id_field: Binary.from_uuid(id_value)})

        if not documento:
            return None
        # Convertir todos los campos que sean Binary a UUID
        for key, value in documento.items():
            if isinstance(value, Binary):
                documento[key] = UUID(bytes=value)

        # Eliminar el campo '_id' para evitar confusión
        documento.pop('_id', None)

        return documento
