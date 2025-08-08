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
        'send_photo': 'Отправьте фотографию для вашего профиля.',
        'not_a_photo': 'Пожалуйста, отправьте фотографию.',
        'photo_added': 'Фотография добавлена в ваш профиль.',
        'max_photos_reached': 'Вы уже добавили максимальное количество фотографий ({max_photos}).',
        'no_photos': 'У вас пока нет фотографий. Добавьте хотя бы одну фотографию.',
        'photo': 'Фото',
        'set_as_main': 'Сделать главной',
        'main_photo': 'Главная',
        'delete_photo': 'Удалить',
        'back': 'Назад',
        'photos_end': 'Конец списка фотографий',
        'main_photo_set': 'Фото установлено как главное!',
        'photo_deleted': 'Фото удалено!',
        'photo_not_found': 'Фото не найдено.',
        'manage_photos': 'Управление фотографиями',
        'view_photos': 'Просмотреть фото',
        'add_photo': 'Добавить фото',
        
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
        
        # Просмотр профилей
        'browse_options': 'Выберите опции поиска:',
        'rate_profile': 'Оцените профиль:',
        'like': '❤️ Нравится',
        'dislike': '❌ Не нравится',
        'next_profile': '⏭️ Следующий',
        'profile_view': 'Просмотр профиля',
        'no_more_profiles': 'Больше профилей нет. Попробуйте позже!',
        'profile_liked': 'Профиль понравился! ❤️',
        'profile_skipped': 'Профиль пропущен.',
        'match_found': 'У вас взаимная симпатия! 💕',
        'start_browsing': 'Начать просмотр профилей',
        'gender_preference': 'Выберите пол для поиска:',
        'all_genders': 'Все',
        'age_range': 'Диапазон возраста',
        'enter_min_age': 'Введите минимальный возраст (18-100):',
        'enter_max_age': 'Введите максимальный возраст (18-100):',
        'invalid_age_range': 'Максимальный возраст должен быть больше минимального.',
        'filters_applied': 'Фильтры применены!',
        'clear_filters_confirm': 'Фильтры очищены!',
        'profile_view_options': 'Выберите действие:',
        'db_error': 'Ошибка базы данных. Попробуйте позже.',
        'choose_gender_preference': 'Кого вы хотите найти?',
        'gender_male': 'Парней',
        'gender_female': 'Девушек',
        'gender_opposite': 'Противоположный пол',
        'gender_male_set': 'Теперь вы будете видеть только парней',
        'gender_female_set': 'Теперь вы будете видеть только девушек',
        'gender_opposite_set': 'Теперь вы будете видеть противоположный пол',
        'invalid_gender_preference': 'Пожалуйста, выберите один из предложенных вариантов.',
        'gender_preference_set': 'Настройки поиска сохранены',
        'age_too_low': 'Минимальный возраст должен быть не менее 18 лет.',
        'max_age_too_low': 'Максимальный возраст должен быть больше минимального.',
        'age_filter_set': 'Фильтр по возрасту установлен',
        'enter_city_filter': 'Введите название города для поиска:',
        'city_filter_set': 'Фильтр по городу установлен',
        'city_filter_cleared': 'Фильтр по городу сброшен',
        'invalid_min_age': 'Минимальный возраст должен быть не менее 18 лет',
        'invalid_max_age': 'Максимальный возраст должен быть больше минимального',
        'no_profile_to_rate': 'Нет профиля для оценки',
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
        'send_photo': 'Please send a photo for your profile.',
        'not_a_photo': 'Please send a photo.',
        'photo_added': 'Photo added to your profile.',
        'max_photos_reached': 'You have already added the maximum number of photos ({max_photos}).',
        'no_photos': 'You don\'t have any photos yet. Please add at least one photo.',
        'photo': 'Photo',
        'set_as_main': 'Set as main',
        'main_photo': 'Main',
        'delete_photo': 'Delete',
        'back': 'Back',
        'photos_end': 'End of photos list',
        'main_photo_set': 'Photo set as main!',
        'photo_deleted': 'Photo deleted!',
        'photo_not_found': 'Photo not found.',
        'manage_photos': 'Manage photos',
        'view_photos': 'View photos',
        'add_photo': 'Add photo',
        
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
        
        # Browsing
        'browse_options': 'Choose search options:',
        'rate_profile': 'Rate the profile:',
        'like': '❤️ Like',
        'dislike': '❌ Dislike',
        'next_profile': '⏭️ Next',
        'profile_view': 'Profile view',
        'no_more_profiles': 'No more profiles. Try again later!',
        'profile_liked': 'Profile liked! ❤️',
        'profile_skipped': 'Profile skipped.',
        'match_found': 'It\'s a match! 💕',
        'start_browsing': 'Start browsing profiles',
        'gender_preference': 'Choose gender for search:',
        'all_genders': 'All',
        'age_range': 'Age range',
        'enter_min_age': 'Enter minimum age (18-100):',
        'enter_max_age': 'Enter maximum age (18-100):',
        'invalid_age_range': 'Maximum age must be greater than minimum age.',
        'filters_applied': 'Filters applied!',
        'clear_filters_confirm': 'Filters cleared!',
        'profile_view_options': 'Choose action:',
        'db_error': 'Database error. Please try again later.',
        'choose_gender_preference': 'Who do you want to find?',
        'gender_male': 'Men',
        'gender_female': 'Women',
        'gender_opposite': 'Opposite gender',
        'gender_male_set': 'Now you will see only men',
        'gender_female_set': 'Now you will see only women',
        'gender_opposite_set': 'Now you will see the opposite gender',
        'invalid_gender_preference': 'Please choose one of the suggested options.',
        'gender_preference_set': 'Search settings saved',
        'age_too_low': 'Minimum age must be at least 18 years.',
        'max_age_too_low': 'Maximum age must be greater than minimum age.',
        'age_filter_set': 'Age filter set',
        'enter_city_filter': 'Enter city name for search:',
        'city_filter_set': 'City filter set',
        'city_filter_cleared': 'City filter cleared',
        'invalid_min_age': 'Minimum age must be at least 18 years',
        'invalid_max_age': 'Maximum age must be greater than minimum age',
        'no_profile_to_rate': 'No profile to rate',
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