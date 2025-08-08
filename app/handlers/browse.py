from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
from app.database import db
from app.keyboards.inline import get_browse_keyboard as get_browse_inline_keyboard, get_like_keyboard
from app.keyboards.reply import get_main_keyboard, get_browse_keyboard, get_profile_view_keyboard, get_gender_preference_keyboard
from app.utils.texts import get_text

class BrowseStates(StatesGroup):
    """Состояния для просмотра профилей"""
    waiting_for_gender_preference = State()  # Ожидание выбора пола для поиска
    waiting_for_age_min = State()  # Ожидание минимального возраста
    waiting_for_age_max = State()  # Ожидание максимального возраста
    waiting_for_city = State()  # Ожидание города

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
    
    # Сбрасываем состояние FSM
    await state.clear()
    
    # Показываем клавиатуру с опциями поиска
    await message.answer(
        get_text('browse_options', language) or "Выберите опции поиска:",
        reply_markup=get_browse_keyboard(language)
    )

async def browse_profiles(message: types.Message, state: FSMContext):
    """Просмотр профилей с текущими фильтрами"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем данные о фильтрах из состояния
    state_data = await state.get_data()
    gender_preference = state_data.get('gender_preference', None)  # None = все
    age_min = state_data.get('age_min', 18)
    age_max = state_data.get('age_max', 100)
    city = state_data.get('city', None)
    
    # Сохраняем фильтры в состоянии для использования при переходе к следующему профилю
    await state.update_data({
        'gender_preference': gender_preference,
        'age_min': age_min,
        'age_max': age_max,
        'city': city
    })
    
    # Получаем следующий профиль с учетом фильтров
    profile = await get_next_profile(user_id, gender_preference, age_min, age_max, city)
    
    if not profile:
        await message.answer(
            get_text('no_profiles_found', language) or "К сожалению, не найдено подходящих профилей.",
            reply_markup=get_browse_keyboard(language)
        )
        return
    
    # Сохраняем ID текущего профиля в состоянии
    await state.update_data(current_profile_id=profile['id'])
    
    # Показываем профиль
    await show_profile_card(message, profile, language)
    
    # Показываем клавиатуру для оценки профиля
    await message.answer(
        get_text('rate_profile', language) or "Оцените профиль:",
        reply_markup=get_profile_view_keyboard(language)
    )

async def show_profile_card(message: types.Message, profile: dict, language: str):
    """Показать карточку профиля"""
    profile_text = f"👤 {profile.get('first_name', 'Пользователь')}\n"
    profile_text += f"🎂 {profile.get('age', 'Не указан')} лет\n"
    
    if profile.get('city'):
        profile_text += f"🏙 {profile.get('city')}\n"
    
    if profile.get('bio'):
        profile_text += f"💬 {profile.get('bio')}\n"
    
    # Получаем главную фотографию профиля
    main_photo = db.get_user_main_photo(profile['id'])
    
    if main_photo:
        # Если есть фото, отправляем его с текстом профиля
        await message.answer_photo(
            photo=main_photo['file_id'],
            caption=profile_text,
            reply_markup=get_like_keyboard(profile['id'])
        )
    else:
        # Если фото нет, отправляем только текст
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
        await callback_query.message.edit_caption(
            caption=callback_query.message.caption + "\n\n" + get_text('match_found', 'ru')
        )
        # Здесь можно добавить уведомление о взаимном лайке
    else:
        await callback_query.message.edit_caption(
            caption=callback_query.message.caption + "\n\n" + get_text('profile_liked', 'ru')
        )
    
    await callback_query.answer()

async def dislike_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Дизлайкнуть профиль"""
    await callback_query.message.edit_caption(
        caption=callback_query.message.caption + "\n\n" + get_text('profile_skipped', 'ru')
    )
    await callback_query.answer()

async def next_profile(message: types.Message, state: FSMContext):
    """Показать следующий профиль"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем данные о фильтрах из состояния
    data = await state.get_data()
    gender_preference = data.get('gender_preference', None)
    age_min = data.get('age_min', 18)
    age_max = data.get('age_max', 100)
    city = data.get('city', None)
    
    # Получаем следующий профиль с учетом фильтров
    profile = await get_next_profile(user_id, gender_preference, age_min, age_max, city)
    
    if not profile:
        await message.answer(
            get_text('no_profiles_found', language) or "К сожалению, не найдено подходящих профилей.",
            reply_markup=get_browse_keyboard(language)
        )
        return
    
    # Сохраняем ID текущего профиля в состоянии
    await state.update_data(current_profile_id=profile['id'])
    
    # Показываем профиль
    await show_profile_card(message, profile, language)
    
    # Показываем клавиатуру для оценки профиля
    await message.answer(
        get_text('rate_profile', language) or "Оцените профиль:",
        reply_markup=get_profile_view_keyboard(language)
    )

async def set_gender_preference_start(message: types.Message, state: FSMContext):
    """Начать выбор пола для поиска"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(BrowseStates.waiting_for_gender_preference)
    
    # Показываем клавиатуру выбора пола
    await message.answer(
        get_text('choose_gender_preference', language) or "Кого вы хотите найти?",
        reply_markup=get_gender_preference_keyboard(language)
    )

