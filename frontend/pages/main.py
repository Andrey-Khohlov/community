import os

import flet as ft
# from .coffees import coffee_list
# from .discussion import discussion
#
# def main(page: ft.Page):
#     def route_change(route):
#         page.views.clear()
#         print(page.route)
#         if page.route == "/" or page.route == "/coffees":
#             coffee_list(page)
#         elif page.route.startswith("/discussion/"):
#             coffee_id = int(page.route.split("/")[-1])
#             discussion(page, coffee_id)
#
#         page.update()
#
#     page.on_route_change = route_change
#     page.go(page.route)

##############################
# import flet as ft
# from .page1 import page1  # Импортируем функцию для первой страницы
# from .page2 import page2  # Импортируем функцию для второй страницы
#
# def main(page: ft.Page):
#     # Функция для обработки изменения маршрута
#     def route_change(route):
#         page.views.clear()  # Очищаем текущие элементы страницы
#         if page.route == "/":  # Главная страница
#             page1(page)
#         elif page.route == "/page2":  # Вторая страница
#             page2(page)
#         page.update()  # Обновляем страницу
#
#     # Назначаем обработчик изменения маршрута
#     page.on_route_change = route_change
#
#     # Загружаем начальный маршрут
#     page.go(page.route)

# Запускаем приложение
# ft.app(target=main)

# import flet as ft
#
# def main(page: ft.Page):
#     def route_change(route):
#         page.views.clear()
#         if page.route == "/":
#             page.views.append(
#                 ft.View(
#                     "/",
#                     [
#                         ft.Text("Страница 1", size=30, color="blue"),
#                         ft.ElevatedButton(
#                             text="Перейти на Страницу 2",
#                             on_click=lambda e: page.go("/page2"),
#                         ),
#                     ],
#                 )
#             )
#         elif page.route == "/page2":
#             page.views.append(
#                 ft.View(
#                     "/page2",
#                     [
#                         ft.Text("Страница 2", size=30, color="green"),
#                         ft.ElevatedButton(
#                             text="Вернуться на Страницу 1",
#                             on_click=lambda e: page.go("/"),
#                         ),
#                     ],
#                 )
#             )
#         page.update()
#
#     page.on_route_change = route_change
#     page.go(page.route)

import flet as ft
from page1 import page1  # Импортируем функцию для первой страницы
from page2 import page2  # Импортируем функцию для второй страницы

def main(page: ft.Page):
    # Функция для обработки изменения маршрута
    def route_change(route):
        page.views.clear()  # Очищаем текущие элементы страницы
        if page.route == "/":  # Главная страница
            page.views.append(page1(page))
        elif page.route == "/page2":  # Вторая страница
            page.views.append(page2(page))
        page.update()  # Обновляем страницу

    # Назначаем обработчик изменения маршрута
    page.on_route_change = route_change

    # Загружаем начальный маршрут
    page.go(page.route)

if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        ft.app(target=main, view=ft.WEB_BROWSER, port=8550)  # host="0.0.0.0",
    else:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)