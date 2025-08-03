import os

import flet as ft
from flet.auth.providers import GoogleOAuthProvider, GitHubOAuthProvider
from app.config import settings


def main(page: ft.Page):
    google_provider = GoogleOAuthProvider(
        client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
        client_secret=settings.OAUTH_GOOGLE_CLIENT_SECRET,
        redirect_url="http://localhost:8550/v1/auth/google/callback",
    )

    github_provider = GitHubOAuthProvider(
        client_id=settings.OAUTH_GITHUB_CLIENT_ID,
        client_secret=settings.OAUTH_GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",
    )

    def google_provider_login_click(e):
        page.login(
            google_provider,
            scope=[
                "openid",
                "profile",
                "email",
            ]
        )

    def github_provider_login_click(e):
        page.login(
            github_provider,
            scope=["public_repo"]
        )
    def on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

    page.on_login = on_login
    page.add(ft.ElevatedButton("Войти с Google", on_click=google_provider_login_click))
    page.add(ft.ElevatedButton("Войти с GitHub", on_click=github_provider_login_click))

ft.app(main, port=8550, view=ft.WEB_BROWSER)