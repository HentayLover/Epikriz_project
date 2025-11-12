# Краткая инструкнция

## Запуск

Если нужен локальный интерфейс

```
python start.py
```

Если нужен веб - интерфейс

```
python web_app.py
```

Или докер образ

```
docker build -t epirkiz-interface .
docker run -it --rm -p 8501:8501 epirkiz-interface
http://localhost:8501
```

Если скаченный (иным путём)

```
# 1. Загрузить образ
docker load -i epirkiz-interface.tar

# 2. Проверить наличие образа
docker images

# 3. Запустить контейнер
docker run -it --rm -p 8501:8501 epirkiz-interface:latest

# 4. Открыть в браузере: http://localhost:8501
```