import os
import django
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from activities.models import Activity

try:
    a = Activity.objects.select_related('client', 'created_by').order_by('-created_at').first()
    if not a:
        print('No activity found')
    else:
        print('id=', a.id)
        print('type=', a.type)
        print('notes=', a.notes)
        print('client=', a.client.name if a.client else None)
        print('date=', a.date)
        print('created_by=', a.created_by.username if a.created_by else None)
except Exception as e:
    print('error=', e)
