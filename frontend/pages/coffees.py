import os

import flet as ft
import httpx

from .discussion import discussion
from . import API_URL


def fetch_coffees():
    """Функция для получения данных о кофе с бэкенда."""
    # Запрос к API
    try:
        response = httpx.get(f"{API_URL}/v1/coffees/", follow_redirects=True)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()["Ok"]
    except httpx.RequestError as e:
        return [f"HTTP Request failed: {e}"]
    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e.response.status_code}",


def show_coffees_page(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Список кофе"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.clean()

    coffees = fetch_coffees()

    # Создаем контейнер для карточек
    cards_list = ft.ListView(expand=True, spacing=20)

    # Заполняем таблицу данными
    for coffee in coffees:
        card = ft.GestureDetector(
            content=ft.Card(
                color=ft.colors.GREY_900,
                content=ft.Container(
                    content=ft.Column(
                        [
                            # Первая строка
                            ft.Row(
                                [
                                    ft.Text(coffee["title"], weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_500),
                                    ft.Text(f'урожай {coffee["yield_"]},'),
                                    ft.Text(coffee["processing"]),
                                    ft.Text(f'{coffee["variety"]},'),
                                    ft.Text(f'высота {coffee["height_min"] if coffee["height_min"] != coffee["height_max"] else " "} - {coffee["height_max"]} м,'),
                                ],
                                spacing=10,  # Расстояние между элементами в строке
                            ),
                            # Вторая строка
                            ft.Row(
                                [
                                    ft.Text(f'{coffee["origin"]},'),
                                    ft.Text(f'{coffee["region"]},'),
                                    ft.Text(f'ферма/станция: {coffee["farm"]},'),
                                    ft.Text(f'производитель: {coffee["farmer"]},'),

                                ],
                                spacing=10,
                            ),
                            # Третья строка
                            ft.Row(
                                [
                                    ft.Text(coffee["roaster"]),
                                    ft.Text(f'{coffee["price"]} руб за {coffee["weight"]} г,'),
                                    ft.Text(f'Q-оценка: {coffee["q_grade_rating"]},'),
                                    ft.Text(f'рейтинг: {coffee["rating"]},'),
                                    ft.Text(f'отзывов: {coffee["reviews"]},'),
                                    ft.Text(f'комментариев: {coffee["comments"]},'),
                                    ft.Text(f'обжарка под {coffee["roasting_level"]}'),
                                ],
                                spacing=10,
                            ),
                            # Четвертая строка
                            ft.Row(
                                [

                                    ft.Text(coffee["description"], max_lines=2),
                                ],
                                spacing=10,
                            ),
                        ],
                        # spacing=5,  # Расстояние между строками
                    ),
                    padding=ft.padding.all(5),
                ),
                elevation=20,  # Тень по умолчанию
            ),
            on_tap=lambda e, coffee_id=coffee["id"]: page.go(f"/discussion/{coffee_id}"),  # Обработка нажатия
            on_hover=lambda e: setattr(e.control.content, "elevation", 8 if e.data == "true" else 2),
            # Увеличиваем тень при наведении
            mouse_cursor=ft.MouseCursor.CLICK,
        )
        cards_list.controls.append(card)

    page.add(cards_list)

    # Обработка изменений маршрута
    def route_change(route) -> None:
        if page.route.startswith("/discussion/"):
            coffee_id = int(page.route.split("/")[-1] ) # Извлекаем ID кофе из URL
            discussion(page, coffee_id)
        elif page.route == "/coffees":
            show_coffees_page(page)


    # Подписываемся на изменения маршрута
    page.on_route_change = route_change
    page.update()

if __name__ == "__main__":
    ft.app(target=show_coffees_page)  # , view=ft.WEB_BROWSER, port=8550