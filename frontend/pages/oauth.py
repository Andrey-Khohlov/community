import httpx

from app.config import settings
import flet as ft
from flet.auth.providers import GoogleOAuthProvider, GitHubOAuthProvider

from . import API_URL


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
        on_click=lambda e: page.login_async(github_provider, scope=["user:email"])
    )
    login_google_btn.on_click = login_google
    login_github_btn.on_click = login_github

    logout_btn = ft.ElevatedButton("Выйти", visible=False)

    def toggle_ui():
        is_logged_in = page.auth is not None
        login_google_btn.visible = not is_logged_in
        login_github_btn.visible = not is_logged_in
        logout_btn.visible = is_logged_in
        page.update()

    def check_user(username, email, provider_id, provider):
        # TODO: функция бэкенда
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
            if user["email"] == email:
                return user
        else:
            # Если пользователь не найден, добавить его в базу данных
            user = {"username": username, "email": email, "password": ""}
            user_response = httpx.post(f"{API_URL}/v1/users/", json=user)
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
                if user["email"] == email:
                    return user
            else:
                return None


    def on_login(e: ft.LoginEvent):
        if not e.error:
            print(f"Logged in: {page.auth.user}")
            # TODO: проверить по базе по provider_id, если нет, то добавить
            if isinstance(page.auth.provider, GoogleOAuthProvider):
                provider = 'Google'
                username = page.auth.user["given_name"]
                email = page.auth.user["email"]
                provider_id = page.auth.user["sub"]
                user = check_user(username, email, provider_id, provider)
                page.session.set("user", user)
            elif isinstance(page.auth.provider, GitHubOAuthProvider):
                # TODO: добавить GitHub
                provider = 'GitHub'
                username = page.auth.user["login"]
                email = page.auth.user["email"]
                provider_id = page.auth.user["id"]
                user = check_user(username, email, provider_id, provider)
                page.session.set("user", user)

            else:
                print("Login provider not implemented")

            toggle_ui()
            # Перенаправление на сохранённый маршрут
            target = getattr(page, "redirect_after_login", "/")
            page.redirect_after_login = "/"
            page.go(target)
        else:
            print("Login error:", e.error)

    def on_logout(e):
        print("User logged out")
        toggle_ui()

    logout_btn.on_click = lambda e: page.logout()
    page.on_login = on_login
    page.on_logout = on_logout
    toggle_ui()

    return ft.View(
        "/login",
        controls=[
            ft.Column([
                ft.Text("Авторизоваться:", size=20),
                ft.Column([login_google_btn, login_github_btn], spacing=10, alignment=ft.MainAxisAlignment.START),
                logout_btn
            ])
        ]
    )