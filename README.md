# Sea Cox's Fire & Safety LLC

A static Django website for **Sea Cox's Fire & Safety** (https://www.seacoxsfire.com/).  
No database — uses [WhiteNoise](https://whitenoise.readthedocs.io/) for static file serving.

## Requirements

- Python 3.11+
- Packages listed in `requirements.txt`

## Local Development

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run development server
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Docker (Recommended for Production)

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

Visit http://localhost:8000

### What Docker does:
- Builds a lightweight Python 3.12 image
- Installs dependencies
- Collects static files (served by WhiteNoise)
- Runs Django via Gunicorn (2 workers)
- Mounts `./logs` and `./media` as volumes

## cPanel Deployment

1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY` in `.env`
3. Run `python manage.py collectstatic --noinput`
4. Configure `passenger_wsgi.py` for your cPanel environment

## Project Structure

```
sea_cox_v2/
├── home/              # Views, data, SEO config
├── core/              # Middleware, logging, error handlers
├── templates/         # Django templates
├── static/assets/     # CSS, images
├── media/uploads/     # Uploaded media files
├── sea_cox_v2/        # Django settings, URLs, WSGI
├── Dockerfile         # Production Docker image
├── docker-compose.yml # Single-service compose
└── requirements.txt   # Python dependencies
```
