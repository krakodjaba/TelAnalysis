# Telanalysis

Telegram Social Media Intelligence (SOCMINT / OSINT) платформа для анализа экспортированных Telegram чатов и каналов.

Telanalysis использует FastAPI для загрузки Telegram JSON-архивов, выполнения NLP и сентимент-анализа, генерации графов взаимодействий, семантического и стилометрического анализа.

## Возможности

- Анализ Telegram каналов и чатов
- Построение WordCloud из сообщений канала
- Частотный анализ слов и ключевых фраз
- Сентимент-анализ сообщений
- Извлечение email-адресов и телефонных номеров
- Построение графов reply-взаимодействий
- Экспорт `nodes_*.csv`, `edges_*.csv` и JSON-графа
- Семантический анализ тем и coherence
- Стилометрический анализ текста
- Временной анализ активности

## Поддерживаемые данные

Проект работает с JSON-экспортами Telegram, полученными из Telegram Desktop или других средств экспорта.

Поддерживаются:

- каналы
- супергруппы
- приватные группы
- история чатов в JSON

## Архитектура проекта

```text
app/
  routers/
    analysis.py      # маршруты загрузки и анализа
  services/
    channel_analyse.py
    chat_analyse.py
    graph_generator.py
    semantic_analyse.py
    stylometric_analyse.py
    temporal_analyse.py
    nltk_analyse.py
    utils.py
  static/
  templates/
graphs/             # сохраняются визуальные артефакты и графы
uploads/            # загруженные JSON-файлы
config.json
requirements.txt
Dockerfile
docker-compose.yml
```

Используемые технологии:

- Python 3.11
- FastAPI
- Uvicorn
- Jinja2
- NLTK
- VaderSentiment
- NetworkX
- WordCloud
- Matplotlib
- JMESPath

## Установка и запуск

### Локально

1. Создайте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Загрузите NLTK-данные:

```bash
python -m nltk.downloader stopwords punkt
```

4. Запустите приложение:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

5. Откройте в браузере:

```text
http://127.0.0.1:8000
```

### В Docker

Проект содержит `Dockerfile` и `docker-compose.yml`.

Запустите:

```bash
docker compose up --build
```

Для фонового режима:

```bash
docker compose up --build -d
```

Остановить контейнеры:

```bash
docker compose down
```

Том монтирует локальные директории:

- `./graphs` → `/app/graphs`
- `./uploads` → `/app/uploads`
- `./config.json` → `/app/config.json`

По умолчанию приложение доступно на `http://127.0.0.1:8000`.

> Если на системе используется старая версия Docker Compose, можно применить `docker-compose up --build`.

## Использование

1. Перейдите на главную страницу.
2. Загрузите Telegram JSON через форму `Анализ канала` или `Анализ чата`.
3. Дождитесь обработки и просмотрите результаты.
4. Сгенерированные артефакты доступны в `graphs/`.

### Основные маршруты

- `/` — главная страница
- `/analyze/channel` — анализ канала
- `/analyze/chat` — анализ чата

## Результаты анализа

После загрузки JSON генерируются:

- `wordcloud.png` для канального анализа
- `nodes_*.csv` и `edges_*.csv` для графовой аналитики
- `*.json` D3-ready граф
- семантические темы и ключевые фразы
- стилометрические метрики
- временные показатели активности
- извлечённые email и телефоны

## Конфигурация

Настройки читаются из `config.json`.

Пример:

```json
{
  "select_type_stem": "Off",
  "most_com": 30,
  "most_com_channel": 100
}
```

## Важные замечания

- Загруженные файлы сохраняются в `uploads/`.
- Сгенерированные графы и изображения сохраняются в `graphs/`.
- Приложение запускается на порту `8000`.

## Дополнительно

Если нужно, добавьте в `config.json` параметры для изменения количества анализируемых слов.

```python
import nltk
nltk.download('stopwords')
exit()
```

Запуск:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 80
```

Открыть в браузере:

```text
http://127.0.0.1:80
```

---

# Docker

## Build

```bash
docker build -t telanalysis .
```

## Run

```bash
docker run -p 80:80 telanalysis
```

---

# Docker Compose

```bash
docker compose up -d --build
```

---

# Результаты анализа

После обработки создаются:

## WordCloud

```text
graphs/<file>_wordcloud.png
```

## Graph JSON

```text
graphs/<file>.json
```

## Nodes CSV

```text
graphs/nodes_<file>.csv
```

## Edges CSV

```text
graphs/edges_<file>.csv
```

---

# Конфигурация

Файл:

```text
config.json
```

Пример:

```json
{
  "select_type_stem": "Off",
  "most_com": 30,
  "most_com_channel": 100
}
```

Параметры:

- select_type_stem — stemming NLP
- most_com — количество top words для чатов
- most_com_channel — количество top words для каналов

---

# API Endpoints

## Главная страница

```http
GET /
```

## Анализ канала

```http
POST /analyze/channel
```

## Анализ чата

```http
POST /analyze/chat
```

---

# Безопасность

Рекомендуется:

- не публиковать uploads/
- использовать reverse proxy
- ограничить CORS в production
- запускать behind VPN/reverse proxy
- использовать isolated Docker runtime
- очищать uploads и graphs

---

# Roadmap

Планируемые функции:

- Neo4j integration
- Gephi export
- Multi-chat correlation
- Temporal graph analysis
- Entity clustering
- Username tracking
- URL extraction
- Telegram API integration
- ML-based anomaly detection
- Centrality metrics
- Community detection

---

# License

Educational / Research Use.

---

# 🔗 Ресурсы и контакты

## Актуальный канал

- https://t.me/IsaevInfra

## OSINT SAN Framework

- https://t.me/osint_san_framework

## Сайт / услуги

- https://isaevlab.ru

## Архивный канал (без обновлений)

- https://t.me/telanalysis

---

# 💬 Комьюнити

## Matrix (основной чат)

```text
#osintsan:icragency.ru
```

