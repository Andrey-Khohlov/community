pyjwt, AuthX

Введение в OAuth 
https://dzen.ru/a/XsTMHgM7H2vsTOg2

Библиотека Python:
Authlib

Консоль Google
https://console.cloud.google.com/

https://developers.google.com/identity/protocols/oauth2?hl=ru
https://developers.google.com/identity/openid-connect/openid-connect?hl=ru#obtainuserinfo

{'sub': '', 
'name': 'А Х', 
'given_name': 'А', 
'family_name': 'Х', 
'picture': 'https://lh3.googleusercontent.com/', 
'email': 'example@gmail.com', 
'email_verified': True}

консоль GitHub
https://github.com/settings/apps

{'login': '..., 
'id': ..., 
'node_id': '...', 
'avatar_url': 'https://avatars.githubusercontent.com/u/...v=4', 
'gravatar_id': '', 
'url': 'https://api.github.com/users/...', 
'html_url': 'https://github.com/...', 
'followers_url': 'https://api.github.com/users/.../followers', 
'following_url': 'https://api.github.com/users/.../following{/other_user}', 
'gists_url': 'https://api.github.com/users/.../gists{/gist_id}', 
'starred_url': 'https://api.github.com/users/.../starred{/owner}{/repo}', 
'subscriptions_url': 'https://api.github.com/users/.../subscriptions', 
'organizations_url': 'https://api.github.com/users/.../orgs', 
'repos_url': 'https://api.github.com/users/.../repos', 
'events_url': 'https://api.github.com/users/.../events{/privacy}', 
'received_events_url': 'https://api.github.com/users/.../received_events', 
'type': 'User', 
'user_view_type': 'private', 
'site_admin': False, 
'name': 'A', 
'company': None, 
'blog': '', 
'location': 'Moscow, Some_City', 
'email': 'example@ya.ru', 
'hireable': True, 
'bio': None, 
'twitter_username': None, 
'notification_email': 'example@ya.ru', 
'public_repos': 12, 
'public_gists': 0, 
'followers': 0, 
'following': 2, 
'created_at': '2020-08-24T04:56:43Z', 
'updated_at': '2020-08-10T21:29:30Z', 
'private_gists': 0, 
'total_private_repos': 2, 
'owned_private_repos': 2, 
'disk_usage': 57373, 
'collaborators': 0, 
'two_factor_authentication': True, 
'plan': {'name': 'free', 'space': 976500099, 'collaborators': 0, 'private_repos': 10000}}

### как правильно построить авторизацию через Google
[Пользователь] 
    ↓ (1) Google OAuth Login
[Flet] 
    ↓ (2) ID Token
[FastAPI] 
    ↓ (3) Проверка подлинности Google токена
[FastAPI] 
    ↓ (4) Создание/поиск пользователя в БД
[FastAPI] 
    ↓ (5) Выдача JWT приложения
[Flet] 
    ↓ (6) Запросы к API с JWT
[FastAPI]
    ↓ (7) Проверка JWT, выполнение запросов

🔸 Подробно по шагам
1. Авторизация через Google на фронтенде
Flet вызывает встроенный механизм page.login() (или кастомный OAuth flow) и получает от Google ID Token.

Этот ID Token — это подписанный JWT, в котором есть:

sub — уникальный ID пользователя в Google

email

name

picture

iss — https://accounts.google.com

aud — твой client_id

exp — срок жизни токена

2. Передача ID Token на бэкенд
Вместо пересылки всех данных из page.auth.user на бэкенд отправляется только ID Token:

```python

httpx.post(
    "https://api.example.com/auth/google",
    json={"id_token": page.auth.token["id_token"]}
)```
3. Проверка подлинности токена на бэкенде
В FastAPI:

```python

from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token: str):
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    return idinfo  # словарь с sub, email, name, picture, ...```
Здесь FastAPI проверит подпись токена Google, аудиторию и срок жизни.

Если токен фейковый или устарел — сразу 401.

4. Поиск или создание пользователя в БД
В PostgreSQL:

Ищем пользователя по sub (Google ID) или email.

Если нет — создаём запись в users:

```sql

id | email          | name     | avatar_url | provider | provider_id
---+----------------+----------+------------+----------+-------------
 1 | user@mail.com  | Alice    | ...        | google   | 1122334455```
 
5. Выдача JWT приложения
После успешной проверки создаём свой JWT с минимальной информацией:

```python

from datetime import datetime, timedelta
import jwt

SECRET_KEY = "supersecret"

def create_app_jwt(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")```
    
Отправляем фронтенду:

```json

{
    "access_token": "<jwt>",
    "token_type": "bearer",
    "user": {
        "email": "...",
        "name": "...",
        "avatar_url": "..."
    }
}```

6. Хранение JWT на фронтенде
В Flet хранить токен в памяти (page.session или переменная) или в защищённых cookies (если браузер).

Не класть в localStorage — легко украсть.

7. Запросы к API
Все запросы к FastAPI идут с заголовком:

```makefile

Authorization: Bearer <jwt>```

FastAPI middleware проверяет подпись токена и exp.

Достаёт user_id и подгружает пользователя из БД.

🔹 Что мы выиграли
Данные от Google валидируются только на бэкенде.

page.auth.user не используется как источник истины.

Google токены не хранятся на фронте.

Свой JWT упрощает работу с авторизацией в API.

Возможна привязка пароля или других соцсетей к одному аккаунту.