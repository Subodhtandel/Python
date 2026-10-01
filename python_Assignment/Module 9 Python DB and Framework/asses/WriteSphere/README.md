# WriteSphere

Django MVT blogging platform for the WriteHub / BlogX scenario: registration and sessions, rich-text posts with cover images, categories and tags, filtered listing, likes, threaded-style comments with edit/delete, author follow/unfollow, custom roles (admin, author, reader), and tailored admin screens.

## Local setup (virtual environment recommended)

```bash
cd WriteSphere
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env`. For SQLite (default): leave `USE_MYSQL=0`. Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sign up readers via the web UI; promote users to **Author** or **Admin** in Django admin (`role` field) so they can use **Write**.

## MySQL (local or PythonAnywhere)

1. Create a database and MySQL user (on PythonAnywhere: **Databases** tab → MySQL password, note hostname like `YOURUSER.mysql.pythonanywhere-services.com`).
2. In `.env` set:

   - `USE_MYSQL=1`
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

3. Windows without a MySQL driver build chain: rely on **PyMySQL** (included in `requirements.txt`); the project activates `pymysql.install_as_MySQLdb()` automatically when `USE_MYSQL` is enabled on Windows. On Linux/PythonAnywhere, **mysqlclient** is preferred if it installs cleanly.

4. Run `python manage.py migrate` again.

## PythonAnywhere checklist

1. Clone from GitHub, open a Bash console in the repo, create a `.venv`, `pip install -r requirements.txt`.
2. **Web tab**: virtualenv points to `.venv`; WSGI file imports `config.wsgi.application` from this project folder.
3. Set `ALLOWED_HOSTS` and `DEBUG=False` in `.env`; set `SECRET_KEY` and MySQL vars.
4. `python manage.py collectstatic` → static root URL mapping to match `STATIC_ROOT`.
5. **Files** permission for `media/` upload directory if authors upload covers or avatars.
6. CKEditor 4 emits a deprecation/security warning at startup; treat content as trusted (staff/authors only) or plan a move to django-ckeditor-5 or another editor later.

## Project layout

| Area | Purpose |
|------|---------|
| `accounts/` | Custom `User` with `Role`, registration, login/logout (POST), profile edit |
| `blog/` | Posts, categories, tags, comments, likes, follows, filters, author profiles |
| `templates/` | Base layout with Bootstrap 5 |
| `.env.example` | Documented secrets and DB toggles |

## Git

Ensure `.env` is **never** committed; use `.env.example` as the template. `venv/`, `media/`, and `*.sqlite3` are listed in `.gitignore`.
