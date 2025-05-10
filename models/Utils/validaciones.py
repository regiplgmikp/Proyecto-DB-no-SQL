import re
from uuid import UUID
from datetime import datetime
from models.Utils.regularExpresions import (
    nombre_regex,
    correo_regex,
    telefono_regex
)
from models.Utils.dictionaries import (
    estadoEnEmpresa as estadoEnEmpresaDict
)

class Validaciones:

    def validar_nombre(nombre):
        if not re.match(nombre_regex, nombre):
            raise ValueError('El nombre debe contener al menos nombre y apellido')
        return nombre.lower()
    
    def validar_formato_correo(correo):
        if not re.match(correo_regex, correo):
            raise ValueError('Formato de correo electrónico inválido')
        return correo.lower()

    @classmethod
    def validar_telefono(cls, telefono):
        if not re.match(telefono_regex, telefono):
            raise ValueError('El teléfono debe contener solo números (10-15 dígitos)')
        return telefono

    @classmethod
    def validar_estadoEnEmpresa(cls, estadoEnEmpresa):
        estado = int(estadoEnEmpresa)
        estados_validos = list(estadoEnEmpresaDict.keys())
        if estado not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return estado
    
    @classmethod
    def validar_idEmpresaExistente(cls, idEmpresa):
        """Convierte el ID a UUID y valida que la empresa exista."""
        from models.Mongo.MongoModel import MongoModel

        try:
            if not isinstance(idEmpresa, UUID):
                idEmpresa = UUID(idEmpresa)

            empresa = MongoModel.obtener_empresa_por_id(idEmpresa)
            if not empresa:
                raise ValueError(f"La empresa con ID {idEmpresa} no existe.")
            return idEmpresa
        except ValueError as e:
            raise ValueError(f"El ID ingresado no es un UUID válido. Error:{e}")

    @classmethod
    def validar_fecha(cls, fecha):
        """Convierte la fecha a datetime y valida el formato."""
        try:
            return datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS.")
