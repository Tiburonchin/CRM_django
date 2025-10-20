from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
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
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
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
