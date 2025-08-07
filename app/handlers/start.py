from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database import db
from app.keyboards.reply import get_main_keyboard
from app.keyboards.inline import get_language_keyboard
from app.utils.texts import get_text

async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Проверяем, существует ли пользователь в базе данных
    user = db.get_user(user_id)
    
    if not user:
        # Новый пользователь - добавляем в базу данных
        db.add_user(
            telegram_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language=message.from_user.language_code or 'ru'
        )
        
        # Показываем выбор языка
        await message.answer(
            get_text('welcome_new_user', 'ru'),
            reply_markup=get_language_keyboard()
        )
    else:
        # Существующий пользователь - показываем главное меню
        language = user.get('language', 'ru')
        
        if not user.get('age') or not user.get('gender'):
            # Профиль не заполнен
            await message.answer(
                get_text('complete_profile', language),
                reply_markup=get_main_keyboard(language)
            )
        else:
            # Профиль заполнен
            await message.answer(
                get_text('welcome_back', language),
                reply_markup=get_main_keyboard(language)
            )

async def set_language(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик выбора языка"""
    language = callback_query.data.split(':')[1]
    user_id = callback_query.from_user.id
    
    # Обновляем язык пользователя в базе данных
    db.update_user_profile(user_id, language=language)
    
    await callback_query.message.edit_text(
        get_text('language_set', language)
    )
    
    # Показываем главное меню
    await callback_query.message.answer(
        get_text('main_menu', language),
        reply_markup=get_main_keyboard(language)
    )

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.message.register(cmd_start, Command("start"))
    dp.callback_query.register(set_language, F.data.startswith("lang:")) 