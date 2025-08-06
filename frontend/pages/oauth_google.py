from app.config import settings
import flet
from flet import ElevatedButton, LoginEvent, Page
from flet.auth.providers import GoogleOAuthProvider


def main(page: Page):
    # Настройка Google OAuth
    provider = GoogleOAuthProvider(
        client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
        client_secret=settings.OAUTH_GOOGLE_CLIENT_SECRET,
        # authorization_endpoint="https://accounts.google.com/o/oauth2/auth",
        # token_endpoint="https://oauth2.googleapis.com/token",
        # userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        redirect_url="http://localhost:8550/oauth_callback",

    )

    def login_button_click(e):
        page.login(
            provider,
            scope=[
                "openid",
                "email",
                "profile",
                # "https://www.googleapis.com/auth/user.addresses.read",
            ])

    def on_login(e: LoginEvent):
        print("Login error:", e.error)
        print("user", page.auth.user)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)
        print("Name:", page.auth.user["given_name"])
        print("Login:", page.auth.user["name"])
        print("Email:", page.auth.user["email"])
        print("Avatar:", page.auth.user["picture"])
        # print("location:", page.auth.user["addresses"])
        if not e.error:
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        if page.auth:
            user_email = page.auth.user.get("email", "Unknown user")
            user_name = page.auth.user.get("name", "No name")
            user_info.value = f"Logged in as: {user_name} ({user_email})"
        else:
            user_info.value = "Not logged in"
        page.update()

    login_button = ElevatedButton("Login with Google", on_click=login_button_click)
    logout_button = ElevatedButton("Logout", on_click=logout_button_click)
    user_info = flet.Text("Not logged in")

    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button, user_info)


flet.app(main, port=8550, view=flet.WEB_BROWSER)