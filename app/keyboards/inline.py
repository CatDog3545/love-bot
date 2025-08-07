from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.texts import get_text

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en")
        ]
    ])
    return keyboard

def get_gender_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура выбора пола"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("male", language), callback_data="gender:male"),
            InlineKeyboardButton(text=get_text("female", language), callback_data="gender:female")
        ]
    ])
    return keyboard

def get_edit_profile_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура редактирования профиля"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("edit_age", language), callback_data="edit:age"),
            InlineKeyboardButton(text=get_text("edit_gender", language), callback_data="edit:gender")
        ],
        [
            InlineKeyboardButton(text=get_text("edit_bio", language), callback_data="edit:bio"),
            InlineKeyboardButton(text=get_text("edit_city", language), callback_data="edit:city")
        ],
        [
            InlineKeyboardButton(text=get_text("back", language), callback_data="back:main")
        ]
    ])
    return keyboard

def get_like_keyboard(profile_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для лайка/дизлайка профиля"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️", callback_data=f"like:{profile_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"dislike:{profile_id}")
        ],
        [
            InlineKeyboardButton(text="⏭️ Следующий", callback_data="next:profile")
        ]
    ])
    return keyboard

def get_browse_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура для просмотра профилей"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("start_browse", language), callback_data="browse:start"),
            InlineKeyboardButton(text=get_text("filters", language), callback_data="browse:filters")
        ],
        [
            InlineKeyboardButton(text=get_text("back", language), callback_data="back:main")
        ]
    ])
    return keyboard

def get_filters_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура фильтров поиска"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("age_filter", language), callback_data="filter:age"),
            InlineKeyboardButton(text=get_text("city_filter", language), callback_data="filter:city")
        ],
        [
            InlineKeyboardButton(text=get_text("online_only", language), callback_data="filter:online"),
            InlineKeyboardButton(text=get_text("clear_filters", language), callback_data="filter:clear")
        ],
        [
            InlineKeyboardButton(text=get_text("back", language), callback_data="back:browse")
        ]
    ])
    return keyboard

def get_match_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура для взаимного лайка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("send_message", language), callback_data="match:message"),
            InlineKeyboardButton(text=get_text("continue_browse", language), callback_data="match:continue")
        ]
    ])
    return keyboard 