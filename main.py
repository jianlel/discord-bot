import os
import logging

from typing import Final
from dotenv import load_dotenv
from pathlib import Path
from discord import Intents, Client
from discord.ext import commands

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
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

message_handler = MessageHandler(bot)

# Handling startup for bot
@bot.event
async def on_ready() -> None:
    logging.info(f"{bot.user} is now running!")
    try:
        await bot.load_extension('cogs.wordle')
        await bot.load_extension('cogs.helper')
    except Exception as e:
        logging.error(f"Failed to load cog: {e}")
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return 
    
    await message_handler.handle_message(message)

# Main entry point
def main():
    logging.info("Bot is starting...")
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()