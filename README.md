# AlumniConnect

A Django-based alumni networking platform for connecting graduates, managing events, sharing job opportunities, and facilitating real-time messaging.

**Live Demo:** [https://pcetconnect.pythonanywhere.com/](https://pcetconnect.pythonanywhere.com/)

## Features

### Currently Deployed (Live on Production)

- **Alumni Directory** - Browse and search alumni by department, year, name, or company ✅
- **Secure Authentication** - OTP-based login and registration system ✅
- **Profile Management** - Users can create and manage their professional profiles ✅
- **Responsive Design** - Works on desktop and mobile devices ✅

### Available in Repository (Not Yet Deployed)

- **Events Management** - Create and RSVP to alumni events, reunions, webinars 📦
- **Job Board** - Post and browse job opportunities 📦
- **Real-time Chat** - Direct messaging and group chats via WebSocket 📦

> **Note:** The live demo at https://pcetconnect.pythonanywhere.com/ currently only includes the Alumni Directory, Authentication, and Profile Management features. Events, Job Board, and Real-time Chat are fully coded and ready to use but require additional configuration (Redis, WebSocket setup) to deploy.

## Deployment Status

| Feature | Status | Notes |
|---------|--------|-------|
| Alumni Directory | ✅ Deployed | Live on production, fully functional |
| Authentication (OTP) | ✅ Deployed | Live on production, secure OTP-based login |
| Profile Management | ✅ Deployed | Live on production, photo upload supported |
| Events Management | 📦 In Code | Available in repository, not deployed |
| Job Board | 📦 In Code | Available in repository, not deployed |
| Real-time Chat | 📦 In Code | Requires Redis + WebSocket setup |
| Responsive Design | ✅ Deployed | Mobile-friendly Bootstrap 5 interface |

## Tech Stack

## Tech Stack

- **Backend:** Django 6.0, Python 3.13
- **Real-time:** Django Channels, Redis
- **Frontend:** Bootstrap 5, Font Awesome
- **Database:** SQLite (default), PostgreSQL (production-ready)
- **Deployment:** PythonAnywhere, Render, Heroku, Docker

## Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Redis (for WebSocket support in production)
- PostgreSQL (optional, for production deployment)

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/GadatheGod/Alumniconnect.git
cd Alumniconnect
```

### 2. Create a virtual environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example `.env` file and update with your settings:

```bash
copy .env .env.local   # Windows
cp .env .env.local     # Linux/Mac
```

Edit `.env.local` with your settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

SITE_NAME=AlumniConnect
SITE_PRIMARY_COLOR=#901d78
SITE_SECONDARY_COLOR=#7a1866

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

DATABASE_URL=  # Leave empty for SQLite
```

**Getting a Gmail App Password:**
1. Go to Google Account settings
2. Enable 2-Step Verification
3. Generate an App Password (Security > App Passwords)
4. Use this password in your `.env` file

### 5. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Seed sample data (optional)

```bash
python manage.py seed_data --count 20
```

This creates 20 sample alumni accounts (password: `testpass123` for all).

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

### 9. Access admin panel

Visit `http://127.0.0.1:8000/admin/` and login with your superuser credentials.

## Production Deployment

### Option 1: PythonAnywhere

**Step 1: Create a PythonAnywhere account**
- Sign up at [pythonanywhere.com](https://www.pythonanywhere.com/)
- Choose a free or paid plan

**Step 2: Upload your code**
- Use Git to clone your repo:
  ```bash
  git clone https://github.com/GadatheGod/Alumniconnect.git
  cd Alumniconnect
  ```
- Or upload via file manager

**Step 3: Create a virtual environment**
```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 4: Configure Web App**
- Go to Web tab > Add a new web app
- Choose Manual configuration
- Select Python 3.13
- Set virtualenv path: `/home/yourusername/Alumniconnect/venv`

**Step 5: Configure WSGI file**
Edit the WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/Alumniconnect'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'alumni_project.settings'
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Step 6: Configure environment variables**
- Go to Web tab > Environment tab
- Add your environment variables (SECRET_KEY, EMAIL_HOST_USER, etc.)

**Step 7: Static files**
```bash
python manage.py collectstatic
```
- In Web tab > Static files section:
  - URL: `/static/`
  - Directory: `/home/yourusername/Alumniconnect/staticfiles/`

**Step 8: Database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Step 9: Reload**
- Click the red "Reload" button in PythonAnywhere Web tab

### Option 1B: PythonAnywhere with WebSocket Support (For Chat Feature)

If you want to enable the **Real-time Chat** feature, follow these additional steps:

**Step 1: Install Redis on PythonAnywhere**
- Upgrade to a paid PythonAnywhere plan (Redis is available on paid plans)
- Or use a free Redis service like [Redis Labs](https://redis.com/redis-enterprise-cloud/)

**Step 2: Install Channels and Redis packages**
```bash
pip install channels channels_redis daphne
```

**Step 3: Update `alumni_project/settings.py`**
Add these to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    # ... existing apps ...
    'channels',
    'alumni',
    'events',
    'jobs',
    'chat',
]
```

Add this to the end of `settings.py`:
```python
# Channels configuration
ASGI_APPLICATION = 'alumni_project.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379/1')],
        },
    },
}
```

**Step 4: Configure Daphne (ASGI server for WebSocket)**
Create `alumni_project/asgi.py` (if not exists):
```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

**Step 5: Update WSGI configuration**
In PythonAnywhere Web tab, edit WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/Alumniconnect'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'alumni_project.settings'
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Step 6: Add URL routes for Events and Jobs**
Update `alumni_project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alumni.urls')),  # Alumni views
    path('events/', include('events.urls')),  # Events views
    path('jobs/', include('jobs.urls')),  # Job views
    path('chat/', include('chat.urls')),  # Chat views
]
```

**Step 7: Create URL files for each app**

`alumni/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('login/verify-otp/', views.login_verify_otp, name='login_verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('directory/', views.directory, name='directory'),
    path('directory/<int:profile_id>/', views.view_profile, name='view_profile'),
    path('directory/<int:profile_id>/edit/', views.edit_profile, name='edit_profile'),
]
```

`events/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/rsvp/', views.event_rsvp, name='event_rsvp'),
]
```

`jobs/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/toggle-status/', views.toggle_job_status, name='toggle_job_status'),
]
```

`chat/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('create-direct/<int:user_id>/', views.create_direct_chat, name='create_direct_chat'),
    path('create-group/', views.create_group_chat, name='create_group_chat'),
]
```

**Step 8: Configure PythonAnywhere for WebSocket**
- In PythonAnywhere Web tab, set "Startup mode" to "Daphne"
- Set "Working directory" to `/home/yourusername/Alumniconnect`
- Set "Entry point" to `alumni_project.asgi:application`
- Add environment variable: `REDIS_URL=redis://your-redis-url:6379/0`

