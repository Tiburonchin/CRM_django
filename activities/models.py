from django.db import models
from django.contrib.auth.models import User
from clients.models import Client


class Activity(models.Model):
    """
    HU 21: Modelo de Actividad asociado a un Cliente
    """
    ACTIVITY_TYPES = [
        ('call', 'Llamada'),
        ('meeting', 'Reunión'),
        ('email', 'Correo'),
        ('task', 'Tarea'),
        ('note', 'Nota'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='activities', verbose_name='Cliente')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name='Tipo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    date = models.DateTimeField(verbose_name='Fecha')
    notes = models.TextField(verbose_name='Notas')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activities_created', verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    # Indica si ya se envió notificación a Slack para evitar duplicados
    slack_notified = models.BooleanField(default=False, verbose_name='Notificado en Slack')

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['-date']

    def __str__(self):
        return f'{self.get_type_display()} - {self.client.name} ({self.date.strftime("%Y-%m-%d")})'
