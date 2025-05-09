from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime
import re
from models.Utils.dictionaries import estadoEnEmpresa as estadoEnEmpresaDict
from models.Utils.regularExpresions import (
    correo_regex,
    telefono_regex,
)

class EmpresaValidationError(Exception):
    """Excepción personalizada para errores de validación de Empresas"""
    def __init__(cls, message="Error de validación en datos del Empresa"):
        cls.message = message
        super().__init__(cls.message)

class Empresa(BaseModel):
    idEmpresa: UUID = Field(default_factory=uuid4) # Si no se proporciona un ID, se genera uno nuevo
    nombre: str
    correo: str
    telefono: str
    direccion: str

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
        if not re.match(telefono_regex, telefono):
            raise ValueError('El teléfono debe contener solo números (10-15 dígitos)')
        return telefono

    @classmethod
    def crear_desde_dict(cls, data: dict):
        try:
            return cls(**data)
        except Exception as e:
            raise EmpresaValidationError(str(e))