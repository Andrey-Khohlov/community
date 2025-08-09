import hashlib

import httpx
import flet as ft
import requests

from app.schemas.comments import CommentsAddSchema
from . import API_URL


FONT_COLOR = 'black'
MAIN_COLOR = '#FFC09876'  # Classic Mocka
MEDIUM_COLOR = '#FFB15616'  # Pantone 18-1421 Baltic Amber
MINOR_COLOR = '#FF966E50'  # Dark Mocha
# '#FFD2B496'  # Light Mocha
# '#FFC4B6A6'  # PANTON 15-1317 Sirocco
# '#FFB15616'  # Pantone 18-1421 Baltic Amber
# '#FF9E7C6B' # Pantone 17-1230 Mocka Moussed
# '#FF966E50'  # Dark Mocha

class Message:
    def __init__(self, user: str, text: str):
        self.user = user
        self.text = text

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.expand = True
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(get_initials(message.user), weight=ft.FontWeight.BOLD, size=28),
                    color=MAIN_COLOR,
                    bgcolor=get_avatar_color(message.user),
                ),
                ft.Column(
                    [
                        ft.Text(message.user, weight="bold", color=FONT_COLOR),
                        ft.Text(message.text, selectable=True, color=FONT_COLOR),
                    ],
                    tight=True,
                    spacing=5,
                    expand=True,
                ),
            ]


def on_hover(e):
    e.control.bgcolor = MAIN_COLOR if e.data == "true" else MINOR_COLOR
    e.control.update()

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

def discussion(page: ft.Page, coffee_id: int = 1):
    page.clean()
    page.horizontal_alignment = ft.CrossAxisAlignment.START  # Выравниваем по левому краю
    # page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = MINOR_COLOR

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

    def on_message(message: Message):
        # chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        chat.controls.append(ChatMessage(message))
        page.update()

    # Подписка на получение сообщений
    page.pubsub.subscribe(on_message)

    def send_click(e):
        user = page.session.get("user")
        if not user:
            # Если пользователь не авторизован, открываем диалог регистрации
            # welcome_dlg.open = True
            # page.overlay.append(welcome_dlg)  # Добавляем диалог в overlay
            # page.update()
            # return

            # Если пользователь не авторизован, перенаправляем на страницу логина
            page.session.set("return_url", page.route)
            page.go(f"/login")
        #     return
        # else:
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
        hint_text="Сообщение",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_click,
    )

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        if not join_user_pass.value:
            join_user_pass.error_text = "Password cannot be blank!"
            join_user_pass.update()
        else:
            try:
                user_response = httpx.get(f"{API_URL}/v1/users", follow_redirects=True)
                user_response.raise_for_status()  # Проверяем успешность запроса
            except httpx.RequestError as e:
                page.add(ft.Text(f"HTTP Request failed: {e}", color="red"))
                return
            except httpx.HTTPStatusError as e:
                page.add(ft.Text(f"HTTP Error: {e.response.status_code}", color="red"))
                return
            # Проверяем, находится ли пользователь в базе данных
            for user in user_response.json()["Ok"]:
                if user["username"] == join_user_name.value and user["password"] == join_user_pass.value:
                    page.session.set("user", user)  # Сохраняем пользователя в sessionStorage
                    break
            else:
                # Если пользователь не найден, выводим сообщение об ошибке
                welcome_dlg.title = ft.Text("oй-ёй-ёй! что-то не то", color="red")
                page.update()
                return
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user=join_user_name.value,
                    text=f"{join_user_name.value} заходит на кофеёк.",
                    # message_type="login_message",
                )
            )
            page.update()

    # A dialog asking for a user display name
    join_user_name = ft.TextField(
        label="Введите имя",
        autofocus=True,
        on_submit=join_chat_click,
    )
    join_user_pass = ft.TextField(
        label="Введите пароль",
        autofocus=True,
        password=True,
        on_submit=join_chat_click,
    )
    welcome_dlg = ft.AlertDialog(
        open=False,
        # modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name, join_user_pass], width=300, height=140, tight=True),
        actions=[ft.ElevatedButton(text="войти", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: page.overlay.remove(welcome_dlg),  # Закрытие при клике вне диалога
    )

    message_field = ft.Row(controls=
                                     [
                                         new_message,
                                         ft.IconButton(
                                            icon=ft.Icons.SEND_ROUNDED,
                                            tooltip="Опубликовать сообщение",
                                            on_click=send_click,
                                        ),
                                     ]
                                )

    page.title = f"{coffee.get('title', 'None')} - кофе, о котором говорят"

    # подгружаем комменты из базы
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    for comment in comments:
        if isinstance(comment, dict):  # Убедиться, что элемент - словарь
            chat.controls.append(ChatMessage(Message(user=comment.get('user', 'N/A').get('username', 'N/A'),
                                                     text=comment.get('content', 'Unknown'))))
        else:
            chat.controls.append(ft.Text(f"Invalid data format: {comment}", color="orange"))

    # Создание карточки обсуждаемого кофе
    card = ft.Container(
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
            scroll=ft.ScrollMode.AUTO,
        ),
        height=140,
        bgcolor=MINOR_COLOR,
        # on_hover=on_hover,
        border_radius=10,
    )

    return ft.View("/discussion/{coffee_id}", [card, chat, message_field], bgcolor=MAIN_COLOR)


if __name__ == "__main__":
    ft.app(target=discussion)