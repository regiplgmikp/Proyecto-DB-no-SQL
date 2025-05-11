
from models.Utils.validaciones import solicitar_input

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