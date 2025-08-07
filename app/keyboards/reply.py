from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from app.utils.texts import get_text

def get_main_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👥 Смотреть профили"),
                KeyboardButton(text="👤 Профиль")
            ],
            [
                KeyboardButton(text="💬 Сообщения"),
                KeyboardButton(text="⚙️ Настройки")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_profile_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура профиля"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✏️ Редактировать"),
                KeyboardButton(text="📸 Добавить фото")
            ],
            [
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_edit_profile_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура редактирования профиля"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎂 Возраст"),
                KeyboardButton(text="👫 Пол")
            ],
            [
                KeyboardButton(text="💬 О себе"),
                KeyboardButton(text="🏙 Город")
            ],
            [
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_browse_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура просмотра профилей"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❤️ Лайк"),
                KeyboardButton(text="❌ Пропустить")
            ],
            [
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_settings_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура настроек"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌍 Язык"),
                KeyboardButton(text="🔔 Уведомления")
            ],
            [
                KeyboardButton(text="🔒 Приватность"),
                KeyboardButton(text="❌ Удалить аккаунт")
            ],
            [
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_remove_keyboard() -> ReplyKeyboardRemove:
    """Убрать клавиатуру"""
    return ReplyKeyboardRemove() 