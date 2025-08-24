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
)
```

3. Проверка подлинности токена на бэкенде

В FastAPI:

```python
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token: str):
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    return idinfo  # словарь с sub, email, name, picture, ...
```
Здесь FastAPI проверит подпись токена Google, аудиторию и срок жизни.

Если токен фейковый или устарел — сразу 401.

4. Поиск или создание пользователя в БД

В PostgreSQL:

Ищем пользователя по sub (Google ID) или email.

Если нет — создаём запись в users:

```sql

id | email          | name     | avatar_url | provider | provider_id
---+----------------+----------+------------+----------+-------------
 1 | user@mail.com  | Alice    | ...        | google   | 1122334455
```
 
# Вам не нужен JWT для общения между вашим Flet-клиентом и вашим же бэкендом. 

page.session идеально справляется с ролью хранилища состояния аутентификации. Роль бэкенда — превратить одноразовый токен провайдера в постоянный, надежный и простой идентификатор пользователя в вашей системе и отдать его фронтенду для хранения в сессии.

Отличный вопрос, который затрагивает ключевую архитектурную дилемму при использовании Flet.

**Короткий ответ:** Нет, в классическом понимании передавать JWT токен с бэкенда на фронтенд **не нужно** и это было бы избыточно. Сессия Flet (`page.session`) — это и есть ваш механизм аутентификации и хранения состояния на стороне клиента.

Давайте разберем подробнее, почему это так и как правильно выстроить流程.

### 1. Роль `page.session` в Flet

Flet — это не просто фронтенд-фреймворк, это полноценный клиент-серверный фреймворк. Когда пользователь открывает ваше Flet-приложение, между браузером (клиентом) и сервером Flet устанавливается **долгоживущее постоянное соединение** (через WebSockets).

`page.session` — это встроенное хранилище данных на стороне *клиента*, которое:
*   Привязано к конкретной вкладке браузера.
*   Существует в течение всей жизни сессии (пока пользователь не закроет вкладку).
*   **Является идеальным местом для хранения факта аутентификации и идентификатора пользователя.**

Вам не нужно изобретать свой велосипед с JWT для хранения состояния на клиенте, потому что Flet уже предоставляет для этого готовый, безопасный и удобный механизм — `page.session`.

### 2. Правильная схема авторизации

Вот как должен выглядеть流程 (flow):

1.  **Фронтенд (Flet) получает токен от провайдера:**
    *   Вы используете фронтенд-библиотеку (например, `google_sign_in` для Flutter или JS-библиотеку Google) для получения `access_token` от Google/GitHub на стороне клиента.

2.  **Фронтенд передает токен на бэкенд (FastAPI):**
    *   Flet-клиент отправляет HTTP-запрос (например, через `httpx`) на ваш эндпоинт FastAPI, скажем, `POST /auth/google`, передавая в теле запроса полученный `access_token`.
    *   **Важно:** Убедитесь, что используете HTTPS для защиты токена при передаче.

3.  **Бэкенд (FastAPI) валидирует токен и получает данные:**
    *   FastAPI-сервер получает `access_token`.
    *   Сервер самостоятельно отправляет запрос к API провайдера (например, к `https://www.googleapis.com/oauth2/v3/userinfo`) с этим токеном, чтобы получить гарантированно достоверные данные пользователя (`email`, `name`, `id` и т.д.).
    *   **Здесь ключевой момент: бэкенд доверяет только тому, что сказал ему провайдер, а не тому, что прислал клиент.** Это защищает от подделки токена.

4.  **Бэкенд создает или находит пользователя в БД:**
    *   На основе полученного `email` или `id` провайдера бэкенд ищет существующего пользователя в вашей базе данных или создает нового.
    *   Бэкенд генерирует свой **внутренний идентификатор пользователя** (например, первичный ключ `user_id` из вашей таблицы `users`). Этот ID — основа для вашей бизнес-логики.

5.  **Бэкенд отвечает фронтенду:**
    *   Бэкенд отправляет ответ на Flet-клиент. В ответе **НЕ JWT**, а просто факт успешной аутентификации и, возможно, тот самый **внутренний `user_id`** (или username, email) и другая информация, нужная для отображения UI (имя пользователя, аватар).
    *   Ответ может быть простым: `{"success": true, "user_id": 123, "email": "user@example.com", "full_name": "John Doe"}`.

6.  **Фронтенд (Flet) сохраняет состояние в сессии:**
    *   Получив успешный ответ от бэкенда, Flet-клиент сохраняет полученные данные в `page.session`.
    ```python
    # Пример на Flet
    import httpx
    # ... шаги 1-2 ...
    
    # Предположим, мы получили токен от Google на клиенте
    provider_token = ... 

    # Шаг 2-3: Отправка токена на бэкенд
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://your-fastapi-backend.com/auth/google",
            json={"token": provider_token}
        )
        if response.status_code == 200:
            data = response.json()
            # Шаг 6: Сохранение в сессию
            page.session.set("user_authenticated", True)
            page.session.set("user_id", data["user_id"])
            page.session.set("user_email", data["email"])
            page.session.set("user_name", data["full_name"])
            
            # Обновляем UI (например, показываем аватарку и кнопку "Выйти")
            update_ui_after_login()
        else:
            # Показываем ошибку
            show_error_dialog()
    ```

7.  **Дальнейшие запросы к бэкенду:**
    *   При последующих вызовах вашего FastAPI бэкенда (для получения конфиденциальных данных), Flet-клиент будет передавать в запросе тот самый **внутренний `user_id`** (или другой идентификатор), который он сохранил в сессии.
    *   Бэкенд будет проверять этот ID и решать, имеет ли пользователь право на доступ к запрашиваемым данным.
    *   **Важно:** Все критические endpoints на FastAPI должны проверять этот идентификатор и права доступа.

### Резюме: Кто за что отвечает?

| Компонент | Что делает? | Что хранит? |
| :--- | :--- | :--- |
| **Фронтенд (Flet)** | Получает токен провайдера. Передает его на бэкенд. Сохраняет ответ бэкенда (ID пользователя) в `page.session`. | `page.session['user_id']`, `page.session['user_email']` |
| **Бэкенд (FastAPI)** | **Валидирует** токен провайдера. Получает данные пользователя. Создает/ищет запись в БД. Генерирует **внутренний ID**. Отправляет его фронтенду. | Ваша база данных с таблицей `users`. Связь `google_id` -> `user_id`. |
| **Провайдер (Google)** | Выдает токен. Предоставляет эндпоинт для получения данных пользователя по этому токену. | Данные пользователя в своем аккаунте. |

**Итог:** Вам не нужен JWT для общения между вашим Flet-клиентом и вашим же бэкендом. `page.session` идеально справляется с ролью хранилища состояния аутентификации. Роль бэкенда — превратить одноразовый токен провайдера в постоянный, надежный и простой идентификатор пользователя *в вашей системе* и отдать его фронтенду для хранения в сессии.