async def set_gender_preference(message: types.Message, state: FSMContext):
    """Установить пол для поиска"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    text = message.text.lower()
    
    # Определяем выбранный пол
    if 'парней' in text or 'men' in text:
        gender_preference = 'male'
    elif 'девушек' in text or 'women' in text:
        gender_preference = 'female'
    elif 'всех' in text or 'everyone' in text:
        gender_preference = 'all'
    else:
        # Если текст не соответствует ни одному из вариантов, просим выбрать снова
        await message.answer(
            get_text('invalid_gender_preference', language) or "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=get_gender_preference_keyboard(language)
        )
        return
    
    # Сохраняем выбранный пол в состоянии
    await state.update_data(gender_preference=gender_preference)
    
    # Сбрасываем состояние
    await state.clear()
    
    # Возвращаемся к опциям поиска
    await message.answer(
        get_text('gender_preference_set', language) or f"Установлен поиск: {text}",
        reply_markup=get_browse_keyboard(language)
    )

async def back_to_browse(message: types.Message, state: FSMContext):
    """Вернуться к опциям поиска"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Сбрасываем состояние
    await state.clear()
    
    # Возвращаемся к опциям поиска
    await message.answer(
        get_text('browse_options', language) or "Выберите опции поиска:",
        reply_markup=get_browse_keyboard(language)
    )

