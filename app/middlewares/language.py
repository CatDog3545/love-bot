from aiogram import types, BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from app.database import db

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Обработка событий для определения языка пользователя"""
        user_id = None
        
        # Определяем user_id в зависимости от типа события
        if isinstance(event, types.Message):
            user_id = event.from_user.id
        elif isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id
        
        if user_id:
            # Получаем пользователя из базы данных
            user = db.get_user(user_id)
            
            if user:
                data['language'] = user.get('language', 'ru')
            else:
                # Если пользователь новый, определяем язык по языку Telegram
                if isinstance(event, types.Message):
                    data['language'] = event.from_user.language_code or 'ru'
                elif isinstance(event, types.CallbackQuery):
                    data['language'] = event.from_user.language_code or 'ru'
                
                # Если язык не поддерживается, используем русский
                if data['language'] not in ['ru', 'en']:
                    data['language'] = 'ru'
        
        return await handler(event, data) 