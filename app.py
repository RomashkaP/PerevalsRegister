from fastapi import FastAPI, HTTPException
from config import WorkingWithDataClass
from models import *


# API
app = FastAPI(title='Pereval API', version='1.0')

@app.post('/submitData/')
def post_pereval(data: PerevalPost):
    db = WorkingWithDataClass()
    try:
        pereval_id = db.post_pereval(
            pereval_area_id=data.pereval_area,
            user_id=data.user,
            coords=data.coords.dict(),
            pereval_data=data.dict(exclude={'pereval_area', 'user', 'coords', 'activity_type'}),
            activity_type_id=data.activity_type,
            images=[img.dict() for img in data.images]
        )
        return {'status': 'success', 'id': pereval_id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/submitData/{pereval_id}')
def get_pereval(pereval_id: int):
    db = WorkingWithDataClass()
    data = db.get_pereval(pereval_id)
    if not data:
        raise HTTPException(status_code=404, detail='Перевал не найден.')
    return PerevalGet(**data)

@app.patch('/submitData/{pereval_id}')
def patch_pereval(pereval_id: int, data: PerevalPost):
    db = WorkingWithDataClass()
    try:
        result = db.patch_pereval(
            pereval_id=pereval_id,
            coords=data.coords.dict(),
            pereval_data=data.dict(exclude={'coords', 'user', 'images'}),
            images=[img.dict() for img in data.images]
        )
        if result:
            return {'state': 1, 'message': 'Запись успешно отредактирована.'}
        else:
            {"state": 0, "message": "Не удалось обновить запись (статус не 'new' или запись не найдена)"}
    except Exception as e:
        return {'state': 0, 'message': str(e)}




















