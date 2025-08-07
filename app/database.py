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
            logger.error(f"Ошибка подключения к базе данных: {e}")
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

# Создание глобального экземпляра базы данных
db = Database() 