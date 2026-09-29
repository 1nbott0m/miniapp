from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from .models import Base
from .models import ChatState, QueueEntry
class Database:
    def __init__(self, url): self.engine=create_async_engine(url); self.sessions=async_sessionmaker(self.engine, expire_on_commit=False)
    async def create(self):
        async with self.engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    async def set_open(self, chat_id, value):
        async with self.sessions() as s:
            row = await s.get(ChatState, chat_id) or ChatState(chat_id=chat_id)
            row.is_open = value; s.add(row); await s.commit()
    async def is_open(self, chat_id):
        async with self.sessions() as s:
            row=await s.get(ChatState, chat_id); return bool(row and row.is_open)
    async def add_queue(self, chat_id, user_id, created_at):
        async with self.sessions() as s:
            existing=(await s.execute(select(QueueEntry).where(QueueEntry.chat_id==chat_id, QueueEntry.user_id==user_id))).scalar_one_or_none()
            if existing: return False
            s.add(QueueEntry(chat_id=chat_id,user_id=user_id,created_at=created_at)); await s.commit(); return True
    async def queue(self, chat_id):
        async with self.sessions() as s:
            rows=(await s.execute(select(QueueEntry).where(QueueEntry.chat_id==chat_id).order_by(QueueEntry.id))).scalars()
            return [r.user_id for r in rows]
