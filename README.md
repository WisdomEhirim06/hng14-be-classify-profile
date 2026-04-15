# Profile Classification API

This is a Stage 1 project of the HNG internship (Backend Track). It is a FastAPI REST API that classifies names using gender, age, and nationality data fetched from external APIs: [Genderize](https://genderize.io), [Agify](https://agify.io), and [Nationalize](https://nationalize.io). Profiles are persisted in a PostgreSQL database (Supabase) with UUID v7 identifiers.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/profiles` | Create a profile for a given name |
| `GET` | `/api/profiles` | List all profiles (filterable by gender, country_id, age_group) |
| `GET` | `/api/profiles/{id}` | Get a single profile by ID |
| `DELETE` | `/api/profiles/{id}` | Delete a profile by ID |

### POST `/api/profiles`
**Request body:** `{ "name": "James" }`
**Response (201):**
```json
{
  "id": "019d9906-...",
  "name": "James",
  "gender": "male",
  "gender_probability": 0.98,
  "sample_size": 142312,
  "age": 56,
  "age_group": "senior",
  "country_id": "AU",
  "country_probability": 0.08,
  "created_at": "2026-04-15T09:00:00.000000Z"
}
```
- Returns **409 Conflict** if a profile with that name already exists.
- Returns **502 Bad Gateway** if external classification APIs are unavailable.

---

## Running Locally

### 1. Setup Environment
```bash
git clone <your-repo-url>
cd classification-logic
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://your_user:your_password@your_host:5432/your_db
```

### 3. Start the Server
```bash
python -m uvicorn main:app --reload
```
Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Deploying to Vercel

The API is configured to run as a serverless function using the `@vercel/python` runtime.

1. **Push to GitHub**: Ensure `vercel.json` and `api/index.py` are committed.
2. **Import Project**: In Vercel, import your repository.
3. **Set Environment Variables**: In **Settings > Environment Variables**, add:
   - `DATABASE_URL`: Your Supabase/PostgreSQL connection string.
4. **Deploy**: Vercel will build the project using `requirements.txt` and route requests through `api/index.py`.

---

## Project Structure
```
classification-logic/
├── api/
│   └── index.py       # Vercel serverless entry point
├── main.py            # FastAPI application logic
├── database.py        # SQLAlchemy & Database configuration
├── models.py          # SQLAlchemy ORM models
├── schemas.py         # Pydantic validation schemas
├── external_apis.py   # Async external API integration
├── vercel.json        # Vercel deployment config
├── requirements.txt   # Pinned dependencies
└── .env               # Local environment variables (ignored by git)
```

---

## Tech Stack
- **FastAPI** — Web Framework
- **SQLAlchemy + PostgreSQL (Supabase)** — Database & ORM
- **HTTPX** — Async HTTP requests
- **UUID6** — UUID v7 generation
- **Vercel** — Serverless Deployment
