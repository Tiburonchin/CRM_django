# Script para Ejecutar el Servidor - Sistema CRM
# Para Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "     INICIANDO SERVIDOR CRM" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Servidor iniciando en:" -ForegroundColor Green
Write-Host "  http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Accesos disponibles:" -ForegroundColor Yellow
Write-Host "  - Pagina Principal:  http://localhost:8000/" -ForegroundColor White
Write-Host "  - Panel Admin:       http://localhost:8000/admin/" -ForegroundColor White
Write-Host "  - API REST:          http://localhost:8000/api/v1/" -ForegroundColor White
Write-Host "  - Clientes:          http://localhost:8000/clients/" -ForegroundColor White
Write-Host "  - Actividades:       http://localhost:8000/activities/" -ForegroundColor White
Write-Host ""
Write-Host "Presione Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar servidor
python manage.py runserver
