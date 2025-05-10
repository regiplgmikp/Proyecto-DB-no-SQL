# Formatos.py
import json
from typing import Dict, Any

class Formatos:
    @staticmethod
    def _encabezado(titulo: str, ancho: int = 90) -> str:
        """Genera un encabezado consistente"""
        iguales = (ancho - len(titulo) - 2)
        return f"\n{'='*(iguales//2)} {titulo} {'='*(iguales//2)}\n"

    @staticmethod
    def _divisor(ancho: int = 90) -> str:
        """Genera un divisor visual"""
        return '-' * ancho

# 1. Agentes por empresa
    @staticmethod
    def agentes_empresa(data: Dict[str, Any]) -> str:
        """Formatea agentes por empresa"""
        empresa = data['empresa'][0]
        output = []
        
        output.append(Formatos._encabezado("REPORTE DE AGENTES"))
        output.append(f"📌 Empresa: {empresa.get('nombreEmpresa', 'N/A')} (ID: {empresa.get('idEmpresa', 'N/A')})")
        output.append(Formatos._divisor())
        output.append("🔹 Agentes:")
        
        for agente in empresa.get('TIENE', []):
            output.append(f"   - {agente.get('nombreAgente', 'N/A')} (ID: {agente.get('idAgente', 'N/A')})")
        
        output.append(Formatos._divisor())
        output.append(f"🔹 Total: {len(empresa.get('TIENE', []))} agentes")
        output.append("=" * 90)
        
        return '\n'.join(output)

# 2. Clientes por empresa
    @staticmethod
    def clientes_empresa(data: Dict[str, Any]) -> str:
        """Formatea clientes por empresa"""
        empresa = data['empresa'][0]
        output = []
        
        output.append(Formatos._encabezado("REPORTE DE CLIENTES"))
        output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
        output.append(Formatos._divisor())
        output.append("🔹 Clientes:")
        
        for cliente in empresa.get('clientes', []):
            output.append(f"   - {cliente.get('nombreCliente', 'N/A')} (ID: {cliente.get('idCliente', 'N/A')})")
        
        output.append(Formatos._divisor())
        output.append(f"🔹 Total: {len(empresa.get('clientes', []))} clientes")
        output.append("=" * 90)
        
        return '\n'.join(output)

# 3. Cliente por ticket
    @staticmethod
    def clientes_ticket(data: Dict[str, Any]) -> str:
        """Cliente_por_ticket"""
        output = []
        if 'ticket' in data and len(data['ticket']) > 0:
            ticket = data['ticket'][0]
            cliente = ticket.get('~ABRE', [{}])[0] if ticket.get('~ABRE') else {}
            
            output.append(Formatos._encabezado("INFORMACIÓN DE TICKET"))
            output.append(f"🎫 Ticket ID: {ticket.get('idTicket', 'N/A')}")
            output.append(f"🔧 Tipo Problema: {ticket.get('tipoProblema', 'N/A')}")
            output.append(f"📝 Descripción: {ticket.get('descripcion', 'N/A')}")
            output.append(Formatos._divisor())
            
            output.append("👤 Cliente Asociado:")
            if cliente:
                output.append(f"   - Nombre: {cliente.get('nombreCliente', 'N/A')}")
                output.append(f"   - ID: {cliente.get('idCliente', 'N/A')}")
            else:
                output.append("   - No se encontró cliente asociado")
            
            output.append("=" * 90)
        else:
            output.append("ℹ️ No se encontró el ticket solicitado")
        
        return '\n'.join(output)

# 4. Tickets por empresa
    @staticmethod
    def tickets_empresa(data: Dict[str, Any]) -> str:
        """Formatea tickets por empresa"""
        empresa = data['empresa'][0]
        output = []
        
        output.append(Formatos._encabezado("TICKETS REPORTE"))
        output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
        output.append(Formatos._divisor())
        
        for ticket in empresa.get('~PERTENECE', []):
            output.append(f"🎫 Ticket ID: {ticket.get('idTicket', 'N/A')}")
            output.append(f"📝 Descripción: {ticket.get('descripcion', 'N/A')}")
            output.append(f"🔧 Tipo Problema: {ticket.get('tipoProblema', 'N/A')}")
            output.append(Formatos._divisor())
        
        output.append(f"🔍 Total tickets: {len(empresa.get('~PERTENECE', []))}")
        output.append("=" * 90)
        
        return '\n'.join(output)

