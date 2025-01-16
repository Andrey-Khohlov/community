import httpx
import flet as ft

# https://github.com/flet-dev/examples/tree/main/python/tutorials/chat

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    # Запрос к API
    try:
        response = httpx.get(f"{API_URL}/v1/reviews/reviews/", follow_redirects=True)
        response.raise_for_status()  # Проверяем успешность запроса
    except httpx.RequestError as e:
        page.add(ft.Text(f"HTTP Request failed: {e}", color="red"))
        return
    except httpx.HTTPStatusError as e:
        page.add(ft.Text(f"HTTP Error: {e.response.status_code}", color="red"))
        return

    # Декодирование JSON-ответа
    try:
        response_data = response.json()  # Преобразуем JSON в Python-объект
        coffee_reviews = response_data.get("Ok", [])  # Извлекаем список отзывов
    except ValueError as e:
        page.add(ft.Text(f"Failed to parse JSON: {e}", color="red"))
        return

    # Убедитесь, что это список
    if not isinstance(coffee_reviews, list):
        page.add(ft.Text("Error: Expected a list of coffee reviews", color="red"))
        return

    # Отображение данных
    for coffee in coffee_reviews:
        if isinstance(coffee, dict):  # Убедиться, что элемент - словарь
            page.add(
                ft.Column(
                    [
                        ft.Text(f"ID: {coffee.get('id', 'N/A')}", size=20, weight="bold"),
                        # ft.Text(f"Method: {coffee.get('comment', 'Unknown')}"),
                        ft.Text(f"Method: {coffee.get('method', 'Unknown')}"),
                        ft.Text(f"Tags: {coffee.get('tags', 'No tags')}"),
                        ft.Text(f"Rating: {coffee.get('rating_4', 'No rating')}"),
                        ft.Text(f"Water: {coffee.get('water', 'Unknown')}"),
                        ft.Text(f"Temperature: {coffee.get('temperature', 'N/A')}°C"),
                    ],
                    spacing=10
                )
            )
        else:
            page.add(ft.Text(f"Invalid data format: {coffee}", color="orange"))

ft.app(target=main)
