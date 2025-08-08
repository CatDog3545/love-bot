from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from app.database import db
from app.keyboards.reply import get_profile_keyboard, get_main_keyboard, get_edit_profile_keyboard, get_photo_manage_keyboard
from app.keyboards.inline import get_gender_keyboard
from app.utils.texts import get_text
from config import MAX_PHOTOS

def get_user_main_photo(user_id):
    """Получить главную фотографию пользователя"""
    return db.get_user_main_photo(user_id)
        
def get_user_photos(user_id):
    """Получить все фотографии пользователя"""
    return db.get_user_photos(user_id)

class ProfileStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_bio = State()
    waiting_for_city = State()
    waiting_for_photo = State()
    waiting_for_photo_action = State()

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
    
    # Получаем главную фотографию пользователя
    main_photo = get_user_main_photo(user['id'])
    
    if main_photo:
        # Если есть фото, отправляем его с текстом профиля
        await message.answer_photo(
            photo=main_photo['file_id'],
            caption=profile_text,
            reply_markup=get_profile_keyboard(language)
        )
    else:
        # Если фото нет, отправляем только текст
        await message.answer(
            profile_text,
            reply_markup=get_profile_keyboard(language)
        )

async def edit_profile(message: types.Message, state: FSMContext):
    """Редактирование профиля"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    language = user.get('language', 'ru') if user else 'ru'
    
    # Используем reply клавиатуру вместо inline
    
    # Сбрасываем состояние FSM
    await state.clear()
    
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



async def back_to_edit_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """Возврат к редактированию профиля через callback"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await callback_query.message.answer(get_text('user_not_found', 'ru'))
        await callback_query.answer()
        return
    
    language = user.get('language', 'ru')
    
    # Сбрасываем состояние FSM
    await state.clear()
    
    await callback_query.message.answer(
        get_text('edit_profile', language),
        reply_markup=get_edit_profile_keyboard(language)
    )
    await callback_query.answer()

async def back_to_edit_profile_message(message: types.Message, state: FSMContext):
    """Возврат к редактированию профиля через сообщение"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Сбрасываем состояние FSM
    await state.clear()
    
    # Выводим сообщение с клавиатурой редактирования профиля
    await message.answer(
        get_text('edit_profile', language),
        reply_markup=get_edit_profile_keyboard(language)
    )

async def manage_photos(message: types.Message, state: FSMContext):
    """Управление фотографиями пользователя"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем все фотографии пользователя
    photos = get_user_photos(user['id'])
    
    # Используем reply клавиатуру вместо inline
    
    await message.answer(
        get_text('manage_photos', language).format(count=len(photos), max_photos=MAX_PHOTOS),
        reply_markup=get_photo_manage_keyboard(language)
    )

async def add_photo_start(message: types.Message, state: FSMContext):
    """Начало процесса добавления фотографии"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Проверяем количество уже загруженных фотографий
    photo_count = db.get_photos_count(user['id'])
    
    if photo_count >= MAX_PHOTOS:
        await message.answer(get_text('max_photos_reached', language).format(max_photos=MAX_PHOTOS))
        return
    
    await state.set_state(ProfileStates.waiting_for_photo)
    await message.answer(get_text('send_photo', language))

async def add_photo_start_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало процесса добавления фотографии через callback"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await callback_query.message.answer(get_text('user_not_found', 'ru'))
        await callback_query.answer()
        return
    
    language = user.get('language', 'ru')
    
    # Проверяем количество уже загруженных фотографий
    photo_count = db.get_photos_count(user['id'])
    
    if photo_count >= MAX_PHOTOS:
        await callback_query.message.answer(get_text('max_photos_reached', language).format(max_photos=MAX_PHOTOS))
        await callback_query.answer()
        return
    
    await state.set_state(ProfileStates.waiting_for_photo)
    await callback_query.message.answer(get_text('send_photo', language))
    await callback_query.answer()

async def add_photo(message: types.Message, state: FSMContext):
    """Обработка загруженной фотографии"""
    if not message.photo:
        user = db.get_user(message.from_user.id)
        language = user.get('language', 'ru') if user else 'ru'
        await message.answer(get_text('not_a_photo', language))
        return
    
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        await state.clear()
        return
    
    language = user.get('language', 'ru')
    
    # Получаем file_id фотографии (берем самый большой размер)
    file_id = message.photo[-1].file_id
    
    # Проверяем, есть ли уже фотографии у пользователя
    photo_count = db.get_photos_count(user['id'])
    
    # Если это первая фотография, делаем ее главной
    is_main = photo_count == 0
    
    # Добавляем фотографию в базу данных
    if db.add_photo(user['id'], file_id, is_main=is_main):
        await message.answer(get_text('photo_added', language))
        await state.clear()
        
        # Показываем обновленный профиль
        await show_profile(message, state)
    else:
        await message.answer(get_text('error', language))
        await state.clear()

async def view_photos(message: types.Message, state: FSMContext):
    """Просмотр всех фотографий пользователя"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await message.answer(get_text('user_not_found', 'ru'))
        return
    
    language = user.get('language', 'ru')
    
    # Получаем все фотографии пользователя
    photos = get_user_photos(user['id'])
    
    if not photos:
        await message.answer(get_text('no_photos', language))
        return
        
    await _view_photos_common(message, photos, language)

async def view_photos_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Просмотр всех фотографий пользователя через callback"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await callback_query.message.answer(get_text('user_not_found', 'ru'))
        await callback_query.answer()
        return
    
    language = user.get('language', 'ru')
    
    # Получаем все фотографии пользователя
    photos = get_user_photos(user['id'])
    
    if not photos:
        await callback_query.message.answer(get_text('no_photos', language))
        await callback_query.answer()
        return
        
    await _view_photos_common(callback_query.message, photos, language)
    await callback_query.answer()
    
