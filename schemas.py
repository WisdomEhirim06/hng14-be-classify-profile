from pydantic import BaseModel
from typing import Optional
import datetime

class ProfileCreate(BaseModel):
    name: str

class ProfileResponse(BaseModel):
    id: str
    name: str
    gender: Optional[str] = None
    gender_probability: Optional[float] = None
    sample_size: Optional[int] = None
    age: Optional[int] = None
    age_group: Optional[str] = None
    country_id: Optional[str] = None
    country_probability: Optional[float] = None
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        from_attributes = True

class ProfileListResponse(BaseModel):
    id: str
    name: str
    gender: Optional[str] = None
    age_group: Optional[str] = None
    country_id: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
