import re
from uuid import UUID
from datetime import datetime
from models.Utils.regularExpresions import (
    nombre_regex,
    correo_regex,
    telefono_regex
)
from models.Utils.dictionaries import (
    estadoEnEmpresa as estadoEnEmpresaDict,
    estadoCuenta as estadoCuentaDict,
    estado as estadoTicketDict,
    prioridad as prioridadTicketDict
)

class Validaciones:

    @staticmethod
    def validar_nombre(nombre):
        if not re.match(nombre_regex, nombre):
            raise ValueError('El nombre debe contener al menos nombre y apellido')
        return nombre.lower()
    
    @staticmethod
    def validar_formato_correo(correo):
        if not re.match(correo_regex, correo):
            raise ValueError('Formato de correo electrónico inválido')
        return correo.lower()

    @staticmethod
    def validar_telefono(telefono):
        if not re.match(telefono_regex, telefono):
            raise ValueError('El teléfono debe contener solo números (10-15 dígitos)')
        return telefono

    @staticmethod
    def validar_estadoEnEmpresa(estadoEnEmpresa):
        estado = int(estadoEnEmpresa)
        estados_validos = list(estadoEnEmpresaDict.keys())
        if estado not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return estado
    
    @staticmethod
    def validar_estadoCuenta(estadoCuenta):
        estadoCuenta = int(estadoCuenta)
        estados_validos = list(estadoCuentaDict.keys())
        if estadoCuenta not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return estadoCuenta

    @staticmethod
    def validar_estadoTicket(estadoTicket):
        estadoTicket = int(estadoTicket)
        estados_validos = list(estadoTicketDict.keys())
        if estadoTicket not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return estadoTicket

    def validar_prioridadTicket(prioridadTicket):
        prioridadTicket = int(prioridadTicket)
        estados_validos = list(prioridadTicketDict.keys())
        if prioridadTicket not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return prioridadTicket
    
    @staticmethod
    def validar_fecha(fecha):
        """Convierte la fecha a datetime y valida el formato."""
        try:
            return datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS.")

    @staticmethod
    def validar_idEmpresaExistente(idEmpresa):
        """Convierte el ID a UUID y valida que la empresa exista."""
        from models.Mongo.MongoModel import MongoModel

        try:
            if not isinstance(idEmpresa, UUID):
                idEmpresa = UUID(idEmpresa)

            empresa = MongoModel.obtener_empresa_por_id(idEmpresa)
            if not empresa:
                raise ValueError(f"La empresa con ID {idEmpresa} no existe.")
            return empresa
        except ValueError as e:
            raise ValueError(f"El ID ingresado no es un UUID válido. Error:{e}")

    @staticmethod
    def validar_idAgenteExistente(idAgente):
        """Convierte el ID a UUID y valida que la empresa exista."""
        from models.Mongo.MongoModel import MongoModel

        try:
            if not isinstance(idAgente, UUID):
                idAgente = UUID(idAgente)

            agente = MongoModel.obtener_agente_por_id(idAgente)
            if not agente:
                raise ValueError(f"El agente con ID {idAgente} no existe.")
            return agente
        except ValueError as e:
            raise ValueError(f"El ID ingresado no es un UUID válido. Error:{e}")

    @staticmethod
    def validar_idClienteExistente(idCliente):
        """Convierte el ID a UUID y valida que la empresa exista."""
        from models.Mongo.MongoModel import MongoModel

        try:
            if not isinstance(idCliente, UUID):
                idCliente = UUID(idCliente)

            cliente = MongoModel.obtener_cliente_por_id(idCliente)
            if not cliente:
                raise ValueError(f"El cliente con ID {idCliente} no existe.")
            return cliente
        except ValueError as e:
            raise ValueError(f"El ID ingresado no es un UUID válido. Error:{e}")
