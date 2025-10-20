# 🚀 GUÍA RÁPIDA - Sistema CRM

## Instalación Rápida

### Windows (PowerShell)
```powershell
# Opción 1: Script automático
.\install.ps1

# Opción 2: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Ejecutar Servidor

### Windows
```powershell
.\run.ps1
# O manualmente:
python manage.py runserver
```

### Linux/Mac
```bash
python manage.py runserver
```

## URLs Principales

- **Home**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Clientes**: http://localhost:8000/clients/
- **Actividades**: http://localhost:8000/activities/

## Primeros Pasos

1. **Crear superusuario** (si no lo hiciste):
   ```bash
   python manage.py createsuperuser
   ```

2. **Iniciar sesión** en http://localhost:8000/users/login/

3. **Crear algunos clientes**:
   - Vía web: http://localhost:8000/clients/
   - Vía API: POST a http://localhost:8000/api/clients/

4. **Crear actividades** asociadas a clientes:
   - Vía web: http://localhost:8000/activities/
   - Vía API: POST a http://localhost:8000/api/activities/

5. **Ver estadísticas**: http://localhost:8000/api/activities/statistics/

## Ejemplos de API

### Autenticación
Primero debes iniciar sesión en la web para obtener la sesión.

### Crear Cliente
```bash
curl -X POST http://localhost:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "123456789",
    "company": "Tech Corp"
  }'
```

### Listar Clientes
```bash
curl http://localhost:8000/api/clients/ -b cookies.txt
```

### Crear Actividad
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "client": 1,
    "type": "call",
    "status": "pending",
    "date": "2025-10-20T15:00:00Z",
    "notes": "Llamada de seguimiento"
  }'
```

### Obtener Estadísticas
```bash
curl http://localhost:8000/api/activities/statistics/ -b cookies.txt
```

## Tests

```bash
# Ejecutar todos los tests
python manage.py test

# Tests por app
python manage.py test users
python manage.py test clients
python manage.py test activities

# Con verbosidad
python manage.py test --verbosity=2
```

## Comandos Útiles

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Shell interactivo
python manage.py shell

# Recopilar estáticos
python manage.py collectstatic

# Ver rutas
python manage.py show_urls  # (requiere django-extensions)
```

## Estructura de Datos

### Cliente
```json
{
  "name": "string (requerido)",
  "email": "string (requerido, único)",
  "phone": "string (requerido)",
  "company": "string (opcional)",
  "address": "string (opcional)"
}
```

### Actividad
```json
{
  "client": "integer (requerido, ID del cliente)",
  "type": "string (call|meeting|email|task|note)",
  "status": "string (pending|completed|cancelled)",
  "date": "datetime (requerido)",
  "notes": "string (requerido)"
}
```

## Solución de Problemas

### Error: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Error: No such table
```bash
python manage.py migrate
```

### Error: CSRF token missing
Asegúrate de incluir `{% csrf_token %}` en los formularios HTML.

### Error de permisos en actividades
Solo el creador puede editar/eliminar sus actividades (HU 30).

## Características Implementadas

✅ Todos los 40 Historias de Usuario (HU)
✅ 4 Sprints completos
✅ 14 tests unitarios pasando
✅ API REST completa
✅ Frontend web funcional
✅ Sistema de autenticación
✅ Permisos y validaciones
✅ Estadísticas y reportes
✅ Documentación completa

## Recursos

- **README.md**: Documentación completa
- **API Docs**: http://localhost:8000/api/ (cuando el servidor esté corriendo)
- **Django Admin**: http://localhost:8000/admin/

---

¡Disfruta del Sistema CRM! 🎉
