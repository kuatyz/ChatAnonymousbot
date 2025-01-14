import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import string
from enum import Enum as PyEnum
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Status(PyEnum):
    searching = "searching"
    matched = "matched"

class Gender(PyEnum):
    male = "Laki-laki"
    female = "Perempuan"
    other = "Lainnya"

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    nama = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    chats = relationship('Chat', back_populates='user1')

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)  # ID chat
    user1_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # User pertama
    user2_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # User kedua
    chat_message = Column(Text, nullable=True)  # Pesan percakapan
    
    user1 = relationship('User', foreign_keys=[user1_id], back_populates='chats')
    user2 = relationship('User', foreign_keys=[user2_id])

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
SESSION = Session()