**Step 9: Reload**
- Click the red "Reload" button in PythonAnywhere Web tab

### Option 2: Render.com

**Step 1: Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit - AlumniConnect"
git remote add origin https://github.com/GadatheGod/Alumniconnect.git
git push -u origin main
```

**Step 2: Create Render account**
- Sign up at [render.com](https://render.com/)

**Step 3: Deploy Web Service**
- Click "New +" > "Web Service"
- Connect your GitHub repository
- Configure:
  - Name: alumni-connect
  - Environment: Python 3
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn alumni_project.wsgi:application`
- Add environment variables from your `.env` file
- Click "Create Web Service"

**Step 4: Add PostgreSQL Database**
- Click "New +" > "PostgreSQL"
- Note the database URL
- Add `DATABASE_URL` to your web service environment variables

**Step 5: Update settings.py**
Ensure your `settings.py` supports DATABASE_URL (already configured)

**Step 6: Redeploy**
- Push changes to GitHub
- Render will automatically redeploy

### Option 3: Docker

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "alumni_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Step 2: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key
      - DEBUG=False
      - ALLOWED_HOSTS=localhost
      - DATABASE_URL=postgres://user:password@db:5432/alumniconnect
    depends_on:
      - db

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=alumniconnect
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

**Step 3: Build and run**

```bash
docker-compose up -d
```

## Enabling Additional Features

The repository includes code for Events, Job Board, and Real-time Chat, but they are not enabled by default. Here's how to enable each feature:

### Enable Events Management

1. **Add URL routes** - Update `alumni_project/urls.py` (see PythonAnywhere WebSocket setup above)
2. **Create events/urls.py** - Add event URL patterns
3. **Run migrations**:
   ```bash
   python manage.py makemigrations events
   python manage.py migrate
   ```
4. **Access**: Navigate to `/events/` after deployment

### Enable Job Board

1. **Add URL routes** - Update `alumni_project/urls.py` (see PythonAnywhere WebSocket setup above)
2. **Create jobs/urls.py** - Add job URL patterns
3. **Run migrations**:
   ```bash
   python manage.py makemigrations jobs
   python manage.py migrate
   ```
4. **Access**: Navigate to `/jobs/` after deployment

### Enable Real-time Chat

**Prerequisites:**
- Redis server installed and running
- Paid PythonAnywhere plan (for Redis support)
- OR use external Redis service (Redis Labs, Upstash, etc.)

**Steps:**
1. **Install required packages**:
   ```bash
   pip install channels channels_redis daphne
   ```

2. **Update `alumni_project/settings.py`**:
   - Add `'channels'` to `INSTALLED_APPS`
   - Add `ASGI_APPLICATION = 'alumni_project.asgi.application'`
   - Add `CHANNEL_LAYERS` configuration with Redis backend

