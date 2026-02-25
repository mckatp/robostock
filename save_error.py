import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robostock.settings')
django.setup()

from django.test import Client
c = Client()
response = c.get('/')
with open('/tmp/error2.html', 'w') as f:
    f.write(response.content.decode('utf-8'))
print("Saved to /tmp/error2.html")
