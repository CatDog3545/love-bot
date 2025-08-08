import sqlite3
from sqlite3 import Error
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "love_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Создает соединение с базой данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Error as e:
            logger.error(f"Ошибка подключения к базе данных {self.db_path}: {e}")
            logger.error(f"Проверьте права доступа и существование директории")
            return None
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        if conn is None:
            return
        
        try:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    bio TEXT,
                    city TEXT,
                    language TEXT DEFAULT 'ru',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица фотографий
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    file_id TEXT NOT NULL,
                    file_path TEXT,
                    is_main BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Таблица лайков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS likes (
                    id INTEGER PRIMARY KEY,
                    from_user_id INTEGER,
                    to_user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_user_id) REFERENCES users (id),
                    FOREIGN KEY (to_user_id) REFERENCES users (id),
                    UNIQUE(from_user_id, to_user_id)
                )
            ''')
            
            conn.commit()
            logger.info("База данных успешно инициализирована")
            
        except Error as e:
            logger.error(f"Ошибка инициализации базы данных: {e}")
        finally:
            conn.close()
    
    def add_user(self, telegram_id: int, username: str = None, first_name: str = None, 
                 last_name: str = None, language: str = "ru") -> bool:
        """Добавление нового пользователя"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (telegram_id, username, first_name, last_name, language)
                VALUES (?, ?, ?, ?, ?)
            ''', (telegram_id, username, first_name, last_name, language))
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка добавления пользователя: {e}")
            return False
        finally:
            conn.close()
    
    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получение пользователя по telegram_id"""
        conn = self.get_connection()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
        except Error as e:
            logger.error(f"Ошибка получения пользователя: {e}")
            return None
        finally:
            conn.close()
    
    def update_user_profile(self, telegram_id: int, **kwargs) -> bool:
        """Обновление профиля пользователя"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values()) + [telegram_id]
            
            cursor.execute(f'''
                UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
            ''', values)
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка обновления профиля: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение пользователя по id"""
        conn = self.get_connection()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
        except Error as e:
            logger.error(f"Ошибка получения пользователя по id: {e}")
            return None
        finally:
            conn.close()
    
    def add_photo(self, user_id: int, file_id: str, file_path: str = None, is_main: bool = False) -> bool:
        """Добавление фотографии пользователя"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Если это главная фотография, сбрасываем флаг главной у других фотографий
            if is_main:
                cursor.execute('UPDATE photos SET is_main = 0 WHERE user_id = ?', (user_id,))
            
            cursor.execute('''
                INSERT INTO photos (user_id, file_id, file_path, is_main)
                VALUES (?, ?, ?, ?)
            ''', (user_id, file_id, file_path, is_main))
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка добавления фотографии: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_photos(self, user_id: int) -> List[Dict[str, Any]]:
        """Получение всех фотографий пользователя"""
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM photos WHERE user_id = ? ORDER BY is_main DESC, created_at ASC', (user_id,))
            photos = cursor.fetchall()
            return [dict(photo) for photo in photos]
        except Error as e:
            logger.error(f"Ошибка получения фотографий: {e}")
            return []
        finally:
            conn.close()
    
    def get_user_main_photo(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение главной фотографии пользователя"""
        conn = self.get_connection()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM photos WHERE user_id = ? AND is_main = 1 LIMIT 1', (user_id,))
            photo = cursor.fetchone()
            return dict(photo) if photo else None
        except Error as e:
            logger.error(f"Ошибка получения главной фотографии: {e}")
            return None
        finally:
            conn.close()
    
    def set_main_photo(self, photo_id: int, user_id: int) -> bool:
        """Установка фотографии как главной"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            # Сбрасываем флаг главной у всех фотографий пользователя
            cursor.execute('UPDATE photos SET is_main = 0 WHERE user_id = ?', (user_id,))
            # Устанавливаем флаг главной для выбранной фотографии
            cursor.execute('UPDATE photos SET is_main = 1 WHERE id = ? AND user_id = ?', (photo_id, user_id))
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка установки главной фотографии: {e}")
            return False
        finally:
            conn.close()
    
    def delete_photo(self, photo_id: int, user_id: int) -> bool:
        """Удаление фотографии"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM photos WHERE id = ? AND user_id = ?', (photo_id, user_id))
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка удаления фотографии: {e}")
            return False
        finally:
            conn.close()
    
    def get_photos_count(self, user_id: int) -> int:
        """Получение количества фотографий пользователя"""
        conn = self.get_connection()
        if conn is None:
            return 0
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM photos WHERE user_id = ?', (user_id,))
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            logger.error(f"Ошибка получения количества фотографий: {e}")
            return 0
        finally:
            conn.close()
    
    def add_like(self, from_user_id: int, to_user_id: int) -> bool:
        """Добавление лайка"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO likes (from_user_id, to_user_id)
                VALUES (?, ?)
            ''', (from_user_id, to_user_id))
            conn.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка добавления лайка: {e}")
            return False
        finally:
            conn.close()
    
    def check_mutual_like(self, user1_id: int, user2_id: int) -> bool:
        """Проверка взаимного лайка"""
        conn = self.get_connection()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM likes 
                WHERE (from_user_id = ? AND to_user_id = ?) 
                OR (from_user_id = ? AND to_user_id = ?)
            ''', (user1_id, user2_id, user2_id, user1_id))
            count = cursor.fetchone()[0]
            return count == 2
        except Error as e:
            logger.error(f"Ошибка проверки взаимного лайка: {e}")
            return False
        finally:
            conn.close()
    
    def get_likes_count(self, user_id: int) -> int:
        """Получение количества лайков пользователя"""
        conn = self.get_connection()
        if conn is None:
            return 0
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM likes WHERE to_user_id = ?', (user_id,))
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            logger.error(f"Ошибка получения количества лайков: {e}")
            return 0
        finally:
            conn.close()
    
    def get_matches_count(self, user_id: int) -> int:
        """Получение количества взаимных лайков (матчей)"""
        conn = self.get_connection()
        if conn is None:
            return 0
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM likes l1
                JOIN likes l2 ON l1.from_user_id = l2.to_user_id AND l1.to_user_id = l2.from_user_id
                WHERE l1.from_user_id = ?
            ''', (user_id,))
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            logger.error(f"Ошибка получения количества матчей: {e}")
            return 0
        finally:
            conn.close()
    
    def get_users_for_browse(self, current_user_id: int, gender_preference: str = None, 
                           age_min: int = 18, age_max: int = 100, city: str = None, 
                           limit: int = 10) -> List[Dict[str, Any]]:
        """Получение пользователей для просмотра с фильтрами"""
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            
            # Получаем текущего пользователя для определения пола
            current_user = self.get_user_by_id(current_user_id)
            if not current_user:
                return []
            
            current_gender = current_user.get('gender')
            
            # Определяем пол для поиска в зависимости от предпочтений
            if gender_preference == 'male':
                search_gender = "male"
            elif gender_preference == 'female':
                search_gender = "female"
            elif gender_preference == 'all' or gender_preference is None:
                search_gender = None
            else:
                # По умолчанию противоположный пол
                search_gender = "female" if current_gender == "male" else "male"
            
            # Базовый запрос
            query = '''
                SELECT u.* FROM users u
                WHERE u.id != ? AND u.is_active = 1
                AND u.age BETWEEN ? AND ?
            '''
            params = [current_user_id, age_min, age_max]
            
            # Добавляем фильтр по полу (если указан предпочтение)
            if search_gender:
                query += ' AND u.gender = ?'
                params.append(search_gender)
            
            # Добавляем фильтр по городу (если указан)
            if city:
                query += ' AND u.city = ?'
                params.append(city)
            
            # Исключаем пользователей, которых уже лайкали
            query += '''
                AND u.id NOT IN (
                    SELECT to_user_id FROM likes WHERE from_user_id = ?
                )
            '''
            params.append(current_user_id)
            
            # Добавляем лимит и сортировку
            query += ' ORDER BY u.updated_at DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            users = cursor.fetchall()
            return [dict(user) for user in users]
            
        except Error as e:
            logger.error(f"Ошибка получения пользователей для просмотра: {e}")
            return []
        finally:
            conn.close()

# Создание глобального экземпляра базы данных
db = Database()