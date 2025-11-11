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

    def get_pereval(self, pereval_id: int): # -- Возвращает полную информацию о перевале.
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        p.id, p.beauty_title, p.title, p.other_titles, p.connects, p.add_time, p.status,
                        p.winter, p.spring, p.summer, p.autumn, 
                        p_ar.id, p_ar.title, 
                        r.id, r.title,
                        u.id, u.email, u.phone_num, u.surname, u.name, u.patronymic,
                        c.id, c.latitude, c.longitude, c.height,
                        a_t.id, a_t.title    
                    FROM perevals p
                    JOIN pereval_areas p_ar ON p.pereval_area = p_ar.id
                    JOIN regions r ON p_ar.region = r.id
                    JOIN users u ON p.user = u.id
                    JOIN coords c ON p.coords = c.id
                    JOIN activity_types a_t ON p.activity_type = a_t.id
                    WHERE p.id = %s;
                    """,
                    (pereval_id)
                )
                row = cur.fetchone()
                if not row:
                    return None

                (
                    p_id, p_beauty_title, p_title, p_other_titles, p_connects, p_add_time, p_status,
                    p_winter, p_spring, p_summer, p_autumn,
                    p_ar_id, p_ar_title,
                    r_id, r_title,
                    u_id, u_email, u_phone_num, u_surname, u_name, u_patronymic,
                    c_id, c_latitude, c_longitude, c_height,
                    a_t_id, a_t_title
                ) = row

                cur.execute(
                    "SELECT id, image FROM images WHERE pereval = %s",
                    (pereval_id,)
                )
                images = [{'id' : img[0], 'image': img[1]} for img in cur.fetchall()]

                return {
                    'id': p_id,
                    'pereval_area': {
                        'id': p_ar_id,
                        'region': {
                            'id': r_id,
                            'title': r_title
                        },
                        'title': p_ar_title
                    },
                    'beauty_title': p_beauty_title,
                    'title': p_title,
                    'other_titles': p_other_titles,
                    'connects': p_connects,
                    'add_time': p_add_time.isoformat() if p_add_time else None,
                    'user': {
                        'id': u_id,
                        'email': u_email,
                        'phone_num': u_phone_num,
                        'surname': u_surname,
                        'name': u_name,
                        'patronymic': u_patronymic
                    },
                    'coords': {
                        'id': c_id,
                        'latitude': c_latitude,
                        'longitude': c_longitude,
                        'height': c_height
                    },
                    'winter': p_winter,
                    'spring': p_spring,
                    'summer': p_summer,
                    'autumn': p_autumn,
                    'activity_type': {
                        'id': a_t_id,
                        'title': a_t_title
                    },
                    'status': p_status,
                    'images': images
                }















