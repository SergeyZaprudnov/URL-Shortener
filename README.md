![CI](https://github.com/SergeyZaprudnov/URL-Shortener/actions/workflows/ci.yml/badge.svg)

# URL Shortener API

Backend service for shortening URLs with analytics and fast redirects.

## Tech Stack
- Python 3.12, Django, Django REST Framework
- PostgreSQL, Redis
- Docker, Docker Compose
- Poetry, Pytest, Ruff
- GitHub Actions (CI)

## Features
- Create short links from long URLs
- Fast redirection with Redis caching
- Click tracking (analytics)
- Fully dockerized for easy setup
- Automated tests and linting on every push

## Quick Start
1. Clone the repository:
git clone https://github.com/SergeyZaprudnov/URL-Shortener.git
cd URL-Shortener

2. Create .env:
cp .env.example .env
# Open .env and set your SECRET_KEY

3. Run with Docker:
docker compose up -d --build

4. Apply migrations:
docker compose exec web python manage.py migrate

5. Open the API:
- Create link: POST http://localhost:8001/api/links/
- Redirect: GET http://localhost:8001/{short_code}/
- Admin: http://localhost:8001/admin/

## Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | your-secret-key |
| DEBUG | Debug mode | True |
| ALLOWED_HOSTS | Comma-separated hosts | localhost,127.0.0.1 |
| POSTGRES_DB | Database name | url_shortener |
| POSTGRES_USER | Database user | postgres |
| POSTGRES_PASSWORD | Database password | postgres |
| POSTGRES_HOST | Database host | localhost |
| POSTGRES_PORT | Database port | 5433 |
| REDIS_URL | Redis connection URL | redis://localhost:6830/1 |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/links/ | Create a short link |
| GET | /{short_code}/ | Redirect to original URL |

## Running Tests
poetry run pytest -v

## Linting
poetry run ruff check .

## Project Structure
url-shortener/
├── config/              # Django settings, URLs
├── shortener/           # Main app: models, views, services, tests
├── .github/workflows/   # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md

## CI
GitHub Actions runs linter and tests on every push to main and develop.
EOF