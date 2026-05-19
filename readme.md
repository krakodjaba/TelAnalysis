# Telanalysis

Telegram Social Media Intelligence (SOCMINT / OSINT) framework for analyzing exported Telegram chats and channels.

Telanalysis is a FastAPI-based analytical platform designed for processing Telegram export archives, extracting metadata, generating communication graphs, identifying entities, analyzing sentiment and building visual intelligence artifacts for OSINT/SOCMINT workflows.

The project is focused on:

- Telegram channel analysis
- Telegram group/chat analysis
- Social graph generation
- Keyword extraction
- Word frequency analysis
- Entity extraction (emails / phone numbers)
- Sentiment analysis
- Interaction mapping between users
- Visual SOCMINT analytics

---

# Возможности

## Анализ каналов

- Анализ экспортированных Telegram-каналов
- Построение WordCloud
- Выделение наиболее частотных слов
- NLP-обработка сообщений
- Очистка текста от emoji и системного мусора
- Поддержка русского и английского языка

## Анализ чатов

- Анализ Telegram-групп и чатов
- Сентимент-анализ сообщений
- Извлечение email-адресов
- Извлечение телефонных номеров
- Выявление пользовательской активности
- Анализ reply-цепочек
- Обработка forwarded-сообщений
- Обнаружение системных действий:
  - join events
  - invite events
  - remove events
  - pin events

## SOCMINT / Graph Intelligence

- Генерация social graph
- Построение связей между пользователями
- Export nodes/edges в CSV
- JSON-граф для D3.js визуализации
- Анализ reply-взаимодействий
- Визуализация network topology

---

# Поддерживаемые данные

Telanalysis работает с JSON-экспортами Telegram.

Экспорт можно получить через:

- Telegram Desktop
- Export chat history
- Export group/channel data

Поддерживаются:

- channels
- supergroups
- private groups
- exported chat history

---

# Архитектура

```text
FastAPI
 ├── Routers
 ├── NLP Engine
 ├── Sentiment Analyzer
 ├── Graph Generator
 ├── Static Graph Storage
 └── Jinja2 Frontend
```

Используемые технологии:

- Python 3
- FastAPI
- Jinja2
- NetworkX
- NLTK
- VaderSentiment
- WordCloud
- Matplotlib
- JMESPath

---

# Использование для Social Media Intelligence

## SOCMINT workflow

### 1. Экспорт Telegram-данных

В Telegram Desktop:

```text
Settings → Advanced → Export Telegram Data
```

Экспортируйте:

- JSON format
- messages
- media metadata
- user information

---

### 2. Загрузка архива

После запуска платформы:

```text
http://127.0.0.1:80
```

Загрузите exported JSON.

---

### 3. Получение аналитики

Система автоматически:

- обработает сообщения
- построит NLP-статистику
- извлечет сущности
- построит communication graph
- сгенерирует wordcloud
- покажет активность участников

---

## Примеры применения

### Threat Intelligence

- Анализ Telegram-комьюнити
- Выявление координации
- Mapping influence-узлов
- Detection suspicious interaction patterns

### Investigations

- Анализ групповых коммуникаций
- Correlation пользователей
- Mapping reply chains
- Поиск контактных данных

### Media Monitoring

- Анализ тематик каналов
- Detection narrative shifts
- Tracking keyword frequency
- Sentiment drift analysis

### Community Intelligence

- Mapping core participants
- Detection high-centrality users
- Reply topology analysis
- Communication density analysis

---

# Структура проекта

```text
.
├── app/
│   ├── routers/
│   ├── services/
│   ├── static/
│   └── templates/
├── graphs/
├── uploads/
├── config.json
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

# Установка

# Linux

## Ubuntu / Debian

Установка зависимостей:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

Клонирование проекта:

```bash
git clone <repo_url>
cd telanalysis
```

Создание virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установка Python-зависимостей:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Загрузка NLTK-данных:

```bash
python
```

В Python shell:

```python
import nltk
nltk.download('stopwords')
exit()
```

Запуск:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

Интерфейс:

```text
http://127.0.0.1:80
```

---

# macOS

## Установка через Homebrew

Установка Python:

```bash
brew install python
```

Клонирование проекта:

```bash
git clone <repo_url>
cd telanalysis
```

Создание virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установка зависимостей:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Установка NLTK stopwords:

```bash
python3
```

```python
import nltk
nltk.download('stopwords')
exit()
```

Запуск:

```bash
uvicorn app.main:app --reload
```

Открыть:

```text
http://127.0.0.1:80
```

---

# Windows

## Windows 10 / Windows 11

Установите:

- Python 3.11+
- Git

Python:

- https://www.python.org/downloads/

Git:

- https://git-scm.com/download/win

Во время установки Python:

```text
Enable → Add Python to PATH
```

Клонирование проекта:

```powershell
git clone <repo_url>
cd telanalysis
```

Создание virtualenv:

```powershell
python -m venv venv
```

Активация virtualenv:

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

CMD:

```cmd
venv\Scripts\activate.bat
```

Установка зависимостей:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Загрузка NLTK stopwords:

```powershell
python
```

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

