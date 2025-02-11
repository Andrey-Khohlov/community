import httpx
import flet as ft
import requests
from flet_core.types import AppView

from app.api.v1.endpoints.comments import add_comment
from app.db.models.comments import CommentsAddModel
from app.db.sessions import SessionDep
from app.schemas.comments import CommentsAddSchema


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
    page.title = f"{coffee.get('title', 'None')}"

    card = ft.Container(
        content=ft.Column(
            [
                # Первая строка
                ft.Row(
                    [
                        ft.Text(coffee["title"], weight=ft.FontWeight.BOLD),
                        ft.Text(f'урожай {coffee["yield_"]},'),
                        ft.Text(coffee["processing"]),
                        ft.Text(f'{coffee["variety"]},'),
                        ft.Text(
                            f'высота {coffee["height_min"] if coffee["height_min"] != coffee["height_max"] else " "} - {coffee["height_max"]} м,'),
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
            spacing=5,  # Расстояние между строками
        ),
        padding=ft.padding.all(5),
    )

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
        user = page.session.get("user")

        # сохраняем сообщение пользователя в базу данных сообщений
        new_message_json = CommentsAddSchema(
            product_id=coffee["id"],
            user_id=user["id"],
            content=new_message.value,
            parent_id=0,
            review_id=0,
        )

        # Запрос к API
        response_post = requests.post(
                f"{API_URL}/v1/comments/",
                json=new_message_json.model_dump(),
                headers={"Content-Type": "application/json"},
            )
        if response_post.status_code == 200:
            page.pubsub.send_all(Message(user=user["username"], text=new_message.value))
            new_message.value = ""
        else:
            print(f"Ошибка: {response_post.status_code}, {response_post.text}")
            page.add(ft.Text(f"HTTP Error: {response_post.status_code}", color="red"))
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
    # Отображение комментариев
    page.add(
        card,
        ft.Divider(),
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