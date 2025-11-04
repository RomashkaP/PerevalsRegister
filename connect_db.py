import os
from dotenv import load_dotenv
import psycopg


load_dotenv()

try:
    with psycopg.connect(
        dbname=os.getenv('FSTR_DB_NAME'),
        user=os.getenv('FSTR_DB_LOGIN'),
        password=os.getenv('FSTR_DB_PASS'),
        host=os.getenv('FSTR_DB_HOST'),
        port=os.getenv('FSTR_DB_PORT')
    ) as conn:
        with conn.cursor() as cur:
            print('✅ Успешное подключение к PostgreSQL!')
            cur.execute('SELECT version();')
            version = cur.fetchone()
            print("Версия PostgreSQL:", version[0])
except Exception as e:
    print('Connect error - ', e)