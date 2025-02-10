import flet as ft
import httpx

from frontend.pages.discussion import discussion

# Адрес вашего бэкенда
API_URL = "http://127.0.0.1:8000"  # Замените на ваш URL

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
    page.title = "Coffee List"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.clean()

    coffees = fetch_coffees()

    # Создаем контейнер для карточек
    cards_list = ft.ListView(expand=True, spacing=30)

    # Заполняем таблицу данными
    for coffee in coffees:
        card = ft.GestureDetector(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(coffee["title"], weight=ft.FontWeight.BOLD),
                            ft.Text(coffee["yield_"], max_lines=2),
                            ft.Text(coffee["processing"], max_lines=2),
                            ft.Text(coffee["origin"], max_lines=2),
                            ft.Text(f'{coffee["height_min"]} - {coffee["height_max"]}', max_lines=2),
                            ft.Text(coffee["variety"], max_lines=2),
                            ft.Text(coffee["region"], max_lines=2),
                            ft.Text(coffee["farm"], max_lines=2),
                            ft.Text(coffee["farmer"], max_lines=2),
                            ft.Text(coffee["roaster"], max_lines=2),
                            ft.Text(coffee["price"], max_lines=2),
                            ft.Text(coffee["weight"], max_lines=2),
                            ft.Text(coffee["q_grade_rating"], max_lines=2),
                            ft.Text(coffee["rating"], max_lines=2),
                            ft.Text(coffee["reviews"], max_lines=2),
                            ft.Text(coffee["comments"], max_lines=2),
                            ft.Text(coffee["roasting_level"], max_lines=2),
                            ft.Text(coffee["description"], max_lines=2),
                        ],
                        spacing=2,
                    ),
                    padding=ft.padding.all(5),
                    # bgcolor=ft.colors.WHITE,  # Цвет фона по умолчанию
                    # border_radius=ft.border_radius.all(5),  # Скругление углов
                    # on_hover=lambda e: setattr(
                    #     e.control, "bgcolor", ft.colors.GREY_300 if e.data == "true" else ft.colors.WHITE
                    # ),  # Изменение цвета при наведении
                ),
                elevation=2,  # Тень по умолчанию
            ),
            on_tap=lambda e, coffee_id=coffee["id"]: page.go(f"/discussion/{coffee_id}"),  # Обработка нажатия
            on_hover=lambda e: setattr(e.control.content, "elevation", 8 if e.data == "true" else 2), # Увеличиваем тень при наведении
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