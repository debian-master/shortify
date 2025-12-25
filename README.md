# shortify

🔗 URL Shortener Backend Service
A URL shortening service built using Django + Django REST Framework, designed for high read traffic, secure user access, and basic analytics.
This project was implemented as a take-home assignment to demonstrate backend design, API development, and containerized deployment.

✨ Features
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

🏗️ Architecture Overview
Client
  │
  ▼
Django + DRF
  │
  ├── Auth (JWT)
  ├── URL APIs
  ├── Redirect Handler
  │
  ▼
PostgreSQL

Stateless backend using JWT
Read-heavy redirect path optimized with indexed lookups
Docker Compose for service networking

🧰 Tech Stack
Python 3.12
Django, Django REST Framework
SimpleJWT
PostgreSQL 18
Docker & Docker Compose

🚀 Setup & Running Instructions
Prerequisites
Docker
Docker Compose

Steps
git clone https://github.com/<your-username>/shortify.git
cd shotify
cp backend/.env.example backend/.env
docker-compose up --build

Run migrations:
docker-compose exec web python manage.py migrate

📄 API Documentation
Swagger UI: http://localhost:8000/api/docs/

path('admin/', admin.site.urls),
    path("api/urls/", include("urls.urls"), name='urls'),
    path("api/auth/", include("users.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view()),

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
Django + DRF for clean, maintainable APIs
PostgreSQL for relational integrity and indexing
JWT for stateless authentication
Click tracking handled synchronously (simpler, slight overhead)
No caching layer to keep scope focused

🚧 Improvements With More Time
Redis caching for redirects
Async click tracking (Celery)
Rate limiting
Aggregated analytics APIs
Nginx reverse proxy
Instead of django's local server using Gunicorn

⏱️ Approximate Time Spent
~6-8 hours
