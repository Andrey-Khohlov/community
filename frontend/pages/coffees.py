import os
import logging

import flet as ft
import httpx

from .discussion import FONT_COLOR, MEDIUM_COLOR, MAIN_COLOR, MINOR_COLOR
from . import API_URL


logging.basicConfig(level=logging.INFO)

def on_hover(e):
    e.control.bgcolor = MEDIUM_COLOR if e.data == "true" else MAIN_COLOR # '#FF5A4A42'
    e.control.update()

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


def coffee_list(page: ft.Page):
    # page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = MINOR_COLOR
    page.title = "кофе, о котором надо поговорить"
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
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f'{coffee["title"]}, урожай {coffee["yield_"]}, {coffee["processing"]}, {coffee["variety"]}, высота {coffee["height_min"] if coffee["height_min"] != coffee["height_max"] else " "} - {coffee["height_max"]} м.',
                                color=FONT_COLOR,
                            ),
                            ft.Text(
                                f'{coffee["origin"]}, {coffee["region"]}, ферма/станция: {coffee["farm"]}, производитель: {coffee["farmer"]}.',
                                color=FONT_COLOR,
                            ),
                            ft.Text(
                                f'{coffee["roaster"]}, {coffee["price"]} руб за {coffee["weight"]} г, Q-оценка: {coffee["q_grade_rating"]}, рейтинг: {coffee["rating"]}, отзывов: {coffee["reviews"]}, комментариев: {coffee["comments"]},обжарка под {coffee["roasting_level"]}.',
                                color=FONT_COLOR,
                            ),
                            ft.Text(
                                coffee["description"], max_lines=3,
                                color=FONT_COLOR,
                            ),
                        ],
                    ),
                    padding=ft.padding.all(5),
                    border_radius=10,
                    bgcolor=MAIN_COLOR,
                    on_hover=on_hover,
                ),
            ),
            on_tap=lambda e, coffee_id=coffee["id"]: page.go(f"/discussion/{coffee_id}"),  # Обработка нажатия
            mouse_cursor=ft.MouseCursor.CLICK,
        )
        cards_list.controls.append(card)

    return ft.View("/coffees", [cards_list], bgcolor=MINOR_COLOR)

if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        ft.app(target=coffee_list, view=ft.WEB_BROWSER, port=8550)  # host="0.0.0.0",
    else:
        ft.app(target=coffee_list, view=ft.AppView.WEB_BROWSER)