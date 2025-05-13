#!/usr/bin/env python3
import datetime
from cassandra.cluster import Cluster
from cassandra.util import uuid_from_time
from datetime import datetime
import logging
import csv
import uuid

from cassandra.query import BatchStatement

# Logger
log = logging.getLogger()

# CREACION TABLAS (MODELADO)
# Keyspace
CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS cassandra_final
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': 1}}
""" 

# Empresas
CREATE_EMPRESA_TABLE = """ 
    CREATE TABLE IF NOT EXISTS empresa (
        idEmpresa UUID, 
        fecha TIMEUUID,
        idTicket UUID,
        PRIMARY KEY ((idEmpresa), fecha)
    )
"""

# Ticket por comentario
CREATE_TICKEY_BY_COMMENT_TABLE = """ 
    CREATE TABLE IF NOT EXISTS ticket_com (
        idTicket UUID,
        fecha TIMEUUID,
        idAgente UUID,
        comentario TEXT,
        PRIMARY KEY((idTicket), fecha)
    )
"""

# Ticket por agente
CREATE_TICKET_BY_AGENT_TABLE = """ 
    CREATE TABLE IF NOT EXISTS ticket_age (
        idTicket UUID,
        fecha TIMEUUID,
        idAgente UUID,
        PRIMARY KEY((idTicket), fecha)
    )
"""

# Ticket por estado
CREATE_TICKET_BY_STATE_TABLE = """ 
    CREATE TABLE IF NOT EXISTS ticket_est (
        idTicket UUID,
        fecha TIMEUUID,
        estado INT, 
        PRIMARY KEY((idTicket), fecha)
    )
"""

# Ticket por prioridad
CREATE_TICKET_BY_PRIORITY_TABLE = """ 
    CREATE TABLE IF NOT EXISTS ticket_prio (
        idTicket UUID,
        fecha TIMEUUID,
        prioridad INT,
        PRIMARY KEY((idTicket), fecha) 
    )
"""

# Agente
CREATE_AGENT_TABLE = """ 
    CREATE TABLE IF NOT EXISTS agente (
        idAgente UUID,
        fecha TIMEUUID,
        estadoEnEmpresa INT,
        PRIMARY KEY((idAgente), fecha)
    )
