"""
Ejemplo de Uso de la API REST del CRM
======================================

Este script demuestra cómo interactuar con la API del sistema CRM
usando Python y la librería requests.

Requisitos:
    pip install requests

Uso:
    python ejemplo_uso_api.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = 'http://localhost:8000/api'
LOGIN_URL = 'http://localhost:8000/users/login/'

# Credenciales (cámbialas por las tuyas)
USERNAME = 'admin'
PASSWORD = 'admin'  # Cambia esto por tu contraseña


class CRMAPIClient:
    """Cliente para interactuar con la API del CRM"""
    
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.login(username, password)
    
    def login(self, username, password):
        """Iniciar sesión en el sistema"""
        print("🔐 Iniciando sesión...")
        
        # Primero obtener el CSRF token
        self.session.get(LOGIN_URL)
        csrftoken = self.session.cookies.get('csrftoken')
        
        # Hacer login
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrftoken
        }
        
        response = self.session.post(
            LOGIN_URL,
            data=login_data,
            headers={'Referer': LOGIN_URL}
        )
        
        if response.status_code == 200:
            print("✅ Sesión iniciada correctamente\n")
        else:
            print("❌ Error al iniciar sesión")
            print(f"Status: {response.status_code}")
    
    def get_clients(self, search=None, page=1):
        """Obtener lista de clientes"""
        url = f"{self.base_url}/clients/"
        params = {'page': page}
        
        if search:
            params['search'] = search
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error al obtener clientes: {response.status_code}")
            return None
    
    def create_client(self, name, email, phone, company=None, address=None):
        """Crear un nuevo cliente"""
        url = f"{self.base_url}/clients/"
        
        data = {
            'name': name,
            'email': email,
            'phone': phone,
        }
        
        if company:
            data['company'] = company
        if address:
            data['address'] = address
        
        # Obtener CSRF token
        csrftoken = self.session.cookies.get('csrftoken')
        
        response = self.session.post(
            url,
            json=data,
            headers={
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"❌ Error al crear cliente: {response.status_code}")
            print(response.text)
            return None
    
    def get_activities(self, client_id=None, type=None, status=None, search=None):
        """Obtener lista de actividades con filtros"""
        url = f"{self.base_url}/activities/"
        params = {}
        
        if client_id:
            params['client'] = client_id
        if type:
            params['type'] = type
        if status:
            params['status'] = status
        if search:
            params['search'] = search
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error al obtener actividades: {response.status_code}")
            return None
    
    def create_activity(self, client_id, type, status, date, notes):
        """Crear una nueva actividad"""
        url = f"{self.base_url}/activities/"
        
        data = {
            'client': client_id,
            'type': type,
            'status': status,
            'date': date,
            'notes': notes
        }
        
        csrftoken = self.session.cookies.get('csrftoken')
        
        response = self.session.post(
            url,
            json=data,
            headers={
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"❌ Error al crear actividad: {response.status_code}")
            print(response.text)
            return None
    
    def get_statistics(self):
        """Obtener estadísticas de actividades"""
        url = f"{self.base_url}/activities/statistics/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error al obtener estadísticas: {response.status_code}")
            return None


def demo_listar_clientes(api):
    """Demostración: Listar clientes"""
    print("=" * 60)
    print("📋 LISTAR CLIENTES")
    print("=" * 60)
    
    data = api.get_clients()
    
    if data:
        print(f"Total de clientes: {data.get('count', len(data))}\n")
        
        clients = data.get('results', data)
        for i, client in enumerate(clients[:5], 1):  # Mostrar solo los primeros 5
            print(f"{i}. {client['name']}")
            print(f"   Email: {client['email']}")
            print(f"   Teléfono: {client['phone']}")
            print(f"   Empresa: {client.get('company', 'N/A')}")
            print()


def demo_crear_cliente(api):
    """Demostración: Crear un nuevo cliente"""
    print("=" * 60)
    print("➕ CREAR NUEVO CLIENTE")
    print("=" * 60)
    
    nuevo_cliente = api.create_client(
        name="Cliente de Prueba API",
        email="prueba_api@example.com",
        phone="999888777",
        company="Tech Solutions",
        address="Av. Ejemplo 123"
    )
    
    if nuevo_cliente:
        print("✅ Cliente creado exitosamente!")
        print(f"ID: {nuevo_cliente['id']}")
        print(f"Nombre: {nuevo_cliente['name']}")
        print(f"Email: {nuevo_cliente['email']}")
        print()
        return nuevo_cliente['id']
    return None


def demo_buscar_clientes(api):
    """Demostración: Buscar clientes"""
    print("=" * 60)
    print("🔍 BUSCAR CLIENTES")
    print("=" * 60)
    
    search_term = "Tech"
    print(f"Buscando: '{search_term}'\n")
    
    data = api.get_clients(search=search_term)
    
    if data:
        clients = data.get('results', data)
        print(f"Resultados encontrados: {len(clients)}\n")
        
        for client in clients:
            print(f"• {client['name']} - {client['company']}")
        print()


def demo_listar_actividades(api):
    """Demostración: Listar actividades"""
    print("=" * 60)
    print("📅 LISTAR ACTIVIDADES")
    print("=" * 60)
    
    data = api.get_activities()
    
    if data:
        activities = data.get('results', data)
        print(f"Total de actividades: {len(activities)}\n")
        
        for i, activity in enumerate(activities[:5], 1):  # Mostrar solo las primeras 5
            print(f"{i}. {activity['type_display']} - {activity['client_name']}")
            print(f"   Estado: {activity['status_display']}")
            print(f"   Fecha: {activity['date']}")
            print(f"   Notas: {activity['notes'][:50]}...")
            print()


def demo_filtrar_actividades(api):
    """Demostración: Filtrar actividades"""
    print("=" * 60)
    print("🔎 FILTRAR ACTIVIDADES")
    print("=" * 60)
    
    # Filtrar por estado pendiente
    print("Actividades PENDIENTES:\n")
    data = api.get_activities(status='pending')
    
    if data:
        activities = data.get('results', data)
        print(f"Encontradas: {len(activities)}\n")
        
        for activity in activities[:3]:  # Mostrar solo las primeras 3
            print(f"• {activity['type_display']} - {activity['client_name']}")
            print(f"  Fecha: {activity['date']}")
        print()
    
    # Filtrar por tipo
    print("\nActividades tipo LLAMADA:\n")
    data = api.get_activities(type='call')
    
    if data:
        activities = data.get('results', data)
        print(f"Encontradas: {len(activities)}\n")


def demo_crear_actividad(api, client_id):
    """Demostración: Crear una actividad"""
    print("=" * 60)
    print("➕ CREAR NUEVA ACTIVIDAD")
    print("=" * 60)
    
    # Fecha para mañana
    fecha = (datetime.now() + timedelta(days=1)).isoformat()
    
    nueva_actividad = api.create_activity(
        client_id=client_id,
        type='call',
        status='pending',
        date=fecha,
        notes='Llamada de seguimiento creada desde la API'
    )
    
    if nueva_actividad:
        print("✅ Actividad creada exitosamente!")
        print(f"ID: {nueva_actividad['id']}")
        print(f"Tipo: {nueva_actividad['type_display']}")
        print(f"Cliente: {nueva_actividad['client_name']}")
        print(f"Estado: {nueva_actividad['status_display']}")
        print()


def demo_estadisticas(api):
    """Demostración: Obtener estadísticas"""
    print("=" * 60)
    print("📊 ESTADÍSTICAS DE ACTIVIDADES")
    print("=" * 60)
    
    stats = api.get_statistics()
    
    if stats:
        print(f"Total de actividades: {stats['total']}\n")
        
        print("Por Estado:")
        for estado, cantidad in stats['by_status'].items():
            print(f"  • {estado.capitalize()}: {cantidad}")
        
        print("\nPor Tipo:")
        for tipo, cantidad in stats['by_type'].items():
            print(f"  • {tipo.capitalize()}: {cantidad}")
        print()


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("  DEMOSTRACIÓN DE USO DE LA API REST DEL CRM")
    print("=" * 60 + "\n")
    
    # Crear cliente de la API
    api = CRMAPIClient(BASE_URL, USERNAME, PASSWORD)
    
    try:
        # 1. Listar clientes
        demo_listar_clientes(api)
        input("Presiona Enter para continuar...")
        
        # 2. Buscar clientes
        demo_buscar_clientes(api)
        input("Presiona Enter para continuar...")
        
        # 3. Crear un cliente
        nuevo_cliente_id = demo_crear_cliente(api)
        input("Presiona Enter para continuar...")
        
        # 4. Listar actividades
        demo_listar_actividades(api)
        input("Presiona Enter para continuar...")
        
        # 5. Filtrar actividades
        demo_filtrar_actividades(api)
        input("Presiona Enter para continuar...")
        
        # 6. Crear una actividad (si se creó un cliente)
        if nuevo_cliente_id:
            demo_crear_actividad(api, nuevo_cliente_id)
            input("Presiona Enter para continuar...")
        
        # 7. Ver estadísticas
        demo_estadisticas(api)
        
        print("\n" + "=" * 60)
        print("✅ DEMOSTRACIÓN COMPLETADA")
        print("=" * 60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")


if __name__ == '__main__':
    print("\n⚠️  IMPORTANTE: Asegúrate de que el servidor Django esté corriendo")
    print("   Ejecuta: python manage.py runserver\n")
    
    continuar = input("¿El servidor está corriendo? (s/n): ")
    
    if continuar.lower() == 's':
        main()
    else:
        print("\n👉 Primero ejecuta el servidor Django:")
        print("   python manage.py runserver")
        print("\nLuego ejecuta este script nuevamente.")
