# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код фронтенда
COPY ./frontend /code/frontend

# Указываем порт, который будет использовать приложение
EXPOSE 8550

# Команда для запуска фронтенда
CMD ["python", "-m", "frontend.pages.frontman"]