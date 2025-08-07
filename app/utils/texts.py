# Словарь с текстами на разных языках
TEXTS = {
    'ru': {
        # Общие
        'welcome_new_user': 'Добро пожаловать в Love Bot! 🌹\nВыберите язык для продолжения:',
        'welcome_back': 'С возвращением! 👋\nЧто хотите сделать?',
        'language_set': 'Язык успешно установлен! ✅',
        'main_menu': 'Главное меню',
        'back': '🔙 Назад',
        'error': 'Произошла ошибка. Попробуйте еще раз.',
        'user_not_found': 'Пользователь не найден.',
        
        # Профиль
        'profile': 'Профиль',
        'name': 'Имя',
        'age': 'Возраст',
        'gender': 'Пол',
        'city': 'Город',
        'bio': 'О себе',
        'complete_profile': 'Для начала заполните свой профиль! 📝',
        'edit_profile': 'Редактирование профиля',
        'enter_age': 'Введите ваш возраст (18-100):',
        'invalid_age': 'Возраст должен быть от 18 до 100 лет.',
        'invalid_age_format': 'Пожалуйста, введите число.',
        'age_set': 'Возраст успешно установлен! ✅',
        'select_gender': 'Выберите ваш пол:',
        'male': 'Мужской',
        'female': 'Женский',
        'gender_set': 'Пол успешно установлен! ✅',
        'enter_bio': 'Расскажите о себе (максимум 500 символов):',
        'bio_set': 'Информация о себе сохранена! ✅',
        'enter_city': 'Введите ваш город:',
        'city_set': 'Город успешно установлен! ✅',
        
        # Редактирование
        'edit_age': '🎂 Возраст',
        'edit_gender': '👫 Пол',
        'edit_bio': '💬 О себе',
        'edit_city': '🏙 Город',
        
        # Просмотр профилей
        'start_browse': 'Начать просмотр',
        'filters': 'Фильтры',
        'complete_profile_first': 'Сначала заполните свой профиль!',
        'no_profiles_found': 'Пока нет профилей для просмотра.',
        'no_more_profiles': 'Больше профилей нет. Попробуйте позже!',
        'profile_liked': 'Профиль понравился! ❤️',
        'profile_skipped': 'Профиль пропущен.',
        'match_found': 'У вас взаимная симпатия! 💕',
        
        # Фильтры
        'age_filter': 'Возраст',
        'city_filter': 'Город',
        'online_only': 'Только онлайн',
        'clear_filters': 'Очистить фильтры',
        
        # Сообщения
        'send_message': 'Написать сообщение',
        'continue_browse': 'Продолжить просмотр',
        
        # Настройки
        'settings': 'Настройки',
        'notifications': 'Уведомления',
        'privacy': 'Приватность',
        'delete_account': 'Удалить аккаунт',
    },
    
    'en': {
        # General
        'welcome_new_user': 'Welcome to Love Bot! 🌹\nChoose your language:',
        'welcome_back': 'Welcome back! 👋\nWhat would you like to do?',
        'language_set': 'Language set successfully! ✅',
        'main_menu': 'Main Menu',
        'back': '🔙 Back',
        'error': 'An error occurred. Please try again.',
        'user_not_found': 'User not found.',
        
        # Profile
        'profile': 'Profile',
        'name': 'Name',
        'age': 'Age',
        'gender': 'Gender',
        'city': 'City',
        'bio': 'About me',
        'complete_profile': 'Please complete your profile first! 📝',
        'edit_profile': 'Edit Profile',
        'enter_age': 'Enter your age (18-100):',
        'invalid_age': 'Age must be between 18 and 100.',
        'invalid_age_format': 'Please enter a number.',
        'age_set': 'Age set successfully! ✅',
        'select_gender': 'Select your gender:',
        'male': 'Male',
        'female': 'Female',
        'gender_set': 'Gender set successfully! ✅',
        'enter_bio': 'Tell us about yourself (max 500 characters):',
        'bio_set': 'About me saved successfully! ✅',
        'enter_city': 'Enter your city:',
        'city_set': 'City set successfully! ✅',
        
        # Editing
        'edit_age': '🎂 Age',
        'edit_gender': '👫 Gender',
        'edit_bio': '💬 About me',
        'edit_city': '🏙 City',
        
        # Browsing
        'start_browse': 'Start browsing',
        'filters': 'Filters',
        'complete_profile_first': 'Please complete your profile first!',
        'no_profiles_found': 'No profiles to browse yet.',
        'no_more_profiles': 'No more profiles. Try again later!',
        'profile_liked': 'Profile liked! ❤️',
        'profile_skipped': 'Profile skipped.',
        'match_found': 'It\'s a match! 💕',
        
        # Filters
        'age_filter': 'Age',
        'city_filter': 'City',
        'online_only': 'Online only',
        'clear_filters': 'Clear filters',
        
        # Messages
        'send_message': 'Send message',
        'continue_browse': 'Continue browsing',
        
        # Settings
        'settings': 'Settings',
        'notifications': 'Notifications',
        'privacy': 'Privacy',
        'delete_account': 'Delete account',
    }
}

def get_text(key: str, language: str = 'ru') -> str:
    """
    Получить текст по ключу и языку
    
    Args:
        key: Ключ текста
        language: Код языка (ru, en)
    
    Returns:
        Текст на указанном языке или ключ, если текст не найден
    """
    if language not in TEXTS:
        language = 'ru'  # Fallback to Russian
    
    return TEXTS[language].get(key, key) 