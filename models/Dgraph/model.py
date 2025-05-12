# 1- Importaciones

#!/usr/bin/env python3
import datetime
import json
import pydgraph
import csv
import sys
import io
from .Formatos import print_formatted
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
    print("👌 Empresas cargadas con éxito en Dgraph.")

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
    print("👌 Agentes cargados con éxito en Dgraph.")

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
    print("👌 Clientes cargados con éxito en Dgraph.")

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
                    'descripcion': row['descripcion']
                }
                tickets.append(ticket)

        response = txn.mutate(set_obj=tickets, commit_now=True)
        for row in tickets:
            ticket_uids[row['idTicket']] = response.uids.get(row['uid'][2:], '')
    finally:
        txn.discard()
    print("👌 Tickets cargados con éxito en Dgraph.")

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
#========================================== QUERYS ===========================================#

def print_json(res):
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))

# 1. Agentes por empresa

def Agentes_por_empresa(client, id_empresa):
    query = """
    query AgentesPorEmpresa($idEmpresa: string) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        idEmpresa
        nombreEmpresa
        TIENE {
          idAgente
          nombreAgente
        }
      }
    }
    """
    variables = {"$idEmpresa": id_empresa}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "agentes_empresa")

# 2. Clientes por empresa

def Clientes_por_empresa(client, id_empresa):
    query = """
    query clientesPorEmpresa($idEmpresa: string) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        idEmpresa
        nombreEmpresa
        clientes: ~AFILIADO_A {
          idCliente
          nombreCliente
        }
      }
    }
    """
    variables = {'$idEmpresa': id_empresa}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "clientes_empresa")

# 3. Cliente por ticket

def Cliente_por_ticket(client, idTicket):
    query = """
    query clientePorTicket($idTicket: string) {
      ticket(func: eq(idTicket, $idTicket)) {
        idTicket
        tipoProblema
        descripcion
        ~ABRE {  
          idCliente
          nombreCliente
        }
      }
    }
    """
    variables = {'$idTicket': idTicket}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "clientes_ticket")

# 4. Tickets por empresa
def Tickets_por_empresa(client, id_empresa):
    query = """
    query ticketsPorEmpresa($idEmpresa: string) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        nombreEmpresa
        ~PERTENECE {
          idTicket
          tipoProblema
          descripcion
        }
      }
    }
    """
    variables = {'$idEmpresa': id_empresa}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "tickets_empresa")

# 5. Tickets por cliente
def Tickets_por_cliente(client, nombre_cliente):
    query = """
    query ticketsPorCliente($nombreCliente: string) {
      cliente(func: eq(nombreCliente, $nombreCliente)) {
        idCliente
        nombreCliente
        ABRE {
          idTicket
          tipoProblema
          descripcion
        }
      }
    }
    """
    variables = {'$nombreCliente': nombre_cliente}
    res = client.txn(read_only=True).query(query, variables=variables)
    #print_json(res)
    print_formatted(res, "tickets_cliente")

# 6. Agentes por ticket
def Agentes_por_ticket(client, id_ticket):
    query = """
    query agentesPorTicket($idTicket: string) {
      ticket(func: eq(idTicket, $idTicket)) {
        idTicket
         ~SOLUCIONA {
          idAgente
          nombreAgente
        }
      }
    }
    """
    variables = {'$idTicket': id_ticket}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "agente_ticket")

# 7. Tickets de empresa por tipo de problema.
def Tickets_por_empresa_tipo(client, id_empresa,tipo_problema):
    query = """
    query ticketsPorAgenteEmpresaTipo($idEmpresa: string, $tipoProblema: int) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        nombreEmpresa
        ~PERTENECE @filter(eq(tipoProblema, $tipoProblema)) {
          idTicket
          tipoProblema
          descripcion
        }
      }
    }
    """
    variables = {'$idEmpresa':id_empresa,'$tipoProblema': tipo_problema}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "tickets_empresa_tipo")

# 8. Tickets por agente por tipo de problema.

def Tickets_por_agente_tipo(client, id_agente,tipo_problema):
    query = """
    query ticketsPorAgenteTipo($idAgente: string, $tipoProblema: int) {
      agente(func: eq(idAgente, $idAgente)) {
        nombreAgente
        SOLUCIONA @filter(eq(tipoProblema, $tipoProblema)) {
          idTicket
          tipoProblema
          descripcion
        }
      }
    }
    """
    variables = {'$idAgente': id_agente,'$tipoProblema': tipo_problema}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "tickets_agente_tipo")


# 9. Ticket por empresa por medio de palabras clave.
def Ticket_por_empresa_palabras(client, empresa_id, palabras_clave):
    query = """
    query ticketsPorEmpresaPalabras($empresa_id: string, $palabras_clave: string) {
      empresa(func: eq(idEmpresa, $empresa_id)) {
        nombreEmpresa
        ~PERTENECE @filter(anyofterms(descripcion, $palabras_clave)) {
          idTicket
          descripcion
          tipoProblema
        }
      }
    }
    """
    variables = {'$empresa_id': empresa_id, '$palabras_clave': palabras_clave}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "tickets_empresa_palabras")

