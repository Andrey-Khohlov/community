import flet as ft

def page2(page: ft.Page):
    page.clean()  # Очищаем страницу перед добавлением новых элементов

    # Заголовок страницы
    title = ft.Text("Страница 2", size=30, color="green")

    # Кнопка для возврата на первую страницу
    button = ft.ElevatedButton(
        text="Вернуться на Страницу 1",
        on_click=lambda e: page.go("/"),  # Переход на маршрут "/"
    )

    # Добавляем элементы на страницу
    page.add(title, button)
    page.update()  # Обновляем страницу
    return ft.View("/page2", [title, button])