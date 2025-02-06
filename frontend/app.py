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


ft.app(target=main)