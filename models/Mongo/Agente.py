from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime
import re
from models.Utils.dictionaries import estadoEnEmpresa as estadoEnEmpresaDict
from models.Utils.regularExpresions import (
    correo_regex,
    telefono_regex,
)

class AgenteValidationError(Exception):
    """Excepción personalizada para errores de validación de agentes"""
    def __init__(cls, message="Error de validación en datos del agente"):
        cls.message = message
        super().__init__(cls.message)

class Agente(BaseModel):
    idAgente: UUID = Field(default_factory=uuid4)
    nombre: str
    correo: str
    telefono: str
    estadoEnEmpresa: int
    idEmpresa: UUID
    fechaIngreso: datetime

    @field_validator('nombre')
    @classmethod
    def validar_nombre_completo(cls, nombre):
        if len(nombre.strip().split()) < 2:
            raise ValueError('El nombre debe contener al menos nombre y apellido')
        return nombre.title()

    @field_validator('correo')
    @classmethod
    def validar_formato_correo(cls, correo):
        if not re.match(correo_regex, correo):
            raise ValueError('Formato de correo electrónico inválido')
        return correo.lower()

    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, telefono):
        if not re.match(telefono_regex, telefono):  # Admite números internacionales
            raise ValueError('El teléfono debe contener solo números (10-15 dígitos)')
        return telefono

    @field_validator('estadoEnEmpresa')
    @classmethod
    def validar_estado(cls, estadoEmpresa):
        estados_validos = [1, 2, 3]
        if estadoEmpresa not in estados_validos:
            raise ValueError(f'Estado inválido. Opciones válidas: {", ".join(estados_validos)}')
        return estadoEmpresa

    @classmethod
    def crear_desde_dict(cls, data: dict):
        try:
            return cls(**data)
        except Exception as e:
            raise AgenteValidationError(str(e))