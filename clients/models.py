from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """
    HU 11: Modelo de Cliente para el CRM
    """
    name = models.CharField(max_length=200, verbose_name='Nombre')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    address = models.TextField(blank=True, null=True, verbose_name='Dirección')
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name='Empresa')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_created')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
