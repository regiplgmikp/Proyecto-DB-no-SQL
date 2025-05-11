# import models.conection as conection
import models.Mongo.populate as populate
from models.Mongo.MongoModel import MongoModel
from models.Utils.validaciones import Validaciones, solicitar_input
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
        1: "Mostrar clientes por empresa",
        2: "Mostrar cliente por ticket",
        3: "Obtener id de cliente en base a su nombre",
        4: "Obtener información de cliente en base a su ID",
        5: "Mostrar clientes con tickets abiertos desde x fecha hasta la actualidad",
        6: "Historial de estado de cuenta de cliente"
    }

    # Consultas de tickets
    mm_option5 = {
        0: "Regresar a menú principal",
        1: "Mostrar tickets por empresa",
        2: "Mostrar tickets por cliente",
        3: "Mostrar tickets de una empresa por tipo de problema ",
        4: "Mostrar tickets de agentes por empresa por tipo de problema ",
        5: "Mostrar una lista ordenada del tipo de problema más frecuente al menor en una empresa en un rango de fechas.",
        6: "Búsqueda de tickets por palabras clave (por empresa)",
        7: "Búsqueda de tickets por palabra clave por agente y empresa",
        8: "Mostrar tickets cerrados por agente",
        9: "Mostrar tickets pendientes por agente",
        10:	"Mostrar tickets cerrados por empresa",
        11:	"Mostrar tickets pendientes por empresa",
        12:	"Mostrar tickets abiertos por empresa",
        13:	"Mostrar tickets cerrados por cliente",
        14:	"Mostrar tickets pendientes por cliente",
        15:	"Mostrar tickets abiertos por cliente",
        16:	"Obtener información de ticket en base a su ID",
        17:	"Mostrar tickets con una antigüedad mayor a “x” fecha",
        18:	"Mostrar tickets cerrados en un periodo de tiempo por agente",
        19:	"Obtener la cantidad de tickets que ha cerrado cada agente de una empresa en un periodo de tiempo",
        20:	"Obtener la cantidad de tickets que ha cerrado un agente de una empresa en un periodo de tiempo",
        21:	"Filtrar tickets de empresa por prioridad",
        22:	"Mostrar historial de comentarios de ticket en base al id del ticket",
        23:	"Historial de cambios en la prioridad de un ticket",
        24:	"Historial de asignación de agentes a un ticket",
        25:	"Historial de estados del ticket",
        26:	"Historial de tickets creados en empresa"
    }

    # Consultas de empresas
    mm_option6 = {
        0: "Regresar a menú principal",
        1: "Mostrar ubicación de la empresa por medio de su id",
        2: "Obtener id de empresa en base a su nombre",
        3: "Obtener informacion de empresa en base a su id"
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

        # Registro de datos
        elif option == 1:
            printMenu(1)
            try:
                option = int(input("Seleccione una opción: "))
                # Registro de Agente
                if option == 0:
                    continue
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
            
            # Regresa al menu principal
            if option == 0:
                continue
        
        # Actualizaciones
        elif option == 2:
            printMenu(2)
            try:
                option = int(input("Seleccione una opción: "))
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

            # Regresa al menu principal    
            if option == 0:
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
                    # "Obtener id de agente en base a su nombre", # Mongo
                    nombreAgente = solicitar_input("Ingrese el nombre del agente del que desea obtener información (vacío para volver): ", Validaciones.validar_nombre, True)
                    if nombreAgente:
                        agentes = MongoModel.obtener_agente_por_nombre(nombreAgente)
                        if agentes:
                            print("Agente(s) encontrado(s) con ese nombre: ")
                            for agente in agentes:
                                print(agente)
                        else:
                            print(f"Agente con nombre {nombreAgente} no encontrado")
                    else:
                        print("Volviendo a menú principal\n")
                elif option == 2: 
                    # "Obtener información de agente en base a su ID", # Mongo
                    idAgente = input("Ingrese el ID del agente del que desea obtener información: ")
                    agente = MongoModel.obtener_agente_por_id(idAgente)
                    print(f"Agente encontrado: \n{agente}" if agente else f"Agente con ID {idAgente} no encontrado")

                elif option == 3: 
                    # "Mostrar agentes por empresa", # Dgraph
                    pass
                elif option == 4: 
                    # "Mostrar agente por ticket", # Draph
                    pass
                elif option == 5: 
                    # "Historial de estado en empresa de agente" # Casssandra
                    pass
            except Exception as e:
                print(f"Error: {e}")
                continue
            # Regresa al menu principal
            if option == 0:
                continue
            
            
        # Consultas de clientes
        elif option == 4:
            printMenu(4)
            try:
                option = int(input("Seleccione una opción: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
            
            # Regresa al menu principal
            if option == 0:
                continue
                
        # Consultas de tickets
        elif option == 5:
            printMenu(5)
            try:
                option = int(input("Seleccione una opción: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue

            # Regresa al menu principal
            if option == 0:
                continue
                
        # Consultas de empresas
        elif option == 6:
            printMenu(6)
            try:
                option = int(input("Seleccione una opción: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
            
            # Regresa al menu principal
            if option == 0:
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
