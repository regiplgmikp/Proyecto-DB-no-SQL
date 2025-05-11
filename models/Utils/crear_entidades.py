import uuid
from models.Mongo.MongoModel import MongoModel
from datetime import datetime
# import models.Dgraph.model as DgraphModel
# import models.Cassandra.model as CassandraModel

import models.Utils.dictionaries as dictionaries
from models.Utils.validaciones import (Validaciones, solicitar_input)

def crear_agente():
    mongo_agente = {}
    cassandra_agente = {}
    dgraph_agente = {}

    estadosEnEmpresa = dictionaries.estadoEnEmpresa

    # Obtener los datos del agente
    idAgente = uuid.uuid4() 
    nombre = solicitar_input("Ingrese el nombre del agente: ", Validaciones.validar_nombre)
    correo = solicitar_input("Ingrese el correo del agente: ", Validaciones.validar_formato_correo)
    telefono = solicitar_input("Ingrese el teléfono del agente: ", Validaciones.validar_telefono)
    estadoEnEmpresa = solicitar_input(f"Ingrese el numero del estado en empresa del agente \n\tEstados posibles: {estadosEnEmpresa}): ", Validaciones.validar_estadoEnEmpresa) 
    idEmpresa = solicitar_input("Ingrese el id de la empresa del agente: ", Validaciones.validar_idEmpresaExistente)['idEmpresa']
    fechaIngreso = solicitar_input("Ingrese la fecha de ingreso (YYYY-MM-DD HH:MM:SS): ", Validaciones.validar_fecha)  # Convertir a datetime
    # Agreguen los datos que necesiten obtener de sus entidades -----------------------------------------------------------

    # Asignar valores a cada diccionario
    # Mongo
    mongo_agente['idAgente'] = idAgente
    mongo_agente['nombre'] = nombre
    mongo_agente['correo'] = correo
    mongo_agente['telefono'] = telefono
    mongo_agente['estadoEnEmpresa'] = estadoEnEmpresa
    mongo_agente['idEmpresa'] = idEmpresa
    mongo_agente['fechaIngreso'] = fechaIngreso

    # Asignen sus valores a sus diccionarios ----------------------------------------------------------------------------
    # Dgraph

    # Cassandra


    # Insertar agentes (Se asume que todos tienen su método insertar_agente() dentro de archivo model)
    try:
        # Insertar en MongoDB
        agente = MongoModel.insertar_agente(mongo_agente)
        print(f"Agente: \n{agente}\nInsertado con éxito")

    
    # Insertar en Dgraph
    # DgraphModel.insertar_atente(dgraph_agente)
    # Insertar en Cassandra
    # CassandraModel.insertar_atente(cassandra_agente)

    except Exception as e:
        print(f"Error en la inserción de agente: {e}")
# Repetir funciones para inserciones de demás entidades
def crear_empresa():

    mongo_empresa = {}

    # Obtener los datos de la empresa
    idEmpresa = uuid.uuid4()
    nombre = solicitar_input("Ingrese el nombre del empresa: ", Validaciones.validar_nombre)
    correo = solicitar_input("Ingrese el correo del empresa: ", Validaciones.validar_formato_correo)
    telefono = solicitar_input("Ingrese el teléfono del empresa: ", Validaciones.validar_telefono)
    direccion = solicitar_input("Inserte la dirección de la empresa: ")

    # Asignar valores a cada diccionario
    # Mongo
    mongo_empresa['idEmpresa'] = idEmpresa
    mongo_empresa['nombre'] = nombre
    mongo_empresa['correo'] = correo
    mongo_empresa['telefono'] = telefono
    mongo_empresa['direccion'] = direccion

    try: 
        # Insertar empresa a bases de datos
        empresa = MongoModel.insertar_empresa(mongo_empresa)
        print(f"Empresa: \n{empresa}\nIngresada con éxito")

    except Exception as e:
        print(f"Error en la inserción de empresa: {e}")

def crear_cliente():
    mongo_cliente = {}

    estadosCuenta = dictionaries.estadoCuenta

    # Obtener los datos del Cliente
    idCliente = uuid.uuid4()
    nombre = solicitar_input("Ingrese el nombre del cliente: ", Validaciones.validar_nombre)
    correo = solicitar_input("Ingrese el correo del cliente: ", Validaciones.validar_formato_correo)
    telefono = solicitar_input("Ingrese el teléfono del cliente: ", Validaciones.validar_telefono)
    estadoCuenta = solicitar_input(f"Inserte el estado de la cuenta del cliente \n\tEstados posibles: {estadosCuenta}): ", Validaciones.validar_estadoCuenta)
    idEmpresa = solicitar_input("Inserte el id de la empresa de la que es cliente: ", Validaciones.validar_idEmpresaExistente)['idEmpresa']

    # Asignar valores a cada diccionario
    # Mongo
    mongo_cliente['idCliente'] = idCliente
    mongo_cliente['nombre'] = nombre
    mongo_cliente['correo'] = correo
    mongo_cliente['telefono'] = telefono
    mongo_cliente['estadoCuenta'] = estadoCuenta
    mongo_cliente['idEmpresa'] = idEmpresa

    try: 
        # Insertar empresa a bases de datos
        cliente = MongoModel.insertar_cliente(mongo_cliente)
        print(f"Cliente: \n{cliente}\nIngresada con éxito")

    except Exception as e:
        print(f"Error en la inserción de cliente: {e}")

def crear_ticket():
    mongo_ticket = {}

    prioridadesTicket = dictionaries.prioridad

    # Obtener los datos del Cliente
    idTicket = uuid.uuid4()
    idCliente = solicitar_input("Inserte el id del cliente que crea el ticket: ", Validaciones.validar_idClienteExistente)['idCliente']
    idAgente = solicitar_input("Inserte el id del agente que se le asignará el ticket (dejar en blanco para no asignar agente): ", Validaciones.validar_idAgenteExistente, True)
    if idAgente:
        idAgente = idAgente['idAgente']
    idEmpresa = solicitar_input("Inserte el id de la empresa de la que es cliente: ", Validaciones.validar_idEmpresaExistente)['idEmpresa']
    fechaCreacion = solicitar_input("Inserte la fecha en la que se crea el ticket (enter para establecer para hoy): ", Validaciones.validar_fecha, True)
    if not fechaCreacion:
        fechaCreacion = datetime.today()
    comentario = solicitar_input("Inserte comentario de inicio de ticket (dejar en blanco para no agregar comentario): ", canBeNone=True)
    estadoTicket = 2 if idAgente else 1
    prioridad = solicitar_input(f"Inserte la prioridad del ticket \n\tPrioridades posibles: {prioridadesTicket}): ", Validaciones.validar_prioridadTicket)


    # Asignar valores a cada diccionario
    # Mongo
    mongo_ticket['idTicket'] = idTicket
    mongo_ticket['idCliente'] = idCliente
    mongo_ticket['idAgente'] = idAgente
    mongo_ticket['idEmpresa'] = idEmpresa
    mongo_ticket['fechaCreacion'] = fechaCreacion
    mongo_ticket['comentarios'] = [comentario] if comentario else []
    mongo_ticket['estado'] = estadoTicket
    mongo_ticket['prioridad'] = prioridad

    try: 
        # Insertar empresa a bases de datos
        ticket = MongoModel.insertar_ticket(mongo_ticket)
        print(f"Ticket: \n{ticket}\nIngresado con éxito")

    except Exception as e:
        print(f"Error en la inserción de ticket: {e}")