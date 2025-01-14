import sqlite3
import os
import stat
from config import DB_NAME

class DatabaseClient:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self._initialize_database()
        self._set_permissions()

    def _initialize_database(self):
        """Inisialisasi tabel users, chats, dan queue jika belum ada."""
        with self._connection as conn:
            cursor = conn.cursor()

            # Membuat tabel users
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    gender TEXT,
                    age INTEGER
                )
                """
            )

            # Membuat tabel chats
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY,
                    chat_one INTEGER,
                    chat_two INTEGER,
                    FOREIGN KEY (chat_one) REFERENCES users(user_id),
                    FOREIGN KEY (chat_two) REFERENCES users(user_id)
                )
                """
            )

            # Membuat tabel queue
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS queue (
                    chat_id INTEGER PRIMARY KEY,
                    gender TEXT,
                    FOREIGN KEY (chat_id) REFERENCES users(user_id)
                )
                """
            )

            print("Tabel users, chats, dan queue berhasil dibuat atau sudah ada.")

    def _set_permissions(self):
        """Set file permissions untuk file database."""
        try:
            os.chmod(self.db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            print(f"Permissions for {self.db_path} set to 644.")
        except Exception as e:
            print(f"Failed to set permissions: {e}")
    
    def add_user(self, user_id: int, user_name: str, gender: str = None, age: int = None):
        """Menambahkan user ke tabel users."""
        if not (user_name and gender and age):  # Pastikan semua data lengkap
            raise ValueError("Data pengguna tidak lengkap. Pastikan semua parameter disediakan.")
        
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
                existing_user = cursor.fetchone()
                
                if not existing_user:
                    cursor.execute(
                        "INSERT INTO users (user_id, user_name, gender, age) VALUES (?, ?, ?, ?)",
                        (user_id, user_name, gender, age),
                        )
                    print(f"User {user_name} dengan ID {user_id} berhasil ditambahkan.")
                else:
                    print(f"User dengan ID {user_id} sudah ada.")
        except Exception as e:
            print(f"Gagal menambahkan user: {e}")


    def delete_user(self, user_id: int):
        """Menghapus user dari tabel users."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                print(f"User dengan ID {user_id} berhasil dihapus.")
        except Exception as e:
            print(f"Gagal menghapus user: {e}")
            
    def get_all_users(self, gender=None):
        """Mengambil semua user dari tabel users, dengan opsi filter gender."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                if gender:
                    cursor.execute(
                        "SELECT user_id, user_name, gender, age FROM users WHERE gender = ?", 
                        (gender,)
                )
                else:
                    cursor.execute("SELECT user_id, user_name, gender, age FROM users")
                return cursor.fetchall()
        except Exception as e:
            print(f"Gagal mengambil daftar user: {e}")
            return []

    
    def get_chat(self, chat_id: int):
        """Mengambil data chat berdasarkan chat_id."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM chats WHERE id = ?", (chat_id,))
                chat = cursor.fetchone()
                
                if chat:
                    print(f"Chat ditemukan: {chat}")
                    return chat
                else:
                    print(f"Chat dengan ID {chat_id} tidak ditemukan.")
                    return None
        except Exception as e:
            print(f"Gagal mengambil chat: {e}")
            return None
        
    def get_active_chat(self):
        """Mengambil semua chat aktif dari tabel chats."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM chats")
                active_chats = cursor.fetchall()
                
                if active_chats:
                    print(f"Chat aktif ditemukan: {active_chats}")
                    return active_chats
                else:
                    print("Tidak ada chat aktif.")
                    return []
        except Exception as e:
            print(f"Gagal mengambil chat aktif: {e}")
            return []

    def add_chat(self, chat_one: int, chat_two: int):
        """Menambahkan chat ke tabel chats."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM chats WHERE chat_one = ? AND chat_two = ?", (chat_one, chat_two))
                existing_chat = cursor.fetchone()

                if not existing_chat:
                    cursor.execute(
                        "INSERT INTO chats (chat_one, chat_two) VALUES (?, ?)", 
                        (chat_one, chat_two)
                    )
                    print(f"Chat antara {chat_one} dan {chat_two} berhasil dibuat.")
                else:
                    print(f"Chat antara {chat_one} dan {chat_two} sudah ada.")
        except Exception as e:
            print(f"Gagal menambahkan chat: {e}")

    def delete_chat(self, chat_id: int):
        """Menghapus chat dari tabel chats."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
                print(f"Chat dengan ID {chat_id} berhasil dihapus.")
        except Exception as e:
            print(f"Gagal menghapus chat: {e}")

    def add_to_queue(self, chat_id: int, gender: str):
        """Menambahkan user ke tabel queue."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO queue (chat_id, gender) VALUES (?, ?)", (chat_id, gender))
                print(f"User dengan ID {chat_id} ditambahkan ke antrian dengan gender {gender}.")
        except Exception as e:
            print(f"Gagal menambahkan ke antrian: {e}")

    def remove_from_queue(self, chat_id: int):
        """Menghapus user dari tabel queue."""
        try:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM queue WHERE chat_id = ?", (chat_id,))
                print(f"User dengan ID {chat_id} berhasil dihapus dari antrian.")
        except Exception as e:
            print(f"Gagal menghapus dari antrian: {e}")

    def __del__(self):
        """Menutup koneksi database saat instance dihancurkan."""
        if self._connection:
            self._connection.close()


# Inisialisasi database
db_path = os.path.abspath(f"./{DB_NAME}.db")
db = DatabaseClient(db_path)
