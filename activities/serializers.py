from rest_framework import serializers
from .models import Activity
from clients.serializers import ClientSerializer


class ActivitySerializer(serializers.ModelSerializer):
    """
    HU 22: Serializer para el modelo Activity
    """
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    # Aceptar múltiples formatos de entrada para la fecha/hora
    date = serializers.DateTimeField(
        input_formats=[
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M%z',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M:%S.%f%z',
            '%Y-%m-%d %H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
        ]
    )

    def validate(self, data):
        """
        Validaciones personalizadas
        """
        if 'notes' in data and not data['notes']:
            raise serializers.ValidationError({'notes': 'Las notas son obligatorias.'})
        return data


class ActivityDetailSerializer(ActivitySerializer):
    """
    Serializer detallado que incluye información completa del cliente
    HU 25: Muestra información del cliente en la actividad
    """
    client = ClientSerializer(read_only=True)

    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields
