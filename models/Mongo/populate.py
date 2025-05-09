import csv
from uuid import UUID
from datetime import datetime
from .model import insertar_agente

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

