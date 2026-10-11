import asyncio, logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from .config import Settings
from .domain import RegistrationService
from .telegram_gateway import TelegramGateway

def create_dispatcher(settings: Settings, service=None):
    router=Router(); service=service or RegistrationService(settings.captcha_ttl_seconds, settings.captcha_max_attempts)
    async def admin(m):
        if not m.from_user:
            return False
        if m.from_user.id in settings.admin_ids:
            return True
        try:
            member = await m.bot.get_chat_member(m.chat.id, m.from_user.id)
            return member.status in {"administrator", "creator"}
        except Exception:
            return False
    @router.message(Command("shift"))
    async def shift(m: Message):
        if await admin(m): service.open(m.chat.id); await m.answer("Регистрация на смену открыта. Напишите + для заявки.")
    @router.message(Command("close"))
    async def close(m: Message):
        if await admin(m): service.close(m.chat.id); await m.answer("Регистрация закрыта.")
    @router.message(Command("queue"))
    async def queue(m: Message):
        if await admin(m): await m.answer("Очередь: " + (", ".join(map(str, service.queue(m.chat.id))) or "пусто"))
    @router.message(Command("clear"))
    async def clear(m: Message):
        if await admin(m): service.clear(m.chat.id); await m.answer("Очередь очищена.")
    @router.message(Command("start"))
    async def start(m: Message):
        if not m.from_user or not m.text:
            return
        parts = m.text.split(maxsplit=1)
        if len(parts) != 2 or not parts[1].startswith("challenge_"):
            await m.answer("Откройте проверку по кнопке из группы.")
            return
        try:
            _, chat_id, user_id, challenge_id = parts[1].split("_", 3)
            chat_id, user_id, challenge_id = int(chat_id), int(user_id), int(challenge_id)
        except ValueError:
            return
        if user_id != m.from_user.id or (chat_id, user_id) not in service.pending:
            await m.answer("Эта заявка устарела или уже подтверждена.")
            return
        await m.answer("Проверка через мини-приложение отключена.")
    @router.message(F.text)
    async def text(m: Message):
        # Typical shift announcements are ordinary admin messages, not commands.
        announcement_markers = ("смета персонала", "заезд организаторов", "основной запуск", "кол-во гостей")
        if m.from_user and await admin(m) and any(marker in (m.text or "").lower() for marker in announcement_markers):
            service.open(m.chat.id)
            await m.answer("Регистрация открыта. Для заявки отправьте +")
            return
        value=(m.text or "").strip().replace("＋", "+").lower()
        if value in {"+", "+1"} and m.from_user:
            await m.answer("Проверка отключена, заявки не принимаются.")
        elif m.from_user and ((m.reply_to_message is not None) or (m.chat.id, m.from_user.id) in service.pending):
            now=__import__('datetime').datetime.now(__import__('datetime').timezone.utc)
            pending = service.pending.get((m.chat.id, m.from_user.id))
            captcha_message_id = m.reply_to_message.message_id if m.reply_to_message else pending.message_id
            accepted = service.answer(m.chat.id, m.from_user.id, captcha_message_id, m.text or "", now)
            try:
                await m.delete()
            except Exception:
                pass
            try:
                await m.bot.delete_message(m.chat.id, captcha_message_id)
                if not accepted and pending:
                    service.pending.pop((m.chat.id, m.from_user.id), None)
                    await m.bot.delete_message(m.chat.id, pending.source_message_id)
            except Exception:
                logging.exception("Could not clean up CAPTCHA messages")
    dp=Dispatcher(); dp.include_router(router); return dp

async def main():
    settings=Settings(); logging.basicConfig(level=settings.log_level); bot=Bot(settings.bot_token); await create_dispatcher(settings).start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
