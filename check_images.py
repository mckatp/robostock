"""
Diagnostic: compares image paths stored in the DB against files on disk.
Run with: python check_images.py
"""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robostock.settings')
django.setup()

from inventory.models import Component
from django.conf import settings

components = Component.objects.all()
print(f"Total components: {components.count()}")
print("-" * 60)

missing = []
ok = []

for c in components:
    if c.image:
        full_path = os.path.join(settings.MEDIA_ROOT, str(c.image))
        url = c.image.url
        exists = os.path.isfile(full_path)
        if exists:
            ok.append(f"[OK]     {c.name} → {url}")
        else:
            missing.append(f"[MISS]   {c.name} → {url}  (not found: {full_path})")
    else:
        ok.append(f"[NO IMG] {c.name} — no image set")

for line in ok:
    print(line)
for line in missing:
    print(line)

print("-" * 60)
print(f"OK: {len(ok)}  |  Missing files: {len(missing)}")