# 5. Tickets por cliente
    @staticmethod
    def tickets_cliente(data: Dict[str, Any]) -> str:
        """Tickets por cliente"""
        cliente = data['cliente'][0]
        output = []
        
        output.append(Formatos._encabezado("TICKETS POR CLIENTE"))
        output.append(f"👤 Cliente: {cliente.get('nombreCliente', 'N/A')}")
        output.append(Formatos._divisor())
        
        for ticket in cliente.get('ABRE', []):
            output.append(f"🎫 Ticket ID: {ticket.get('idTicket', 'N/A')}")
            output.append(f"📝 Descripción: {ticket.get('descripcion', 'N/A')}")
            output.append(f"🔧 Tipo Problema: {ticket.get('tipoProblema', 'N/A')}")
            output.append(Formatos._divisor())
        
        output.append(f"🔍 Total tickets: {len(cliente.get('ABRE', []))}")
        output.append("=" * 90)
        
        return '\n'.join(output)

# 6. Agentes por ticket
    @staticmethod
    def agente_ticket(data: Dict[str, Any]) -> str:
        """Formatea la información de agentes asociados a un ticket"""
        output = []
        
        if 'ticket' in data and len(data['ticket']) > 0:
            ticket = data['ticket'][0]
            agentes = ticket.get('~SOLUCIONA', [])
            
            output.append(Formatos._encabezado("AGENTES ASIGNADOS AL TICKET"))
            output.append(f"🎫 Ticket ID: {ticket.get('idTicket', 'N/A')}")
            output.append(Formatos._divisor())
            
            if agentes:
                output.append("🔧 Agentes asignados:")
                for agente in agentes:
                    output.append(f"   - {agente.get('nombreAgente', 'N/A')} (ID: {agente.get('idAgente', 'N/A')})")
            else:
                output.append("⚠️ No hay agentes asignados a este ticket")
            
            output.append("=" * 90)
        else:
            output.append("❌ No se encontró el ticket solicitado")
        
        return '\n'.join(output)

# 7. Tickets de agente de una empresa por tipo de problema.
    @staticmethod
    def tickets_agente_empresa_tipo(data: Dict[str, Any]) -> str:
        """Formatea tickets filtrados por empresa y tipo de problema"""
        output = []
        
        if 'empresa' in data and len(data['empresa']) > 0:
            empresa = data['empresa'][0]
            tickets = empresa.get('~PERTENECE', [])
            
            output.append(Formatos._encabezado("TICKETS POR TIPO DE PROBLEMA"))
            output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
            output.append(f"🔧 Tipo de Problema: {tickets[0].get('tipoProblema', 'N/A') if tickets else 'N/A'}")
            output.append(Formatos._divisor())
            
            if tickets:
                output.append("🎫 Tickets encontrados:")
                for ticket in tickets:
                    output.append(f"\n  • ID: {ticket.get('idTicket', 'N/A')}")
                    output.append(f"  📝 Descripción: {ticket.get('descripcion', 'N/A')}")
                    output.append(f"  🔧 Tipo: {ticket.get('tipoProblema', 'N/A')}")
                    output.append(Formatos._divisor(60))  # Divisor más corto para items
                output.append(f"\n🔍 Total tickets: {len(tickets)}")
            else:
                output.append("ℹ️ No se encontraron tickets para este tipo de problema")
            
            output.append("=" * 90)
        else:
            output.append("❌ No se encontró la empresa o no hay datos")
        
        return '\n'.join(output)

