import csv
from uuid import UUID
from datetime import datetime
import ast
from .model import (
    insertar_agente,
    insertar_empresa,
    insertar_cliente,
    insertar_ticket
) 

def populate_agentes(csv_path: str):
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        exitosos = 0
        errores = []

        for num_fila, row in enumerate(csv_reader, 2):
            try:
                data = {
                    'idAgente': UUID(row['idAgente']),
                    'nombre': row['nombre'],
                    'correo': row['correo'],
                    'telefono': row['telefono'],
                    'estadoEnEmpresa': int(row['estadoEnEmpresa']),
                    'idEmpresa': UUID(row['idEmpresa']),
                    'fechaIngreso': datetime.strptime(
                        row['fechaIngreso'], 
                        '%Y-%m-%dT%H:%M:%S'
                    )
                }
                
                insertar_agente(data)

                exitosos += 1
                
            except Exception as e:
                errores.append({
                    'fila': num_fila,
                    'error': str(e),
                    'datos': row
                })

        print(f"\nResultado de la importación de agentes:")
        print(f"• Registros exitosos: {exitosos}")
        print(f"• Errores: {len(errores)}")
        
        if errores:
            print("\nDetalle de errores:")
            for error in errores[:3]:
                print(f"Fila {error['fila']}\nError: {error['error']}")
                print(f"Datos: {error['datos']}\n")

def populate_empresas(csv_path: str):
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        exitosos = 0
        errores = []

        for num_fila, row in enumerate(csv_reader, 2):
            try:
                data = {
                    'idEmpresa': UUID(row['idEmpresa']),
                    'nombre': row['nombre'],
                    'correo': row['correo'],
                    'telefono': row['telefono'],
                    'direccion': row['direccion'],
                }
                
                insertar_empresa(data)

                exitosos += 1
                
            except Exception as e:
                errores.append({
                    'fila': num_fila,
                    'error': str(e),
                    'datos': row
                })

        print(f"\nResultado de la importación de Empresas:")
        print(f"• Registros exitosos: {exitosos}")
        print(f"• Errores: {len(errores)}")
        
        if errores:
            print("\nDetalle de errores:")
            for error in errores[:3]:
                print(f"Fila {error['fila']}\nError: {error['error']}")
                print(f"Datos: {error['datos']}\n")

def populate_clientes(csv_path: str):
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        exitosos = 0
        errores = []

        for num_fila, row in enumerate(csv_reader, 2):
            try:
                data = {
                    'idCliente': UUID(row['idCliente']),
                    'nombre': row['nombre'],
                    'correo': row['correo'],
                    'telefono': row['telefono'],
                    'estadoCuenta': row['estadoCuenta'],
                    'idEmpresa': UUID(row['idEmpresa'])
                }
                
                insertar_cliente(data)

                exitosos += 1
                
            except Exception as e:
                errores.append({
                    'fila': num_fila,
                    'error': str(e),
                    'datos': row
                })

        print(f"\nResultado de la importación de Clientes:")
        print(f"• Registros exitosos: {exitosos}")
        print(f"• Errores: {len(errores)}")
        
        if errores:
            print("\nDetalle de errores:")
            for error in errores[:3]:
                print(f"Fila {error['fila']}\nError: {error['error']}")
                print(f"Datos: {error['datos']}\n")

def populate_tickets(csv_path: str):
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        exitosos = 0
        errores = []

        for num_fila, row in enumerate(csv_reader, 2):
            try:
                data = {
                    'idTicket': UUID(row['idTicket']),
                    'idCliente': UUID(row['idCliente']),
                    'idAgente': UUID(row['idAgente']) if row['idAgente'] else None,
                    'idEmpresa': UUID(row['idEmpresa']),
                    'fechaCreacion': datetime.strptime(
                        row['fechaCreacion'],
                        '%Y-%m-%dT%H:%M:%S'
                    ),
                    'fechaCierre': datetime.strptime(
                        row['fechaCierre'],
                        '%Y-%m-%dT%H:%M:%S'
                    ) if row['fechaCierre'] else None,
                    'comentarios': ast.literal_eval(row['comentarios']) if row['comentarios'] else [],
                    'estado': int(row['estado']),
                    'prioridad': int(row['prioridad'])
                }
                
                insertar_ticket(data)

                exitosos += 1
                
            except Exception as e:
                errores.append({
                    'fila': num_fila,
                    'error': str(e),
                    'datos': row
                })

        print(f"\nResultado de la importación de tickets:")
        print(f"• Registros exitosos: {exitosos}")
        print(f"• Errores: {len(errores)}")
        
        if errores:
            print("\nDetalle de errores:")
            for error in errores[:3]:
                print(f"Fila {error['fila']}\nError: {error['error']}")
                print(f"Datos: {error['datos']}\n")

