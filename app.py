from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from config import WorkingWithDataClass


# Схема данных
class Coord(BaseModel):
    latitude: float
    longitude: float
    height: int

class Image(BaseModel):
    image: str

class Pereval(BaseModel):
    pereval_area: int
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connects: str
    user: int
    coords: Coord
    winter: Optional[str] = None
    spring: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    activity_type: int
    images: List[Image] = []

# API
app = FastAPI(title='Pereval API', version='1.0')

@app.post('/submitData/')
def submit_data(data: Pereval):
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





















