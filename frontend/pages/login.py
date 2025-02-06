from logging import disable

import flet as ft
from  flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent

from coffees import show_coffees_page


def main(page: ft.Page) -> None:
    page.title = "Signup"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False

    # Set our fields
    text_username: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label='Я согласен с правилами использования', value=False)
    button_submit: ElevatedButton = ElevatedButton(text="Вперёд к вкусному кофе!", width=200, disabled=True)

    def validate(event: ControlEvent) -> None:
        if all([text_username.value, text_password.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True
        page.update()

    def submit(event: ControlEvent) -> None:
        print('Username:', text_username.value)
        print('Password:', text_password.value)
        # Переход на страницу /coffees
        page.go("/coffees")

        # page.clean()
        # page.add(
        #     Row(
        #         controls=[Text("Вперёд к вкусному кофе!", size=24, weight=ft.FontWeight.BOLD)],
        #         alignment=ft.MainAxisAlignment.CENTER
        #     )
        # )

    checkbox_signup.on_change = validate
    text_username.on_change = validate
    text_password.on_change = validate
    button_submit.on_click = submit

    # Render our sign-up page
    page.add(
        Row(
            controls=[
                Column(
                        [text_username,
                        text_password,
                        checkbox_signup,
                        button_submit,]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    # Обработчик маршрутов
    # Обработчик маршрутов
    def route_change(route):
        if page.route == "/coffees":
            show_coffees_page(page)  # Используем функцию из отдельного файла

    # Подписываемся на изменения маршрута
    page.on_route_change = route_change
    page.update()


if __name__ == "__main__":
    ft.app(target=main)