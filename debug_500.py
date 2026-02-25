import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robostock.settings')
django.setup()

from django.test import Client
import traceback

c = Client()
try:
    response = c.get('/')
    if response.status_code >= 500:
        print(f"Status: {response.status_code}")
        # print first 2000 chars of HTML which should contain the traceback in DEBUG=True
        print(response.content.decode('utf-8')[:2000])
    else:
        print(f"Success: {response.status_code}")
except Exception as e:
    traceback.print_exc()
