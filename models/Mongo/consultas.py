
from models.Utils.validaciones import solicitar_input, Validaciones
from bson import Binary
from uuid import UUID
from models.Mongo.MongoModel import MongoModel
from datetime import datetime

#Obtener información de agente en base a su nombre", # Mongo
def obtenerEntidades(input_message, get_function, val_function):
    result = ""
    campoObtenido = solicitar_input(input_message, val_function, True)
    if campoObtenido:
        entidades = get_function(campoObtenido)
        if entidades:
            result += "Información encontrada: "
            for entidad in entidades:
                result += str(entidad) + "\n"
        else:
            result += f"Ninguna información encontrada relacionada a '{campoObtenido}'\n"
    else:
        result += "Volviendo a menú principal\n"

    return result

def clientesConTicketsPorFecha():
    # "Mostrar IDs de clientes de una empresa con tickets abiertos a partir de “x” fecha hasta la actualidad", # Mongo
    empresa = solicitar_input("Ingrese el id de la empresa de la que quiere obtener los clientes: ", Validaciones.validar_idEmpresaExistente)
    idEmpresa = empresa.idEmpresa
    fecha = solicitar_input("Ingrese la fecha desde la que desea buscar: ", Validaciones.validar_fecha)
    query = {
        "idEmpresa": Binary.from_uuid(idEmpresa),
        "fechaCreacion": {
            "$gte": fecha
        }
    }

    # Definir la proyección (solo mostrar `idCliente`)
    projection = {"idCliente": 1, "idTicket": 1}
    resultStr = ""
    result = MongoModel.buscar_documentos('tickets', query, projection)
    if result:
        resultStr += f"{str(len(result))} clientes con tickets encontrados:\n" 
        for dict in result:
            cliente = MongoModel.obtener_cliente_por_id(dict['idCliente'])
            resultStr += f"idTicket: {dict['idTicket']}:" + str(cliente) + "\n\n"

    else:
        resultStr = f"No se encontraron clientes de la empresa {idEmpresa} que hayan abierto tickets desde {fecha}"

    return resultStr