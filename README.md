# AlumniConnect

A Django-based alumni networking platform for connecting graduates, managing events, sharing job opportunities, and facilitating real-time messaging.

**Live Demo:** [https://pcetconnect.pythonanywhere.com/](https://pcetconnect.pythonanywhere.com/)

## Features

- **Alumni Directory** - Browse and search alumni by department, year, name, or company
- **Secure Authentication** - OTP-based login and registration system
- **Profile Management** - Users can create and manage their professional profiles
- **Events Management** - Create and RSVP to alumni events, reunions, webinars
- **Job Board** - Post and browse job opportunities
- **Real-time Chat** - Direct messaging and group chats via WebSocket
- **Responsive Design** - Works on desktop and mobile devices

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

## Similar Deployed Sites

- [AlumniConnect Demo](https://pcetconnect.pythonanywhere.com/) - PythonAnywhere deployment
- [AlumniConnect on Render](https://pcet-alumni.onrender.com/) - Render deployment

## License

MIT License - feel free to use this project for any educational institution or organization.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with Django ❤️**
