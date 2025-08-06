import os

from app.config import settings
import flet
from flet import ElevatedButton, LoginEvent, Page
from flet.auth.providers import GitHubOAuthProvider

def main(page: Page):
    provider = GitHubOAuthProvider(
        client_id=settings.OAUTH_GITHUB_CLIENT_ID,
        client_secret=settings.OAUTH_GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",
    )

    def login_button_click(e):
        page.login(provider)

    def on_login(e: LoginEvent):
        print("Login error:", e.error)
        print("user", page.auth.user)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)
        print("Name:", page.auth.user["name"])
        print("Login:", page.auth.user["login"])
        print("Email:", page.auth.user["email"])
        print("Avatar:", page.auth.user["avatar_url"])
        print("location:", page.auth.user["location"])
        if not e.error:
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    login_button = ElevatedButton("Login with GitHub", on_click=login_button_click)
    logout_button = ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)

flet.app(main, port=8550, view=flet.WEB_BROWSER)