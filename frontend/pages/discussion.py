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
    page.title = f"{coffee.get('title', 'None')} - кофе, о котом говорят"

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
        if not user:
            # Если пользователь не авторизован, открываем диалог регистрации
            welcome_dlg.open = True
            page.overlay.append(welcome_dlg)  # Добавляем диалог в overlay
            page.update()
            return
        else:
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
                welcome_dlg.title = ft.Text("oй-ёй-ёй! что-то не то", color="red")  #TODO make it vanished
                page.update()
                return
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            # TODO make it vanished, не писать в базу?
            page.pubsub.send_all(
                Message(
                    user=join_user_name.value,
                    text=f"{join_user_name.value} заходит на кофеёк.",
                    # message_type="login_message",
                )
            )
            page.update()

    # def login(e):
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

    # page.overlay.append(welcome_dlg)




    def message_field() -> ft.Row:
        if False:
            return ft.Row(controls=
                                     [
                                         ft.TextField("********"),
                                         ft.IconButton(
                                            icon=ft.Icons.SEND_ROUNDED,
                                            tooltip="Войдите для комментирования",
                                            on_click=login,
                                        ),
                                     ]
                                )
        else:
            return ft.Row(controls=
                                     [
                                         new_message,
                                         ft.IconButton(
                                            icon=ft.Icons.SEND_ROUNDED,
                                            tooltip="напишите свои комментарии",
                                            on_click=send_click,
                                        ),
                                     ]
                                )


    page.add(
        card,  # Отображение данных о кофе
        ft.Divider(),  # Отображение комментариев
        chat,
        message_field(),
        )


    page.update()


if __name__ == "__main__":
    ft.app(target=discussion)