3. **Create `alumni_project/asgi.py`** (if not exists):
   - Configure ProtocolTypeRouter with WebSocket support
   - Reference `chat.routing.websocket_urlpatterns`

4. **Update WSGI/ASGI configuration**:
   - Use Daphne as ASGI server for WebSocket support
   - Configure PythonAnywhere to use ASGI startup mode

5. **Add URL routes** - Update `alumni_project/urls.py` and create `chat/urls.py`

6. **Set Redis URL** - Add `REDIS_URL` environment variable

7. **Run migrations**:
   ```bash
   python manage.py makemigrations chat
   python manage.py migrate
   ```

8. **Access**: Navigate to `/chat/` after deployment

> **Note:** Real-time Chat requires WebSocket support, which needs Redis and an ASGI server (Daphne). Standard WSGI servers (Gunicorn) do not support WebSockets.

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode (True/False) | No | False |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | No | localhost,127.0.0.1 |
| `SITE_NAME` | Website name | No | AlumniConnect |
| `SITE_PRIMARY_COLOR` | Primary brand color (hex) | No | #901d78 |
| `SITE_SECONDARY_COLOR` | Secondary brand color (hex) | No | #7a1866 |
| `EMAIL_HOST` | SMTP host | No | smtp.gmail.com |
| `EMAIL_PORT` | SMTP port | No | 587 |
| `EMAIL_HOST_USER` | Email username | Yes | - |
| `EMAIL_HOST_PASSWORD` | Email password | Yes | - |
| `EMAIL_USE_TLS` | Use TLS (True/False) | No | True |
| `DATABASE_URL` | Database connection string | No | SQLite |
| `DJANGO_LOG_LEVEL` | Logging level | No | INFO |

## Project Structure

