class TelegramGateway:
    def __init__(self, bot): self.bot=bot
    async def send_text(self, chat_id, text, **kwargs): return await self.bot.send_message(chat_id, text, **kwargs)
    async def send_captcha(self, chat_id, image, caption, **kwargs):
        from aiogram.types import BufferedInputFile
        return await self.bot.send_photo(chat_id, BufferedInputFile(image, filename="captcha.png"), caption=caption, **kwargs)
    async def delete_message(self, chat_id, message_id): return await self.bot.delete_message(chat_id, message_id)
