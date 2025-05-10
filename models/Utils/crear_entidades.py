import uuid
from models.Mongo.MongoModel import MongoModel
# import models.Dgraph.model as DgraphModel
# import models.Cassandra.model as CassandraModel

import models.Utils.dictionaries as dictionaries
from models.Utils.validaciones import Validaciones

def solicitar_input(mensaje, validacion_func=None):
    """Solicita un input al usuario y lo valida si es necesario."""
    while True:
        valor = input(mensaje)
        if validacion_func:
            try:
                return validacion_func(valor)
            except ValueError as e:
                print(f"\tError: {e}")
        else:
            return valor

def create_agente():
    mongo_agente = {}
    cassandra_agente = {}
    dgraph_agente = {}

    estadoEnEmpresa = dictionaries.estadoEnEmpresa

    # Obtener los datos del agente
    idAgente = uuid.uuid4() 
    nombre = solicitar_input("Ingrese el nombre del agente: ", Validaciones.validar_nombre)
    correo = solicitar_input("Ingrese el correo del agente: ", Validaciones.validar_formato_correo)
    telefono = solicitar_input("Ingrese el teléfono del agente: ", Validaciones.validar_telefono)
    estadoEnEmpresa = solicitar_input(f"Ingrese el numero del estado en empresa del agente \n\tEstados posibles: {estadoEnEmpresa}): ", Validaciones.validar_estadoEnEmpresa) 
    idEmpresa = solicitar_input("Ingrese el id de la empresa del agente: ", Validaciones.validar_idEmpresaExistente)
    fechaIngreso = solicitar_input("Ingrese la fecha de ingreso (YYYY-MM-DD HH:MM:SS): ", Validaciones.validar_fecha)  # Convertir a datetime
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
    try:
        MongoModel.insertar_agente(mongo_agente)
    
    # Insertar en Dgraph
    # DgraphModel.insertar_atente(dgraph_agente)
    # Insertar en Cassandra
    # CassandraModel.insertar_atente(cassandra_agente)

    except Exception as e:
        print(f"Erro en la inserción de agente: {e}")
# Repetir funciones para inserciones de demás entidades
def create_empresa():
    pass

def create_cliente():
    pass

def create_ticket():
    pass