async def set_age_filter_start(message: types.Message, state: FSMContext): 
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Устанавливаем состояние ожидания минимального возраста
    await state.set_state(BrowseStates.waiting_for_age_min)
    
    # Запрашиваем минимальный возраст
    await message.answer(
        get_text('enter_min_age', language) or "Введите минимальный возраст (от 18):",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def set_age_min(message: types.Message, state: FSMContext):
    """Установить минимальный возраст для поиска"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Проверяем, что введено число
    try:
        age_min = int(message.text)
        if age_min < 18:
            await message.answer(
                get_text('age_too_low', language) or "Минимальный возраст должен быть не менее 18 лет."
            )
            return
    except ValueError:
        await message.answer(
            get_text('invalid_age', language) or "Пожалуйста, введите число."
        )
        return
    
    # Сохраняем минимальный возраст в состоянии
    await state.update_data(age_min=age_min)
    
    # Переходим к вводу максимального возраста
    await state.set_state(BrowseStates.waiting_for_age_max)
    
    # Запрашиваем максимальный возраст
    await message.answer(
        get_text('enter_max_age', language) or f"Введите максимальный возраст (от {age_min}):"
    )

async def set_age_max(message: types.Message, state: FSMContext):
    """Установить максимальный возраст для поиска"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем минимальный возраст из состояния
    data = await state.get_data()
    age_min = data.get('age_min', 18)
    
    # Проверяем, что введено число
    try:
        age_max = int(message.text)
        if age_max < age_min:
            await message.answer(
                get_text('max_age_too_low', language) or f"Максимальный возраст должен быть не менее {age_min} лет."
            )
            return
    except ValueError:
        await message.answer(
            get_text('invalid_age', language) or "Пожалуйста, введите число."
        )
        return
    
    # Сохраняем максимальный возраст в состоянии
    await state.update_data(age_max=age_max)
    
    # Сбрасываем состояние
    await state.clear()
    
    # Возвращаемся к опциям поиска
    await message.answer(
        get_text('age_filter_set', language) or f"Установлен возрастной фильтр: {age_min}-{age_max} лет",
        reply_markup=get_browse_keyboard(language)
    )

async def set_city_filter_start(message: types.Message, state: FSMContext):
    """Начать установку фильтра по городу"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Устанавливаем состояние ожидания города
    await state.set_state(BrowseStates.waiting_for_city)
    
    # Запрашиваем город
    await message.answer(
        get_text('enter_city_filter', language) or "Введите название города для поиска:",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def set_city_filter(message: types.Message, state: FSMContext):
    """Установить фильтр по городу"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    city = message.text.strip()
    
    # Сохраняем город в состоянии
    await state.update_data(city=city)
    
    # Сбрасываем состояние
    await state.clear()
    
    # Возвращаемся к опциям поиска
    await message.answer(
        get_text('city_filter_set', language) or f"Установлен фильтр по городу: {city}",
        reply_markup=get_browse_keyboard(language)
    )

async def get_next_profile(current_user_id: int, gender_preference: str = None, age_min: int = 18, age_max: int = 100, city: str = None) -> dict:
    """Получить следующий профиль для просмотра с учетом фильтров"""
    users = db.get_users_for_browse(current_user_id, gender_preference, age_min, age_max, city, limit=1)
    return users[0] if users else None

def add_like(from_user_id: int, to_user_id: int) -> bool:
    """Добавить лайк в базу данных"""
    # Получаем ID пользователя из таблицы users
    from_user = db.get_user(from_user_id)
    if not from_user:
        return False
    
    return db.add_like(from_user['id'], to_user_id)

def check_mutual_like(user1_id: int, user2_id: int) -> bool:
    """Проверить взаимность лайков"""
    # Получаем ID пользователя из таблицы users
    user1 = db.get_user(user1_id)
    user2 = db.get_user(user2_id)
    
    if not user1 or not user2:
        return False
    
    return db.check_mutual_like(user1['id'], user2['id'])

async def like_profile_message(message: types.Message, state: FSMContext):
    """Лайкнуть профиль через сообщение"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем данные о текущем профиле из состояния
    data = await state.get_data()
    current_profile_id = data.get('current_profile_id')
    
    if not current_profile_id:
        await message.answer(get_text('no_profile_to_rate', language) or "Нет профиля для оценки")
        return
    
    # Добавляем лайк в базу данных
    add_like(user_id, current_profile_id)
    
    # Проверяем взаимность
    if check_mutual_like(user_id, current_profile_id):
        await message.answer(get_text('match_found', language))
    else:
        await message.answer(get_text('profile_liked', language))
    
    # Показываем следующий профиль
    await next_profile(message, state)

async def dislike_profile_message(message: types.Message, state: FSMContext):
    """Дизлайкнуть профиль через сообщение"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    await message.answer(get_text('profile_skipped', language))
    
    # Показываем следующий профиль
    await next_profile(message, state)

async def back_to_main_menu(message: types.Message, state: FSMContext):
    """Возврат в главное меню"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Сбрасываем состояние FSM
    await state.clear()
    
    await message.answer(
        get_text('main_menu', language),
        reply_markup=get_main_keyboard(language)
    )

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    # Основные команды
    dp.message.register(start_browse, F.text.in_({"👥 Смотреть профили", "👥 Browse profiles"}))
    dp.message.register(browse_profiles, F.text.in_({"🔍 Искать", "🔍 Search"}))
    
    # Фильтры поиска
    dp.message.register(set_gender_preference_start, F.text.in_({"👫 Кого искать", "👫 Who to search"}))
    dp.message.register(set_age_filter_start, F.text.in_({"🎂 Возраст", "🎂 Age range"}))
    dp.message.register(set_city_filter_start, F.text.in_({"🏙 Город", "🏙 City"}))
    
    # Обработчики состояний
    dp.message.register(set_gender_preference, BrowseStates.waiting_for_gender_preference)
    dp.message.register(set_age_min, BrowseStates.waiting_for_age_min)
    dp.message.register(set_age_max, BrowseStates.waiting_for_age_max)
    dp.message.register(set_city_filter, BrowseStates.waiting_for_city)
    
    # Обработчики для кнопки "Назад к поиску"
    dp.message.register(back_to_browse, F.text.in_({"🔙 Назад к поиску", "🔙 Back to search"}))
    
    # Обработчики для кнопок просмотра профилей
    dp.message.register(next_profile, F.text.in_({"⏭ Следующий профиль", "⏭ Next profile"}))
    
    # Обработчики для кнопок лайк/дизлайк (через сообщения)
    dp.message.register(like_profile_message, F.text.in_({"👍 Лайк", "👍 Like"}))
    dp.message.register(dislike_profile_message, F.text.in_({"👎 Дизлайк", "👎 Dislike"}))
    
    # Callback обработчики
    dp.callback_query.register(like_profile, F.data.startswith("like:"))
    dp.callback_query.register(dislike_profile, F.data.startswith("dislike:"))
    
    # Обработчики для кнопок "Назад" и "На главную"
    dp.message.register(back_to_main_menu, F.text == "🔙 Назад")
    dp.message.register(back_to_main_menu, F.text == "🔙 Back")
    dp.message.register(back_to_main_menu, F.text == "🏠 На главную")
    dp.message.register(back_to_main_menu, F.text == "🏠 Main menu")