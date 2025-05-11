from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from models.Utils.validaciones import Validaciones

class DgraphAgente(BaseModel):
    idAgente: str = Field(default_factory=lambda: str(uuid4()))
    nombreAgente: str

    @validator('nombreAgente')
    def validar_nombre(cls, v):
        return Validaciones.validar_nombre(v)

class DgraphCliente(BaseModel):
    idCliente: str = Field(default_factory=lambda: str(uuid4()))
    nombreCliente: str

    @validator('nombreCliente')
    def validar_nombre(cls, v):
        return Validaciones.validar_nombre(v)

class DgraphTicket(BaseModel):
    idTicket: str = Field(default_factory=lambda: str(uuid4()))
    tipoProblema: int
    descripcion: str

class DgraphEmpresa(BaseModel):
    idEmpresa: str = Field(default_factory=lambda: str(uuid4()))
    nombreEmpresa: str
    direccion: str
