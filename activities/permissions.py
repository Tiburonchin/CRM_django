from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    HU 30: Permiso personalizado para que solo el propietario pueda editar/eliminar
    """
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura permitidos para cualquier request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permisos de escritura solo para el propietario
        return obj.created_by == request.user
