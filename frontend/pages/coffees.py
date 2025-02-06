import flet as ft
from flet import Row, Text

def show_coffees_page(page: ft.Page) -> None:
    """
    Функция для отображения страницы с кофе.
    """
    page.clean()
    page.add(
        Row(
            controls=[Text("Добро пожаловать на страницу кофе!", size=24, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )