from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    HU 13-16: ViewSet para operaciones CRUD de Cliente
    HU 17: Solo usuarios autenticados pueden acceder
    HU 32: Implementa ordenamiento
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'email', 'company']
    search_fields = ['name', 'email', 'phone', 'company']
    ordering_fields = ['created_at', 'name', 'email']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        HU 13: Crear cliente y asignar el usuario que lo creó
        """
        serializer.save(created_by=self.request.user)


# Vistas Web (Frontend) para Clientes

@login_required
def client_list_view(request):
    """
    HU 19: Vista web para listar clientes
    """
    clients = Client.objects.all().order_by('-created_at')
    context = {
        'clients': clients,
    }
    return render(request, 'clients/client_list.html', context)


@login_required
def client_detail_view(request, pk):
    """
    HU 20: Vista web para detalle de cliente
    """
    client = get_object_or_404(Client, pk=pk)
    context = {
        'client': client,
    }
    return render(request, 'clients/client_detail.html', context)
