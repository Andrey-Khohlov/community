import os

import flet as ft
import httpx
from  flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent

from  frontend.pages.coffees import show_coffees_page
from . import API_URL

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
    checkbox_signup: Checkbox = Checkbox(label='Я сегодня пил кофе', value=False)
    button_submit: ElevatedButton = ElevatedButton(text="Вперёд к вкусному кофе!", width=250, disabled=True)
    error_message: Text = Text(value="", color="red")  # Создаем текстовое поле для сообщения об ошибке

    def validate(event: ControlEvent) -> None:
        if all([text_username.value, text_password.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True
        page.update()

    def submit(event: ControlEvent) -> None:
        """Проверяет, находится ли пользователь в базе данных и перенаправляет на страницу /coffees"""
        print('Username:', text_username.value)
        print('Password:', text_password.value)
        # Запрос к API
        try:
            response = httpx.get(f"{API_URL}/v1/users", follow_redirects=True)
            response.raise_for_status()  # Проверяем успешность запроса
        except httpx.RequestError as e:
            page.add(ft.Text(f"HTTP Request failed: {e}", color="red"))
            return
        except httpx.HTTPStatusError as e:
            page.add(ft.Text(f"HTTP Error: {e.response.status_code}", color="red"))
            return
        # Проверяем, находится ли пользователь в базе данных
        for user in response.json()["Ok"]:
            if user["username"] == text_username.value and user["password"] == text_password.value:
                page.session.set("user", user) # Сохраняем пользователя в sessionStorage
                page.go("/coffees")
                return
        else:
            # Если пользователь не найден, выводим сообщение об ошибке
            error_message.value = "Неверное имя пользователя или пароль"
            page.update()
        return

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
                        button_submit,
                        error_message,]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    # Обработчик маршрутов
    def route_change(route):
        if page.route == "/coffees":
            show_coffees_page(page)  # Используем функцию из отдельного файла

    # Подписываемся на изменения маршрута
    page.on_route_change = route_change
    page.update()


if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
    else:
        ft.app(target=main)