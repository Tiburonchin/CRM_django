#!/usr/bin/env python
"""
Script para crear datos de muestra: clientes y actividades de Lima y Callao, Perú
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from clients.models import Client
from activities.models import Activity

User = get_user_model()

# Datos de muestra para Lima y Callao
DISTRITOS_LIMA_CALLAO = [
    'San Miguel', 'Magdalena del Mar', 'Pueblo Libre', 'Jesús María',
    'Lince', 'San Isidro', 'Miraflores', 'Barranco', 'Surco',
    'La Molina', 'San Borja', 'Surquillo', 'San Luis',
    'Callao', 'Bellavista', 'La Perla', 'Ventanilla', 'Carmen de la Legua'
]

EMPRESAS_PERU = [
    'Corporación Lima SAC', 'Inversiones del Pacífico', 'Grupo Callao',
    'Soluciones Digitales Perú', 'Comercial San Miguel', 'Tech Lima',
    'Distribuidora Magdalena', 'Servicios Profesionales Callao',
    'Consultoría Miraflores', 'Importadora del Sur', 'Exportadora Callao',
    'Marketing Digital Lima', 'Logística Ventanilla', 'Grupo San Isidro',
    'Constructora Lima Norte', 'Alimentos del Pacífico'
]

NOMBRES = [
    'Carlos', 'María', 'José', 'Ana', 'Luis', 'Carmen', 'Miguel', 'Rosa',
    'Pedro', 'Julia', 'Antonio', 'Laura', 'Francisco', 'Isabel', 'Manuel',
    'Patricia', 'Jorge', 'Sofía', 'Ricardo', 'Elena', 'Fernando', 'Gabriela',
    'Alejandro', 'Mónica', 'Diego', 'Daniela', 'Roberto', 'Valeria'
]

APELLIDOS = [
    'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez',
    'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
    'Díaz', 'Cruz', 'Morales', 'Herrera', 'Jiménez', 'Mendoza',
    'Vargas', 'Castillo', 'Rojas', 'Vega', 'Silva', 'Ramos'
]

def generar_telefono():
    """Genera un número de teléfono peruano con formato +51"""
    # Celulares en Perú empiezan con 9
    return f"+51 9{random.randint(10000000, 99999999)}"

def generar_email(nombre, apellido, empresa):
    """Genera un email basado en el nombre y empresa"""
    nombre_limpio = nombre.lower().replace(' ', '')
    apellido_limpio = apellido.lower().replace(' ', '')
    empresa_limpia = empresa.lower().replace(' ', '').replace('sac', '').replace('.', '')[:15]
    return f"{nombre_limpio}.{apellido_limpio}@{empresa_limpia}.com.pe"

def generar_direccion(distrito):
    """Genera una dirección en el distrito especificado"""
    calles = ['Av. La Marina', 'Av. Brasil', 'Av. Universitaria', 'Calle Los Olivos',
              'Jr. Comercio', 'Av. Faucett', 'Av. Venezuela', 'Calle Lima',
              'Av. Colonial', 'Av. San Martín', 'Calle Las Flores', 'Av. Arequipa']
    calle = random.choice(calles)
    numero = random.randint(100, 9999)
    return f"{calle} {numero}, {distrito}, Lima, Perú"

def crear_clientes(usuario, cantidad=20):
    """Crea clientes de muestra"""
    print(f"\n📋 Creando {cantidad} clientes...")
    clientes = []
    
    for i in range(cantidad):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        nombre_completo = f"{nombre} {apellido}"
        empresa = random.choice(EMPRESAS_PERU)
        distrito = random.choice(DISTRITOS_LIMA_CALLAO)
        
        cliente = Client.objects.create(
            name=nombre_completo,
            email=generar_email(nombre, apellido, empresa),
            phone=generar_telefono(),
            company=empresa,
            address=generar_direccion(distrito),
            created_by=usuario
        )
        clientes.append(cliente)
        print(f"✅ Cliente {i+1}: {cliente.name} - {cliente.company} ({distrito})")
    
    return clientes

def crear_actividades(usuario, clientes, cantidad_por_cliente=3):
    """Crea actividades de muestra para los clientes"""
    print(f"\n📅 Creando actividades para los clientes...")
    
    tipos_actividad = ['call', 'meeting', 'email', 'task', 'note']
    estados = ['pending', 'completed', 'cancelled']
    
    notas_templates = {
        'call': [
            'Llamada de seguimiento para renovación de contrato',
            'Contacto inicial para presentación de servicios',
            'Seguimiento de propuesta comercial enviada',
            'Llamada de coordinación para reunión presencial',
            'Atención de consulta sobre productos'
        ],
        'meeting': [
            'Reunión presencial en oficinas de {distrito}',
            'Presentación de propuesta comercial',
            'Reunión de seguimiento - cierre de negociación',
            'Meeting kick-off del proyecto',
            'Revisión de avances y próximos pasos'
        ],
        'email': [
            'Envío de cotización y términos comerciales',
            'Seguimiento post-reunión con documentación',
            'Envío de contrato para revisión y firma',
            'Confirmación de orden de compra',
            'Newsletter mensual y novedades'
        ],
        'task': [
            'Preparar propuesta personalizada',
            'Coordinar visita técnica a instalaciones',
            'Elaborar presentación ejecutiva',
            'Revisar y actualizar datos del cliente',
            'Programar demo del producto'
        ],
        'note': [
            'Cliente interesado en expansión a otras sedes',
            'Requiere facturación electrónica',
            'Solicita descuento por volumen',
            'Prefiere comunicación vía WhatsApp',
            'Cliente referido por {empresa}'
        ]
    }
    
    actividades_creadas = 0
    
    for cliente in clientes:
        # Extraer distrito de la dirección del cliente
        distrito = cliente.address.split(',')[1].strip() if ',' in cliente.address else 'Lima'
        
        for i in range(cantidad_por_cliente):
            tipo = random.choice(tipos_actividad)
            
            # Generar fecha (pasadas, presentes y futuras)
            dias_offset = random.randint(-30, 30)
            fecha = datetime.now() + timedelta(days=dias_offset, hours=random.randint(8, 18))
            
            # Determinar estado basado en la fecha
            if dias_offset < -7:
                estado = random.choice(['completed', 'cancelled'])
            elif dias_offset < 0:
                estado = random.choice(['completed', 'pending'])
            else:
                estado = 'pending'
            
            # Generar nota contextual
            nota_template = random.choice(notas_templates[tipo])
            nota = nota_template.format(distrito=distrito, empresa=cliente.company)
            
            actividad = Activity.objects.create(
                client=cliente,
                created_by=usuario,
                type=tipo,
                status=estado,
                date=fecha,
                notes=nota
            )
            actividades_creadas += 1
    
    print(f"✅ {actividades_creadas} actividades creadas exitosamente")
    return actividades_creadas

def main():
    print("=" * 70)
    print("🇵🇪 CREACIÓN DE DATOS DE MUESTRA - CRM PERÚ (Lima y Callao)")
    print("=" * 70)
    
    # Verificar si existe un superusuario
    try:
        usuario = User.objects.filter(is_superuser=True).first()
        if not usuario:
            print("\n⚠️  No se encontró ningún superusuario.")
            print("Por favor, crea uno primero con: python manage.py createsuperuser")
            return
        
        print(f"\n👤 Usuario asignado: {usuario.username}")
        
        # Limpiar datos anteriores (opcional)
        respuesta = input("\n¿Deseas eliminar los datos existentes? (s/n): ").lower()
        if respuesta == 's':
            Activity.objects.all().delete()
            Client.objects.all().delete()
            print("🗑️  Datos anteriores eliminados")
        
        # Crear clientes
        cantidad_clientes = int(input("\n¿Cuántos clientes deseas crear? (default: 20): ") or "20")
        clientes = crear_clientes(usuario, cantidad_clientes)
        
        # Crear actividades
        actividades_por_cliente = int(input("\n¿Cuántas actividades por cliente? (default: 3): ") or "3")
        crear_actividades(usuario, clientes, actividades_por_cliente)
        
        # Resumen
        print("\n" + "=" * 70)
        print("✅ PROCESO COMPLETADO")
        print("=" * 70)
        print(f"📊 Resumen:")
        print(f"   - Clientes creados: {len(clientes)}")
        print(f"   - Actividades creadas: {len(clientes) * actividades_por_cliente}")
        print(f"   - Distritos: {', '.join(random.sample(DISTRITOS_LIMA_CALLAO, 5))}...")
        print(f"\n🌐 Accede al sistema:")
        print(f"   - Admin: http://localhost:8000/admin/")
        print(f"   - Clientes: http://localhost:8000/clients/")
        print(f"   - Actividades: http://localhost:8000/activities/")
        print(f"   - API: http://localhost:8000/api/v1/")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
