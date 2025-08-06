from pathlib import Path

from app.config import settings
import flet as ft
from flet.auth.providers import GoogleOAuthProvider, GitHubOAuthProvider


def main(page: ft.Page):
    # Настройка провайдеров
    google_provider = GoogleOAuthProvider(
        client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
        client_secret=settings.OAUTH_GOOGLE_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback"
    )

    github_provider = GitHubOAuthProvider(
        client_id=settings.OAUTH_GITHUB_CLIENT_ID,
        client_secret=settings.OAUTH_GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback"
    )

    # Элементы UI
    # login_google_btn = ft.ElevatedButton("Login with Google", visible=True)
    # login_github_btn = ft.ElevatedButton("Login with GitHub", visible=True)

    # Создаем кнопки с иконками
    login_google_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Image(
                    src="images/google-logo.svg",
                    width=24,
                    height=24,
                ),
                ft.Text("Войти через Google"),
            ],
            spacing=10,
        ),
        on_click=lambda e: page.login_async(google_provider, scope=["openid", "email", "profile"]),
        style=ft.ButtonStyle(
            padding=ft.Padding(15, 10, 15, 10),
        )
    )

    login_github_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Image(
                    src="images/github-logo.svg",
                    width=24,
                    height=24,
                ),
                ft.Text("Войти через GitHub"),
            ],
            spacing=10,
        ),
        on_click=lambda e: page.login_async(github_provider, scope=["user:email"]),
        style=ft.ButtonStyle(
            padding=ft.Padding(15, 10, 15, 10),
        )
    )

    logout_btn = ft.ElevatedButton("Выйти", visible=False)
    user_info = ft.Text("Not logged in")
    provider_info = ft.Text("")

    def toggle_ui():
        """Обновляем видимость кнопок в зависимости от состояния авторизации"""
        is_logged_in = page.auth is not None
        login_google_btn.visible = not is_logged_in
        login_github_btn.visible = not is_logged_in
        logout_btn.visible = is_logged_in

        if is_logged_in:
            user = page.auth.user
            provider = "Google" if isinstance(page.auth.provider, GoogleOAuthProvider) else "GitHub"
            user_email = user.get("email", "No email")
            user_name = user.get("name", user.get("login", "Unknown"))
            avatar = user.get("picture") or user.get("avatar_url")

            user_info.value = f"Logged in via {provider} as: {user_name} ({user_email})"
            provider_info.value = f"Provider: {provider}"

            if avatar:
                user_info.value += f"\nAvatar: {avatar}"
        else:
            user_info.value = "Not logged in"
            provider_info.value = ""

        page.update()

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

    def logout(e):
        page.logout()

    def on_login(e: ft.LoginEvent):
        if not e.error:
            provider = "Google" if isinstance(page.auth.provider, GoogleOAuthProvider) else "GitHub"
            print(f"Successful login via: {provider}")
            print("User data:", page.auth.user)
            toggle_ui()
        else:
            print("Login error:", e.error)

    def on_logout(e):
        print("User logged out")
        toggle_ui()

    # Назначаем обработчики
    login_google_btn.on_click = login_google
    login_github_btn.on_click = login_github
    logout_btn.on_click = logout
    page.on_login = on_login
    page.on_logout = on_logout

    # Добавляем элементы на страницу
    page.add(
        ft.Column([
            ft.Text("Login with:", size=20),
            ft.Row([login_google_btn, login_github_btn], spacing=10),
            logout_btn,
            user_info,
            provider_info
        ], spacing=15)
    )

    # Инициализация UI
    toggle_ui()


ft.app(main, port=8550, view=ft.WEB_BROWSER, assets_dir="assets")