"""

# Cliente
CREATE_CLIENT_TABLE = """ 
    CREATE TABLE IF NOT EXISTS cliente (
        idCliente UUID,
        fecha TIMEUUID,
        estadoCuenta INT,
        PRIMARY KEY ((idCliente), fecha)
    )
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    # Creacion de las tablas
    session.execute(CREATE_EMPRESA_TABLE)
    session.execute(CREATE_TICKEY_BY_COMMENT_TABLE)
    session.execute(CREATE_TICKET_BY_AGENT_TABLE)
    session.execute(CREATE_TICKET_BY_STATE_TABLE)
    session.execute(CREATE_TICKET_BY_PRIORITY_TABLE)
    session.execute(CREATE_AGENT_TABLE)
    session.execute(CREATE_CLIENT_TABLE)
    print("✅ Tablas creadas")

    # Insertar los datos del csv empresas
    with open('data/cassandra/empresas.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_empresa = uuid.UUID(row['idEmpresa'])
            fecha_csv = row['fecha']
            id_ticket = uuid.UUID(row['idTicket'])

            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO empresa (idEmpresa, fecha, idTicket)
                VALUES(%s, %s, %s)
                """,
                (id_empresa, fecha_uuid, id_ticket)
            )

        print("✅ Datos insertados en tabla EMPRESA.")

    # Insertar los datos del csv ticket_com
    with open('data/cassandra/tickets_com.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_ticket = uuid.UUID(row['idTicket'])
            fecha_csv = row['fecha']
            id_agente = uuid.UUID(row['idAgente'])
            comm = row['comentario']

            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO ticket_com (idTicket, fecha, idAgente, comentario)
                VALUES(%s, %s, %s, %s)
                """,
                (id_ticket, fecha_uuid, id_agente, comm)
            )

        print("✅ Datos insertados en tabla TICKET_COM")

    # Insertar los datos del csv ticket_age
    with open('data/cassandra/tickets_age.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_ticket = uuid.UUID(row['idTicket'])
            fecha_csv = row['fecha']
            # Elimina los espacios en blanco (los idAgente cuando el ticket no tiene uno)
            raw_id_agente = row['idAgente'].strip()
            # Automaticamente no asigna ningun agente
            id_agente = None

            if raw_id_agente:
                id_agente = uuid.UUID(raw_id_agente)
        
            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv.replace("Z", ""))
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO ticket_age (idTicket, fecha, idAgente)
                VALUES(%s, %s, %s)
                """,
                (id_ticket, fecha_uuid, id_agente)
            )

        print("✅ Datos insertados en tabla TICKET_AGE")

    # Insertar los datos del csv ticket_est
    with open('data/cassandra/tickets_est.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_ticket = uuid.UUID(row['idTicket'])
            fecha_csv = row['fecha']
            estado_csv = int(row['estado'])

            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO ticket_est (idTicket, fecha, estado)
                VALUES(%s, %s, %s)
                """,
                (id_ticket, fecha_uuid, estado_csv)
            )
        
        print("✅ Datos insertados en tabla TICKET_EST")

    # Insertar los datos del csv ticket_prio
    with open('data/cassandra/tickets_prio.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_ticket = uuid.UUID(row['idTicket'])
            fecha_csv = row['fecha']
            prio = int(row['prioridad'])

            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO ticket_prio (idTicket, fecha, prioridad)
                VALUES(%s, %s, %s)
                """,
                (id_ticket, fecha_uuid, prio)
            )

        print("✅ Datos insertados en tabla TICKET_PRIO")

    # Insertar los datos del csv agente
    with open('data/cassandra/agentes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_agente = uuid.UUID(row['idAgente'])
            fecha_csv = row['fecha']
            estado_empresa = int(row['estadoEnEmpresa'])

            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO agente (idAgente, fecha, estadoEnEmpresa)
                VALUES(%s, %s, %s)
                """,
                (id_agente, fecha_uuid, estado_empresa)
            )

        print("✅ Datos insertados en tabla AGENTE")

    # Insertar los datos del csv cliente
    with open('data/cassandra/clientes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            id_cliente = uuid.UUID(row['idCliente'])
            fecha_csv = row['fecha']
            estado_cuenta = int(row['estado'])
            
            # Convertir fecha ISO a TIMEUUID
            fecha_datetime = datetime.fromisoformat(fecha_csv)
            fecha_uuid = uuid_from_time(fecha_datetime)

            session.execute(
                """
                INSERT INTO cliente (idCliente, fecha, estadoCuenta)
                VALUES(%s, %s, %s)
                """,
                (id_cliente, fecha_uuid, estado_cuenta)
            )
        
        print("✅ Datos insertados en tabla CLIENTE")

# Creacion de un nuevo agente
def insertar_agente(session, new_age):
    try:
        # Parametros del nuevo agente
        id_agente = new_age['idAgente']
        fecha = new_age['fecha']
        estado = int(new_age['estadoenEmpresa'])

        # Convertir la fecha de datetime a UUID
        fecha_uuid = uuid_from_time(fecha)

        # Agregar datos a la tabla agente
        session.execute(
            """
            INSERT INTO agente (idAgente, fecha, estadoEnEmpresa)
            VALUES (%s, %s, %s)
            """,
            (id_agente, fecha_uuid, estado)
        )

        print(f"Agente {id_agente} agregado!")
    
    except Exception as error:
        print(f"Error al insertar agente: {error}")

# Creacion de una nueva empresa
def insertar_empresa(session, new_emp):
    try:
        # Parametros de la nueva empresa
        id_empresa = new_emp['idEmpresa']
        fecha = new_emp['fecha']
        id_ticket = new_emp['idTicket']

        # Convertir fecha de datetime a UUID
        fecha_uuid = uuid_from_time(fecha)

        # Agregar la empresa a la tabla
        session.execute(
            """
            INSERT INTO empresa (idEmpresa, fecha, idTicket)
            VALUES (%s, %s, %s)
            """,
            (id_empresa, fecha_uuid, id_ticket)
        )

        print(f"Empresa {id_empresa} agregada!")

    except Exception as error:
        print(f"Error al insertar empresa: {error}")

# Creacion de un nuevo cliente
def insertar_cliente(session, new_cli):
    try:
        # Parametros del nuevo cliente
        id_cliente = new_cli['idCliente']
        fecha = new_cli['fecha']
        estado_cuenta = new_cli['estado']

        # Convertir fecha de datetime a UUID
        fecha_uuid = uuid_from_time(fecha)

        # Agregar cliente a la tabla
        session.execute(
            """
            INSERT INTO cliente (idCliente, fecha, estado)
            VALUES (%s, %s, %s)
            """,
            (id_cliente, fecha_uuid, estado_cuenta)
        )

        print(f"Cliente {id_cliente} agregado!")

    except Exception as error:
        print(f"Error al insertar cliente: {error}")

def delete_schema(session):
    session.execute("DROP KEYSPACE IF EXISTS cassandra_final")
    print("💥 Keyspace cassandra_final eliminado por completo.")