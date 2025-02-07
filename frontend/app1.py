# https://github.com/TonyXdZ/flet-base

import flet as ft
from flet_model import Model, Router
from pages.home import HomeModel
from pages.login import LoginModel
from pages.signup import SignUpModel

def main(page: ft.Page):
    page.title = "Flet Boilerplate"
    page.window.height = 712
    page.window.width = 375
    Router(
        {'login': LoginModel(page)},
        {'home': HomeModel(page)},
        {'signup': SignUpModel(page)},
    )
    page.go(page.route)

# def route_change(route):
#     if page.route == "/login":
#         from login_page import show_login_page
#         show_login_page(page)
#     elif page.route == "/signup":
#         from signup_page import show_signup_page
#         show_signup_page(page)
#     elif page.route == "/coffees":
#         from coffees_page import show_coffees_page
#         show_coffees_page(page)

ft.app(target=main)