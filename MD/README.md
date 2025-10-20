# Sistema CRM - Django REST Framework

Sistema de Gestión de Relaciones con Clientes (CRM) desarrollado con Django y Django REST Framework.

## 📚 Documentación Adicional

- **[GUIA_API_REST.md](GUIA_API_REST.md)** - Guía completa de uso de la API REST
- **[INSTALACION_OTRA_PC.md](INSTALACION_OTRA_PC.md)** - Cómo instalar en otra computadora
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - Referencia rápida de endpoints
- **[ejemplo_uso_api.py](ejemplo_uso_api.py)** - Script de ejemplo para usar la API

## 📋 Características Principales

### ✅ SPRINT 1: Base del Sistema y Gestión de Usuarios
- **HU 1-2**: Proyecto Django configurado con DRF y SQLite
- **HU 3-5**: Sistema completo de autenticación (Registro, Login, Logout, Perfiles)
- **HU 6-7**: API REST con autenticación por sesión
- **HU 8**: Panel de administración de Django
- **HU 9**: Sistema de templates con herencia (base.html)
- **HU 10**: Validadores de contraseña y protección CSRF

### ✅ SPRINT 2: Módulo de Clientes
- **HU 11-16**: CRUD completo de Clientes (API REST)
- **HU 17-18**: Autenticación requerida y validaciones
- **HU 19-20**: Vistas web para lista y detalle de clientes

### ✅ SPRINT 3: Gestión de Actividades
- **HU 21-23**: CRUD completo de Actividades vinculadas a Clientes
- **HU 24-25**: Filtrado por cliente y serializers anidados
- **HU 26-27**: Búsqueda y CRUD web
- **HU 28**: Paginación (10 items por página)
- **HU 29**: Tests unitarios para modelos y serializers
- **HU 30**: Permisos personalizados (IsOwnerOrReadOnly)

### ✅ SPRINT 4: Reportes y Optimización
- **HU 31**: Endpoint de estadísticas (`/api/activities/statistics/`)
- **HU 32**: Ordenamiento en listados
- **HU 33**: Vista de reportes con consumo de API
- **HU 34**: Configuración de caching (preparada)
- **HU 35**: Optimización con `select_related` y `prefetch_related`
- **HU 36**: Sistema de logging configurado
- **HU 37**: Manejo correcto de códigos HTTP
- **HU 38**: requirements.txt generado
- **HU 39**: Documentación de API
- **HU 40**: Suite de tests completa

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Windows (CMD):
```cmd
venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario (HU 8)**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

8. **Acceder a la aplicación**
- Aplicación web: http://localhost:8000/
- Panel admin: http://localhost:8000/admin/
- API REST: http://localhost:8000/api/

## 📚 Documentación de la API

### Autenticación
La API utiliza autenticación por sesión de Django. Para acceder a los endpoints, debes estar autenticado.

### Endpoints Disponibles

#### 🏠 Raíz de la API
```
GET /api/
```
Retorna información general de la API y listado de endpoints disponibles.

**Respuesta:**
```json
{
  "message": "Bienvenido al API del CRM",
  "version": "1.0",
  "endpoints": {
    "clients": "/api/clients/",
    "activities": "/api/activities/",
    "statistics": "/api/activities/statistics/"
  }
}
```

---

#### 👥 Clientes

**Listar Clientes**
```
GET /api/clients/
```
Parámetros de query opcionales:
- `search`: Buscar en nombre, email, teléfono, empresa
- `ordering`: Ordenar por `created_at`, `name`, `email` (agregar `-` para descendente)
- `name`, `email`, `company`: Filtros específicos

**Respuesta:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "phone": "123456789",
      "address": "Calle 123",
      "company": "Tech Corp",
      "created_by": 1,
      "created_by_username": "admin",
      "created_at": "2025-10-19T10:00:00Z",
      "updated_at": "2025-10-19T10:00:00Z"
    }
  ]
}
```

**Crear Cliente**
```
POST /api/clients/
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "123456789",
  "company": "Tech Corp",
  "address": "Calle 123"
}
```

**Obtener Cliente**
```
GET /api/clients/{id}/
```

**Actualizar Cliente**
```
PUT /api/clients/{id}/
Content-Type: application/json

{
  "name": "Juan Pérez Actualizado",
  "email": "juan@example.com",
  "phone": "987654321",
  "company": "New Corp",
  "address": "Nueva Dirección"
}
```

**Actualización Parcial**
```
PATCH /api/clients/{id}/
Content-Type: application/json

{
  "phone": "999888777"
}
```

**Eliminar Cliente**
```
DELETE /api/clients/{id}/
```

---

#### 📅 Actividades

**Listar Actividades**
```
GET /api/activities/
```
Parámetros de query opcionales:
- `client`: Filtrar por ID de cliente
- `type`: Filtrar por tipo (`call`, `meeting`, `email`, `task`, `note`)
- `status`: Filtrar por estado (`pending`, `completed`, `cancelled`)
- `search`: Buscar en notas, nombre de cliente, tipo
- `ordering`: Ordenar por `date`, `created_at`, `type`

**Respuesta:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "client": 1,
      "client_name": "Juan Pérez",
      "type": "call",
      "type_display": "Llamada",
      "status": "pending",
      "status_display": "Pendiente",
      "date": "2025-10-20T14:00:00Z",
      "notes": "Llamada de seguimiento",
      "created_by": 1,
      "created_by_username": "admin",
      "created_at": "2025-10-19T10:00:00Z",
      "updated_at": "2025-10-19T10:00:00Z"
    }
  ]
}
```

**Crear Actividad**
```
POST /api/activities/
Content-Type: application/json

