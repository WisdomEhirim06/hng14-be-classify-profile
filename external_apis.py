import httpx
from fastapi import HTTPException
import asyncio

async def fetch_api_data(url: str):
    """Fetch data from a URL. Returns None on any error instead of raising."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def determine_age_group(age) -> str:
    if age is None:
        return None
    age = int(age)
    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    else:
        return "senior"

async def fetch_all_demographics(name: str):
    urls = [
        f"https://api.genderize.io?name={name}",
        f"https://api.agify.io?name={name}",
        f"https://api.nationalize.io?name={name}",
    ]
    results = await asyncio.gather(*[fetch_api_data(url) for url in urls])

    gender_data, agify_data, nationalize_data = results

    # Specific 502 requirements
    if gender_data is None or gender_data.get("gender") is None or gender_data.get("count") == 0:
        raise HTTPException(status_code=502, detail="Genderize returned an invalid response")
    
    if agify_data is None or agify_data.get("age") is None:
        raise HTTPException(status_code=502, detail="Agify returned an invalid response")
    
    if nationalize_data is None or not nationalize_data.get("country"):
        raise HTTPException(status_code=502, detail="Nationalize returned an invalid response")

    gender = gender_data.get("gender")
    gender_probability = gender_data.get("probability")

    age = agify_data.get("age")
    age_group = determine_age_group(age)

    country_id = None
    country_probability = None
    countries = nationalize_data.get("country") or []
    if countries:
        top_country = countries[0]
        country_id = top_country.get("country_id")
        country_probability = top_country.get("probability")

    sample_size = gender_data.get("count") or 0

    return {
        "gender": gender,
        "gender_probability": gender_probability,
        "sample_size": sample_size,
        "age": age,
        "age_group": age_group,
        "country_id": country_id,
        "country_probability": country_probability,
    }
