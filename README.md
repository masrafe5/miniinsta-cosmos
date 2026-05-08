# MiniInsta – Django Photo Sharing App
### Built for Python 3.14 · Django 5.2 (LTS)

---

## Quick Start

### 1. Create virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations photos
python manage.py migrate
```

### 4. Create admin/superuser
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## How to create a Creator account

Creator accounts are **not** available via public sign-up (as per coursework spec).
Only staff/admin can create them:

**Option A – Django Admin panel:**
1. Go to http://127.0.0.1:8000/admin/
2. Users → Custom Users → Add User
3. Set `role = Creator`

**Option B – site UI (staff only):**
- Log in as superuser → click the ➕ icon in the navbar → fill the form

---

## User Roles

| Feature                   | Consumer | Creator |
|---------------------------|:--------:|:-------:|
| Public registration       |    ✅    |   ❌    |
| View feed & search        |    ✅    |   ✅    |
| Like photos               |    ✅    |   ✅    |
| Comment on photos         |    ✅    |   ✅    |
| Rate photos (1-5 stars)   |    ✅    |   ✅    |
| Upload photos             |    ❌    |   ✅    |
| Set title/caption/location/people/tags | ❌ | ✅ |
| Edit & delete own photos  |    ❌    |   ✅    |
| Creator dashboard + stats |    ❌    |   ✅    |
| Follow/unfollow users     |    ✅    |   ✅    |
| Edit own profile          |    ✅    |   ✅    |

---

## Project Structure

```
miniinsta/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3              ← created after migrate
├── media/                  ← uploaded files
├── static/                 ← CSS/JS assets
├── templates/
│   ├── base.html
│   ├── photos/
│   │   ├── feed.html
│   │   ├── photo_detail.html
│   │   ├── upload.html
│   │   └── creator_dashboard.html
│   └── users/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── edit_profile.html
│       └── explore_users.html
├── miniinsta/              ← project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  ← auth app
│   ├── models.py           (CustomUser, Follow)
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
└── photos/                 ← main app
    ├── models.py           (Photo, Comment, Rating, Like)
    ├── views.py
    ├── forms.py
    ├── urls.py
    └── admin.py
```

---

## Package versions (Python 3.14 compatible)

| Package               | Version     | Why                                    |
|-----------------------|-------------|----------------------------------------|
| Django                | 5.2.1       | First Django LTS to support Python 3.14|
| Pillow                | 12.0.0      | First Pillow with Python 3.14 wheels   |
| django-crispy-forms   | 2.4         | Supports Python 3.14 + Django 5.2      |
| crispy-bootstrap5     | 2024.10     | Matching Bootstrap 5 template pack     |

---

## Cloud Deployment (CW2 Task 2)

- **Static files**: `python manage.py collectstatic` → serve via AWS S3 / Azure Blob / Cloudflare CDN
- **Database**: swap SQLite → PostgreSQL (`psycopg2`), configure `DATABASES` in `settings.py`
- **Media storage**: `django-storages` + S3/Azure for scalable object storage
- **Platforms**: AWS Elastic Beanstalk · Azure App Service · Heroku · Railway · Render
- **Caching/scalability**: add Redis (`django-redis`) + CDN for dynamic DNS routing
