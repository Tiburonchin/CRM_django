# Guía Completa: API REST del Sistema CRM

## ¿Qué es una API REST?

Una **API REST** (Application Programming Interface - Representational State Transfer) es una interfaz que permite la comunicación entre diferentes aplicaciones o sistemas a través de HTTP. En este proyecto, la API REST permite:

- **Separar el frontend del backend**: El servidor Django proporciona datos, y cualquier cliente (web, móvil, desktop) puede consumirlos
- **Integración con otras aplicaciones**: Otros sistemas pueden conectarse a tu CRM
- **Desarrollo de aplicaciones móviles**: Puedes crear una app móvil que use la misma API
- **Automatización**: Scripts y herramientas externas pueden interactuar con tu sistema

## ¿Cómo Funciona en Este Proyecto?

### Arquitectura del Sistema

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Navegador     │ ←─HTTP─→│  Servidor Django │ ←─ORM─→│  Base de    │
│   (Frontend)    │         │   (Backend/API)  │         │   Datos     │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

### Componentes del Proyecto

1. **Backend (Django + Django REST Framework)**:
   - `views.py`: Contiene los ViewSets que manejan las peticiones HTTP
   - `serializers.py`: Convierte objetos Python a JSON y viceversa
   - `models.py`: Define la estructura de datos
   - `urls.py`: Define las rutas de la API

2. **Frontend (Templates HTML + JavaScript)**:
   - Hace peticiones AJAX a la API usando `fetch()`
   - Muestra los datos en la interfaz web
   - Actualiza dinámicamente sin recargar la página

## Endpoints Disponibles

### URL Base
```
http://localhost:8000/api/
```

### 1. Clientes (`/api/clients/`)

#### Listar todos los clientes
```http
GET /api/clients/
```
**Ejemplo de respuesta:**
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/clients/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "phone": "999888777",
      "company": "Tech Corp",
      "address": "Av. Principal 123",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

#### Crear un nuevo cliente
```http
POST /api/clients/
Content-Type: application/json

{
  "name": "María García",
  "email": "maria@example.com",
  "phone": "987654321",
  "company": "Innovate SA",
  "address": "Calle Secundaria 456"
}
```

#### Obtener un cliente específico
```http
GET /api/clients/5/
```

#### Actualizar un cliente
```http
PUT /api/clients/5/
Content-Type: application/json

{
  "name": "María García Actualizada",
  "email": "maria.nueva@example.com",
  "phone": "987654321",
  "company": "Innovate SA",
  "address": "Nueva Dirección 789"
}
```

#### Actualización parcial
```http
PATCH /api/clients/5/
Content-Type: application/json

{
  "phone": "999000111"
}
```

#### Eliminar un cliente
```http
DELETE /api/clients/5/
```

### 2. Actividades (`/api/activities/`)

#### Listar actividades con filtros
```http
GET /api/activities/?type=call&status=pending
GET /api/activities/?client=5
GET /api/activities/?search=reunion
```

**Parámetros de consulta:**
- `type`: call, meeting, email, task, note
- `status`: pending, completed, cancelled
- `client`: ID del cliente
- `search`: Busca en notas y nombre del cliente
- `ordering`: date, -date, created_at, -created_at
- `page`: Número de página (paginación de 10 items)

**Ejemplo de respuesta:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "client": 5,
      "client_name": "Juan Pérez",
      "type": "call",
      "type_display": "Llamada",
      "status": "pending",
      "status_display": "Pendiente",
      "date": "2025-10-20T15:00:00Z",
      "notes": "Seguimiento de propuesta comercial",
      "created_by": 1,
      "created_by_username": "admin",
      "created_at": "2025-10-19T10:00:00Z"
    }
  ]
}
```

#### Crear una actividad
```http
POST /api/activities/
Content-Type: application/json

{
  "client": 5,
  "type": "meeting",
  "status": "pending",
  "date": "2025-10-25T14:00:00",
  "notes": "Reunión de cierre de ventas"
}
```

### 3. Estadísticas (`/api/activities/statistics/`)

```http
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
  "recent_activities": [...]
}
```

## Cómo Usar la API

### 1. Desde el Navegador Web (Interfaz DRF)

Django REST Framework proporciona una interfaz web automática:

```
http://localhost:8000/api/
http://localhost:8000/api/clients/
http://localhost:8000/api/activities/
```

Puedes navegar, crear, editar y eliminar datos directamente desde el navegador.

### 2. Desde JavaScript (Frontend)

```javascript
// Obtener todos los clientes
fetch('http://localhost:8000/api/clients/')
  .then(response => response.json())
  .then(data => {
    console.log(data.results);
  });

// Crear un nuevo cliente
fetch('http://localhost:8000/api/clients/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken  // Necesario en Django
  },
  body: JSON.stringify({
    name: 'Nuevo Cliente',
    email: 'nuevo@example.com',
    phone: '123456789'
  })
})
.then(response => response.json())
.then(data => console.log('Cliente creado:', data));

