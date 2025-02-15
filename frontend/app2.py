import flet as ft

# Главная страница
def main_page(page: ft.Page):
    page.title = "Главная страница"
    page.add(ft.Text("Добро пожаловать на главную страницу!"))
    page.add(ft.ElevatedButton(
        text="Перейти на страницу кофе",
        on_click=lambda e: page.go("/coffee/1")  # Переход на страницу кофе
    ))

# Страница кофе
def coffee_page(page: ft.Page, coffee_id: int):
    page.title = f"Страница кофе {coffee_id}"
    page.add(ft.Text(f"Это страница кофе с ID {coffee_id}"))
    page.add(ft.ElevatedButton(
        text="Вернуться на главную",
        on_click=lambda e: page.go("/")  # Возврат на главную страницу
    ))

# Обработка изменений маршрута
def route_change(page: ft.Page, route: str):
    page.clean()  # Очищаем текущие элементы
    if page.route == "/":
        main_page(page)  # Отображаем главную страницу
    elif page.route.startswith("/coffee/"):
        coffee_id = int(page.route.split("/")[-1])  # Извлекаем ID кофе из URL
        coffee_page(page, coffee_id)  # Отображаем страницу кофе
    page.update()

# Инициализация приложения
def main(page: ft.Page):
    page.on_route_change = route_change  # Подписываемся на изменения маршрута
    page.go("/")  # Переходим на главную страницу

# Запуск приложения
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)