async def _view_photos_common(message, photos, language):
    """Общая логика для просмотра фотографий"""
    # Получаем все фотографии пользователя
    if not photos:
        await message.answer(get_text('no_photos', language))
        return
    
    # Создаем клавиатуру для управления фотографиями
    
    for i, photo in enumerate(photos):
        # Для каждой фотографии создаем клавиатуру с действиями
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('set_as_main', language) if photo['is_main'] == 0 else get_text('main_photo', language),
                    callback_data=f"photo:main:{photo['id']}" if photo['is_main'] == 0 else "photo:info"
                ),
                InlineKeyboardButton(
                    text=get_text('delete_photo', language),
                    callback_data=f"photo:delete:{photo['id']}"
                )
            ]
        ])
        
        # Отправляем фотографию с клавиатурой
        photo_caption = f"{get_text('photo', language)} {i+1}/{len(photos)}"
        if photo['is_main'] == 1:
            photo_caption += f" ({get_text('main_photo', language)})"
            
        await message.answer_photo(
            photo=photo['file_id'],
            caption=photo_caption,
            reply_markup=keyboard
        )
    
    # Добавляем кнопку возврата после всех фотографий
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('back', language), callback_data="back:photos")
        ]
    ])
    
    await message.answer(
        get_text('photos_end', language),
        reply_markup=back_keyboard
    )

async def set_main_photo(callback_query: types.CallbackQuery, state: FSMContext):
    """Установка главной фотографии"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await callback_query.message.answer(get_text('user_not_found', 'ru'))
        await callback_query.answer()
        return
    
    language = user.get('language', 'ru')
    
    # Получаем ID фотографии из callback_data
    photo_id = int(callback_query.data.split(':')[2])
    
    # Устанавливаем фотографию как главную
    if db.set_main_photo(photo_id, user['id']):
        # Обновляем сообщение с фотографией
        await callback_query.message.edit_caption(
            caption=f"{callback_query.message.caption.split('(')[0]} ({get_text('main_photo', language)})",
            reply_markup=callback_query.message.reply_markup
        )
        
        await callback_query.answer(get_text('main_photo_set', language))
    else:
        await callback_query.message.answer(get_text('error', language))
        await callback_query.answer()

async def delete_photo(callback_query: types.CallbackQuery, state: FSMContext):
    """Удаление фотографии"""
    user_id = callback_query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await callback_query.message.answer(get_text('user_not_found', 'ru'))
        await callback_query.answer()
        return
    
    language = user.get('language', 'ru')
    
    # Получаем ID фотографии из callback_data
    photo_id = int(callback_query.data.split(':')[2])
    
    # Удаляем фотографию
    if db.delete_photo(photo_id, user['id']):
        # Удаляем сообщение с фотографией
        await callback_query.message.delete()
        
        await callback_query.answer(get_text('photo_deleted', language))
    else:
        await callback_query.answer(get_text('photo_not_found', language))

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
    # Русский интерфейс
    dp.message.register(show_profile, F.text == "👤 Профиль")
    dp.message.register(edit_profile, F.text == "✏️ Редактировать")
    dp.message.register(set_age_start, F.text == "🎂 Возраст")
    dp.message.register(set_gender_start, F.text == "👫 Пол")
    dp.message.register(set_bio_start, F.text == "💬 О себе")
    dp.message.register(set_city_start, F.text == "🏙 Город")
    dp.message.register(manage_photos, F.text == "📷 Управление фото")
    
    # Английский интерфейс
    dp.message.register(show_profile, F.text == "👤 Profile")
    dp.message.register(edit_profile, F.text == "✏️ Edit")
    dp.message.register(set_age_start, F.text == "🎂 Age")
    dp.message.register(set_gender_start, F.text == "👫 Gender")
    dp.message.register(set_bio_start, F.text == "💬 About me")
    dp.message.register(set_city_start, F.text == "🏙 City")
    dp.message.register(manage_photos, F.text == "📷 Manage photos")
    
    # Обработчики состояний
    dp.message.register(set_age, ProfileStates.waiting_for_age)
    dp.message.register(set_bio, ProfileStates.waiting_for_bio)
    dp.message.register(set_city, ProfileStates.waiting_for_city)
    dp.message.register(add_photo, ProfileStates.waiting_for_photo)
    
    # Обработчики для кнопок управления фотографиями
    dp.message.register(add_photo_start, F.text == "📷 Добавить фото")
    dp.message.register(add_photo_start, F.text == "📷 Add photo")
    dp.message.register(view_photos, F.text == "🖼 Просмотр фото")
    dp.message.register(view_photos, F.text == "🖼 View photos")
    
    # Обработчики для кнопок "На главную"
    dp.message.register(back_to_main_menu, F.text == "🏠 На главную")
    dp.message.register(back_to_main_menu, F.text == "🏠 Main menu")
    
    # Обработчики для кнопок "Назад" и "К профилю"
    dp.message.register(back_to_edit_profile_message, F.text.in_({"🔙 Назад", "🔙 Back", "↩️ К профилю", "↩️ To profile"}))
    
    # Callback обработчики
    dp.callback_query.register(set_gender, F.data.startswith("gender:"))
    dp.callback_query.register(add_photo_start_callback, F.data == "photo:add")
    dp.callback_query.register(view_photos_callback, F.data == "photo:view")
    dp.callback_query.register(set_main_photo, F.data.startswith("photo:main:"))
    dp.callback_query.register(delete_photo, F.data.startswith("photo:delete:"))
    dp.callback_query.register(back_to_edit_profile, F.data == "back:edit")
    dp.callback_query.register(back_to_edit_profile, F.data == "back:photos")