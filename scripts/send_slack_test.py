import os
import requests
import sys

def main():
    webhook = os.environ.get('SLACK_WEBHOOK_URL', '')
    if not webhook:
        print('SLACK_WEBHOOK_URL not set in environment; aborting test')
        sys.exit(2)
    try:
        r = requests.post(webhook, json={'text': 'Prueba local: notificación desde proyecto'}, timeout=10)
        print('status_code=', r.status_code)
        print('text=', r.text)
    except Exception as e:
        print('error=', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
