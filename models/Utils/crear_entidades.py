import uuid
import models.Mongo.model as MongoModel
import models.Dgraph.model as DgraphModel
import models.Cassandra.model as CassandraModel
from uuid import UUID
from datetime import datetime
import models.Utils.dictionaries as dictionaries

def create_agente():
    mongo_agente = {}
    cassandra_agente = {}
    dgraph_agente = {}

    estadoEnEmpresa = dictionaries.estadoEnEmpresa

    # Obtener los datos del agente
    idAgente = uuid.uuid4() 
    nombre = input("Ingrese el nombre del agente: ")
    correo = input("Ingrese el correo del agente: ")
    telefono = input("Ingrese el teléfono del agente: ")
    estadoEnEmpresa = int(input(f"Ingrese el numero del estado en empresa del agente \n\tEstados posibles: {estadoEnEmpresa}): "))  
    idEmpresa = UUID(input("Ingrese el idEmpresa del agente: ")) 
    fechaIngreso = datetime.strptime(input("Ingrese la fecha de ingreso (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")  # Convertir a datetime
    # Agreguen los datos que necesiten obtener de sus entidades -----------------------------------------------------------

    # Asignar valores al diccionario
    mongo_agente['idAgente'] = idAgente
    mongo_agente['nombre'] = nombre
    mongo_agente['correo'] = correo
    mongo_agente['telefono'] = telefono
    mongo_agente['estadoEnEmpresa'] = estadoEnEmpresa
    mongo_agente['idEmpresa'] = idEmpresa
    mongo_agente['fechaIngreso'] = fechaIngreso

    # Asignen sus valores a sus diccionarios ----------------------------------------------------------------------------

    # Insertar agentes (Se asume que todos tienen su método insertar_agente() dentro de archivo model)
    # Insertar en MongoDB
    MongoModel.insertar_agente(mongo_agente)
    # Insertar en Dgraph
    DgraphModel.insertar_atente(dgraph_agente)
    # Insertar en Cassandra
    CassandraModel.insertar_atente(cassandra_agente)

# Repetir funciones para inserciones de demás entidades
def create_empresa():
    pass

def create_cliente():
    pass

def create_ticket():
    pass