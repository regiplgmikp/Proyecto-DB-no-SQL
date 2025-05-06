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

            DA_SERVICIO
            TIENE
            GUARDA
        }

        type Agente {
            idAgente
            nombreAgente

            TRABAJA
        }

        type Cliente {
            idCliente
            nombreCliente

            AFILIADO_A
            ABRE
        }

        type Ticket {
            idTicket
            tipoProblema
            descripcion

            SOLUCIONA
            LE_CORRESPONDE
            PERTENECE_EMPRESA
            PERTENECE_CLIENTE
        }

        idEmpresa: string @index(exact) @upsert .
        nombreEmpresa: string @index(term) .
        ubicacion: geo .

        idAgente: string @index(exact) @upsert .
        nombreAgente: string @index(term) .

        idCliente: string @index(exact) @upsert .
        nombreCliente: string @index(term) .

        idTicket: string @index(exact) @upsert .
        TipoProblema: int .
        descripcion: string @index(fulltext) .

        DA_SERVICIO: [uid] @reverse .
        TIENE: [uid] @reverse .
        TRABAJA: uid @reverse .
        SOLUCIONA: uid @reverse .
        LE_CORRESPONDE: uid @reverse .
        ABRE: uid @reverse .
        PERTENECE_EMPRESA: uid @reverse .
        PERTENECE_CLIENTE: uid @reverse .
        AFILIADO_A: uid @reverse .
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
        with open('data/empresas.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                empresa = {
                    'idEmpresa': row['idEmpresa'],
                    'nombreEmpresa': row['nombreEmpresa'],
                    'ubicacion': row['ubicacion']
                }
                empresa_uid = txn.mutate(set_obj=empresa, commit_now=True)
                empresa_uids[empresa['idEmpresa']] = empresa_uid.get('uid')
        txn.mutate(set_obj=empresas)
        empresa_uids = get_existing_uids(client, "idEmpresa", [e['idEmpresa'] for e in empresas])


    agente_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los agentes
        with open('data/agentes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                agente = {
                    'idAgente': row['idAgente'],
                    'nombreAgente': row['nombreAgente'],
                    'TRABAJA': empresa_uids.get(row['empresa'])
                }
                agente_uid = txn.mutate(set_obj=agente, commit_now=True)
                agente_uids[agente['idAgente']] = agente_uid.get('uid')
        txn.mutate(set_obj=agentes)
        agente_uids = get_existing_uids(client, "idAgente", [a['idAgente'] for a in agentes])

    cliente_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los clientes
        with open('data/clientes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cliente = {
                    'idCliente': row['idCliente'],
                    'nombreCliente': row['nombreCliente'],
                    'AFILIADO_A': empresa_uids.get(row['empresa'])
                }
                cliente_uid = txn.mutate(set_obj=cliente, commit_now=True)
                cliente_uids[cliente['idCliente']] = cliente_uid.get('uid')
        txn.mutate(set_obj=clientes)
        cliente_uids = get_existing_uids(client, "idCliente", [c['idCliente'] for c in clientes])

    ticket_uids = {}
    txn = client.txn()
    try:
        #Carga de datos de los tickets
        with open('data/tickets.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticket = {
                    'idTicket': row['idTicket'],
                    'tipoProblema': int(row['tipoProblema']),
                    'descripcion': row['descripcion'],
                    'SOLUCIONA': agente_uids.get(row['agente']),
                    'LE_CORRESPONDE': cliente_uids.get(row['cliente']),
                    'PERTENECE_EMPRESA': empresa_uids.get(row['empresa']),
                    'PERTENECE_CLIENTE': cliente_uids.get(row['cliente'])
                }
                ticket_uid = txn.mutate(set_obj=ticket, commit_now=True)
                ticket_uids[ticket['idTicket']] = ticket_uid.get('uid')
        txn.mutate(set_obj=tickets)
        ticket_uids = get_existing_uids(client, "idTicket", [t['idTicket'] for t in tickets])

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

# 4.4 Mostrar tickets por empresa