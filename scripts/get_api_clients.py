import os, sys, django, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','crm_project.settings')
django.setup()
from django.test import Client as DjangoClient
from django.contrib.auth.models import User

username='api_test_user'
password='testpass123'
User.objects.filter(username=username).delete()
user=User.objects.create_user(username=username,password=password)

c=DjangoClient()
logged=c.login(username=username,password=password)
print('logged=', logged)
resp=c.get('/api/v1/clients/')
print('status=', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.content)