```
Alumniconnect/
├── alumni/                  # Alumni profiles, authentication, directory
│   ├── models.py           # User and AlumniProfile models
│   ├── views.py            # Login, register, directory views
│   ├── forms.py            # Registration and profile forms
│   ├── services/           # Email service, etc.
│   └── management/         # Custom management commands (seed_data)
├── alumni_project/          # Django project configuration
│   ├── settings.py         # Settings and configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py            # WSGI application
├── events/                  # Events management
│   ├── models.py           # Event and RSVP models
│   ├── views.py            # Event listing, creation, RSVP
│   └── forms.py            # Event creation form
├── jobs/                    # Job board
│   ├── models.py           # JobPost model
│   ├── views.py            # Job listing, creation, detail
│   └── forms.py            # Job creation form
├── chat/                    # Real-time messaging
│   ├── models.py           # ChatRoom, Message models
│   ├── consumers.py        # WebSocket consumers
│   ├── routing.py          # WebSocket URL routing
│   └── views.py            # Chat room views
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── alumni/             # Alumni templates
│   ├── events/             # Event templates
│   ├── jobs/               # Job templates
│   └── chat/               # Chat templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Customization

### Changing Brand Colors

Edit the `.env` file:
```env
SITE_PRIMARY_COLOR=#901d78
SITE_SECONDARY_COLOR=#7a1866
```

Or modify `alumni_project/settings.py`:
```python
SITE_PRIMARY_COLOR = os.environ.get('SITE_PRIMARY_COLOR', '#901d78')
SITE_SECONDARY_COLOR = os.environ.get('SITE_SECONDARY_COLOR', '#7a1866')
```

### Adding Custom Departments

Edit `alumni_project/settings.py`:
```python
DEPARTMENTS = [
    ('CSE', 'Computer Science and Engineering'),
    ('NEW', 'Your Custom Department'),
    # ... add more
]
```

### Changing Site Name

Edit the `.env` file:
```env
SITE_NAME=My Alumni Network
```

## Troubleshooting

### Email not sending
- Ensure you're using a Gmail App Password, not your regular password
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in `.env`
- Verify EMAIL_USE_TLS=True for port 587

### Static files not loading
- Run `python manage.py collectstatic`
- Ensure DEBUG=False in production
- Check static files configuration in settings.py

### WebSocket not working
- Ensure Redis is running
- Check channels_redis is installed
- Verify WebSocket routing in chat/routing.py

### Database errors
- For PostgreSQL, ensure DATABASE_URL is correctly formatted
- Run migrations: `python manage.py migrate`
- Check database credentials

### Chat WebSocket not connecting
- Ensure Redis is running and accessible
- Verify `channels_redis` is installed
- Check that Daphne is used instead of Gunicorn for WebSocket support
- Confirm `ASGI_APPLICATION` is set in settings.py
- Check browser console for WebSocket connection errors
- Verify `chat.routing.websocket_urlpatterns` is correctly configured

### Jobs/Events pages return 404
- Ensure URL routes are added to `alumni_project/urls.py`
- Create app-specific URL files (`jobs/urls.py`, `events/urls.py`)
- Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
- Check that views are correctly imported in URL files

## FAQ

### Why doesn't the live demo have chat and job posting?
The live demo at https://pcetconnect.pythonanywhere.com/ currently only includes the core features: Alumni Directory, Authentication, and Profile Management. The Events, Job Board, and Real-time Chat features are fully coded and tested but require additional infrastructure to deploy:
- **Real-time Chat** requires Redis server and WebSocket support (Daphne server)
- **Events and Job Board** require URL routing configuration and database migrations

### How can I enable all features?
Follow the "Enabling Additional Features" section above. For Events and Job Board, you just need to add URL routes and run migrations. For Real-time Chat, you'll also need Redis and WebSocket configuration.

### What's the difference between WSGI and ASGI?
- **WSGI** (Web Server Gateway Interface) handles HTTP requests only (used by Gunicorn)
- **ASGI** (Asynchronous Server Gateway Interface) handles HTTP and WebSocket requests (used by Daphne)
- For Real-time Chat, you need ASGI with Daphne

### Can I use this for my university/organization?
Yes! AlumniConnect is fully generic and can be customized for any educational institution or organization. Simply update the `.env` file with your site name, colors, and email settings.

### Is Redis required for chat?
Yes, Redis is required for Django Channels to manage WebSocket connections. You can use:
- Local Redis server (install on your machine)
- PythonAnywhere Redis (paid plans)
- External Redis services (Redis Labs, Upstash, etc.)

### How do I change the brand colors?
Edit the `.env` file:
```env
SITE_PRIMARY_COLOR=#your-color
SITE_SECONDARY_COLOR=#your-color
```
Or modify `alumni_project/settings.py` directly.

## Similar Deployed Sites

- [AlumniConnect Demo](https://pcetconnect.pythonanywhere.com/) - PythonAnywhere deployment
- [AlumniConnect on Render](https://pcet-alumni.onrender.com/) - Render deployment

## Security Best Practices

### SECRET_KEY Generation
Generate a secure SECRET_KEY for production:
```python
import secrets
print(secrets.token_urlsafe(50))
```

### HTTPS Setup
- Enable HTTPS on your hosting provider
- Set `SECURE_SSL_REDIRECT = True` in settings.py
- Update `ALLOWED_HOSTS` with your domain
- Add `CSRF_TRUSTED_ORIGINS` with your HTTPS domain

### Database Security
- Use PostgreSQL for production (not SQLite)
- Set strong database passwords
- Restrict database user permissions
- Regular database backups

### Email Security
- Use Gmail App Passwords (not regular passwords)
- Store email credentials in environment variables
- Never commit `.env` to version control
- Use different email accounts for production/staging

### File Upload Security
- Validate file types (images only: JPG, PNG, GIF)
- Set maximum file size limits (5MB recommended)
- Store uploads outside web root when possible
- Regularly clean up old uploads

## Maintenance Guide

### Database Backups
```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL backup
pg_dump your_database > backup.sql

# Restore PostgreSQL
psql your_database < backup.sql
```

### Regular Updates
```bash
# Update Django
pip install --upgrade Django

# Check for security updates
pip list --outdated

# Run migrations after updates
python manage.py makemigrations
python manage.py migrate
```

### Log Monitoring
```bash
# View Django logs
tail -f logs/django.log

# Check for errors
grep "ERROR" logs/django.log
```

### Performance Optimization
- Enable static file compression (WhiteNoise)
- Use PostgreSQL indexes for frequently queried fields
- Implement caching with Redis
- Optimize database queries with `select_related()` and `prefetch_related()`
- Use Django Debug Toolbar in development to identify slow queries

### Monitoring
- Set up error tracking with Sentry
- Monitor server resources (CPU, memory, disk)
- Track application performance metrics
- Set up uptime monitoring (UptimeRobot, Pingdom)

## License

This project is licensed under the [MIT License](LICENSE).

### Dependent Package Licenses

This project uses several third-party packages, each with their own licenses:

| Package | License |
|---------|---------|
| Django, Django Channels, Django REST Framework | BSD License |
| Bootstrap 5 | MIT License |
| Font Awesome | SIL OFL 1.1 License |
| Pillow | HPND License |
| Redis, Gunicorn, Daphne | BSD/MIT License |
| Requests | Apache License 2.0 |
| certifi | MPL 2.0 |
| jQuery, Select2 | MIT License |

For a complete list of all dependent packages and their licenses, please refer to the [LICENSE](LICENSE) file.

**Note:** All licenses are permissive and allow commercial use, modification, and distribution. You are not required to open-source your entire project. See the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with Django ❤️** Loved to Vibe Code!.
