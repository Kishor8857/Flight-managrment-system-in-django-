# Flight Management System - Django

A Django-based flight management system with booking capabilities.

## Deployment to Render

### Prerequisites
- GitHub account with this repo pushed
- Render account (https://render.com)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create a New Web Service on Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: your-app-name
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn myproject.wsgi:application`

3. **Set Environment Variables**
   - In Render dashboard, go to your service's "Environment" tab
   - Add the following variables:
     ```
     DEBUG=False
     SECRET_KEY=<generate-a-strong-secret-key>
     ALLOWED_HOSTS=your-app-name.onrender.com
     CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
     ```
   
   **To generate a SECRET_KEY**, run in Python:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. **Database Setup**
   - Render will use PostgreSQL if DATABASE_URL is set via a PostgreSQL service
   - Or use the default SQLite (included)
   - If using PostgreSQL:
     - Create a PostgreSQL database on Render
     - The DATABASE_URL will be automatically set

5. **Static Files**
   - WhiteNoise is configured to serve static files automatically
   - Your static files from `static/` and `staticfiles/` will be collected during build

6. **Deploy**
   - Push changes to GitHub
   - Render will automatically build and deploy
   - Check the "Logs" tab for deployment progress

## Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file** (copy from .env.example)
   ```bash
   cp .env.example .env
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `myproject/` - Django project settings
- `base/` - Main Django app with models, views, and templates
- `templates/` - HTML templates
- `static/` - CSS, JS, and other static files
- `requirements.txt` - Python dependencies
- `Procfile` - Render deployment configuration
- `runtime.txt` - Python version specification

## Notes

- DEBUG is set to False in production (via environment variable)
- SECRET_KEY should be a strong, random string in production
- Static files are automatically collected and served by WhiteNoise
- Database migrations run automatically during deployment via Procfile
