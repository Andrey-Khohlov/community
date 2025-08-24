import json
import logging
from datetime import datetime

import httpx
from pygments.styles.dracula import background

from app.api.v1.endpoints.users import add_user
from app.config import settings
import flet as ft
from flet.auth.providers import GoogleOAuthProvider, GitHubOAuthProvider

from app.schemas.users import UsersAddSchema
from . import API_URL
from .discussion import MINOR_COLOR, MAIN_COLOR, FONT_COLOR


# logging.basicConfig(level=logging.DEBUG)

def login_page(page: ft.Page, redirect_route="/"):
    # Настройка провайдеров
    google_provider = GoogleOAuthProvider(
        client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
        client_secret=settings.OAUTH_GOOGLE_CLIENT_SECRET,
        redirect_url="https://q90.online/oauth_callback"
    )
    github_provider = GitHubOAuthProvider(
        client_id=settings.OAUTH_GITHUB_CLIENT_ID,
        client_secret=settings.OAUTH_GITHUB_CLIENT_SECRET,
        redirect_url="https://q90.online/oauth_callback",
    )

    async def login_google(e):
        await page.login_async(
            google_provider,
            scope=["openid", "email", "profile"]
        )

    async def login_github(e):
        await page.login_async(
            github_provider,
            scope=["user:email"]
        )

    login_google_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Image(
                    src="images/google-logo.svg",
                    width=24,
                    height=24,
                ),
                ft.Text("войти через Google"),
            ],
            spacing=10,
        ),
        width=240,  # Фиксированная ширина
        bgcolor=MAIN_COLOR,
        color=FONT_COLOR,
        on_click=lambda e: page.login_async(google_provider, scope=["openid", "email", "profile"])
    )
    login_github_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Image(
                    src="images/github-logo.svg",
                    width=24,
                    height=24,
                ),
                ft.Text("войти через GitHub"),
            ],
            spacing=10,
        ),
        width=240,  # Фиксированная ширина
        color=FONT_COLOR,
        bgcolor=MAIN_COLOR,
        on_click=lambda e: page.login_async(github_provider, scope=["user:email"])
    )
    login_google_btn.on_click = login_google
    login_github_btn.on_click = login_github

    logout_btn = ft.ElevatedButton("Выйти из аккаунта", color=FONT_COLOR, bgcolor=MAIN_COLOR, visible=False)

    def toggle_ui():
        is_logged_in = page.auth is not None
        login_google_btn.visible = not is_logged_in
        login_github_btn.visible = not is_logged_in
        logout_btn.visible = is_logged_in
        page.update()

    def check_user(user_from_provider: dict):
        # TODO: функция бэкенда
        # TODO на бэке Неча таскать пользователей из базы, надо туда запрос отправлять
        try:
            user_response = httpx.get(f"{API_URL}/v1/users", follow_redirects=True)
            user_response.raise_for_status()  # Проверяем успешность запроса
        except httpx.RequestError as e:
            page.add(ft.Text(f"HTTP Request failed: {e}", color="red"))
            return None
        except httpx.HTTPStatusError as e:
            page.add(ft.Text(f"HTTP Error: {e.response.status_code}", color="red"))
            return None
        # Проверяем, находится ли пользователь в базе данных
        for user in user_response.json()["Ok"]:
            if user["provider_id"] == user_from_provider["provider_id"] and user["provider"] == user_from_provider["provider"]:
                return user
        else:
            # Если пользователь не найден, добавить его в базу данных
            user_from_provider.update({"is_active": True, "roles": "user"})
            logging.info(f'Добавляем в базу user_from_provider: {user_from_provider}')
            user_response = httpx.post(f"{API_URL}/v1/users/", json=user_from_provider)
            user_response.raise_for_status()  # Проверяем успешность запроса

            # получим этого пользователя из базы, чтобы передать его дальше
            try:
                user_response = httpx.get(f"{API_URL}/v1/users", follow_redirects=True)
                user_response.raise_for_status()  # Проверяем успешность запроса
            except httpx.RequestError as e:
                page.add(ft.Text(f"HTTP Request failed: {e}", color="red"))
                return None
            except httpx.HTTPStatusError as e:
                page.add(ft.Text(f"HTTP Error: {e.response.status_code}", color="red"))
                return None
            # Проверяем, находится ли пользователь в базе данных
            for user in user_response.json()["Ok"]:
                if user["provider_id"] == user_from_provider['provider_id'] and user["provider"] == user_from_provider['provider']:
                    return user
            else:
                return None


    def on_login(e: ft.LoginEvent):
        if not e.error:
            # отправить токен на бэк, в ответ получить имя, аватар, id
            # id, avatar, user_name = check_user(page.auth.token)

            # проверяет по базе по provider_id, если нет, то добавляет
            if isinstance(page.auth.provider, GoogleOAuthProvider):
                user_from_provider = {
                    "provider": 'google',
                    "username": page.auth.user["given_name"],
                    "email": page.auth.user["email"],
                    "password": None,
                    "provider_id": page.auth.user["sub"],
                    "avatar_url": page.auth.user["picture"],
                    "is_verified": page.auth.user["email_verified"],
                    "locality": None,
                    "language": None,
                    # "is_active": True,
                    # "roles": "user",
                }
                user = check_user(user_from_provider)
                page.session.set("user", user)

            elif isinstance(page.auth.provider, GitHubOAuthProvider):
                user_from_provider = {
                    "provider": 'github',
                    "username": page.auth.user["name"],
                    "email": page.auth.user["email"],
                    "password": None,
                    "provider_id": str(page.auth.user["id"]),
                    "avatar_url": page.auth.user["avatar_url"],
                    "is_verified": True,
                    "locality": page.auth.user["location"],
                    "language": None,
                    # "is_active": True,
                    # "roles": "user",
                }
                user = check_user(user_from_provider)
                page.session.set("user", user)
            else:
                print("Login provider not implemented")

            toggle_ui()
            # Перенаправление на сохранённый маршрут
            target = page.session.get("return_url") or "/coffees"
            page.go(target)
        else:
            print("Login error:", e.error)

    def on_logout(e):
        if page.auth is None:  # Если уже вышли
            return

        logging.info(f"Performing logout {page.auth}")
        page.client_storage.remove(AUTH_TOKEN_KEY)
        page.logout()  # Основной выход
        page.session.remove("user")  # Очищаем сессию

        # Редирект
        target = page.session.get("return_url") or "/coffees"
        page.go(target)

    logout_btn.on_click = on_logout
    page.on_login = on_login
    page.on_logout = on_logout
    toggle_ui()

    return ft.View(
        "/login",
        controls=[
            ft.Column([
                ft.Text("Авторизация:", size=20),
                ft.Column([login_google_btn, login_github_btn], spacing=10, alignment=ft.MainAxisAlignment.START),
                logout_btn
            ])
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=MINOR_COLOR,
    )