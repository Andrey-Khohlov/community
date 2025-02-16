import hashlib

import httpx
import flet as ft
import requests

from app.schemas.comments import CommentsAddSchema
from . import API_URL


class Message:
    def __init__(self, user: str, text: str):
        self.user = user
        self.text = text


def get_initials(user_name: str):
    return user_name[:1].capitalize()


def stable_hash(obj):
    if isinstance(obj, str):
        obj = obj.encode('utf-8')
    elif isinstance(obj, int):
        obj = str(obj).encode('utf-8')
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")

    return int(hashlib.sha256(obj).hexdigest(), 16)

def get_avatar_color(user_name: str):
    colors_lookup = [
        ft.Colors.AMBER,
        ft.Colors.BLUE,
        ft.Colors.BROWN,
        ft.Colors.CYAN,
        ft.Colors.GREEN,
        ft.Colors.INDIGO,
        ft.Colors.LIME,
        ft.Colors.ORANGE,
        ft.Colors.PINK,
        ft.Colors.PURPLE,
        ft.Colors.RED,
        ft.Colors.TEAL,
        ft.Colors.YELLOW,
    ]
    return colors_lookup[stable_hash(user_name) % len(colors_lookup)]


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(get_initials(message.user)),
                    color=ft.Colors.WHITE,
                    bgcolor=get_avatar_color(message.user),
                ),
                ft.Column(
                    [
                        ft.Text(message.user, weight="bold"),
                        ft.Text(message.text, selectable=True),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]


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
    page.title = f"Обсуждаем {coffee.get('title', 'None')}"

    card = ft.Container(
        content=ft.Column(
            [
                # Первая строка
                ft.Row(
                    [
                        ft.Text(coffee["title"], weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_500),
                        ft.Text(f'урожай {coffee["yield_"]},', color=ft.Colors.GREEN_600),
                        ft.Text(coffee["processing"], color=ft.Colors.GREEN_600 ),
                        ft.Text(f'{coffee["variety"]},', color=ft.Colors.GREEN_600),
                        ft.Text(
                            f'высота {coffee["height_min"] if coffee["height_min"] != coffee["height_max"] else " "} - {coffee["height_max"]} м,', color=ft.Colors.GREEN_600),
                    ],
                    spacing=10,  # Расстояние между элементами в строке
                ),
                # Вторая строка
                ft.Row(
                    [
                        ft.Text(f'{coffee["origin"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'{coffee["region"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'ферма/станция: {coffee["farm"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'производитель: {coffee["farmer"]},', color=ft.Colors.GREEN_600),

                    ],
                    spacing=10,
                ),
                # Третья строка
                ft.Row(
                    [
                        ft.Text(coffee["roaster"], color=ft.Colors.GREEN_600),
                        ft.Text(f'{coffee["price"]} руб за {coffee["weight"]} г,', color=ft.Colors.GREEN_600),
                        ft.Text(f'Q-оценка: {coffee["q_grade_rating"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'рейтинг: {coffee["rating"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'отзывов: {coffee["reviews"]},',  color=ft.Colors.GREEN_600),
                        ft.Text(f'комментариев: {coffee["comments"]},', color=ft.Colors.GREEN_600),
                        ft.Text(f'обжарка под {coffee["roasting_level"]}', color=ft.Colors.GREEN_600),
                    ],
                    spacing=10,
                ),
                # Четвертая строка
                ft.Row(
                    [

                        ft.Text(coffee["description"], max_lines=3, color=ft.Colors.GREEN_600),
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
            chat.controls.append(ChatMessage(Message(user=comment.get('user', 'N/A').get('username', 'N/A'), text=comment.get('content', 'Unknown'))))
            # chat.controls.append(ft.Text(
            #                 f"{comment.get('user', 'N/A').get('username', 'N/A')}: {comment.get('content', 'Unknown')}")
            # )
        else:
            chat.controls.append(ft.Text(f"Invalid data format: {comment}", color="orange"))



    def on_message(message: Message):
        # chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        chat.controls.append(ChatMessage(message))
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
        hint_text="Тут писать комментарии ...",
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
                            tooltip="напишите свои комментарии",
                            on_click=send_click,
                        ),
                     ]
                ),
    )


    page.update()


if __name__ == "__main__":
    ft.app(target=discussion)