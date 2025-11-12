FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt сначала для кэширования
COPY interface/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Streamlit
RUN pip install --no-cache-dir streamlit

# Копируем остальные файлы
COPY interface/ .

# Запускаем Streamlit вместо Tkinter
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]