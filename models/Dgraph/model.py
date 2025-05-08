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

def create_data(client):
     empresa_uids = {}
    txn = client.txn()

    try:
        #Carga de datos de la empresa
        ith open('data/empresas.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                empresa = {
                    'uid': '_:{}'.format(row['idEmpresa']),
                    'idEmpresa': row['idEmpresa'],
                    'nombreEmpresa': row['nombreEmpresa'],
                    'ubicacion': row['ubicacion']
                }
                empresas.append(empresa)

        response = txn.mutate(set_obj=empresas, commit_now=True)
        for empresa in empresas:
            empresa_uids[empresa['idEmpresa']] = response.uids.get(empresa['uid'][2:], '')


    agente_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los agentes
        with open('data/agentes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                agente = {
                    'uid': '_:{}'.format(row['idAgente']),
                    'idAgente': row['idAgente'],
                    'nombreAgente': row['nombreAgente'],
                    'TRABAJA': {'uid': empresa_uids.get(row['empresa'])}
                }
                agentes.append(agente)

        response = txn.mutate(set_obj=agentes, commit_now=True)
        for agente in agentes:
            agente_uids[agente['idAgente']] = response.uids.get(agente['uid'][2:], '')

    cliente_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los clientes
        with open('data/clientes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cliente = {
                    'uid': '_:{}'.format(row['idCliente']),
                    'idCliente': row['idCliente'],
                    'nombreCliente': row['nombreCliente'],
                    'AFILIADO_A': {'uid': empresa_uids.get(row['empresa'])}
                }
                clientes.append(cliente)

        response = txn.mutate(set_obj=clientes, commit_now=True)
        for cliente in clientes:
            cliente_uids[cliente['idCliente']] = response.uids.get(cliente['uid'][2:], '')

    ticket_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los tickets
        with open('data/tickets.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticket = {
                    'uid': '_:{}'.format(row['idTicket']),
                    'idTicket': row['idTicket'],
                    'tipoProblema': int(row['tipoProblema']),
                    'descripcion': row['descripcion'],
                    'SOLUCIONA': {'uid': agente_uids.get(row['agente'])},
                    'LE_CORRESPONDE': {'uid': cliente_uids.get(row['cliente'])},
                    'PERTENECE': {'uid': empresa_uids.get(row['empresa'])},
                    'ABRE': {'uid': cliente_uids.get(row['cliente'])}
                }
                tickets.append(ticket)

        response = txn.mutate(set_obj=tickets, commit_now=True)
        for ticket in tickets:
            ticket_uids[ticket['idTicket']] = response.uids.get(ticket['uid'][2:], '')
        
        # Cargar relaciones desde relaciones.csv
        all_uids = {**empresa_uids, **agente_uids, **cliente_uids, **ticket_uids}

        with open('data/relaciones.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                origen_id = row['origen'].strip()
                tipo_relacion = row['relacion'].strip()
                destino_id = row['destino'].strip()

                origen_uid = all_uids.get(origen_id)
                destino_uid = all_uids.get(destino_id)

                if origen_uid and destino_uid:
                    relacion = {
                        'uid': origen_uid,
                        tipo_relacion: {'uid': destino_uid}
                    }
                    txn.mutate(set_obj=relacion, commit_now=True)
                else:
                    print(f"UIDs no encontrados: origen={origen_id}, destino={destino_id}")

    finally:
        txn.discard()

    print("Datos cargados exitosamente en DGraph.")

# ---------------------------------------------------------------------------------------

# 4. Consultas

def print_json(res):
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))

# 4.1 Mostrar agente por empresa
def search_agentes_by_empresa(client, empresa_id):
    query = """
    query all($empresa_id: string) {
      all(func: has(TRABAJA)) @filter(eq(TRABAJA, $empresa_id)) {
        idAgente
        nombreAgente
      }
    }
    """
    variables = {'$empresa_id': empresa_id}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_json(res)

# 4.2 Mostrar clientes por empresa
def search_clientes_by_empresa(client, empresa_id):
    query = """
    query all($empresa_id: string) {
      all(func: has(AFILIADO_A)) @filter(eq(AFILIADO_A, $empresa_id)) {
        idCliente
        nombreCliente
      }
    }
    """
    variables = {'$empresa_id': empresa_id}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_json(res)

# 4.3 Mostrar cliente por ticket
def search_cliente_by_ticket(client, ticket_id):
    query = """
    query all($ticket_id: string) {
      all(func: has(LE_CORRESPONDE)) @filter(eq(LE_CORRESPONDE, $ticket_id)) {
        idCliente
        nombreCliente
      }
    }
    """
    variables = {'$ticket_id': ticket_id}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_json(res)

# 4.4 Mostrar tickets por empresa :)