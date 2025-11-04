import os
from dotenv import load_dotenv
import psycopg


load_dotenv()

try:
    with psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    ) as conn:
        with conn.cursor() as cur:
            print('✅ Успешное подключение к PostgreSQL!')
            cur.execute('SELECT version();')
            version = cur.fetchone()
            print("Версия PostgreSQL:", version[0])
except Exception as e:
    print('Connect error - ', e)