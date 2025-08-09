import flet as ft

def page1(page: ft.Page):
    page.clean()  # Очищаем страницу перед добавлением новых элементов

    # Заголовок страницы
    title = ft.Text("Страница 1", size=30, color="blue")

    # Кнопка для перехода на вторую страницу
    button = ft.ElevatedButton(
        text="Перейти на Страницу 2",
        on_click=lambda e: page.go("/page2"),  # Переход на маршрут "/page2"
    )

    # Добавляем элементы на страницу
    # page.add(title, button)
    # page.update()  # Обновляем страницу
    return ft.View("/", [title, button])