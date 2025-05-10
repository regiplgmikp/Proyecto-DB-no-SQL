from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime
from models.Utils.validaciones import Validaciones

class AgenteValidationError(Exception):
    """Excepción personalizada para errores de validación de agentes"""
    def __init__(cls, message="Error de validación en datos del agente"):
        cls.message = message
        super().__init__(cls.message)

class Agente(BaseModel):
    idAgente: UUID = Field(default_factory=uuid4) # Si no se proporciona un ID, se genera uno nuevo
    nombre: str
    correo: str
    telefono: str
    estadoEnEmpresa: int
    idEmpresa: UUID
    fechaIngreso: datetime

    @field_validator('nombre')
    def validar_nombre_completo(nombre):
        return Validaciones.validar_nombre(nombre)

    @field_validator('correo')
    def validar_formato_correo(correo):
        return Validaciones.validar_formato_correo(correo)

    @field_validator('telefono')
    def validar_telefono(telefono):
        return Validaciones.validar_telefono(telefono)

    @field_validator('estadoEnEmpresa')
    def validar_estadoEnEmpresa(estadoEnEmpresa):
        return Validaciones.validar_estadoEnEmpresa(estadoEnEmpresa)

    @field_validator('idEmpresa')
    def validar_idEmpresa(idEmpresa):
        return Validaciones.validar_idEmpresaExistente(idEmpresa)

    @classmethod
    def crear_desde_dict(cls, data: dict):
        try:
            return cls(**data)
        except Exception as e:
            raise AgenteValidationError(str(e))