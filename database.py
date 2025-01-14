import stat
import sqlite3
import os
from config import DB_NAME

class DatabaseClient:
    def __init__(self, db_path: str) -> None:
        """Inisialisasi kelas DatabaseClient untuk menghubungkan ke database SQLite."""
        self.db_path = db_path
        self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self._initialize_database()
        self._set_permissions()
    
    def _set_permissions(self):
        """Set file permissions untuk file database."""
        try:
            os.chmod(self.db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            print(f"Permissions for {self.db_path} set to 644.")
        except Exception as e:
            print(f"Failed to set permissions: {e}")

    def _initialize_database(self):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                gender_preference TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY,
                user_one INTEGER NOT NULL,
                user_two INTEGER NOT NULL,
                FOREIGN KEY (user_one) REFERENCES users (user_id),
                FOREIGN KEY (user_two) REFERENCES users (user_id)
            )
            """)
            conn.commit()
    
    def set_gender(self, user_id: int, name: str, gender: str, age: int, chat_id: int) -> None:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, chat_id, name, gender, age)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, chat_id, name, gender, age))
            conn.commit()

    def get_user(self, user_id: int):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return user
    
    def get_all_gender(self, gender: str):
        """Mengambil semua pengguna dengan gender tertentu."""
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE gender = ?", (gender,))
            users = cursor.fetchall()
            return users
        
    def get_gender(self, user_id: int):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT gender FROM users WHERE user_id = ?", (user_id,))
            gender = cursor.fetchone()
            return gender[0] if gender else None
    
    def add_queue(self, user_id: int, gender_preference: str, chat_id: int) -> None:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO queue (user_id, chat_id, gender_preference)
                VALUES (?, ?, ?)
                """, (user_id, chat_id, gender_preference))
            conn.commit()
    
    def del_queue(self, user_id: int) -> None:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM queue WHERE user_id = ?
                """, (user_id,))
            conn.commit()
    
    def get_queue(self) -> list:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, gender_preference, chat_id FROM queue")
            queue = cursor.fetchall()
        return queue
    
    def match_users(self, user_id: int, gender_preference: str) -> tuple:
        queue = self.get_queue()
        for user in queue:
            if user[1] == gender_preference:
                self.remove_from_queue(user[0])
                return user[0]
        return None
    
    def add_chat(self, chat_id, user_one: int, user_two: int) -> None:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chats (chat_id, user_one, user_two)
                VALUES (?, ?, ?)
                """, (chat_id, user_one, user_two))
            conn.commit()
    
    def get_active_chat(self, user_id: int):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT chat_id, user_one, user_two FROM chats WHERE user_one = ? OR user_two = ?
                """, (user_id, user_id))
            chat = cursor.fetchall()
            return chat if chat else None
        
    def get_chat(self, chat_id: int):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT chat_id, user_one, user_two FROM chats WHERE chat_id = ?
            """, (chat_id,))
            chat = cursor.fetchone()
            return chat if chat else None


db_path = os.path.abspath(f"./{DB_NAME}.db")
db = DatabaseClient(db_path)
print(f"DATABASE BERHASIL TERKONEKSI DENGAN {db_path}")