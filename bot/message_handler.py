import logging

from bot.bot_responses import get_response

class MessageHandler():
    def __init__(self, bot):
        self.bot = bot

    async def handle_message(self, message):
        # If bot wrote the message, ignore it
        if message.author == self.bot.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        logging.info(f'[{channel}] {username}: "{user_message}"')
        await self.send_message(message, user_message)

    async def send_message(self, message, user_message):
        if not user_message:
            logging.warning("Message was empty (likely due to missing intents).")
            return

        # Send to user only, indicate private through '?'
        if user_message[0] == '?':
            user_message = user_message[1:]
            is_private = True
        else:
            is_private = False

        try:
            response = get_response(user_message)
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        except Exception as e:
            logging.error(f"Error sending message: {e}")
