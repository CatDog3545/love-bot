from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    bio: Optional[str]
    city: Optional[str]
    language: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            telegram_id=data['telegram_id'],
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            gender=data['gender'],
            bio=data['bio'],
            city=data['city'],
            language=data['language'],
            is_active=bool(data['is_active']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

@dataclass
class Photo:
    id: int
    user_id: int
    file_id: str
    file_path: Optional[str]
    is_main: bool
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            file_id=data['file_id'],
            file_path=data['file_path'],
            is_main=bool(data['is_main']),
            created_at=datetime.fromisoformat(data['created_at'])
        )

@dataclass
class Like:
    id: int
    from_user_id: int
    to_user_id: int
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            from_user_id=data['from_user_id'],
            to_user_id=data['to_user_id'],
            created_at=datetime.fromisoformat(data['created_at'])
        )

@dataclass
class UserProfile:
    user: User
    photos: List[Photo]
    likes_count: int
    matches_count: int
    
    @property
    def main_photo(self) -> Optional[Photo]:
        """Возвращает главную фотографию пользователя"""
        for photo in self.photos:
            if photo.is_main:
                return photo
        return self.photos[0] if self.photos else None

@dataclass
class SearchFilters:
    min_age: int = 18
    max_age: int = 100
    gender: Optional[str] = None
    city: Optional[str] = None
    online_only: bool = False 