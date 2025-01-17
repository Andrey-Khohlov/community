import httpx
import flet as ft

# https://github.com/flet-dev/examples/tree/main/python/tutorials/chat

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    coffee_id = 1
    # Запрос к API
    try:
        response = httpx.get(f"{API_URL}/v1/comments/{coffee_id}", follow_redirects=True)
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
        comments = response_data.get("Ok", [])  # Извлекаем список отзывов
        coffee = response_data.get("coffee", {})
    except ValueError as e:
        page.add(ft.Text(f"Failed to parse JSON: {e}", color="red"))
        return

    # Убедитесь, что это список
    if not isinstance(comments, list):
        page.add(ft.Text("Error: Expected a list of comment reviews", color="red"))
        return

    # Отображение данных
    page.add(
        ft.Text(f"{coffee.get('title', 'N/A')}: {coffee.get('description', 'Unknown')}", weight="bold"),
        ft.Text(f"Ratings: {coffee.get('q_grade_rating', 'N/A')}", color="green"),
        ft.Text(f"Price: {coffee.get('price', 'N/A')}", color="green"),
        ft.Text(f"Origin: {coffee.get('origin', 'N/A')}", color="green"),
        ft.Text(f"Region: {coffee.get('region', 'N/A')}", color="green"),
        ft.Text(f"Farm: {coffee.get('farm', 'N/A')}", color="green"),
        ft.Text(f"Farmer: {coffee.get('farmer', 'N/A')}", color="green"),
        ft.Text(f"Variety: {coffee.get('variety', 'N/A')}", color="green"),
        ft.Text(f"Processing: {coffee.get('processing', 'N/A')}", color="green"),
        ft.Text(f"Height: {coffee.get('height_min', 'N/A')} - {coffee.get('height_max', 'N/A')}", color="green"),
        ft.Text(f"Yield: {coffee.get('yield_', 'N/A')}", color="green"),
        ft.Text(f"Rating: {coffee.get('rating', 'N/A')}", color="green"),
        ft.Text(f"Reviews: {coffee.get('reviews', 'N/A')}", color="green"),
        ft.Text(f"Comments: {coffee.get('comments', 'N/A')}", color="green"),
        ft.Text(f"Pack image: {coffee.get('pack_img', 'N/A')}", color="green"),
        ft.Text(""),
    )
    for comment in comments:
        if isinstance(comment, dict):  # Убедиться, что элемент - словарь
            page.add(
                ft.Column(
                    [
                        ft.Text(f"{comment.get('user_id', 'N/A')}: {comment.get('content', 'Unknown')}"),
                    ],
                    spacing=10
                )
            )
        else:
            page.add(ft.Text(f"Invalid data format: {comment}", color="orange"))

ft.app(target=main)
