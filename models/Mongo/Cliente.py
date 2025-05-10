from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
import re
from models.Utils.dictionaries import estadoCuenta as estadoCuentaDict
from models.Utils.regularExpresions import (
    nombre_regex,
    correo_regex,
    telefono_regex
)

class ClienteValidationError(Exception):
    """Excepción personalizada para errores de validación de Clientes"""
    def __init__(cls, message="Error de validación en datos del Cliente"):
        cls.message = message
        super().__init__(cls.message)

class Cliente(BaseModel):
    idCliente: UUID = Field(default_factory=uuid4) # Si no se proporciona un ID, se genera uno nuevo
    nombre: str
    correo: str
    telefono: str
    estadoCuenta: int
    idEmpresa: UUID

    @field_validator('nombre')
    @classmethod
    def validar_nombre_completo(cls, nombre):
        if not re.match(nombre_regex, nombre):
            raise ValueError('El nombre debe contener al menos nombre y apellido')
        return nombre.lower()
    
    @field_validator('correo')
    @classmethod
    def validar_formato_correo(cls, correo):
        if not re.match(correo_regex, correo):
            raise ValueError('Formato de correo electrónico inválido')
        return correo.lower()

    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, telefono):
        if not re.match(telefono_regex, telefono):
            raise ValueError('El teléfono debe contener solo números (10-15 dígitos)')
        return telefono
    
    @field_validator('estadoCuenta')
    @classmethod
    def validar_estado(cls, estadoCuenta):
        estados_validos = list(estadoCuentaDict.keys())
        if estadoCuenta not in estados_validos:
            raise ValueError(f'Estado inválido. estados válidos: {estados_validos}')
        return estadoCuenta

    @classmethod
    def crear_desde_dict(cls, data: dict):
        try:
            return cls(**data)
        except Exception as e:
            raise ClienteValidationError(str(e))