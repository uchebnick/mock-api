# Mock API Service

Сервис для эмуляции API с использованием искусственного интеллекта. Сервис предоставляет API для тестирования и разработки, имитируя поведение реальных API с помощью AI моделей.

## Особенности

- Эмуляция API с использованием AI моделей
- Автоматическая генерация документации API
- Подробное логирование запросов
- Обработка ошибок и исключений
- Поддержка CORS
- Мониторинг состояния сервера
- Гибкая конфигурация через YAML и .env файлы

## Требования

- Python 3.8+
- FastAPI
- Uvicorn
- Другие зависимости указаны в `requirements.txt`

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

1. Запустите сервер в режиме разработки:
```bash
uvicorn app.main:app --reload
```

2. Для продакшена:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/process
Основной эндпоинт для обработки запросов с помощью AI.

**Запрос:**
```json
{
    "query": "ваш запрос"
}
```

**Ответ:**
```json
{
    "response": "ответ от AI"
}
```

### GET /health
Проверка работоспособности сервера.

**Ответ:**
```json
{
    "status": "healthy"
}
```

## Middleware

### RequestLoggingMiddleware
- Логирует все входящие запросы
- Отслеживает время выполнения
- Логирует тело запроса
- Добавляет request_id для отслеживания

### ErrorHandlingMiddleware
- Перехватывает необработанные исключения
- Логирует ошибки
- Возвращает структурированные ответы с ошибками

## Логирование

Сервис использует встроенный модуль logging Python. Логи включают:
- Время начала и завершения запроса
- Метод и URL запроса
- Тело запроса (если есть)
- Время выполнения
- Ошибки и исключения

## Конфигурация

Конфигурация сервера находится в файле `app/config/app_config.py`. Основные параметры:
- Максимальное количество шагов для AI
- Настройки логирования
- Параметры CORS

### AI Конфигурация (.env)
Настройки для работы с AI моделями хранятся в файле `.env` в корне проекта:

```env
AI_TYPE=chatgpt
AI_MODEL=gemma3:1b
AI_TOKEN=your_token_here
AI_BASE_URL=https://api.example.com
```

- `AI_TYPE` - тип AI сервиса (например, chatgpt, ollama)
- `AI_MODEL` - название модели для использования
- `AI_TOKEN` - API токен для доступа к сервису
- `AI_BASE_URL` - базовый URL API сервиса

### Конфигурация приложения (config.yaml)
Настройки приложения хранятся в файле `config.yaml` в корне проекта:

```yaml
terminal:
  enabled: false

database:
  enabled: false

text_storage:
  enabled: false

system:
  enabled: true
  max_steps: 2
```

#### Секции конфигурации:

- **terminal** - настройки терминальных команд
  - `enabled` - включены ли терминальные команды

- **database** - настройки базы данных
  - `enabled` - включены ли команды базы данных

- **text_storage** - настройки текстового хранилища
  - `enabled` - включено ли текстовое хранилище

- **system** - системные настройки
  - `enabled` - включены ли системные промпты
  - `max_steps` - максимальное количество шагов выполнения

### Использование конфигурации

```python
from app.config.ai_config import get_ai_config
from app.config.app_config import get_app_config

# Получение AI конфигурации
ai_config = get_ai_config()
print(ai_config.ai_type)  # chatgpt
print(ai_config.model)    # gemma3:1b

# Получение конфигурации приложения
app_config = get_app_config()
print(app_config.use_terminal)  # False
print(app_config.max_steps)     # 2
```

## Разработка

### Структура проекта
```