# 📄 ExtracTable

**ExtracTable** is a **Django REST API** service for extracting tables from PDF documents using AI.
It’s containerized with Docker, powered by Celery for asynchronous task processing, Redis for message brokering, and comes with a ready-to-use development & production setup.

## 🚀 Features

* **Django 5.2** backend with REST API (Django REST Framework)
* **User authentication** with Djoser & JWT
* **Celery** & **Redis** for background task processing
* **Flower** for Celery task monitoring
* **Ngrok** integration for public URL tunneling
* **Automatic superuser creation** from `.env`
* **PostgreSQL-ready** (via `dj-database-url`)
* **CORS support** for frontend integration
* **Static & media file management** with Docker volumes

## 🛠 Tech Stack

* **Backend:** Django, Django REST Framework, Djoser, DRF Spectacular
* **Auth:** JWT-based authentication
* **Task Queue:** Celery + Redis
* **Monitoring:** Flower
* **Deployment:** Docker & Docker Compose
* **Environment Management:** python-decouple
* **Documentation:** OpenAPI/Swagger

## 📂 Project Structure

```bash
backend/
 ├── extractable/         # Django project settings
 ├── apps/                # Your Django apps
 ├── celery.py            # Celery configuration
 ├── entrypoint.sh        # Docker entry script
docker-compose.yml        # Services (web, worker, beat, redis, flower, ngrok)
pyproject.toml            # Python dependencies
```

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Chitresh-code/extractable-backend.git
cd extractable-backend
```

### 2️⃣ Create `.env` file

```env
# General Django Settings
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1,your-ngrok-domain.ngrok-free.app
API_BASE_URL=https://your-ngrok-domain.ngrok-free.app

# Database Configuration
DEV_DATABASE_URL=postgresql://user:password@localhost:5432/dev_db
PROD_DATABASE_URL=postgresql://user:password@prod-db-host:5432/prod_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
EMAIL_USE_TLS=True

# Ngrok Configuration
NGROK_AUTHTOKEN=your_ngrok_authtoken_here
NGROK_DOMAIN=your-ngrok-domain.ngrok-free.app

# Superuser Credentials
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_NAME=Admin
DJANGO_SUPERUSER_PASSWORD=your_secure_password_here

# Redis / Celery
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 3️⃣ Build & Run with Docker

```bash
docker compose build --no-cache
docker compose up -d
```

Services:

* **Web:** `http://localhost:8000`
* **Flower UI:** `http://localhost:5555`
* **Ngrok:** `http://localhost:4040` (dashboard)

## 📜 API Documentation

Once the server is running, visit:

```bash
http://localhost:8000/api/docs/                 # Swagger UI
http://localhost:8000/api/schema/redoc/         # Redoc UI
```

You can also find the complete OpenAPI specification in the [`openapi.yaml`](./openapi.yaml) file at the root of the project.

## 🗄 Running Background Workers

Celery workers & beat scheduler are already included in `docker-compose.yml`:

```bash
docker-compose up worker
docker-compose up beat
```

## 🛡 License

This project is licensed under the terms of the [MIT License](LICENSE).
