
# Documentación de Endpoints de la API

## URL Base
http://localhost:8000/api/

## Autenticación
Autenticación basada en sesión (Django)

## Endpoints

### 1. API Root
**GET** `/api/`

Devuelve información general de la API y los endpoints disponibles.

### 2. Clients

#### Listar Clientes
**GET** `/api/clients/`

Parámetros de consulta:
- `search`: Buscar en name, email, phone, company
- `ordering`: Ordenar por created_at, name, email (agregar `-` para descendente)
- `page`: Número de página

#### Crear Cliente
**POST** `/api/clients/`

Cuerpo:
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "company": "string (opcional)",
  "address": "string (opcional)"
}
```

#### Obtener Cliente
**GET** `/api/clients/{id}/`

#### Actualizar Cliente
**PUT** `/api/clients/{id}/`
**PATCH** `/api/clients/{id}/`

#### Eliminar Cliente
**DELETE** `/api/clients/{id}/`

### 3. Activities

#### Listar Actividades
**GET** `/api/activities/`

Parámetros de consulta:
- `client`: Filtrar por client ID
- `type`: Filtrar por tipo (call, meeting, email, task, note)
- `status`: Filtrar por estado (pending, completed, cancelled)
- `search`: Buscar en notes, client name, type
- `ordering`: Ordenar por date, created_at, type
- `page`: Número de página

#### Crear Actividad
**POST** `/api/activities/`

Cuerpo:
```json
{
  "client": 1,
  "type": "call|meeting|email|task|note",
  "status": "pending|completed|cancelled",
  "date": "2025-10-20T15:00:00Z",
  "notes": "string"
}
```

#### Obtener Actividad
**GET** `/api/activities/{id}/`

#### Actualizar Actividad
**PUT** `/api/activities/{id}/`
**PATCH** `/api/activities/{id}/`

*Nota: Solo el creador puede actualizar*

#### Eliminar Actividad
**DELETE** `/api/activities/{id}/`

*Nota: Solo el creador puede eliminar*

### 4. Statistics

#### Obtener Estadísticas
**GET** `/api/activities/statistics/`

Devuelve:
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

## Códigos de Estado HTTP

- `200 OK`: Éxito
- `201 Created`: Recurso creado
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor
