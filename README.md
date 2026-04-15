# Profile Classification API


This is Stage 1 project of the HNG internship in backend track. A FastAPI REST API that classifies names using gender, age, and nationality data from external APIs ([Genderize](https://genderize.io), [Agify](https://agify.io), [Nationalize](https://nationalize.io)). Profiles are persisted in a SQLite database with UUID v7 identifiers.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/profiles` | Create a profile for a given name |
| `GET` | `/api/profiles` | List all profiles (filterable) |
| `GET` | `/api/profiles/{id}` | Get a single profile by ID |
| `DELETE` | `/api/profiles/{id}` | Delete a profile by ID |

### POST `/api/profiles`

**Request body:**
```json
{ "name": "James" }
```

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
  "created_at": "2026-04-15T09:00:00.000000"
}
```

- Returns **409** if a profile for that name already exists.
- Returns **502** if all three external classification APIs are unreachable.

### GET `/api/profiles`

Optional query filters: `gender`, `country_id`, `age_group`

```
GET /api/profiles?gender=male&age_group=adult
```

### GET `/api/profiles/{id}`
Returns **404** if not found.

### DELETE `/api/profiles/{id}`
Returns **204** on success, **404** if not found.

---

## Running Locally

### 1. Clone & create virtual environment

```bash
git clone <your-repo-url>
cd classification-logic
python -m venv venv
```

### 2. Install dependencies

```bash
# Windows
venv\Scripts\pip install -r requirements.txt

# macOS/Linux
venv/bin/pip install -r requirements.txt
```

### 3. Start the server

```bash
# Windows
venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000

# macOS/Linux
venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## Deploying to pxxl.app

I used pxxl.app for this project. To deploy here's how you'dd do yours. [pxxl.app](https://pxxl.app) is a zero-config Git-based cloud platform.

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

> Make sure `profiles.db` and `venv/` are in your `.gitignore`.

### 2. Create a `.gitignore`

```
venv/
profiles.db
__pycache__/
*.pyc
.env
```

### 3. Deploy on pxxl.app

1. Go to [pxxl.app](https://pxxl.app) and sign in.
2. Click **New Project** → **Deploy from GitHub**.
3. Authorize pxxl and select your repository.
4. pxxl auto-detects Python projects. It will use the `Procfile` included in this repo to start the server:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **Deploy**. pxxl will install dependencies from `requirements.txt` and start the server.
6. Once live, your public URL will be shown in the dashboard.

### Environment variables (optional)

If you later switch to PostgreSQL or add secret keys, add them in the pxxl project **Settings → Environment Variables** panel.

---

## Project Structure

```
classification-logic/
├── main.py            # FastAPI app & all route handlers
├── database.py        # SQLAlchemy / SQLite setup
├── models.py          # Profile ORM model
├── schemas.py         # Pydantic request/response schemas
├── external_apis.py   # Async callers for Genderize, Agify, Nationalize
├── requirements.txt   # Python dependencies
├── Procfile           # Process start command (for pxxl / Heroku)
└── README.md
```

---

## Tech Stack

- **FastAPI** — ASGI web framework
- **SQLAlchemy + SQLite** — ORM and database
- **httpx** — Async HTTP client for external APIs
- **uuid6** — UUID v7 generation
- **uvicorn** — ASGI server
