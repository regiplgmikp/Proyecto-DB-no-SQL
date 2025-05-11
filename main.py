# import models.conection as conection
import models.Mongo.populate as populate
from models.Mongo.MongoModel import MongoModel
from models.Mongo.consultas import obtenerEntidades
from models.Utils.validaciones import Validaciones
from models.Utils.crear_entidades import (
    crear_agente,
    crear_empresa,
    crear_cliente,
    crear_ticket
)
from models.Utils.actualizar_entidades import (
    actualizar_agente,
    actualizar_cliente,
    actualizar_ticket
)

#Importaciones Dgraph
import os
import pydgraph
import models.Dgraph.model as dgraph

#Cliente Dgraph
def get_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')  # Ajusta la URL según tu configuración
    return pydgraph.DgraphClient(client_stub)


def printMenu(option=0):
    # Menú principal
    mm_options = {
        0: "Poblar de datos",
        1: "Registros",
        2: "Actualizaciones",
        3: "Consultas de agentes",
        4: "Consultas de clientes",
        5: "Consultas de tickets",
        6: "Consultas de empresas",
        7: "Eliminar bases de datos",
        8: "Salir"
    }

    # Registros
    mm_option1 = {
        0: "Regresar a menú principal",
        1: "Registro de Agente",
        2: "Registro de Cliente",
        3: "Registro de Ticket",
        4: "Registro de Empresa"
    }
    
    # Actualizaciones
    mm_option2 = {
        0: "Regresar a menú principal",
        1: "Actualizar Agente",
        2: "Actualizar Cliente",
        3: "Actualizar Ticket"
    }

    # Consultas de agentes
    mm_option3 = {
        0: "Regresar a menú principal",
        1: "Obtener información de agente en base a su nombre", # Mongo
        2: "Obtener información de agente en base a su ID", # Mongo
        3: "Mostrar agentes por empresa", # Dgraph
        4: "Mostrar agente por ticket", # Draph
        5: "Historial de estado en empresa de agente" # Casssandra
    }

    # Consultas de clientes
    mm_option4 = {
        0: "Regresar a menú principal",
        1: "Obtener información de cliente en base a su nombre", # Mongo
        2: "Obtener información de cliente en base a su ID", #Mongo
        3: "Mostrar IDs de clientes de una empresa con tickets abiertos a partir de “x” fecha hasta la actualidad", # Mongo
        4: "Mostrar clientes por empresa", # Dgraph
        5: "Mostrar cliente por ticket", # Dgraph
        6: "Historial de estado de cuenta de cliente" # Cassandra
    }

    # Consultas de tickets
    mm_option5 = {
        0:  "Regresar a menú principal", 
        1:  "Obtener información de ticket en base a su ID", # Mongo
        2:  "Mostrar Tickets con estado “Cerrado” por Agente", # Mongo
        3:  "Mostrar Tickets con estado “Pendiente” por Agente", # Mongo
        4:  "Mostrar Tickets con estado “Cerrado” por Empresa", # Mongo
        5:  "Mostrar Tickets con estado “Pendiente” por Empresa", # Mongo
        6:  "Mostrar Tickets con estado “Abierto” por Empresa", # Mongo
        7:  "Mostrar Tickets con estado “Cerrado” por Cliente.", # Mongo            
        8:  "Mostrar Tickets con estado “Pendiente” por Cliente.", # Mongo
        9: "Mostrar Tickets con estado “Abierto” por Cliente.", # Mongo
        10:	"Mostrar tickets con una antigüedad mayor a “x” fecha", # Mongo
        11:	"Mostrar tickets cerrados en un periodo de tiempo por agente", # Mongo
        12:	"Obtener la cantidad de tickets que ha cerrado cada agente de una empresa en un periodo de tiempo", # Mongo
        13:	"Obtener la cantidad de tickets que ha cerrado un agente de una empresa en un periodo de tiempo", # Mongo
        14:	"Filtrar tickets de empresa por prioridad", # Mongo
        15: "Mostrar tickets por empresa", # Dgraph
        16: "Mostrar tickets por cliente", # Dgraph
        17: "Mostrar tickets de una empresa por tipo de problema ", # Dgraph
        18: "Mostrar tickets de un agente de una empresa por tipo de problema ", # Dgraph
        19: "Búsqueda de Ticket por empresa por medio de palabras clave", # Dgraph
        20: "Búsqueda de Ticket por Agente y Empresa por medio de palabras clave", # Dgraph
        21:	"Historial de comentarios de ticket en base al id del ticket", # Cassandra
        22:	"Historial de cambios en la prioridad de un ticket", # Cassandra
        23:	"Historial de asignación de agentes a un ticket", # Cassandra
        24:	"Historial de estados del ticket", # Cassandra
        25:	"Historial de tickets creados en empresa" # Cassandra
    }

    # Consultas de empresas
    mm_option6 = {
        0: "Regresar a menú principal",
        1: "Obtener información de empresa en base a su nombre", # Mongo
        2: "Obtener información de empresa en base a su id", # Mongo
        3: "Mostrar ubicación de la empresa por medio de su id" # Dgraph
    }

    if option == 0:
        for key in mm_options.keys():
            print(key, '--', mm_options[key])
    if option == 1:
        for key in mm_option1.keys():
            print(key, '--', mm_option1[key])
    elif option == 2:
        for key in mm_option2.keys():
            print(key, '--', mm_option2[key])
    elif option == 3:
        for key in mm_option3.keys():
            print(key, '--', mm_option3[key])
    elif option == 4:
        for key in mm_option4.keys():
            print(key, '--', mm_option4[key])
    elif option == 5:
        for key in mm_option5.keys():
            print(key, '--', mm_option5[key])
    elif option == 6:
        for key in mm_option6.keys():
            print(key, '--', mm_option6[key])
    