# 8. Ticket por empresa por medio de palabras clave.
    @staticmethod
    def tickets_empresa_palabras(data: Dict[str, Any]) -> str:
        """Formatea tickets encontrados por palabras clave en una empresa"""
        output = []
        
        if 'empresa' in data and len(data['empresa']) > 0:
            empresa = data['empresa'][0]
            tickets = empresa.get('~PERTENECE', [])
            
            output.append(Formatos._encabezado("TICKETS POR PALABRAS CLAVE"))
            output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
            output.append(Formatos._divisor())
            
            if tickets:
                output.append("🔍 Tickets encontrados:")
                for ticket in tickets:
                    output.append(f"\n  • ID: {ticket.get('idTicket', 'N/A')}")
                    output.append(f"  📝 Descripción: {ticket.get('descripcion', 'N/A')}")
                    output.append(f"  🔧 Tipo: {ticket.get('tipoProblema', 'N/A')}")
                    output.append(Formatos._divisor(60))
                output.append(f"\n🔍 Total tickets encontrados: {len(tickets)}")
            else:
                output.append("ℹ️ No se encontraron tickets con las palabras clave especificadas")
            
            output.append("=" * 90)
        else:
            output.append("❌ No se encontró la empresa especificada")
        
        return '\n'.join(output)

# 9. Búsqueda de Ticket por Agente y Empresa por medio de palabras clave.
    @staticmethod
    def tickets_agente_empresa_palabras(data: Dict[str, Any]) -> str:
        """Formatea tickets encontrados por agente, empresa y palabras clave"""
        output = []
        
        if 'empresa' in data and len(data['empresa']) > 0:
            empresa = data['empresa'][0]
            agentes = empresa.get('TIENE', [])
            
            output.append(Formatos._encabezado("TICKETS POR AGENTE Y PALABRAS CLAVE"))
            output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
            output.append(Formatos._divisor())
            
            if agentes:
                agente = agentes[0]  # Solo debería haber uno por el filtro de ID
                tickets = agente.get('SOLUCIONA', [])
                
                output.append(f"👤 Agente: {agente.get('nombreAgente', 'N/A')} (ID: {agente.get('idAgente', 'N/A')})")
                output.append(Formatos._divisor())
                
                if tickets:
                    output.append("🔍 Tickets encontrados:")
                    for ticket in tickets:
                        output.append(f"\n  • ID: {ticket.get('idTicket', 'N/A')}")
                        output.append(f"  📝 Descripción: {ticket.get('descripcion', 'N/A')}")
                        output.append(f"  🔧 Tipo: {ticket.get('tipoProblema', 'N/A')}")
                        output.append(Formatos._divisor(60))
                    output.append(f"\n🔍 Total tickets encontrados: {len(tickets)}")
                else:
                    output.append("ℹ️ No se encontraron tickets con las palabras clave especificadas para este agente")
            else:
                output.append("⚠️ No se encontró el agente especificado en esta empresa")
            
            output.append("=" * 90)
        else:
            output.append("❌ No se encontró la empresa especificada")
        
        return '\n'.join(output)

# 10. Dirección de la empresa por medio de su ID.

    @staticmethod
    def direccion_empresa(data: Dict[str, Any]) -> str:
        """Formatea la información de ubicación de la empresa con enlace a Google Maps"""
        output = []
        
        if 'empresa' in data and len(data['empresa']) > 0:
            empresa = data['empresa'][0]
            ubicacion = empresa.get('ubicacion', {})
            coords = ubicacion.get('coordinates', [])
            
            output.append(Formatos._encabezado("UBICACIÓN DE EMPRESA"))
            output.append(f"🏢 Empresa: {empresa.get('nombreEmpresa', 'N/A')}")
            output.append(Formatos._divisor())
            
            if coords and len(coords) >= 2:
                lon, lat = coords[0], coords[1]
                google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
                
                output.append("📍 Coordenadas:")
                output.append(f"  - Latitud: {lat}")
                output.append(f"  - Longitud: {lon}")
                output.append(Formatos._divisor())
                output.append("🗺️ Enlace a Google Maps:")
                output.append(f"  {google_maps_link}")
            else:
                output.append("⚠️ No hay datos de ubicación disponibles")
            
            output.append("=" * 90)
        else:
            output.append("❌ No se encontró la empresa especificada")
        
        return '\n'.join(output)

def print_formatted(res, formato: str):
    """Imprime los datos formateados"""
    try:
        parsed = json.loads(res.json)
        formatter = getattr(Formatos, formato.lower().replace(" ", "_"), None)
        
        if formatter:
            print(formatter(parsed))
        else:
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error al formatear: {str(e)}")
        print("Salida cruda:")
        print(json.dumps(parsed, indent=2))