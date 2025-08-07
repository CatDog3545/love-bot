from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from app.database import db
from app.keyboards.inline import get_browse_keyboard, get_like_keyboard
from app.utils.texts import get_text

async def start_browse(message: types.Message, state: FSMContext):
    """Начать просмотр профилей"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Проверяем, заполнен ли профиль
    if not user.get('age') or not user.get('gender'):
        await message.answer(get_text('complete_profile_first', language))
        return
    
    # Получаем следующий профиль для просмотра
    next_profile = get_next_profile(user_id, user.get('gender'))
    
    if not next_profile:
        await message.answer(get_text('no_profiles_found', language))
        return
    
    await show_profile_card(message, next_profile, language)

async def show_profile_card(message: types.Message, profile: dict, language: str):
    """Показать карточку профиля"""
    profile_text = f"👤 {profile.get('first_name', 'Пользователь')}\n"
    profile_text += f"🎂 {profile.get('age', 'Не указан')} лет\n"
    
    if profile.get('city'):
        profile_text += f"🏙 {profile.get('city')}\n"
    
    if profile.get('bio'):
        profile_text += f"💬 {profile.get('bio')}\n"
    
    # Здесь можно добавить фотографию профиля
    # await message.answer_photo(photo=profile_photo, caption=profile_text, reply_markup=get_like_keyboard())
    
    await message.answer(
        profile_text,
        reply_markup=get_like_keyboard(profile['id'])
    )

async def like_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Лайкнуть профиль"""
    user_id = callback_query.from_user.id
    target_user_id = int(callback_query.data.split(':')[1])
    
    # Добавляем лайк в базу данных
    add_like(user_id, target_user_id)
    
    # Проверяем взаимность
    if check_mutual_like(user_id, target_user_id):
        await callback_query.message.edit_text(get_text('match_found', 'ru'))
        # Здесь можно добавить уведомление о взаимном лайке
    else:
        await callback_query.message.edit_text(get_text('profile_liked', 'ru'))
    
    await callback_query.answer()

async def dislike_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Дизлайкнуть профиль"""
    await callback_query.message.edit_text(get_text('profile_skipped', 'ru'))
    await callback_query.answer()

async def next_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Показать следующий профиль"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    # Получаем следующий профиль
    next_profile = get_next_profile(user_id, user.get('gender'))
    
    if not next_profile:
        await callback_query.message.edit_text(get_text('no_more_profiles', language))
        return
    
    await show_profile_card(callback_query.message, next_profile, language)
    await callback_query.answer()

def get_next_profile(current_user_id: int, current_gender: str) -> dict:
    """Получить следующий профиль для просмотра"""
    # Здесь должна быть логика получения следующего профиля
    # Пока возвращаем заглушку
    return {
        'id': 1,
        'first_name': 'Анна',
        'age': 25,
        'city': 'Москва',
        'bio': 'Люблю путешествия и хорошие книги'
    }

def add_like(from_user_id: int, to_user_id: int) -> bool:
    """Добавить лайк в базу данных"""
    # Здесь должна быть логика добавления лайка
    # Пока возвращаем True
    return True

def check_mutual_like(user1_id: int, user2_id: int) -> bool:
    """Проверить взаимность лайков"""
    # Здесь должна быть логика проверки взаимности
    # Пока возвращаем False
    return False

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.message.register(start_browse, F.text == "👥 Смотреть профили")
    dp.callback_query.register(like_profile, F.data.startswith("like:"))
    dp.callback_query.register(dislike_profile, F.data.startswith("dislike:"))
    dp.callback_query.register(next_profile, F.data.startswith("next:")) 