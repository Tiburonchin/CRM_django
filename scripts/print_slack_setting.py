import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Print environment variable and decouple config
print('ENV SLACK_WEBHOOK_URL=', os.environ.get('SLACK_WEBHOOK_URL'))

try:
    from decouple import config
    print('python-decouple available')
    try:
        print("decouple config('SLACK_WEBHOOK_URL')=", config('SLACK_WEBHOOK_URL', default='(no-value)'))
    except Exception as e:
        print('decouple config error:', e)
except Exception as e:
    print('python-decouple not available:', e)

# Now import django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
import django
try:
    django.setup()
    from django.conf import settings
    print('Django settings SLACK_WEBHOOK_URL=', repr(getattr(settings, 'SLACK_WEBHOOK_URL', None)))
except Exception as e:
    print('django setup error:', e)
