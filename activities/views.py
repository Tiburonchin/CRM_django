from django.shortcuts import render
import logging
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Activity
from .serializers import ActivitySerializer, ActivityDetailSerializer
from .permissions import IsOwnerOrReadOnly


class ActivityViewSet(viewsets.ModelViewSet):
    """
    HU 22-23: ViewSet para operaciones CRUD de Activity
    HU 24: Filtrado por cliente
    HU 27: Búsqueda por palabras clave
    HU 28: Paginación implementada
    HU 30: Permisos personalizados
    HU 31: Endpoint de estadísticas
    HU 32: Ordenamiento
    """
    queryset = Activity.objects.select_related('client', 'created_by').all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'type', 'status', 'created_by']
    search_fields = ['notes', 'client__name', 'type']
    ordering_fields = ['date', 'created_at', 'type']
    ordering = ['-date']

    def get_serializer_class(self):
        """
        Usar serializer detallado para retrieve
        """
        if self.action == 'retrieve':
            return ActivityDetailSerializer
        return ActivitySerializer

    def perform_create(self, serializer):
        """
        HU 22: Asignar el usuario que creó la actividad
        """
        # Guardar la actividad y asignar el creador
        activity = serializer.save(created_by=self.request.user)

        # --- INICIO DE MEJORA (CRITERIO 4): Notificar a Slack si es una reunión ---
        logger = logging.getLogger(__name__)
        try:
            # Comprobar que la actividad es de tipo 'meeting'
            is_meeting = getattr(activity, 'type', '').lower() == 'meeting'
            has_webhook = bool(getattr(settings, 'SLACK_WEBHOOK_URL', ''))

            # Log values useful for debugging Slack notifications
            logger.info('perform_create: is_meeting=%s has_webhook=%s slack_notified=%s SLACK_WEBHOOK_URL=%s',
                        is_meeting, has_webhook, getattr(activity, 'slack_notified', False),
                        ('<hidden>' if has_webhook else '<empty>'))

            if is_meeting and has_webhook and not getattr(activity, 'slack_notified', False):
                # Construir mensaje detallado
                try:
                    date_str = activity.date.strftime('%d/%m/%Y %H:%M') if getattr(activity, 'date', None) else ''
                except Exception:
                    date_str = str(getattr(activity, 'date', ''))

                client_name = getattr(activity.client, 'name', '') if getattr(activity, 'client', None) else ''
                notes = getattr(activity, 'notes', '')

                message = (
                    f"¡Nueva Reunión Agendada! 📅\n"
                    f"Cliente: *{client_name}*\n"
                    f"Notas: {notes}\n"
                    f"Fecha: {date_str}\n"
                    f"Agendada por: {self.request.user.username}"
                )

                # Enviar la petición a Slack (timeout corto para no bloquear)
                try:
                    # Use a DB transaction and select_for_update to avoid duplicate sends
                    resp = None
                    reserved = False
                    # Reserve the notification slot under lock to avoid race conditions
                    with transaction.atomic():
                        locked = Activity.objects.select_for_update().get(pk=activity.pk)
                        if getattr(locked, 'slack_notified', False):
                            logger.info('Slack notification skipped: activity id=%s already slack_notified', activity.pk)
                        else:
                            # mark as reserved so other concurrent requests won't send
                            locked.slack_notified = True
                            locked.save(update_fields=['slack_notified'])
                            reserved = True

                    if reserved:
                        # perform the HTTP request outside the DB lock
                        resp = requests.post(
                            settings.SLACK_WEBHOOK_URL,
                            json={'text': message},
                            timeout=10,
                        )
                    # Log response for easier debugging (status and body)
                    if resp is not None:
                        try:
                            logger.info('Slack webhook response status=%s body=%s', resp.status_code, resp.text)
                        except Exception:
                            logger.info('Slack webhook response received (unable to read body)')

                        # Si la petición fue exitosa, mantener slack_notified=True; si falló, revertir
                        try:
                            if 200 <= resp.status_code < 300:
                                logger.info('Slack notification confirmed for activity id=%s', activity.pk)
                            else:
                                # Non-2xx response — record as error and revert reservation
                                logger.error('Slack webhook returned non-2xx: status=%s body=%s', resp.status_code, resp.text)
                                try:
                                    with transaction.atomic():
                                        a = Activity.objects.select_for_update().get(pk=activity.pk)
                                        a.slack_notified = False
                                        a.save(update_fields=['slack_notified'])
                                except Exception:
                                    logger.exception('Error reverting slack_notified after non-2xx response')
                        except Exception as e:
                            logger.exception('Error procesando respuesta de Slack: %s', e)
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error al enviar notificación a Slack: {e}")
            elif is_meeting and not has_webhook:
                # Registrar información útil para depuración cuando falta webhook
                logger.info('SLACK_WEBHOOK_URL no configurado; se omite notificación a Slack para la actividad id=%s', getattr(activity, 'id', 'n/a'))
        except Exception as e:
            # No bloquear el flujo normal de creación de actividades por errores de notificación
            logging.getLogger(__name__).exception(f"Error en notificación Slack: {e}")
        # --- FIN DE MEJORA ---

    @action(detail=False, methods=['get'])
    def statistics(self, request, *args, **kwargs):
        """
        HU 31: Endpoint para obtener estadísticas de actividades
        """
        total = Activity.objects.count()
        pending = Activity.objects.filter(status='pending').count()
        completed = Activity.objects.filter(status='completed').count()
        cancelled = Activity.objects.filter(status='cancelled').count()

        # Estadísticas por tipo
        by_type = Activity.objects.values('type').annotate(count=Count('id'))

        # Actividades recientes (últimas 10)
        recent = Activity.objects.select_related('client')[:10]
        recent_data = ActivitySerializer(recent, many=True).data

        stats = {
            'total': total,
            'by_status': {
                'pending': pending,
                'completed': completed,
                'cancelled': cancelled,
            },
            'by_type': {item['type']: item['count'] for item in by_type},
            'recent_activities': recent_data,
        }

        return Response(stats)


# Vistas Web (Frontend) para Actividades

@login_required
def activity_list_view(request):
    """
    HU 26: Vista web para listar actividades
    """
    activities = Activity.objects.select_related('client', 'created_by').all()
    context = {
        'activities': activities,
    }
    return render(request, 'activities/activity_list.html', context)
