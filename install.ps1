# Script de Instalación y Configuración - Sistema CRM
# Para Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   INSTALACION SISTEMA CRM - DJANGO" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Python
Write-Host "[1/7] Verificando Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Python OK" -ForegroundColor Green
Write-Host ""

# 2. Crear entorno virtual
Write-Host "[2/7] Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "El entorno virtual ya existe. Saltando..." -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "Entorno virtual creado" -ForegroundColor Green
}
Write-Host ""

# 3. Activar entorno virtual
Write-Host "[3/7] Activando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# 4. Instalar dependencias
Write-Host "[4/7] Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "Dependencias instaladas" -ForegroundColor Green
Write-Host ""

# 5. Ejecutar migraciones
Write-Host "[5/7] Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "Migraciones completadas" -ForegroundColor Green
Write-Host ""

# 6. Crear superusuario
Write-Host "[6/7] Crear superusuario (HU 8)..." -ForegroundColor Yellow
Write-Host "Ingrese los datos del superusuario:" -ForegroundColor Cyan
python manage.py createsuperuser
Write-Host ""

# 7. Ejecutar tests
Write-Host "[7/7] Ejecutando tests (HU 40)..." -ForegroundColor Yellow
python manage.py test
Write-Host ""

# Finalizado
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar el servidor, ejecute:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "URLs disponibles:" -ForegroundColor Yellow
Write-Host "  - Aplicacion Web: http://localhost:8000/" -ForegroundColor White
Write-Host "  - Panel Admin:    http://localhost:8000/admin/" -ForegroundColor White
Write-Host "  - API REST:       http://localhost:8000/api/v1/" -ForegroundColor White
Write-Host ""
