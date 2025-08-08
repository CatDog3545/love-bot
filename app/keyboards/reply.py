from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from app.utils.texts import get_text

def get_main_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    if language == "ru":
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
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👥 Browse profiles"),
                    KeyboardButton(text="👤 Profile")
                ],
                [
                    KeyboardButton(text="💬 Messages"),
                    KeyboardButton(text="⚙️ Settings")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_profile_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура профиля"""
    if language == "ru":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="✏️ Редактировать"),
                    KeyboardButton(text="📷 Управление фото")
                ],
                [
                    KeyboardButton(text="🏠 На главную")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="✏️ Edit"),
                    KeyboardButton(text="📷 Manage photos")
                ],
                [
                    KeyboardButton(text="🏠 Main menu")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_edit_profile_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура редактирования профиля"""
    if language == "ru":
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
                    KeyboardButton(text="↩️ К профилю")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🎂 Age"),
                    KeyboardButton(text="👫 Gender")
                ],
                [
                    KeyboardButton(text="💬 About me"),
                    KeyboardButton(text="🏙 City")
                ],
                [
                    KeyboardButton(text="↩️ To profile")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_browse_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура настройки поиска профилей"""
    if language == "ru":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🔍 Искать"),
                    KeyboardButton(text="👫 Кого искать")
                ],
                [
                    KeyboardButton(text="🎂 Возраст"),
                    KeyboardButton(text="🏙 Город")
                ],
                [
                    KeyboardButton(text="🏠 На главную")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🔍 Search"),
                    KeyboardButton(text="👫 Who to search")
                ],
                [
                    KeyboardButton(text="🎂 Age range"),
                    KeyboardButton(text="🏙 City")
                ],
                [
                    KeyboardButton(text="🏠 Main menu")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_profile_view_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура просмотра профилей при поиске"""
    if language == "ru":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👍 Лайк"),
                    KeyboardButton(text="👎 Дизлайк")
                ],
                [
                    KeyboardButton(text="⏭ Следующий профиль")
                ],
                [
                    KeyboardButton(text="🔙 Назад к поиску")
                ],
                [
                    KeyboardButton(text="🏠 На главную")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👍 Like"),
                    KeyboardButton(text="👎 Dislike")
                ],
                [
                    KeyboardButton(text="⏭ Next profile")
                ],
                [
                    KeyboardButton(text="🔙 Back to search")
                ],
                [
                    KeyboardButton(text="🏠 Main menu")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_settings_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура настроек"""
    if language == "ru":
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
                    KeyboardButton(text="🏠 На главную")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🌍 Language"),
                    KeyboardButton(text="🔔 Notifications")
                ],
                [
                    KeyboardButton(text="🔒 Privacy"),
                    KeyboardButton(text="❌ Delete account")
                ],
                [
                    KeyboardButton(text="🏠 Main menu")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_gender_preference_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура выбора пола для поиска"""
    if language == "ru":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👨 Парней"),
                    KeyboardButton(text="👩 Девушек")
                ],
                [
                    KeyboardButton(text="👫 Всех")
                ],
                [
                    KeyboardButton(text="🔙 Назад к поиску")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👨 Men"),
                    KeyboardButton(text="👩 Women")
                ],
                [
                    KeyboardButton(text="👫 Everyone")
                ],
                [
                    KeyboardButton(text="🔙 Back to search")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard
def get_photo_manage_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура управления фотографиями"""
    if language == "ru":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📷 Добавить фото"),
                    KeyboardButton(text="🖼 Просмотр фото")
                ],
                [
                    KeyboardButton(text="↩️ К профилю")
                ]
            ],
            resize_keyboard=True
        )
    else:  # English
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📷 Add photo"),
                    KeyboardButton(text="🖼 View photos")
                ],
                [
                    KeyboardButton(text="↩️ To profile")
                ]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_remove_keyboard() -> ReplyKeyboardRemove:
    """Убрать клавиатуру"""
    return ReplyKeyboardRemove()