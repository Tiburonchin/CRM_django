# Guía: Versionado de la API y Documentación Automática

Resumen rápido:
- La API está ahora versionada en la ruta base `/api/v1/`.
- Documentación automática generada con `drf-spectacular` disponible en:
  - Swagger UI: `/api/v1/swagger/`
  - ReDoc: `/api/v1/redoc/`
  - OpenAPI JSON/YAML: `/api/v1/schema/`

Qué hace y para qué sirve
- Versionado (URLPathVersioning): permite introducir cambios incompatibles en el futuro (p.ej. `/api/v2/`) sin romper clientes existentes.
- `drf-spectacular` genera automáticamente el esquema OpenAPI a partir de tus serializers, viewsets y configuración de DRF, y expone interfaces interactivas (Swagger/ReDoc) para explorar y probar la API.

Cómo usarlo (rápido)
- Accede a la raíz de la API:
  - `GET /api/v1/` → información general y enlaces a recursos.
- Endpoints principales (ejemplos):
  - `GET /api/v1/clients/` — listar clientes
  - `POST /api/v1/clients/` — crear cliente
  - `GET /api/v1/activities/` — listar actividades
  - `GET /api/v1/activities/statistics/` — obtener estadísticas
- Documentación interactiva:
  - Abre `http://localhost:8000/api/v1/swagger/` (Swagger UI) para probar endpoints desde el navegador.
  - Abre `http://localhost:8000/api/v1/redoc/` para ver la documentación más enfocada a lectura.

Cambios en código cliente y plantillas
- Actualiza las URL fijas del frontend y scripts desde `/api/...` a `/api/v1/...`.
- Recomendación: en lugar de hardcodear rutas, usar variables base en JS (por ejemplo: `const API_BASE = '/api/v1/';`) y construir rutas con `API_BASE + 'clients/'`.

Compatibilidad y migraciones futuras
- Si necesitas mantener compatibilidad con clientes antiguos, puedes añadir una ruta alias que redirija `/api/` a `/api/v1/` o mantener ambas rutas durante un tiempo de transición.
- Para una futura `/api/v2/`, crea nuevos viewsets o serializadores que reflejen los cambios y agrégalos bajo `/api/v2/`.

Cómo probar localmente
1. Instala dependencias:
```powershell
python -m pip install -r requirements.txt
```
2. Ejecuta servidor:
```powershell
python manage.py runserver
```
3. Abre:
- `http://localhost:8000/api/v1/` — raíz
- `http://localhost:8000/api/v1/swagger/` — Swagger UI
- `http://localhost:8000/api/v1/redoc/` — ReDoc

Notas para desarrolladores
- Configuración relevante en `crm_project/settings.py`:
  - `DEFAULT_VERSIONING_CLASS`: `rest_framework.versioning.URLPathVersioning`
  - `DEFAULT_SCHEMA_CLASS`: `drf_spectacular.openapi.AutoSchema`
  - `SPECTACULAR_SETTINGS` contiene metadata del API
- Rutas en `crm_project/urls.py`: la API y documentación están agrupadas en `api_urlpatterns` e incluidas con `re_path(r'^api/(?P<version>(v1))/', include(api_urlpatterns))`.

Recomendaciones finales
- Actualiza la documentación externa y scripts que consumen la API a la nueva base `/api/v1/`.
- Usa `reverse()` en tests en vez de hardcoded URLs para reducir mantenimiento cuando cambie el versionado.
- Considera añadir pruebas para asegurar que `schema/`, `swagger/` y `redoc/` estén disponibles (HTTP 200) como parte de la CI.

---
Si quieres, puedo:
- Añadir una redirección automática `/api/` → `/api/v1/` para compatibilidad.
- Actualizar los tests para usar `reverse()` o `APIClient` con `reverse('client-list')`.
- Ejecutar los tests aquí y corregir referencias en tests que fallen.
