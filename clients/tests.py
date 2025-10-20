from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer


class ClientModelTestCase(TestCase):
    """
    HU 29: Tests unitarios para el modelo Client
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            name='Test Client',
            email='client@example.com',
            phone='123456789',
            created_by=self.user
        )

    def test_client_creation(self):
        """Test de creación de cliente"""
        self.assertEqual(self.client_obj.name, 'Test Client')
        self.assertEqual(self.client_obj.email, 'client@example.com')

    def test_client_str(self):
        """Test del método __str__"""
        self.assertEqual(str(self.client_obj), 'Test Client')


class ClientSerializerTestCase(TestCase):
    """
    HU 29: Tests para el serializer de Cliente
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client_data = {
            'name': 'Test Client',
            'email': 'client@example.com',
            'phone': '123456789',
            'address': 'Test Address',
        }

    def test_serializer_valid_data(self):
        """Test con datos válidos"""
        serializer = ClientSerializer(data=self.client_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_email(self):
        """Test con email inválido"""
        invalid_data = self.client_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = ClientSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class ClientAPITestCase(APITestCase):
    """
    HU 29: Tests de integración para la API de clientes
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_create_client(self):
        """Test de creación de cliente vía API"""
        data = {
            'name': 'API Client',
            'email': 'api@example.com',
            'phone': '987654321',
        }
        response = self.client.post('/api/clients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_clients(self):
        """Test de listado de clientes"""
        response = self.client.get('/api/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
