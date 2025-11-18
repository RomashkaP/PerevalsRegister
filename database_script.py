import psycopg
import os
from dotenv import load_dotenv


load_dotenv()


class DatabaseClass:
    def __init__(self):
        pass

    def get_connect(self):
        return psycopg.connect(
            dbname=os.getenv('RENDER_DB_NAME'),
            user=os.getenv('RENDER_DB_LOGIN'),
            password=os.getenv('RENDER_DB_PASS'),
            host=os.getenv('RENDER_DB_HOST'),
            port=os.getenv('RENDER_DB_PORT')
        )

    def check_connect(self):
        try:
            with self.get_connect() as conn:
                with conn.cursor() as cur:
                    print('Успешное подключение к базе данных.')
        except Exception as e:
            print(f'Подключение не удалось - {e}.')

    def check_tables(self):
        with self.get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
                tables = cur.fetchall()
                for table in tables:
                    print(table)

    def delete_table(self):
        with self.get_connect() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "DROP TABLE IF EXISTS users"
                    )
                    print('Table did delete.')
                except Exception as e:
                    print(f'NOT delete - {e}')

    def create_tables_in_database(self):
        try:
            with self.get_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        -- Create table for users
                        CREATE TABLE "users" (
                            "id" SERIAL PRIMARY KEY,
                            "email" VARCHAR(256), -- Без NULL, т.к. ниже есть проверка.
                            "phone_num" VARCHAR(20), -- Телефон обязательно является строкой. 
                                -- Без NULL, т.к. ниже есть проверка.
                            "surname" VARCHAR(254) NOT NULL,
                            "name" VARCHAR(254) NOT NULL,
                            "patronymic" VARCHAR(254),
                            CHECK (email IS NOT NULL OR phone_num IS NOT NULL)	-- Проверка хотя бы одного способа связи.
                        );
                        
                        -- Create table for regions
                        CREATE TABLE "regions" (
                            "id" SERIAL PRIMARY KEY,
                            "title" VARCHAR(254) NOT NULL
                        );
                        
                        -- Create table for coords
                        CREATE TABLE "coords" (
                            "id" SERIAL PRIMARY KEY,
                            "latitude" NUMERIC(9, 6) NOT NULL,
                            "longitude" NUMERIC(10,6) NOT NULL,
                            "height" INTEGER NOT NULL
                        );
                        
                        -- Create table for areas
                        CREATE TABLE "pereval_areas" (
                            "id" SERIAL PRIMARY KEY,
                            "region" INTEGER REFERENCES regions (id) ON DELETE RESTRICT,
                            "title" VARCHAR(254) NOT NULL
                        );
                        
                        -- Create table for activities_types
                        CREATE TABLE "activities_types" (
                            "id" SERIAL PRIMARY KEY,
                            "title" VARCHAR(254) NOT NULL
                        );
                        
                        -- Created ENUM for season difficulty
                        CREATE TYPE season_difficulty AS ENUM ('1A', '1B', '2A', '2B', '3A', '3B'); -- Создание 
                            -- последовательного типа
                        -- для сохранения целостности данных.
                        
                        
                        -- Create table perevals
                        CREATE TABLE "perevals" (
                            "id" SERIAL PRIMARY KEY,
                            "pereval_area" INTEGER REFERENCES pereval_areas (id) ON DELETE RESTRICT,
                            "beauty_title" VARCHAR(254),
                            "title" VARCHAR(254) NOT NULL,
                            "other_titles" VARCHAR(254),
                            "connects" TEXT NOT NULL,
                            "add_time" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            "user" INTEGER REFERENCES users (id) ON DELETE SET NULL,
                            "coords" INTEGER REFERENCES coords (id) ON DELETE RESTRICT,
                            "winter" season_difficulty, -- Применение последовательного типа.
                            "spring" season_difficulty,
                            "summer" season_difficulty,
                            "autumn" season_difficulty,
                            "activity_type" INTEGER REFERENCES activities_types (id) ON DELETE RESTRICT,
                            "status" VARCHAR(20) NOT NULL DEFAULT 'new' -- Обязательное поле для модерации.
                        );
                        
                        -- Create table for images
                        CREATE TABLE "images" (
                            "id" SERIAL PRIMARY KEY,
                            "pereval" INTEGER REFERENCES perevals (id) ON DELETE CASCADE,
                            "image"  TEXT
                        );
                        """
                    )
                    print('Таблицы успешно созданы.')
        except Exception as e:
            print(f'EXCEPT - {e}')

    def insert_tables(self):
        try:
            with self.get_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO pereval_areas (region, title)
                        VALUES (3, 'Карасук');
                        """
                    )
                    print('Данные успешно добавлены.')
        except Exception as e:
            print(f'EXCEPT - {e}')

    def check_data_in_tables(self):
        try:
            with self.get_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT * FROM perevals;
                        """
                    )
                    items = cur.fetchall()
                    for item in items:
                        print(item)

        except Exception as e:
            print(f'EXCEPT - {e}')

base = DatabaseClass()

if __name__ == '__main__':
    base.check_data_in_tables()