from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime

import models
import schemas
from database import engine, get_db
from external_apis import fetch_all_demographics

try:
    from uuid6 import uuid7
    def generate_id():
        return str(uuid7())
except ImportError:
    import uuid
    def generate_id():
        return str(uuid.uuid4())

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Profile Classification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/profiles", response_model=schemas.ProfileResponse, status_code=201)
async def create_profile(payload: schemas.ProfileCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    # Idempotency: check existing profile by lowercase name
    existing = db.query(models.Profile).filter(
        models.Profile.name.ilike(name)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Profile already exists")

    demographics = await fetch_all_demographics(name)

    profile = models.Profile(
        id=generate_id(),
        name=name,
        gender=demographics["gender"],
        gender_probability=demographics["gender_probability"],
        sample_size=demographics["sample_size"],
        age=demographics["age"],
        age_group=demographics["age_group"],
        country_id=demographics["country_id"],
        country_probability=demographics["country_probability"],
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@app.get("/api/profiles/{profile_id}", response_model=schemas.ProfileResponse)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.get("/api/profiles", response_model=List[schemas.ProfileListResponse])
def list_profiles(
    gender: Optional[str] = Query(None),
    country_id: Optional[str] = Query(None),
    age_group: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Profile)
    if gender:
        query = query.filter(models.Profile.gender.ilike(gender))
    if country_id:
        query = query.filter(models.Profile.country_id.ilike(country_id))
    if age_group:
        query = query.filter(models.Profile.age_group.ilike(age_group))
    return query.all()


@app.delete("/api/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(profile)
    db.commit()
    return None
