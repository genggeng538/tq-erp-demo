from django.db import connection

def ensure_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS erp_inventoryitem (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        );
        """)
