import os

from typing import Final
from dotenv import load_dotenv
from pathlib import Path
from discord import Intents, Client, Message
from responses import get_response

# Load token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup, activate intents
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Mesasge was empty because intents were not enabled, probably)")
        return
    
    # Send to user only, indicate private through '?'
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try: 
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling startup for bot
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    # If bot is the one who wrote the message
    if message.author == client.user:
        return 

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main entry point
def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()