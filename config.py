import os
from dotenv import load_dotenv
import psycopg


load_dotenv()

class WorkingWithDataClass():
    def __init__(self):
        pass

    def get_connection(self): # Метод для создания соединения.
        return psycopg.connect(
            dbname=os.getenv('FSTR_DB_NAME'),
            user=os.getenv('FSTR_DB_LOGIN'),
            password=os.getenv('FSTR_DB_PASS'),
            host=os.getenv('FSTR_DB_HOST'),
            port=os.getenv('FSTR_DB_PORT')
        )
    # ------- Закомментировал эту часть, т.к. в FAQ написано, что авторизация пользователя не нужна.
    #-------- Удалять пока не буду, вдруго понадобиться в следующих спринтах.
    # def create_user( # Метод для создания пользователя.
    #         self,
    #         surname: str,
    #         name: str,
    #         patronymic: str = None,
    #         email: str = None,
    #         phone_num: str = None,
    # ) -> int: # Требуется хотя бы email или phone_num. Возвращает id нового пользователя.
    #     if not email and not phone_num:
    #         raise ValueError('Должен быть указан email или номер телефона.')
    #     with self.get_connection() as conn:
    #         with conn.cursor() as cur:
    #             cur.execute(
    #                 "INSERT INTO users (email, phone_num, surname, name, patronymic)"
    #                 "VALUES (%s, %s, %s, %s, %s)"
    #                 "RETURNING id;",
    #                 (email, phone_num, surname, name, patronymic)
    #             )
    #             user_id = cur.fetchone()[0]
    #             return user_id

    def submit_pereval( # Метод  для создания перевала.
            self,
            pereval_area_id: int,
            user_id: int,
            coords: dict,
            pereval_data: dict,
            activity_type_id: int,
            images: list = None
    ) -> int: # Требует существующий user_id. Возвращает id созданного перевала.
        if images is None:
            images = []
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Создаем координаты.
                cur.execute(
                    """
                    INSERT INTO coords (latitude, longitude, height)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        coords['latitude'],
                        coords['longitude'],
                        coords['height']
                    )
                )
                coords_id = cur.fetchone()[0]
                # Создаем перевал.
                cur.execute(
                    """
                    INSERT INTO perevals(
                        pereval_area, beauty_title, title, other_titles, connects,
                        "user", coords, winter, spring, summer, autumn,
                        activity_type, status
                    ) VALUES (
                        %(pereval_area_id)s,
                        %(beauty_title)s,
                        %(title)s,
                        %(other_titles)s,
                        %(connects)s,
                        %(user_id)s,
                        %(coords_id)s,
                        %(winter)s,
                        %(spring)s,
                        %(summer)s,
                        %(autumn)s,
                        %(activity_type_id)s,
                        'new'
                    )
                    RETURNING id;
                    """,
                    {
                        'pereval_area_id': pereval_area_id,
                        'beauty_title': pereval_data.get('beauty_title'),
                        'title': pereval_data.get('title'),
                        'other_titles': pereval_data.get('other_titles'),
                        'connects': pereval_data.get('connects'),
                        'user_id': user_id,
                        'coords_id': coords_id,
                        'winter': pereval_data.get('winter'),
                        'spring': pereval_data.get('spring'),
                        'summer': pereval_data.get('summer'),
                        'autumn': pereval_data.get('autumn'),
                        'activity_type_id': activity_type_id,
                    }
                )
                pereval_id = cur.fetchone()[0]
                # Сохраняем изображения.
                for img in images:
                    cur.execute(
                        """
                        INSERT INTO images (pereval, image)
                        VALUES (%s, %s);
                        """,
                        (pereval_id, img)
                    )
                return pereval_id



















