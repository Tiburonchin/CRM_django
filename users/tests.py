from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTestCase(TestCase):
    """
    HU 29: Tests unitarios para el modelo UserProfile
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test que el perfil se crea automáticamente"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_user_profile_str(self):
        """Test del método __str__"""
        expected = f'Perfil de {self.user.username}'
        self.assertEqual(str(self.user.profile), expected)

    def test_user_profile_update(self):
        """Test de actualización del perfil"""
        self.user.profile.phone = '123456789'
        self.user.profile.address = 'Test Address'
        self.user.profile.save()

        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone, '123456789')
        self.assertEqual(profile.address, 'Test Address')