// Filtrar actividades
fetch('http://localhost:8000/api/activities/?status=pending&type=call')
  .then(response => response.json())
  .then(data => console.log('Actividades pendientes:', data.results));
```

### 3. Desde Python (Script Externo)

```python
import requests

# URL base
BASE_URL = 'http://localhost:8000/api'

# Crear una sesión para mantener las cookies
session = requests.Session()

# 1. Login (si es necesario)
login_data = {
    'username': 'admin',
    'password': 'tu_contraseña'
}
session.post('http://localhost:8000/users/login/', data=login_data)

# 2. Obtener clientes
response = session.get(f'{BASE_URL}/clients/')
clientes = response.json()
print(f"Total de clientes: {clientes['count']}")

# 3. Crear una actividad
nueva_actividad = {
    'client': 1,
    'type': 'call',
    'status': 'pending',
    'date': '2025-10-25T10:00:00',
    'notes': 'Llamada de seguimiento'
}
response = session.post(f'{BASE_URL}/activities/', json=nueva_actividad)
print(f"Actividad creada: {response.json()}")

# 4. Filtrar actividades
response = session.get(f'{BASE_URL}/activities/', params={
    'status': 'pending',
    'type': 'call'
})
actividades = response.json()
print(f"Actividades encontradas: {len(actividades['results'])}")
```

### 4. Desde PowerShell

```powershell
# GET: Obtener clientes
Invoke-RestMethod -Uri "http://localhost:8000/api/clients/" -Method GET

# POST: Crear cliente
$body = @{
    name = "Cliente desde PowerShell"
    email = "powershell@example.com"
    phone = "999888777"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/clients/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### 5. Desde cURL

```bash
# GET: Listar clientes
curl http://localhost:8000/api/clients/

# POST: Crear cliente
curl -X POST http://localhost:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phone":"123456789"}'

# GET con filtros
curl "http://localhost:8000/api/activities/?status=pending&type=call"
```

### 6. Desde Postman o Insomnia

1. Abre Postman/Insomnia
2. Crea una nueva petición
3. Selecciona el método HTTP (GET, POST, PUT, DELETE)
4. Ingresa la URL: `http://localhost:8000/api/clients/`
5. Para POST/PUT, en "Body" selecciona "JSON" y escribe el contenido
6. Envía la petición

## Autenticación

El sistema usa **autenticación por sesión**:

1. Debes iniciar sesión primero en `/users/login/`
2. La cookie de sesión se mantiene automáticamente
3. Si usas scripts externos, mantén la sesión activa

**Ejemplo:**
```python
import requests
session = requests.Session()
session.post('http://localhost:8000/users/login/', data={
    'username': 'admin',
    'password': 'admin123'
})
# Ahora puedes usar session.get(), session.post(), etc.
```

## Casos de Uso Prácticos

### 1. Dashboard Personalizado
Crear un dashboard externo que consuma la API para mostrar métricas del CRM.

### 2. Aplicación Móvil
Desarrollar una app móvil (React Native, Flutter) que se conecte a la misma API.

### 3. Integración con Otros Sistemas
- Sincronizar clientes con un sistema de facturación
- Enviar notificaciones cuando hay nuevas actividades
- Importar/exportar datos automáticamente

### 4. Automatización
```python
# Script que envía un reporte diario
import requests
from datetime import datetime

session = requests.Session()
# Login...

# Obtener estadísticas
stats = session.get('http://localhost:8000/api/activities/statistics/').json()

# Enviar por email o guardar en archivo
print(f"Reporte del {datetime.now()}")
print(f"Total actividades: {stats['total']}")
print(f"Pendientes: {stats['by_status']['pending']}")
```

### 5. Webhooks y Notificaciones
Puedes extender la API para enviar notificaciones cuando ocurren eventos:
- Cliente nuevo creado
- Actividad vencida
- Estado de actividad cambiado

## Ventajas de Usar la API

✅ **Flexibilidad**: Múltiples clientes pueden usar la misma fuente de datos
✅ **Escalabilidad**: Frontend y backend pueden escalar independientemente
✅ **Mantenimiento**: Cambios en uno no afectan necesariamente al otro
✅ **Integración**: Fácil conexión con servicios externos
✅ **Desarrollo paralelo**: Equipos diferentes pueden trabajar en frontend y backend
✅ **Multiplataforma**: Web, móvil, desktop usando la misma API

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa (sin contenido)
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Seguridad

🔒 **Recomendaciones:**
- Usa HTTPS en producción
- Implementa rate limiting
- Valida todos los datos de entrada
- Usa tokens JWT para APIs públicas
- Mantén las dependencias actualizadas
- No expongas información sensible en los errores

---

**Recuerda:** Esta API está diseñada para ser RESTful, siguiendo las mejores prácticas de diseño de APIs modernas.
