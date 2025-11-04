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
            cur.execute("INSERT INTO pereval_areas (region, title) VALUES ( %s, %s) RETURNING id;",
                        (1, "Кату-Ярык")
            )
            area_id = cur.fetchone()
            print("ID созданного района:", area_id[0])
except Exception as e:
    print('Connect error - ', e)