def main():
    client = get_dgraph_client()
    # Mientras el usuario no quiera salir, se imprime el menu
    while (True):
        printMenu(0)
        try:
            option = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
        
        # Poblar de datos
        if option == 0:
            # Hacer el poblado de datos en la base de datos
            # Se puede cambiar el path a la carpeta donde se encuentran los csv
            try:
                print(populate.populate_all("data/mongo/")['resumen'])
            except FileNotFoundError as e:
                print(e)

            # Dgraph (esquema y poblado de datos)
            dgraph.set_schema(client)
            dgraph.create_data(client)

        # Registro de datos
        elif option == 1:
            printMenu(1)
            try:
                option = int(input("Seleccione una opción: "))
                # Regresa al menu principal
                if option == 0:
                    continue
                # Registro de Agente
                elif option == 1:
                    crear_agente()
                # Registro de Cliente
                elif option == 1:
                    crear_cliente()
                # Registro de Ticket
                elif option == 1:
                    crear_ticket()
                # Registro de Empresa
                elif option == 1:
                    crear_empresa()
                    
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
                    
        # Actualizaciones
        elif option == 2:
            printMenu(2)
            try:
                option = int(input("Seleccione una opción: "))
                # Regresa al menu principal    
                if option == 0:
                    continue
                # Actualización de agente
                elif option == 1:
                    print(actualizar_agente())
                # Actualización de cliente
                elif option == 2:
                    print(actualizar_cliente())
                # Actualización de Ticket
                elif option == 3:
                    print(actualizar_ticket())

            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue                
                
        # Consultas de agentes
        elif option == 3:
            printMenu(3)
            try:
                option = int(input("Seleccione una opción: "))
                if option == 0: 
                    # "Regresar a menú principal",
                    continue
                elif option == 1: 
                    # "Obtener información de agente en base a su nombre", # Mongo
                    print(obtenerEntidades("Ingrese el nombre del agente del que desea obtener información (Enter para volver): ", MongoModel.obtener_agente_por_nombre, Validaciones.validar_nombre))
                
                elif option == 2: 
                    # "Obtener información de agente en base a su ID", # Mongo
                    id = input("Ingrese el ID del agente del que desea obtener información: ")
                    entidad = MongoModel.obtener_agente_por_id(id)
                    print(f"Agente encontrado: \n{entidad}\n" if entidad else f"Agente con ID {id} no encontrado")

                elif option == 3: 
                    # "Mostrar agentes por empresa", # Dgraph
                    id_empresa = input("Ingrese ID de la empresa: ")
                    result = dgraph.Agentes_por_empresa(client, id_empresa)

                elif option == 4: 
                     # "Mostrar agente por ticket", # Draph
                    id_ticket = input("Ingrese ID del ticket: ")
                    result = dgraph.Agentes_por_ticket(client, id_ticket)

                elif option == 5: 
                    # "Historial de estado en empresa de agente" # Casssandra
                    pass
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue          
            
        # Consultas de clientes
        elif option == 4:
            printMenu(4)
            try:
                option = int(input("Seleccione una opción: "))
                # Regresa al menu principal
                if option == 0:
                    continue
                # "Obtener información de cliente en base a su nombre", # Mongo
                elif option == 1: 
                    print(obtenerEntidades("Ingrese el nombre del cliente del que desea obtener información (Enter para volver): ", MongoModel.obtener_cliente_por_nombre, Validaciones.validar_nombre))

                # "Obtener información de cliente en base a su ID", #Mongo
                elif option == 2: 
                    id = input("Ingrese el ID del cliente del que desea obtener información: ")
                    entidad = MongoModel.obtener_cliente_por_id(id)
                    print(f"Cliente encontrado: \n{entidad}\n" if entidad else f"Cliente con ID {id} no encontrado")

                # "Mostrar IDs de clientes de una empresa con tickets abiertos a partir de “x” fecha hasta la actualidad", # Mongo
                elif option == 3: 
                    pass
                # "Mostrar clientes por empresa", # Dgraph
                elif option == 4: 
                    pass
                # "Mostrar cliente por ticket", # Dgraph
                elif option == 5: 
                    pass
                # "Historial de estado de cuenta de cliente" # Cassandra
                elif option == 6: 
                    pass

            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
                
        # Consultas de tickets
        elif option == 5:
            printMenu(5)
            try:
                option = int(input("Seleccione una opción: "))
                # Regresa al menu principal
                if option == 0:
                    continue
                # "Obtener información de ticket en base a su ID", # Mongo
                elif option == 1:
                    id = input("Ingrese el ID del ticket del que desea obtener información: ")
                    entidad = MongoModel.obtener_ticket_por_id(id)
                    print(f"Ticket encontrado: \n{entidad}\n" if entidad else f"Ticket con ID {id} no encontrado")

                # "Mostrar Tickets con estado “Cerrado” por Agente", # Mongo
                elif option == 2:
                    pass
                # "Mostrar Tickets con estado “Pendiente” por Agente", # Mongo
                elif option == 3:
                    pass
                # "Mostrar Tickets con estado “Cerrado” por Empresa", # Mongo
                elif option == 4:
                    pass
                # "Mostrar Tickets con estado “Pendiente” por Empresa", # Mongo
                elif option == 5:
                    pass
                # "Mostrar Tickets con estado “Abierto” por Empresa", # Mongo
                elif option == 6:
                    pass
                # "Mostrar Tickets con estado “Cerrado” por Cliente.", # Mongo            
                elif option == 7:
                    pass
                # "Mostrar Tickets con estado “Pendiente” por Cliente.", # Mongo
                elif option == 8:
                    pass
                # "Mostrar Tickets con estado “Abierto” por Cliente.", # Mongo
                elif option == 9:
                    pass
                # "Mostrar tickets con una antigüedad mayor a “x” fecha", # Mongo
                elif option == 10:
                    pass
                # "Mostrar tickets cerrados en un periodo de tiempo por agente", # Mongo
                elif option == 11:
                    pass
                # "Obtener la cantidad de tickets que ha cerrado cada agente de una empresa en un periodo de tiempo", # Mongo
                elif option == 12:
                    pass
                # "Obtener la cantidad de tickets que ha cerrado un agente de una empresa en un periodo de tiempo", # Mongo
                elif option == 13:
                    pass
                # "Filtrar tickets de empresa por prioridad", # Mongo
                elif option == 14:
                    pass
                # "Mostrar tickets por empresa", # Dgraph
                elif option == 15:
                    pass
                # "Mostrar tickets por cliente", # Dgraph
                elif option == 16:
                    pass
                # "Mostrar tickets de una empresa por tipo de problema ", # Dgraph
                elif option == 17:
                    pass
                # "Mostrar tickets de un agente de una empresa por tipo de problema ", # Dgraph
                elif option == 18:
                    pass
                # "Búsqueda de Ticket por empresa por medio de palabras clave", # Dgraph
                elif option == 19:
                    pass
                # "Búsqueda de Ticket por Agente y Empresa por medio de palabras clave", # Dgraph
                elif option == 20:
                    pass
                # "Historial de comentarios de ticket en base al id del ticket", # Cassandra
                elif option == 21:
                    pass
                # "Historial de cambios en la prioridad de un ticket", # Cassandra
                elif option == 22:
                    pass
                # "Historial de asignación de agentes a un ticket", # Cassandra
                elif option == 23:
                    pass
                # "Historial de estados del ticket", # Cassandra
                elif option == 24:
                    pass
                # "Historial de tickets creados en empresa" # Cassandra
                elif option == 25:
                    pass
            
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
                
        # Consultas de empresas
        elif option == 6:
            printMenu(6)
            try:
                option = int(input("Seleccione una opción: "))
                # Regresa al menu principal
                if option == 0:
                    continue
                # "Obtener información de empresa en base a su nombre", # Mongo
                elif option == 1:
                    pass
                # "Obtener información de empresa en base a su id", # Mongo
                elif option == 2:
                    pass
                # "Mostrar ubicación de la empresa por medio de su id" # Dgraph
                elif option == 3:
                    pass

            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue            
                
        # Eliminar bases de datos
        elif option == 7:
            print("Datos eliminados correctamente.")
            
        # Salir
        elif option == 8:
            print("Saliendo...")
            break

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error:', e)
