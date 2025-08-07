from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database import db
from app.keyboards.reply import get_profile_keyboard, get_main_keyboard
from app.keyboards.inline import get_gender_keyboard, get_edit_profile_keyboard
from app.utils.texts import get_text

class ProfileStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_bio = State()
    waiting_for_city = State()

async def show_profile(message: types.Message, state: FSMContext):
    """Показать профиль пользователя"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Формируем текст профиля
    profile_text = f"👤 {get_text('profile', language)}\n\n"
    profile_text += f"📝 {get_text('name', language)}: {user.get('first_name', 'Не указано')}\n"
    
    if user.get('age'):
        profile_text += f"🎂 {get_text('age', language)}: {user['age']}\n"
    
    if user.get('gender'):
        profile_text += f"👫 {get_text('gender', language)}: {get_text(user['gender'], language)}\n"
    
    if user.get('city'):
        profile_text += f"🏙 {get_text('city', language)}: {user['city']}\n"
    
    if user.get('bio'):
        profile_text += f"💬 {get_text('bio', language)}: {user['bio']}\n"
    
    await message.answer(
        profile_text,
        reply_markup=get_profile_keyboard(language)
    )

async def edit_profile(message: types.Message, state: FSMContext):
    """Редактирование профиля"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    await message.answer(
        get_text('edit_profile', language),
        reply_markup=get_edit_profile_keyboard(language)
    )

async def set_age_start(message: types.Message, state: FSMContext):
    """Начало установки возраста"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    await state.set_state(ProfileStates.waiting_for_age)
    await message.answer(get_text('enter_age', language))

async def set_age(message: types.Message, state: FSMContext):
    """Установка возраста"""
    try:
        age = int(message.text)
        if age < 18 or age > 100:
            await message.answer(get_text('invalid_age', 'ru'))
            return
        
        user_id = message.from_user.id
        db.update_user_profile(user_id, age=age)
        
        await state.clear()
        await message.answer(get_text('age_set', 'ru'))
        
    except ValueError:
        await message.answer(get_text('invalid_age_format', 'ru'))

async def set_gender_start(message: types.Message, state: FSMContext):
    """Начало установки пола"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    await message.answer(
        get_text('select_gender', language),
        reply_markup=get_gender_keyboard(language)
    )

async def set_gender(callback_query: types.CallbackQuery, state: FSMContext):
    """Установка пола"""
    gender = callback_query.data.split(':')[1]
    user_id = callback_query.from_user.id
    
    db.update_user_profile(user_id, gender=gender)
    
    await callback_query.message.edit_text(get_text('gender_set', 'ru'))
    await callback_query.answer()

async def set_bio_start(message: types.Message, state: FSMContext):
    """Начало установки био"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    await state.set_state(ProfileStates.waiting_for_bio)
    await message.answer(get_text('enter_bio', language))

async def set_bio(message: types.Message, state: FSMContext):
    """Установка био"""
    bio = message.text[:500]  # Ограничиваем длину
    user_id = message.from_user.id
    
    db.update_user_profile(user_id, bio=bio)
    
    await state.clear()
    await message.answer(get_text('bio_set', 'ru'))

async def set_city_start(message: types.Message, state: FSMContext):
    """Начало установки города"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    await state.set_state(ProfileStates.waiting_for_city)
    await message.answer(get_text('enter_city', language))

async def set_city(message: types.Message, state: FSMContext):
    """Установка города"""
    city = message.text
    user_id = message.from_user.id
    
    db.update_user_profile(user_id, city=city)
    
    await state.clear()
    await message.answer(get_text('city_set', 'ru'))

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.message.register(show_profile, F.text == "👤 Профиль")
    dp.message.register(edit_profile, F.text == "✏️ Редактировать")
    dp.message.register(set_age_start, F.text == "🎂 Возраст")
    dp.message.register(set_gender_start, F.text == "👫 Пол")
    dp.message.register(set_bio_start, F.text == "💬 О себе")
    dp.message.register(set_city_start, F.text == "🏙 Город")
    
    # Обработчики состояний
    dp.message.register(set_age, ProfileStates.waiting_for_age)
    dp.message.register(set_bio, ProfileStates.waiting_for_bio)
    dp.message.register(set_city, ProfileStates.waiting_for_city)
    
    # Callback обработчики
    dp.callback_query.register(set_gender, F.data.startswith("gender:")) 