{
  "client": 1,
  "type": "meeting",
  "status": "pending",
  "date": "2025-10-20T15:00:00Z",
  "notes": "Reunión de presentación del producto"
}
```

**Obtener Actividad**
```
GET /api/activities/{id}/
```
*Nota: Este endpoint retorna información detallada del cliente asociado.*

**Actualizar Actividad**
```
PUT /api/activities/{id}/
PATCH /api/activities/{id}/
```
*Solo el creador de la actividad puede modificarla (HU 30).*

**Eliminar Actividad**
```
DELETE /api/activities/{id}/
```
*Solo el creador de la actividad puede eliminarla (HU 30).*

---

#### 📊 Estadísticas

**Obtener Estadísticas de Actividades (HU 31)**
```
GET /api/activities/statistics/
```

**Respuesta:**
```json
{
  "total": 50,
  "by_status": {
    "pending": 20,
    "completed": 25,
    "cancelled": 5
  },
  "by_type": {
    "call": 15,
    "meeting": 12,
    "email": 10,
    "task": 8,
    "note": 5
  },
  "recent_activities": [
    {
      "id": 1,
      "client_name": "Juan Pérez",
      "type_display": "Llamada",
      "date": "2025-10-20T14:00:00Z",
      "notes": "Seguimiento"
    }
  ]
}
```

---

### Códigos de Estado HTTP (HU 37)

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

---

## 🧪 Ejecutar Tests (HU 40)

```bash
python manage.py test
```

Para ejecutar tests específicos:
```bash
python manage.py test users
python manage.py test clients
python manage.py test activities
```

Para ver cobertura:
```bash
python manage.py test --verbosity=2
```

---

## 📁 Estructura del Proyecto

```
crm_project/
├── activities/          # App de Actividades
│   ├── models.py       # Modelo Activity
│   ├── serializers.py  # Serializers
│   ├── views.py        # ViewSets y vistas web
│   ├── urls.py         # URLs
│   ├── permissions.py  # Permisos personalizados
│   ├── admin.py        # Configuración admin
│   └── tests.py        # Tests unitarios
├── clients/            # App de Clientes
│   ├── models.py       # Modelo Client
│   ├── serializers.py  # Serializers
│   ├── views.py        # ViewSets y vistas web
│   ├── urls.py         # URLs
│   ├── admin.py        # Configuración admin
│   └── tests.py        # Tests unitarios
├── users/              # App de Usuarios
│   ├── models.py       # Modelo UserProfile
│   ├── forms.py        # Formularios de registro
│   ├── views.py        # Vistas de autenticación
│   ├── urls.py         # URLs
│   ├── admin.py        # Configuración admin
│   └── tests.py        # Tests unitarios
├── crm_project/        # Configuración principal
│   ├── settings.py     # Configuración de Django
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # WSGI
├── templates/          # Templates HTML
│   ├── base.html       # Template base (HU 9)
│   ├── home.html       # Página principal
│   ├── users/          # Templates de usuarios
│   ├── clients/        # Templates de clientes
│   └── activities/     # Templates de actividades
├── static/             # Archivos estáticos
├── logs/               # Logs del sistema (HU 36)
├── manage.py           # Script de gestión
└── requirements.txt    # Dependencias (HU 38)
```

---

## 🔒 Seguridad (HU 10)

- **Validadores de Contraseña**: Configurados en `settings.py`
  - UserAttributeSimilarityValidator
  - MinimumLengthValidator (8 caracteres)
  - CommonPasswordValidator
  - NumericPasswordValidator

- **Protección CSRF**: Implementada en todos los formularios con `{% csrf_token %}`

- **Permisos**: Solo usuarios autenticados pueden acceder a la API

- **Ownership**: Solo el creador puede modificar/eliminar sus actividades

---

## 📝 Características Técnicas

### Optimización (HU 35)
- Uso de `select_related()` para relaciones ForeignKey
- Uso de `prefetch_related()` para relaciones inversas
- Queries optimizadas en ViewSets

### Logging (HU 36)
- Configuración en `settings.py`
- Logs de errores en `logs/errors.log`
- Logs en consola para desarrollo

### Paginación (HU 28)
- 10 items por página por defecto
- Configuración en `REST_FRAMEWORK` settings

### Filtrado y Búsqueda
- Filtros por campos específicos
- Búsqueda de texto completo
- Ordenamiento flexible

---

## 👨‍💻 Desarrollo

### Variables de Entorno Recomendadas (Producción)
```
DEBUG=False
SECRET_KEY=<tu-secret-key>
ALLOWED_HOSTS=tu-dominio.com
DATABASE_URL=<url-de-base-de-datos>
```

### Comandos Útiles

**Crear migraciones:**
```bash
python manage.py makemigrations
```

**Aplicar migraciones:**
```bash
python manage.py migrate
```

**Crear superusuario:**
```bash
python manage.py createsuperuser
```

**Recopilar archivos estáticos:**
```bash
python manage.py collectstatic
```

**Shell interactivo:**
```bash
python manage.py shell
```

---

## 📞 Soporte

Para problemas o preguntas, consulta los logs en `logs/errors.log` o revisa el código en cada app.

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos.

---

**Desarrollado con ❤️ usando Django & Django REST Framework**
