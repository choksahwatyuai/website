import os
import json
import pickle
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession

class SessionManager:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_file = 'session_data.pickle'
        self.cookies_file = 'cookies.json'
        self.session = None
        self.client = None

    async def load_session(self):
        """Загружает существующую сессию или создает новую"""
        try:
            # Пробуем загрузить существующую сессию
            if os.path.exists(self.session_file):
                with open(self.session_file, 'rb') as f:
                    session_data = pickle.load(f)
                    
                # Проверяем срок действия сессии
                if self._is_session_valid(session_data):
                    self.session = session_data['session']
                    print("Сессия успешно загружена из файла")
                    return True
                else:
                    print("Сессия устарела, требуется новая авторизация")
                    os.remove(self.session_file)
                    if os.path.exists(self.cookies_file):
                        os.remove(self.cookies_file)
            
            return False
        except Exception as e:
            print(f"Ошибка при загрузке сессии: {e}")
            return False

    async def create_new_session(self):
        """Создает новую сессию и сохраняет её"""
        try:
            # Создаем новую строковую сессию
            string_session = StringSession()
            self.client = TelegramClient(string_session, self.api_id, self.api_hash)
            
            # Подключаемся и сохраняем данные сессии
            await self.client.start()
            
            session_data = {
                'session': string_session.save(),
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
            }

            # Сохраняем сессию
            with open(self.session_file, 'wb') as f:
                pickle.dump(session_data, f)

            # Сохраняем куки
            if hasattr(self.client, 'session') and hasattr(self.client.session, 'cookies'):
                cookies = self.client.session.cookies
                with open(self.cookies_file, 'w') as f:
                    json.dump(cookies, f)

            print("Новая сессия успешно создана и сохранена")
            return True
        except Exception as e:
            print(f"Ошибка при создании новой сессии: {e}")
            return False

    def _is_session_valid(self, session_data):
        """Проверяет, действительна ли текущая сессия"""
        try:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            return datetime.now() < expires_at
        except:
            return False

    async def get_client(self):
        """Возвращает активный клиент, создавая новую сессию если необходимо"""
        if not await self.load_session():
            if not await self.create_new_session():
                raise Exception("Не удалось создать сессию")
        
        if not self.client:
            self.client = TelegramClient(
                StringSession(self.session),
                self.api_id,
                self.api_hash
            )
            await self.client.start()
        
        return self.client

    async def close(self):
        """Закрывает клиент"""
        if self.client:
            await self.client.disconnect() 