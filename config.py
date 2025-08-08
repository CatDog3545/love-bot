import os
from dotenv import load_dotenv, dotenv_values 

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройки базы данных
DATABASE_URL = "sqlite:///love_bot.db"

# Настройки приложения
DEFAULT_LANGUAGE = "ru"
SUPPORTED_LANGUAGES = ["ru", "en"]

# Настройки поиска
MAX_SEARCH_RESULTS = 10
MIN_AGE = 18
MAX_AGE = 100

# Настройки профиля
MAX_PHOTOS = 5
MAX_BIO_LENGTH = 500