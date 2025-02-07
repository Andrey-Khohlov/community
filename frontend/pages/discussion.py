import httpx
import flet as ft
from flet_core.types import AppView


# https://github.com/flet-dev/examples/tree/main/python/tutorials/chat

class Message:
    def __init__(self, user: str, text: str):
        self.user = user
        self.text = text


API_URL = "http://127.0.0.1:8000"

def discussion(page: ft.Page, coffee_id: int = 1):
    page.theme_mode = ft.ThemeMode.DARK
    page.clean()

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

    # Заголовок
    page.title = f"чат о кофеёчке {coffee.get('title', 'None')}"

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
    coffee_description = ft.Row(
        controls=[column1, column2, column3, column4],
        spacing=20,  # Отступ между столбцами
        alignment=ft.MainAxisAlignment.START,  # Выравнивание по левому краю
    )

    # chat init
    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    for comment in comments:
        if isinstance(comment, dict):  # Убедиться, что элемент - словарь
            chat.controls.append(ft.Text(
                            f"{comment.get('user', 'N/A').get('username', 'N/A')}: {comment.get('content', 'Unknown')}")
            )
        else:
            chat.controls.append(ft.Text(f"Invalid data format: {comment}", color="orange"))



    def on_message(message: Message):
        chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        page.update()

    # Подписка на получение сообщений
    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(Message(user='Я', text=new_message.value))
        new_message.value = ""
        page.update()

    # Поле для ввода
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_click,
    )

    # Отображение данных о кофе
    page.add(
        ft.Row(
            [ft.Text(f"{coffee.get('title', 'N/A')}: {coffee.get('description', 'Unknown')}",
                     weight=ft.FontWeight.BOLD,
                     color="green"
                     )
             ],
            alignment=ft.MainAxisAlignment.START
        ),
        coffee_description,
        ft.Divider(),
    )

    # Отображение комментариев
    page.add(
        chat,
        ft.Row(controls=
                     [
                         new_message,
                         ft.IconButton(
                            icon=ft.Icons.SEND_ROUNDED,
                            tooltip="Send message",
                            on_click=send_click,
                        ),
                     ]
                ),
    )


    page.update()


if __name__ == "__main__":
    ft.app(target=discussion)