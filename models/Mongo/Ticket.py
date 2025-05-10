from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from models.Utils.dictionaries import (
    estado as estadoDict, 
    prioridad as prioridadDict
    )

class TicketValidationError(Exception):
    """Excepción personalizada para errores de validación de Tickets"""
    def __init__(cls, message="Error de validación en datos del Ticket"):
        cls.message = message
        super().__init__(cls.message)

class Ticket(BaseModel):
    idTicket: UUID = Field(default_factory=uuid4)
    idCliente: UUID
    idAgente: Optional[UUID] = None
    idEmpresa: UUID
    fechaCreacion: datetime
    fechaCierre: Optional[datetime] = None
    comentarios: list[str] = []
    estado: int
    prioridad: int

    @model_validator(mode='after')
    def validar_fechas(self):
        if self.fechaCierre and self.fechaCierre < self.fechaCreacion:
            raise ValueError("La fecha de cierre no puede ser anterior a la fecha de creación")
        return self

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, estado):
        estados_validos = list(estadoDict.keys())
        if estado not in estados_validos:
            raise ValueError(f'Estado inválido. Estados válidos: {estados_validos}')
        return estado

    @field_validator('prioridad')
    @classmethod
    def validar_prioridad(cls, prioridad):
        prioridades_validas = list(prioridadDict.keys())
        if prioridad not in prioridades_validas:
            raise ValueError(f'Prioridad inválida. Prioridades válidas: {prioridades_validas}')
        return prioridad

    
    @classmethod
    def crear_desde_dict(cls, data: dict):
        try:
            return cls(**data)
        except Exception as e:
            raise TicketValidationError(str(e))