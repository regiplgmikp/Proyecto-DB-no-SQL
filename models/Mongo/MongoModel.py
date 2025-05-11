import models.conection as conection
from typing import Type, Union
from .Agente import Agente
from .Empresa import Empresa
from .Cliente import Cliente
from .Ticket import Ticket
from bson import Binary
from uuid import UUID
from models.Utils.validaciones import Validaciones

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
        agente = cls._obtener_documentos_por_campo('agentes', idAgente, 'idAgente')
        if agente:
            return Agente.crear_desde_dict(agente[0])
    
    @classmethod
    def actualizar_agente(cls, idAgente: UUID, cambios: dict):
        """Actualiza el estado y teléfono de un agente en la base de datos."""
        try:
            collection = cls.db["agentes"]

            # Convertir UUID a Binary
            idAgente_bin = Binary.from_uuid(idAgente)
            
            cambios_filtrados = Validaciones.validar_camposActualizacion(cambios, ["estadoEnEmpresa", "telefono"])

            # Actualizar en MongoDB
            resultado = collection.update_one({"idAgente": idAgente_bin}, {"$set": cambios_filtrados})

            if resultado.matched_count == 0:
                raise ValueError(f"No se encontró un agente con ID {idAgente}")

            return cls.obtener_agente_por_id(idAgente)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def insertar_empresa(cls, empresa):
        return cls._insertar_documento('empresas', empresa, Empresa)

    @classmethod
    def obtener_empresa_por_id(cls, idEmpresa: UUID):
        empresa = cls._obtener_documentos_por_campo('empresas', idEmpresa, 'idEmpresa')
        if empresa:
            return Empresa.crear_desde_dict(empresa[0])

    @classmethod
    def insertar_cliente(cls, cliente):
        return cls._insertar_documento('clientes', cliente, Cliente)

    @classmethod
    def obtener_cliente_por_id(cls, idCliente: UUID):
        cliente = cls._obtener_documentos_por_campo('clientes', idCliente, 'idCliente')
        if cliente:
            return Cliente.crear_desde_dict(cliente[0])
    
    @classmethod
    def actualizar_cliente(cls, idCliente: UUID, cambios: dict):
        """Actualiza el telefono, correo, estadoCuenta de un cliente en la base de datos."""
        try:
            collection = cls.db["clientes"]

            # Convertir UUID a Binary
            idCliente_bin = Binary.from_uuid(idCliente)
            
            cambios_filtrados = Validaciones.validar_camposActualizacion(cambios, ["telefono", "correo", "estadoCuenta"])

            # Actualizar en MongoDB
            resultado = collection.update_one({"idCliente": idCliente_bin}, {"$set": cambios_filtrados})

            if resultado.matched_count == 0:
                raise ValueError(f"No se encontró un cliente con ID {idCliente}")

            return cls.obtener_cliente_por_id(idCliente)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def insertar_ticket(cls, ticket):
        return cls._insertar_documento('tickets', ticket, Ticket)

    @classmethod
    def obtener_ticket_por_id(cls, idTicket: UUID):
        # Retornamos solo el ticket, no una lista
        ticket = cls._obtener_documentos_por_campo('tickets', idTicket, 'idTicket')
        if ticket:
            return Ticket.crear_desde_dict(ticket[0])

    @classmethod
    def actualizar_ticket(cls, idTicket: UUID, cambios: dict):
        """Actualiza el fecha de cierre, estado, agente asignado, prioridad de un agente en la base de datos."""
        try:
            collection = cls.db["tickets"]

            # Convertir UUID a Binary
            idTicket_bin = Binary.from_uuid(idTicket)

            # cambios_filtrados = Validaciones.validar_camposActualizacion(cambios, ["fechaCierre", "estadoTicket", "idAgente", "prioridad"])
            cambios_filtrados = Validaciones.validar_camposActualizacion(cambios, ["fechaCierre", "estadoTicket", "idAgente", "prioridad"])

            # Actualizar en MongoDB
            resultado = collection.update_one({"idTicket": idTicket_bin}, {"$set": cambios_filtrados})

            if resultado.matched_count == 0:
                raise ValueError(f"No se encontró un ticket con ID {idTicket}")

            return cls.obtener_ticket_por_id(idTicket)
        except Exception as e:
            raise Exception(e)

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
            return data # Si hay algún error en la inserción, no se llega a esta linea, solo si todo salio correctamente, se retorna la coleccion creada
        except Exception as e:
            raise e


    @classmethod
    def _obtener_documentos_por_campo(cls, collection_name: str, field_value, field_name: str):
        """ Recibe un nombre de colleción a buscar, el nombre del campo en base al que se va a buscar y el valor que se quiere buscar
            Retorna los documentos encontrados con esas caracteristicas o lista vacía si no encuentra ninguno en la base de datos
        """
        collection = cls.db[collection_name]

        # Si el valor es un UUID, convertirlo a Binary para la consulta
        if isinstance(field_value, UUID):
            field_value = Binary.from_uuid(field_value)

        # Se buscan documentos con campos recibidos
        documentos = list(collection.find({field_name: field_value}))

        # Convertir todos los campos que sean Binary a UUID
        for documento in documentos:
            for key, value in documento.items():
                if isinstance(value, Binary):
                    documento[key] = UUID(bytes=value)

            # Eliminar el campo '_id' para evitar confusión
            documento.pop('_id', None)

        return documentos
