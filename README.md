# Love Bot - Telegram Dating Bot

Telegram бот для знакомств с поддержкой многоязычности (русский/английский).

## Структура проекта

```
love_bot/
├── app/
│   ├── database.py          # Работа с базой данных
│   ├── models.py            # Модели данных
│   ├── middlewares/
│   │   └── language.py      # Middleware для языка
│   ├── handlers/
│   │   ├── start.py         # Обработчик /start
│   │   ├── profile.py       # Обработчик профиля
│   │   └── browse.py        # Обработчик просмотра профилей
│   ├── keyboards/
│   │   ├── inline.py        # Inline клавиатуры
│   │   └── reply.py         # Reply клавиатуры
│   └── utils/
│       └── texts.py         # Тексты на разных языках
├── main.py                  # Главный файл бота
├── config.py               # Конфигурация
├── love_bot.db             # База данных SQLite
├── requirements.txt        # Зависимости
├── env.example            # Пример переменных окружения
└── README.md              # Документация
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd love_bot
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

5. Отредактируйте `.env` файл и добавьте токен вашего бота:
```
BOT_TOKEN=your_actual_bot_token_here
```

## Запуск

```bash
python main.py
```

## Функциональность

### Основные возможности:
- ✅ Регистрация новых пользователей
- ✅ Выбор языка (русский/английский)
- ✅ Создание и редактирование профиля
- ✅ Просмотр профилей других пользователей
- ✅ Система лайков и взаимных симпатий
- ✅ База данных SQLite

### Планируемые функции:
- 📸 Загрузка фотографий
- 💬 Система сообщений
- 🔍 Фильтры поиска
- 🔔 Уведомления
- ⚙️ Настройки приватности

## Технологии

- **Python 3.8+**
- **aiogram 2.25.1** - Telegram Bot API
- **SQLite** - База данных
- **python-dotenv** - Переменные окружения

## Лицензия

MIT License 