import os
import sys
import django

# Ensure project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

django.setup()

from django.test import Client as DjangoClient
from django.contrib.auth.models import User
from clients.models import Client as ClientModel
import json

# Create user and login via test client
username = 'slack_test_user'
password = 'testpass123'

User.objects.filter(username=username).delete()
user, _ = User.objects.get_or_create(username=username)
user.set_password(password)
user.save()

# Create or get a client entry
client_obj, _ = ClientModel.objects.get_or_create(email='slack@test.local', defaults={
    'name': 'Test Slack Client',
    'phone': '000',
    'created_by': user,
})

c = DjangoClient()
logged_in = c.login(username=username, password=password)
print('logged_in=', logged_in)

payload = {
    'client': client_obj.id,
    'type': 'meeting',
    'status': 'pending',
    'date': '2025-11-20T15:00:00-05:00',
    'notes': 'Prueba desde script que crea actividad y debería notificar Slack'
}

# Test client sends requests with host 'testserver' by default which may be rejected
# by ALLOWED_HOSTS. Set HTTP_HOST to a permitted host (localhost) to avoid DisallowedHost.
resp = c.post('/api/v1/activities/', data=json.dumps(payload), content_type='application/json', HTTP_HOST='localhost')
print('POST status_code=', resp.status_code)
try:
    print('response:', resp.json())
except Exception:
    print('response text:', resp.content)

# Print latest activity to confirm
from activities.models import Activity
a = Activity.objects.select_related('client', 'created_by').order_by('-created_at').first()
print('latest activity id=', a.id, 'type=', a.type, 'created_by=', a.created_by.username)
