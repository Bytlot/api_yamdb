# API YAMDB


## About

API Service where people can leave reviews for films, books, and musical compositions.

---

## Functionality

Getting confirmation code using email and then Auth with JWT-token.
Permission system for different roles: admin/moderator/user.
CRUD title, category, genre, review, comment.

---

## Technology stack

- Django
- Django REST
- Simple JWT
- PostgreSQL

---

## Documentation

Start app:
```
git clone https://github.com/Bytlot/api_yamdb

python -m pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
API documentation available at: http://localhost/redoc/

## License

MIT License