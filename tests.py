from config import WorkingWithDataClass
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


test = WorkingWithDataClass()

# result = test.create_user('Петров', 'Иннокентий',None ,'vladlenych@gmail.com')
# print(f'Пользователь успешно создан. Ваш id - {result}')

r = test.submit_pereval(
    1,
    1,
    {'latitude': 50.909958, 'longitude': 88.217849, 'height':  515},
    {
        'beaty_title': '',
        'title': 'Кату-Ярык',
        'other_titles': '',
        'connects': 'Долину реки Чулышман с внешним миром.',
        'winter': '1B',
        'spring': '1B',
        'summer': '2B',
        'autumn': '1A'
    },
    1
)
print(f'All works, pereval ID - {r}')