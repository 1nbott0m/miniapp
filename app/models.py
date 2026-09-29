from sqlalchemy import String, Integer, Boolean, DateTime, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase): pass
class ChatState(Base):
    __tablename__='chat_states'; chat_id: Mapped[int]=mapped_column(primary_key=True); is_open: Mapped[bool]=mapped_column(Boolean, default=False)
class QueueEntry(Base):
    __tablename__='queue_entries'; id: Mapped[int]=mapped_column(primary_key=True); chat_id: Mapped[int]; user_id: Mapped[int]; created_at: Mapped[datetime]; __table_args__=(UniqueConstraint('chat_id','user_id'),)
