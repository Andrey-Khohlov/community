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


    # Создаем четыре столбца
    column1 = ft.Column(
        controls=[
            ft.Text(f"Обжарщик: {coffee.get('roaster', 'N/A')}", color="green"),
            ft.Text(f"Q-оценка: {coffee.get('q_grade_rating', 'N/A')}", color="green"),
            ft.Text(f"Цена: {coffee.get('price', 'N/A')} за {coffee.get('weight', 'N/A')} г", color="green"),
            ft.Text("")
        ],
        spacing=10,  # Отступ между элементами
    )

    column2 = ft.Column(
        controls=[
            ft.Text(f"Страна: {coffee.get('origin', 'N/A')}", color="green"),
            ft.Text(f"Регион: {coffee.get('region', 'N/A')}", color="green"),
            ft.Text(f"Ферма/Станция: {coffee.get('farm', 'N/A')}", color="green"),
            ft.Text(f"Производитель: {coffee.get('farmer', 'N/A')}", color="green"),
        ],
        spacing=10,
    )

    column3 = ft.Column(
        controls=[
            ft.Text(f"Разновидность: {coffee.get('variety', 'N/A')}", color="green"),
            ft.Text(f"Обработка: {coffee.get('processing', 'N/A')}", color="green"),
            ft.Text(f"Высота произрастания: {coffee.get('height_min', 'N/A')} - {coffee.get('height_max', 'N/A')}",
                    color="green"),
            ft.Text(f"Урожай: {coffee.get('yield_', 'N/A')}", color="green"),
        ],
        spacing=10,
    )

    column4 = ft.Column(
        controls=[
            ft.Text(f"Рейтинг покупателей: {coffee.get('rating', 'N/A')}", color="green"),
            ft.Text(f"Оценок: {coffee.get('reviews', 'N/A')}", color="green"),
            ft.Text(f"Комментариев: {coffee.get('comments', 'N/A')}", color="green"),
            ft.Text(f"Фото упаковки: {coffee.get('pack_img', 'N/A')}", color="green"),
        ],
        spacing=10,
    )

    # Размещаем столбцы в строке
    row = ft.Row(
        controls=[column1, column2, column3, column4],
        spacing=20,  # Отступ между столбцами
        alignment=ft.MainAxisAlignment.START,  # Выравнивание по левому краю
    )

    # Отображение данных
    page.add(
        ft.Text(f"{coffee.get('title', 'N/A')}: {coffee.get('description', 'Unknown')}", weight=ft.FontWeight.BOLD, color="green"),
        row,
        ft.Divider(),
    )
    for comment in comments:
        if isinstance(comment, dict):  # Убедиться, что элемент - словарь
            page.add(
                ft.Column(
                    [
                        ft.Text(f'''{comment.get('user', 'N/A').get('username', 'N/A')}: {comment.get('content', 'Unknown')}'''),
                    ],
                    spacing=10
                )
            )
        else:
            page.add(ft.Text(f"Invalid data format: {comment}", color="orange"))

ft.app(target=main)
