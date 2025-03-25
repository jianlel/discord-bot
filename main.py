import os
import logging

from typing import Final
from dotenv import load_dotenv
from pathlib import Path
from discord import Intents, Client, Message

from bot.message_handler import MessageHandler

# Load token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set log level (INFO, DEBUG, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
        logging.FileHandler('bot_logs.log')  # Output logs to a file
    ]
)


# Bot setup, activate intents
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

messageHandler = MessageHandler(client)

# Handling startup for bot
@client.event
async def on_ready() -> None:
    logging.info(f"{client.user} is now running!")

# Handling incoming messages
@client.event
async def on_message(message):
    await messageHandler.handle_message(message)

# Main entry point
def main():
    logging.info("Bot is starting...")
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()