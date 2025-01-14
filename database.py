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

    def set_gender(self, user_id, chat_id, name, gender, age):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result:
                cursor.execute(
                    "UPDATE users SET gender = ? WHERE user_id = ?",
                    (gender, user_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO users (user_id, chat_id, name, gender, age) VALUES (?, ?, ?, ?, ?)",
                    (user_id, chat_id, name, gender, age)
                )
            conn.commit()

    def get_all_gender(self):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, gender FROM users")
            return cursor.fetchall()

    def get_gender_by_user_id(self, user_id):
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT gender FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

db_path = os.path.abspath(f"./{DB_NAME}.db")
db = DatabaseClient(db_path)
print(f"DATABASE BERHASIL TERKONEKSI DENGAN {db_path}")