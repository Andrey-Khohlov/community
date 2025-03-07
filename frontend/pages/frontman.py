import os

import flet as ft
from .coffees import coffee_list
from .discussion import discussion


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.title = "Q90 online"

    def route_change(route):
        page.views.clear()
        print(page.route)
        if page.route == "/" or page.route == "/coffees":
             page.views.append(coffee_list(page))
        elif page.route.startswith("/discussion/"):
            coffee_id = int(page.route.split("/")[-1])
            page.views.append(discussion(page, coffee_id))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        ft.app(target=main, view=ft.WEB_BROWSER, port=8550)  # host="0.0.0.0",
    else:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)