# 10. Búsqueda de Ticket por Agente y Empresa por medio de palabras clave.
def Ticket_por_agente_empresa_palabras(client, empresa_id, agente_id, palabras_clave):
    query = """
    query buscarTicketsAgenteEmpresa($idEmpresa: string, $idAgente: string, $palabras_clave: string) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        nombreEmpresa
        TIENE @filter(eq(idAgente, $idAgente)) {
          nombreAgente
          SOLUCIONA @filter(anyofterms(descripcion, $palabras_clave)) {
            idTicket
            descripcion
            tipoProblema
          }
        }
      }
    }
    """
    variables = {'$idEmpresa': empresa_id,'$idAgente': agente_id,'$palabras_clave': palabras_clave}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "tickets_agente_empresa_palabras")

# 11. Dirección de la empresa por medio de su ID.

def Direccion_empresa_por_id(client, idEmpresa):
    query = """
    query ubicacionEmpresa($idEmpresa: string) {
      empresa(func: eq(idEmpresa, $idEmpresa)) {
        nombreEmpresa
        ubicacion {
          type
          coordinates
        }
      }
    }
    """
    variables = {'$idEmpresa': idEmpresa}
    res = client.txn(read_only=True).query(query, variables=variables)
    print_formatted(res, "direccion_empresa")

# 12. BORRAR DATOS
def drop_all(client):
    try:
        op = pydgraph.Operation(drop_all=True)
        client.alter(op)
        print("Se ha eliminado todo el esquema y los datos de Dgraph.")
    except Exception as e:
        print(f"Error al eliminar todo: {e}")

# ==================================== INSERTACIONES ===========================================

# 13. Insertar agente

def insertar_agente(client, dgraph_agente):
   mutation = {
        'uid': f"_:{dgraph_agente['idAgente']}",
        'idAgente': dgraph_agente['idAgente'],
        'nombreAgente': dgraph_agente['nombre'],
        'dgraph.type': 'Agente',
        'TRABAJA': {
            'uid': f"_:{dgraph_agente['idEmpresa']}",
            'idEmpresa': dgraph_agente['idEmpresa'],
            'dgraph.type': 'Empresa'
        }
    }
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=mutation, commit_now=True)
        print(f"✅ Empresa {dgraph_empresa['idEmpresa']} insertada")
        return response
    finally:
        txn.discard()

# 14. insertar empresa 
def insertar_empresa(client, dgraph_empresa):
   mutation = {
        'uid': f"_:{dgraph_empresa['idEmpresa']}",
        'idEmpresa': dgraph_empresa['idEmpresa'],
        'nombreEmpresa': dgraph_empresa['nombreEmpresa'],
        'ubicacion': dgraph_empresa['ubicacion'],
        'dgraph.type': 'Empresa'
    }
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=mutation, commit_now=True)
        print(f"✅ Empresa {dgraph_empresa['idEmpresa']} insertada")
        return response
    finally:
        txn.discard()

# 15. Insertar cliente

def insertar_cliente(client, dgraph_cliente):
  mutation = {
        'uid': f"_:{dgraph_cliente['idCliente']}",
        'idCliente': dgraph_cliente['idCliente'],
        'nombreCliente': dgraph_cliente['nombreCliente'],
        'dgraph.type': 'Cliente',
        'AFILIADO_A': {
            'uid': f"_:{dgraph_cliente['idEmpresa']}",
            'idEmpresa': dgraph_cliente['idEmpresa'],
            'dgraph.type': 'Empresa'
        }
    }
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=mutation, commit_now=True)
        print(f"✅ Cliente {dgraph_cliente['idCliente']} insertado")
        return response
    finally:
        txn.discard()

# 16. Insertar ticket

def insertar_ticket(client, dgraph_ticket):
  mutation = {
        'uid': f"_:{dgraph_ticket['idTicket']}",
        'idTicket': dgraph_ticket['idTicket'],
        'tipoProblema': dgraph_ticket['tipoProblema'],
        'descripcion': dgraph_ticket['descripcion'],
        'dgraph.type': 'Ticket',
        'ABRE': {
            'uid': f"_:{dgraph_ticket['idCliente']}",
            'idCliente': dgraph_ticket['idCliente'],
            'dgraph.type': 'Cliente'
        },
        'PERTENECE': {
            'uid': f"_:{dgraph_ticket['idEmpresa']}",
            'idEmpresa': dgraph_ticket['idEmpresa'],
            'dgraph.type': 'Empresa'
        }
    }
    if dgraph_ticket.get('idAgente'):
        mutation['SOLUCIONA'] = {
            'uid': f"_:{dgraph_ticket['idAgente']}",
            'idAgente': dgraph_ticket['idAgente'],
            'dgraph.type': 'Agente'
        }
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=mutation, commit_now=True)
        print(f"✅ Ticket {dgraph_ticket['idTicket']} insertado")
        return response
    finally:
        txn.discard()
