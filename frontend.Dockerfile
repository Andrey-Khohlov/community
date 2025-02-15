# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код фронтенда
COPY . .

# Указываем порт, который будет использовать приложение
EXPOSE 8550

# Команда для запуска фронтенда
# CMD ["python", "pages/login.py", "--port", "8550"]
CMD ["python", "-m", "frontend.pages.login"]