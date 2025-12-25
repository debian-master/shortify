# Shortify

🔗 **URL Shortener Backend Service**

A URL shortening service built using **Django** and **Django REST Framework**, designed for high read traffic, secure user access, and basic analytics.  
This project was implemented as a take-home assignment to demonstrate backend design, API development, and containerized deployment.

---

## ✨ Features

- JWT authentication (register, login, refresh)
- Create short URLs (auto-generated or custom alias)
- Optional expiration (TTL)
- List and manage user-owned URLs
- Fast redirect endpoint
- Click tracking:
  - Timestamp
  - Referrer
  - Browser / OS
  - IP & country (GeoIP)

---

## 🏗️ Architecture Overview

The backend is designed to be stateless and optimized for read-heavy operations.

```mermaid
graph TD
    A[Client Request: /short_code] --> B{Redirect Handler};
    B --> C[Indexed Lookup in PostgreSQL];
    B --> D[Click Tracking (Synchronous)];
    C --> E{If Found?};
    E -- Yes --> F[302 Redirect to Long URL];
    E -- No --> G[404 Not Found];
```


- Stateless backend using JWT
- Read-heavy redirect path optimized with indexed lookups
- Docker Compose used for service orchestration

---

## 🧰 Tech Stack

- Python 3.12
- Django, Django REST Framework
- SimpleJWT
- PostgreSQL 18
- Docker & Docker Compose

---

## 🚀 Setup & Running Instructions

### Prerequisites
- Docker
- Docker Compose

### Steps

```bash
git clone https://github.com/<your-username>/shortify.git
cd shortify
cp backend/.env.example backend/.env
docker-compose up --build
```

Run migrations:
docker-compose exec web python manage.py migrate

📄 API Documentation
Swagger UI: http://localhost:8000/api/docs/

📌 Core Endpoints
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/urls/
GET /api/urls/
GET /api/urls/{short_code}/
DELETE /api/urls/{short_code}/
GET /{short_code} (redirect)

⚖️ Key Design Decisions & Trade-offs
- Django + DRF for clean, maintainable APIs
- PostgreSQL for relational integrity and indexing
- JWT for stateless authentication
- Click tracking handled synchronously (simpler, slight overhead)
- No caching layer to keep scope focused

🚧 Improvements With More Time
- Redis caching for redirects
- Async click tracking (Celery)
- Rate limiting
- Aggregated analytics APIs
- Nginx reverse proxy
- Using Gunicorn instead of Django’s local server

⏱️ Approximate Time Spent
~5-7 hours
