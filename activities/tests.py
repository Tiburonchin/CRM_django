from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from clients.models import Client
from .models import Activity
from .serializers import ActivitySerializer


class ActivityModelTestCase(TestCase):
    """
    HU 29: Tests unitarios para el modelo Activity
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client.objects.create(
            name='Test Client',
            email='client@example.com',
            phone='123456789',
            created_by=self.user
        )
        self.activity = Activity.objects.create(
            client=self.client,
            type='call',
            status='pending',
            date=timezone.now(),
            notes='Test notes',
            created_by=self.user
        )

    def test_activity_creation(self):
        """Test de creación de actividad"""
        self.assertEqual(self.activity.type, 'call')
        self.assertEqual(self.activity.status, 'pending')
        self.assertEqual(self.activity.client, self.client)

    def test_activity_str(self):
        """Test del método __str__"""
        self.assertIn('Llamada', str(self.activity))
        self.assertIn('Test Client', str(self.activity))


class ActivitySerializerTestCase(TestCase):
    """
    HU 29: Tests para el serializer de Activity
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client.objects.create(
            name='Test Client',
            email='client@example.com',
            phone='123456789',
            created_by=self.user
        )
        self.activity_data = {
            'client': self.client.id,
            'type': 'meeting',
            'status': 'pending',
            'date': timezone.now().isoformat(),
            'notes': 'Test meeting notes',
        }

    def test_serializer_valid_data(self):
        """Test con datos válidos"""
        serializer = ActivitySerializer(data=self.activity_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_empty_notes(self):
        """Test con notas vacías (debe fallar)"""
        invalid_data = self.activity_data.copy()
        invalid_data['notes'] = ''
        serializer = ActivitySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class ActivityAPITestCase(APITestCase):
    """
    HU 29: Tests de integración para la API de actividades
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.client_obj = Client.objects.create(
            name='Test Client',
            email='client@example.com',
            phone='123456789',
            created_by=self.user
        )

    def test_statistics_endpoint(self):
        """Test del endpoint de estadísticas"""
        response = self.client.get('/api/activities/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('by_status', response.data)
