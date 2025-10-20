# Guía: Instalar y Ejecutar el Sistema CRM en Otra Computadora

Esta guía te explica paso a paso cómo ejecutar este proyecto Django en otra computadora.

## Requisitos Previos

### Software Necesario

1. **Python 3.8 o superior**
   - Descarga desde: https://www.python.org/downloads/
   - Durante la instalación, marca "Add Python to PATH"

2. **Git** (opcional, pero recomendado)
   - Descarga desde: https://git-scm.com/downloads

3. **Editor de código** (opcional)
   - Visual Studio Code: https://code.visualstudio.com/
   - PyCharm: https://www.jetbrains.com/pycharm/

## Método 1: Instalación Completa (Recomendado)

### Paso 1: Copiar el Proyecto

Tienes dos opciones:

**Opción A: Usando Git (si el proyecto está en GitHub)**
```powershell
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

**Opción B: Copiar manualmente**
1. Copia toda la carpeta del proyecto a la nueva computadora
2. Abre PowerShell o CMD en la carpeta del proyecto

### Paso 2: Verificar Python

```powershell
python --version
```

Debe mostrar Python 3.8 o superior. Si no funciona, intenta:
```powershell
python3 --version
py --version
```

### Paso 3: Crear Entorno Virtual

**En Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1
```

**Si aparece error de permisos en PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 4: Instalar Dependencias

Con el entorno virtual activado:

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

Si `requirements.txt` no existe o quieres instalar manualmente:
```powershell
pip install django==5.2.7
pip install djangorestframework==3.16.1
pip install django-filter==25.2
```

### Paso 5: Configurar Base de Datos

```powershell
# Aplicar migraciones (crear tablas en la base de datos)
python manage.py migrate

# Crear superusuario (administrador)
python manage.py createsuperuser
```

Te pedirá:
- **Username**: elige un nombre de usuario (ej: admin)
- **Email**: tu email (opcional, puedes dejarlo en blanco)
- **Password**: elige una contraseña segura
- **Password (again)**: repite la contraseña

### Paso 6: (Opcional) Cargar Datos de Ejemplo

Si existe el script de datos de ejemplo:
```powershell
python create_sample_data.py
```

### Paso 7: Ejecutar el Servidor

```powershell
python manage.py runserver
```

Verás algo como:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Paso 8: Abrir en el Navegador

Abre tu navegador favorito y visita:
- **Página principal**: http://localhost:8000/
- **Panel admin**: http://localhost:8000/admin/
- **API REST**: http://localhost:8000/api/

## Método 2: Usando el Script de Instalación Automático

Si existe el archivo `install.ps1`:

```powershell
# Permitir ejecución de scripts (una sola vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar script de instalación
.\install.ps1
```

Luego para ejecutar el servidor:
```powershell
.\run.ps1
```

## Verificación de la Instalación

### 1. Verificar que el servidor está corriendo
Abre http://localhost:8000/ en tu navegador

### 2. Verificar la API
Abre http://localhost:8000/api/ y deberías ver la interfaz de Django REST Framework

### 3. Verificar el admin
Abre http://localhost:8000/admin/ e inicia sesión con tu superusuario

### 4. Probar las funcionalidades
- Crear un cliente
- Crear una actividad
- Probar los filtros

## Estructura del Proyecto

```
vs2/                          # Carpeta raíz del proyecto
├── .venv/                    # Entorno virtual (se crea localmente)
├── manage.py                 # Script de administración de Django
├── requirements.txt          # Lista de dependencias
├── db.sqlite3               # Base de datos SQLite
├── install.ps1              # Script de instalación (Windows)
├── run.ps1                  # Script para ejecutar servidor (Windows)
├── crm_project/             # Configuración del proyecto
│   ├── settings.py          # Configuración principal
│   └── urls.py              # URLs principales
├── clients/                 # App de clientes
├── activities/              # App de actividades
├── users/                   # App de usuarios
├── templates/               # Plantillas HTML
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
└── logs/                    # Logs del sistema
```

## Solución de Problemas Comunes

### Error: "python no se reconoce como comando"

**Solución:**
1. Reinstala Python y marca "Add Python to PATH"
2. O usa `py` en lugar de `python`:
   ```powershell
   py -m venv .venv
   py manage.py runserver
   ```

### Error: "No module named django"

**Solución:**
Asegúrate de tener el entorno virtual activado y las dependencias instaladas:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "cannot be loaded because running scripts is disabled"

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Port 8000 already in use"

**Solución 1:** Cerrar el proceso que usa el puerto
```powershell
# En Windows
netstat -ano | findstr :8000
taskkill /PID <numero_proceso> /F
```

**Solución 2:** Usar otro puerto
```powershell
python manage.py runserver 8080
```

### Error: "Secret key must not be empty"

**Solución:**
El archivo `settings.py` ya debe tener una SECRET_KEY. Si no, agrega una:
```python
SECRET_KEY = 'django-insecure-tu-clave-secreta-aqui'
```

### La base de datos está vacía

**Solución:**
```powershell
python manage.py migrate
python manage.py createsuperuser
python create_sample_data.py  # Si existe
```

## Configuración para Producción

⚠️ **Importante:** Los siguientes cambios son necesarios para un servidor de producción:

### 1. Modificar `settings.py`

```python
# Cambiar DEBUG a False
DEBUG = False

# Agregar el dominio permitido
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']

# Cambiar SECRET_KEY por una generada
# Genera una nueva en: https://djecrety.ir/
SECRET_KEY = 'nueva-clave-secreta-super-compleja-y-larga'
```

### 2. Usar Base de Datos Profesional

SQLite es solo para desarrollo. Para producción usa:
- **PostgreSQL** (recomendado)
- **MySQL**
- **MariaDB**

Ejemplo con PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_bd',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Usar un Servidor WSGI

No uses `runserver` en producción. Opciones:
- **Gunicorn** (Linux)
- **uWSGI**
- **Mod_WSGI** (Apache)
- **Waitress** (Windows)

Ejemplo con Gunicorn:
```bash
pip install gunicorn
gunicorn crm_project.wsgi:application --bind 0.0.0.0:8000
```

### 4. Configurar Servidor Web

Usa Nginx o Apache como proxy inverso frente a tu aplicación Django.

### 5. Configurar HTTPS

Usa certificados SSL (Let's Encrypt es gratuito).

## Compartir el Proyecto

### Opción 1: GitHub (Recomendado)

```powershell
# Inicializar repositorio
git init
git add .
git commit -m "Initial commit"

# Crear repositorio en GitHub y luego:
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

**Importante:** Crea un archivo `.gitignore`:
```
.venv/
*.pyc
__pycache__/
db.sqlite3
*.log
.env
```

### Opción 2: Archivo ZIP

1. Comprime toda la carpeta (excepto `.venv/`)
2. Comparte el archivo ZIP
3. La otra persona debe seguir los pasos de instalación

### Opción 3: Docker (Avanzado)

Crea un `Dockerfile` para empaquetar todo el entorno.

## Comandos Útiles de Django

```powershell
# Ejecutar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Abrir shell de Django
python manage.py shell

# Ver todas las rutas
python manage.py show_urls  # (requiere django-extensions)

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## Recursos Adicionales

📚 **Documentación:**
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Python: https://docs.python.org/

🎓 **Tutoriales:**
- Django Girls Tutorial: https://tutorial.djangogirls.org/
- Mozilla Django Tutorial: https://developer.mozilla.org/es/docs/Learn/Server-side/Django

💬 **Comunidad:**
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django

## Checklist de Instalación

Usa esta lista para verificar que todo está instalado:

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Superusuario creado (`python manage.py createsuperuser`)
- [ ] Servidor ejecutándose (`python manage.py runserver`)
- [ ] Página web accesible (http://localhost:8000/)
- [ ] Panel admin accesible (http://localhost:8000/admin/)
- [ ] API accesible (http://localhost:8000/api/)

---

**¡Listo!** Si seguiste todos los pasos, tu sistema CRM debería estar funcionando en la nueva computadora.

Para cualquier duda, revisa la documentación o los archivos de ayuda incluidos en el proyecto.
