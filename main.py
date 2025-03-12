import models.conection as conection

def printMenu():
    print("\nSistema de Soporte al Cliente")
    print("1. Poblar bases de datos")
    print("2. Consultar clientes")
    print("3. Actualizar estado de cuenta")
    print("4. Actualizar estado de ticket")
    print("5. Encuesta de satisfacción")
    print("6. Salir")
    option = int(input("Seleccione una opción: "))
    return option


if __name__ == "__main__":
    option = 7
    while option != 6:
        option = printMenu()
        