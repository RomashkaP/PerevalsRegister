from fastapi import FastAPI, HTTPException
from config import WorkingWithDataClass
from models import *


# API
app = FastAPI(title='Pereval API', version='1.0')

@app.post('/submitData/')
def post_pereval(data: PerevalPost):
    db = WorkingWithDataClass()
    try:
        pereval_id = db.submit_pereval(
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






















