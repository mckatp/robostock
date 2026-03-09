"""
One-shot fix: removes the orphaned `component_type` column left by
migration 0009 which was never reversed after the git rollback.
Run with: python fix_db.py
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robostock.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # 1. Drop the orphaned column
    cursor.execute("""
        ALTER TABLE inventory_component
        DROP COLUMN IF EXISTS component_type;
    """)
    print("✓ Dropped column: component_type")

    # 2. Remove the stale migration record so Django doesn't think 0009 is applied
    cursor.execute("""
        DELETE FROM django_migrations
        WHERE app = 'inventory' AND name = '0009_component_component_type';
    """)
    rows = cursor.rowcount
    print(f"✓ Removed {rows} stale migration record(s) for 0009")

print("\nAll done! Restart Gunicorn now.")
