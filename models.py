from typing import List, Optional
from pydantic import BaseModel


# Схема данных
class Coord(BaseModel):
    id: int
    latitude: float
    longitude: float
    height: int

class Image(BaseModel):
    id: int
    image: str

class PerevalPost(BaseModel):
    id: int
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

class Region(BaseModel):
    id: int
    title: str

class PerevalArea(BaseModel):
    id: int
    region: Region
    title: str

class User(BaseModel):
    id: int
    email: Optional[str]
    phone_num: Optional[str]
    surname: str
    name: str
    patronymic: Optional[str]

class ActivityType(BaseModel):
    id: int
    title: str

class PerevalGet(BaseModel):
    id: int
    pereval_area: PerevalArea
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connects: str
    add_time: str
    user: User
    coords: Coord
    winter: Optional[str] = None
    spring: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    activity_type: ActivityType
    images: List[Image] = []
    status: str












