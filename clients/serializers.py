from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    HU 12: Serializer para el modelo Cliente
    Transforma objetos Python a JSON y viceversa
    """
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate_email(self, value):
        """
        HU 18: Validación personalizada para el email
        """
        if self.instance:
            # Si estamos actualizando, excluir el cliente actual de la validación
            if Client.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError('Ya existe un cliente con este correo electrónico.')
        else:
            # Si estamos creando, verificar que no exista
            if Client.objects.filter(email=value).exists():
                raise serializers.ValidationError('Ya existe un cliente con este correo electrónico.')
        return value

    def validate_phone(self, value):
        """
        Validación básica para el teléfono
        """
        if not value:
            raise serializers.ValidationError('El teléfono es obligatorio.')
        return value
