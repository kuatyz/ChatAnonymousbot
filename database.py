import sqlite3
import os
import stat

class DatabaseClient:
    _connection: sqlite3.Connection

    def __init__(self, connection: sqlite3.Connection, db_path: str) -> None:
        self._connection = connection
        self.db_path = db_path
        self._initialize_database()
        self._set_permissions()

    def _initialize_database(self):
        """Inisialisasi tabel users, chats, dan queue jika belum ada."""
        cursor = self._connection.cursor()

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

        # Membuat tabel queue (antrian)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS queue (
                chat_id INTEGER PRIMARY KEY,
                gender TEXT,
                FOREIGN KEY (chat_id) REFERENCES users(user_id)
            )
            """
        )

        self._connection.commit()
        print("Tabel users, chats, dan queue berhasil dibuat atau sudah ada.")
        cursor.close()

    def _set_permissions(self):
        """Set file permissions untuk file database."""
        try:
            os.chmod(self.db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            print(f"Permissions for {self.db_path} set to 644.")
        except Exception as e:
            print(f"Failed to set permissions: {e}")

    def add_user(self, user_id: int, user_name: str, gender: str = None, age: int = None):
        cursor = self._connection.cursor()
        try:
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                cursor.execute(
                    "INSERT INTO users (user_id, user_name, gender, age) VALUES (?, ?, ?, ?)",
                    (user_id, user_name, gender, age),
                )
                self._connection.commit()
                print(f"User {user_name} dengan ID {user_id} berhasil ditambahkan.")

        except Exception as e:
            print(f"Gagal menambahkan user: {e}")
        finally:
            cursor.close()

    def delete_user(self, user_id: int):
        """Menghapus user dari tabel users."""
        cursor = self._connection.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self._connection.commit()
            print(f"User dengan ID {user_id} berhasil dihapus.")
        except Exception as e:
            print(f"Gagal menghapus user: {e}")
        finally:
            cursor.close()

    def get_all_users(self):
        cursor = self._connection.cursor()
        try:
            cursor.execute("SELECT user_id, user_name, gender, age FROM users")
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Gagal mengambil daftar user: {e}")
            return []
        finally:
            cursor.close()

    def get_user(self, user_id: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute("SELECT user_id, user_name, gender, age FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Gagal mengambil data user: {e}")
            return None
        finally:
            cursor.close()

    def add_chat(self, chat_one: int, chat_two: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute("SELECT * FROM chats WHERE chat_one = ? AND chat_two = ?", (chat_one, chat_two))
            existing_chat = cursor.fetchone()

            if not existing_chat:
                cursor.execute(
                    "INSERT INTO chats (chat_one, chat_two) VALUES (?, ?)", 
                    (chat_one, chat_two)
                )
                self._connection.commit()
                print(f"Chat antara {chat_one} dan {chat_two} berhasil dibuat.")
            else:
                print(f"Chat antara {chat_one} dan {chat_two} sudah ada.")
        except Exception as e:
            print(f"Gagal menambahkan chat: {e}")
        finally:
            cursor.close()

    def delete_chat(self, chat_id: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
            self._connection.commit()
            print(f"Chat dengan ID {chat_id} berhasil dihapus.")
        except Exception as e:
            print(f"Gagal menghapus chat: {e}")
        finally:
            cursor.close()

    def get_chat(self, chat_id: int):
        cursor = self._connection.cursor()
        try:
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
        finally:
            cursor.close()
            
    def get_active_chat(self, user_id: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute("SELECT * FROM chats WHERE chat_one = ? OR chat_two = ?", (user_id, user_id))
            active_chats = cursor.fetchall()
            
            if active_chats:
                print(f"Chats aktif untuk user {user_id}: {active_chats}")
                return active_chats
            else:
                print(f"Tidak ada chat aktif untuk user {user_id}.")
                return []
        except Exception as e:
            print(f"Gagal mengambil chat aktif: {e}")
        finally:
            cursor.close()
            
    def add_to_queue(self, chat_id: int, gender: str):
        cursor = self._connection.cursor()
        try:
            cursor.execute("INSERT INTO queue (chat_id, gender) VALUES (?, ?)", (chat_id, gender))
            self._connection.commit()
            print(f"User dengan ID {chat_id} ditambahkan ke antrian dengan gender {gender}.")
        except Exception as e:
            print(f"Gagal menambahkan ke antrian: {e}")
        finally:
            cursor.close()

    def remove_from_queue(self, chat_id: int):
        cursor = self._connection.cursor()
        try:
            cursor.execute("DELETE FROM queue WHERE chat_id = ?", (chat_id,))
            self._connection.commit()
            print(f"User dengan ID {chat_id} berhasil dihapus dari antrian.")
        except Exception as e:
            print(f"Gagal menghapus dari antrian: {e}")
        finally:
            cursor.close()

db_path = os.path.abspath("./mydatabase.db")
data = sqlite3.connect(db_path)
db = DatabaseClient(data, db_path)