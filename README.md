> ## 🛠 Status: In Development
> Django template is currently in development. So we encourage you to use it and give us your feedback, but there are things that haven't been finalized yet and you can expect some changes.
>
> See the list of Known Issues and TODOs, below, for updates.


# Django Template
TBD

# Todos
- set up a password hashing algorithm with:
  - Argon2. ✅
  - bcrypt. ✅
  - PBKDF2. ✅
- Selecting an app type from the following options:
  - A plain django with django templates. ✅
  - Django Rest Framework:
    - with dj-rest-auth
      - add to the pyporject.toml. ✅
      - setup to the settings.py.
      - setup to the urls.py.
      - setup to the views.py.
      - setup to the serializers.py.
      - create an adopter.py.
    - with firebase auth:
      - add to the pyporject.toml. ✅
      - setup to the settings.py.
      - setup to the urls.py.
      - setup to the views.py.
      - setup to the serializers.py.
      - create an authentication.py.
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
    - add drf-spectacular pyporject.toml. ✅
    - setup drf-spectacular to the settings.py.
    - setup drf-spectacular to the urls.py with .env to disable the route if needed.
  - Django-ninja:
    - with Jwt auth
    - with firebase auth
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - GraphQL with graphene:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - GraphQL with ariadne:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - GraphQL with strawberry:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
- Selecting a background task from the following options:
  - Django-q:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - Celery:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
- Selecting a production_storage from the following options:
  - filesystem. ✅
  - MinIO:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - Amazon S3:
    - add to the pyporject.toml. ✅
    - setup to the settings.py.
  - Dropbox:
    - add to the pyporject.toml. ✅
    - setup to the settings.py. ✅
- Enable django-dbbackup for backup (Optional):
  - add to the pyporject.toml. ✅
  - setup to the settings.py.
- Enable redis (Optional):
  - add to the pyporject.toml. ✅
  - setup to the settings.py.
- Enable sentry (Optional):
  - add to the pyporject.toml. ✅
  - setup to the settings.py.
- Enable mkdocs (Optional):
  - add to the pyporject.toml. ✅
- Selecting from `pycharm` or `vscode`:
  - pycharm:
    - create configuration folder.
  - vscode:
    - create configuration folder. ✅
- Selecting a platform for deployment from the following options:
  - heroku:
    - create Procfile. ✅
  - qovery:
    - create Dockerfile.
- Selecting a license. ✅
