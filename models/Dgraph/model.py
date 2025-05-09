# 1- Importaciones

#!/usr/bin/env python3
import datetime
import json
import pydgraph
import csv
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 2- Definición de esquema

def set_schema(client):
    schema = """
    type Empresa {
        idEmpresa
        nombreEmpresa
        ubicacion
        
        DA_SERVICIO: [Ticket]
        TIENE: [Agente]
        GUARDA: [Ticket]
    }

    type Agente {
        idAgente
        nombreAgente
        
        TRABAJA: Empresa
        SOLUCIONA: [Ticket]
    }

    type Cliente {
        idCliente
        nombreCliente
        
        AFILIADO_A: Empresa
        ABRE: [Ticket]
    }

    type Ticket {
        idTicket
        tipoProblema
        descripcion
        
        SOLUCIONA: Agente
        LE_CORRESPONDE: Cliente
        PERTENECE: Empresa
        ABRE: Cliente
    }

    idEmpresa: string @index(exact) @upsert .
    nombreEmpresa: string @index(term) .
    ubicacion: geo .

    idAgente: string @index(exact) @upsert .
    nombreAgente: string @index(term) .

    idCliente: string @index(exact) @upsert .
    nombreCliente: string @index(term) .

    idTicket: string @index(exact) @upsert .
    tipoProblema: int .
    descripcion: string @index(fulltext) .

    DA_SERVICIO: [uid] @reverse .
    TIENE: [uid] @reverse .
    TRABAJA: uid @reverse .
    SOLUCIONA: [uid] @reverse .
    LE_CORRESPONDE: uid @reverse .
    ABRE: [uid] @reverse .
    PERTENECE: uid @reverse .
    AFILIADO_A: uid @reverse .
    GUARDA: [uid] @reverse .
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op) 
# ---------------------------------------------------------------------------------------

# 3- Carga de datos

import csv

def create_data(client):
    empresa_uids = {}
    empresas = []

    # 1️ EMPRESAS
    txn = client.txn()
    try:
        with open('data/dgraph/empresas.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                coords = json.loads(row['ubicacion'])
                lat, lon = coords
                empresa = {
                    'uid': f"_:{row['idEmpresa']}",
                    'idEmpresa': row['idEmpresa'],
                    'nombreEmpresa': row['nombreEmpresa'],
                    'ubicacion': {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    }
                }
                empresas.append(empresa)

        response = txn.mutate(set_obj=empresas, commit_now=True)
        for row in empresas:
            empresa_uids[row['idEmpresa']] = response.uids.get(row['uid'][2:], '')
    finally:
        txn.discard()
    print("👌 Empresas cargadas con éxito.")

    # 2️ AGENTES
    agente_uids = {}
    agentes = []

    txn = client.txn()
    try:
        with open('data/dgraph/agentes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                agente = {
                    'uid': f"_:{row['idAgente']}",
                    'idAgente': row['idAgente'],
                    'nombreAgente': row['nombreAgente']
                }
                agentes.append(agente)

        response = txn.mutate(set_obj=agentes, commit_now=True)
        for row in agentes:
            agente_uids[row['idAgente']] = response.uids.get(row['uid'][2:], '')
    finally:
        txn.discard()
    print("👌 Agentes cargados con éxito.")

    # 3️ CLIENTES
    cliente_uids = {}
    clientes = []

    txn = client.txn()
    try:
        with open('data/dgraph/clientes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cliente = {
                    'uid': f"_:{row['idCliente']}",
                    'idCliente': row['idCliente'],
                    'nombreCliente': row['nombreCliente']
                }
                clientes.append(cliente)

        response = txn.mutate(set_obj=clientes, commit_now=True)
        for row in clientes:
            cliente_uids[row['idCliente']] = response.uids.get(row['uid'][2:], '')
    finally:
        txn.discard()
    print("👌 Clientes cargados con éxito.")

    # 4️ TICKETS
    ticket_uids = {}
    tickets = []

    txn = client.txn()
    try:
        with open('data/dgraph/tickets.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticket = {
                    'uid': f"_:{row['idTicket']}",
                    'idTicket': row['idTicket'],
                    'tipoProblema': int(row['tipoProblema']),
                    'descripción': row['descripción']
                }
                tickets.append(ticket)

        response = txn.mutate(set_obj=tickets, commit_now=True)
        for row in tickets:
            ticket_uids[row['idTicket']] = response.uids.get(row['uid'][2:], '')
    finally:
        txn.discard()
    print("👌 Tickets cargados con éxito.")

    # 5️ RELACIONES
    txn = client.txn()
    try:
        all_uids = {**empresa_uids, **agente_uids, **cliente_uids, **ticket_uids}
        with open('data/dgraph/relaciones.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # No toma en cuenta las filas vacías 
                if not row['origen'].strip() or not row['relacion'].strip() or not row['destino'].strip():
                    continue
                origen_id = row['origen'].strip()
                tipo_relacion = row['relacion'].strip().strip('"')
                destino_id = row['destino'].strip()

                origen_uid = all_uids.get(origen_id)
                destino_uid = all_uids.get(destino_id)

                if origen_uid and destino_uid:
                    relacion = {
                        'uid': origen_uid,
                        tipo_relacion: {'uid': destino_uid}
                    }
                    txn.mutate(set_obj=relacion)
                else:
                    print(f"🤦‍♀️ UIDs no encontrados: origen={origen_id}, destino={destino_id}")

        txn.commit()
        print("👌 Todas las relaciones cargadas con éxito.")
    finally:
        txn.discard()

    