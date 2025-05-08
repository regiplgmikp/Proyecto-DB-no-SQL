import csv
from uuid import UUID
from datetime import datetime
from .Agente import Agente, AgenteValidationError
from models.conection import connect_mongodb



def populate_agentes(csv_path: str):
    db = connect_mongodb()
    collection = db['agentes']
    
    # Crear índice único para UUID
    collection.create_index('idAgente', unique=True)

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
                    'estadoEmpresa': row['estadoEmpresa'],
                    'idEmpresa': UUID(row['idEmpresa']),
                    'fechaIngreso': datetime.strptime(
                        row['fechaIngreso'],
                        '%Y-%m-%dT%H:%M:%S'
                    )
                }
                
                agente = Agente.crear_desde_dict(data)
                collection.insert_one(agente.model_dump(by_alias=True))
                exitosos += 1
                
            except Exception as e:
                errores.append({
                    'fila': num_fila,
                    'error': str(e),
                    'datos': row
                })

        # (Mantener el mismo reporte de resultados)
        # Reporte final
        print(f"\nResultado de la importación:")
        print(f"• Registros exitosos: {exitosos}")
        print(f"• Errores: {len(errores)}")
        
        if errores:
            print("\nDetalle de errores:")
            for error in errores[:3]:  # Mostrar primeros 3 errores
                print(f"Fila {error['fila']}: {error['error']}")
                print(f"Datos: {error['datos']}\n")

if __name__ == "__main__":
    path = 'data/mongo/agentes.csv'

    populate_agentes(path)