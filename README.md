# Sea Cox V2

This is a static Django site for **Sea Coxs Fire** (https://www.seacoxsfire.com/). 
It has no database backend, and uses [Whitenoise](https://whitenoise.readthedocs.io/) to efficiently serve static assets in production.

## Requirements

- Python 3.x
- Packages listed in `requirements.txt`

## Local Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment / Production

Before deploying to production, make sure to:
1. Ensure `DEBUG = False` in `settings.py`
2. Run collectstatic to process and gather all static files:
   ```bash
   python manage.py collectstatic
   ```
   *(Note: `WHITENOISE_MANIFEST_STRICT = False` has been set in `settings.py` so collectstatic will gracefully ignore any missing sourcemaps from 3rd party vendor libraries).*
