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

    # Создаем таблицу
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Название")),

            ft.DataColumn(ft.Text("Урожай")),
            ft.DataColumn(ft.Text("Обработка")),
            ft.DataColumn(ft.Text("Страна")),
            ft.DataColumn(ft.Text("Высота")),
            ft.DataColumn(ft.Text("Разновидность")),


            ft.DataColumn(ft.Text("Регион")),
            ft.DataColumn(ft.Text("Ферма/станция")),
            ft.DataColumn(ft.Text("Производитель")),

            ft.DataColumn(ft.Text("Обжарщик")),
            ft.DataColumn(ft.Text("Цена")),
            ft.DataColumn(ft.Text("Вес")),
            ft.DataColumn(ft.Text("Q-оценка")),

            ft.DataColumn(ft.Text("Рейтинг")),
            ft.DataColumn(ft.Text("Оценок")),
            ft.DataColumn(ft.Text("Комментариев")),

            ft.DataColumn(ft.Text("Обжарка")),
            ft.DataColumn(ft.Text("Описание")),

            # ft.DataColumn(ft.Text(" ")),
        ],
        rows=[],
    )

    coffees = fetch_coffees()

    # Заполняем таблицу данными
    for coffee in coffees:
        data_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.ElevatedButton(
                            text=coffee["title"],
                            on_click=lambda _, coffee_id=coffee["id"]: page.go(f"/discussion/{coffee_id}"),
                        ),
                    ),

                    ft.DataCell(ft.Text(coffee["yield_"], max_lines=2)),
                    ft.DataCell(ft.Text(coffee["processing"], max_lines=2)),
                    ft.DataCell(ft.Text(coffee["origin"])),
                    ft.DataCell(ft.Text(f'{coffee["height_min"]} - {coffee["height_max"]}', max_lines=2)),
                    ft.DataCell(ft.Text(coffee["variety"], max_lines=2)),

                    ft.DataCell(ft.Text(coffee["region"], max_lines=2)),
                    ft.DataCell(ft.Text(coffee["farm"], max_lines=2)),
                    ft.DataCell(ft.Text(coffee["farmer"], max_lines=2)),


                    ft.DataCell(ft.Text(coffee["roaster"], max_lines=2)),
                    ft.DataCell(ft.Text(coffee["price"])),
                    ft.DataCell(ft.Text(coffee["weight"])),
                    ft.DataCell(ft.Text(coffee["q_grade_rating"])),

                    ft.DataCell(ft.Text(coffee["rating"])),
                    ft.DataCell(ft.Text(coffee["reviews"])),
                    ft.DataCell(ft.Text(coffee["comments"])),

                    ft.DataCell(ft.Text(coffee["roasting_level"])),
                    ft.DataCell(ft.Text(coffee["description"], max_lines=2)),
                ],
            )
        )

    # Добавляем таблицу на страницу
    page.add(
        ft.Row(
            controls=[data_table],
            scroll=ft.ScrollMode.AUTO,  # Включаем горизонтальную прокрутку
        )
    )

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