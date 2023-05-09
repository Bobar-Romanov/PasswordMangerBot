import asyncio
import telebot


class Service:
    def __init__(self, bot):
        self.bot = bot

    async def delete_messages(self, *args, delay, loop):
        await asyncio.sleep(delay)
        for message in args:
            self.bot.delete_message(message.chat.id, message.message_id)
        loop.stop()
