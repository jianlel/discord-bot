from discord.ext import commands
import database.database as db

import logging
import random
import datetime

WORDS = []
with open("words.txt", 'r') as file:
    WORDS = [line.strip() for line in file.readlines()]

def get_daily_word():
    today = datetime.date.today()
    random.seed(today.toordinal())
    return random.choice(WORDS)

def check_guess(guess, target):
    result = ["⬜"] * len(guess)  # Initialize result as all gray
    target_list = list(target)  # Convert to list for easy modification
    used_positions = set()

    # Check for exact matches (Green) first, and mark them as used
    for i in range(len(guess)):
        if guess[i] == target[i]:
            result[i] = "🟩"  # Correct position
            used_positions.add(i)

    # Check for misplaced letters (Yellow) in the second loop
    for i in range(len(guess)):
        if result[i] == "⬜" and guess[i] in target_list:
            # Check if the letter has not been used yet and exists in the target
            target_index = target_list.index(guess[i])
            if target_index not in used_positions:
                result[i] = "🟨"
                used_positions.add(target_index)

    return "".join(result)

# Wordle class to handle game state
class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    # Command to start wordle game
    @commands.command()
    async def wordle(self, ctx):
        # Check for active game
        if ctx.author.id in self.players and not self.players[ctx.author.id]["game_over"]:
            await ctx.send("You already have an active game. Finish it before starting a new one.")
            return
        
        # Start the wordle game
        self.players[ctx.author.id] = {
            "attempts": 6,
            "target_word": random.choice(WORDS),
            "game_over": False
        }
        await ctx.send("Welcome to Wordle! Guess a 5-letter word.")
        logging.info(f'{ctx.author} started a Wordle game')
        logging.info(f'Word is {self.players[ctx.author.id]["target_word"]}')

    # Command to start Daily wordle game
    @commands.command()
    async def daily(self, ctx):
        if await db.has_played_today(ctx.author.id):
            await ctx.send("You have already completed today's Daily Challenge!")
            return
        
        # Check for active game
        if ctx.author.id in self.players and not self.players[ctx.author.id]["game_over"]:
            await ctx.send("You already have an active game. Finish it before starting a new one.")
            return

        # Start the daily challenge
        self.players[ctx.author.id] = {
            "attempts": 6,
            "target_word": get_daily_word(),
            "game_over": False,
            "daily": True
        }
        await ctx.send("Welcome to the Daily Wordle Challenge! Guess today's 5-letter word.")
        logging.info(f'{ctx.author} started a Daily Wordle challenge')

    # Command to make a guess
    @commands.command()
    async def guess(self, ctx, guess):
        # Make a guess in the game
        # Ensure that player started the game 
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You need to start a Wordle game with '!start_wordle' first")
            return
        
        player_data = self.players[ctx.author.id]
        attempts = player_data["attempts"]
        target_word = player_data["target_word"]

        # Validation
        guess = guess.lower()
        if len(guess) != 5 or not guess.isalpha():
            await ctx.send("Invalid guess. Please enter a 5-letter word")
            return
        
        # Check guess
        feedback = check_guess(guess, target_word)
        await ctx.send(feedback)

        # If guess is correct, end the game!
        if guess == target_word:
            if player_data.get("daily"):
                await db.mark_daily_completed(ctx.author.id)
                await db.increment_daily_streak(ctx.author.id)
                daily_streak = await db.get_daily_streak(ctx.author.id)
                await ctx.send(f"You won today's Daily Challenge! The word was {target_word}. Current Daily streak = {daily_streak}")
                player_data["game_over"] = True
                logging.info(f'{ctx.author} won the Daily Wordle game! The word was {target_word}. Current daily streak: {daily_streak}')
                return
            else:
                await db.win(ctx.author.id)
                #db.increment_streak(ctx.author.id)
                streak = await db.get_streak(ctx.author.id)
                await ctx.send(f"You won! Current streak = {streak}")
                player_data["game_over"] = True
                logging.info(f'{ctx.author} won the Wordle game! The word was {target_word}. Current streak: {streak}')
                return
        
        # If guess is incorrect, decrease attempts
        attempts -= 1
        self.players[ctx.author.id]["attempts"] = attempts
        if attempts == 0:
            if player_data.get("daily"):
                await ctx.send(f"Game over! The daily word was: {target_word}")
                await db.reset_daily_streak(ctx.author.id)
                player_data["game_over"] = True
                logging.info(f'{ctx.author} loss the Daily Wordle game! The word was {target_word}.')

            else:
                await ctx.send(f"Game over! The word was: {target_word}")
                await db.reset_streak(ctx.author.id)
                await db.lose(ctx.author.id)
                player_data["game_over"] = True
                logging.info(f'{ctx.author} loss the Wordle game! The word was {target_word}.')

        if attempts > 0:
            await ctx.send(f"You have {attempts} attempts left.")

    # Command to see how many attempts left
    @commands.command()
    async def attempts(self, ctx):
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You need to start a Wordle game with '!start_wordle' first")
            return
        
        attempts_left = self.players[ctx.author.id]["attempts"]
        await ctx.send(f"You have {attempts_left} attempts left.")

    # Command to see user streaks 
    @commands.command()
    async def streak(self, ctx):
        streak = await db.get_streak(ctx.author.id)
        daily_streak = await db.get_daily_streak(ctx.author.id)
        await ctx.send(f"Your game streak: {streak}, Your daily streak: {daily_streak}")
    
    # Command to see user stats
    @commands.command()
    async def stats(self, ctx):
        wins = await db.get_wins(ctx.author.id)
        losses = await db.get_losses(ctx.author.id)
        if wins != 0:
            win_percent = wins / (wins + losses) * 100
            await ctx.send(f"Wins: {wins}, Losses: {losses}, Percentage: {round(win_percent, 1)}%")
        else:
            await ctx.send(f"Wins: {wins}, Losses: {losses}")

async def setup(bot):
    await db.init_db()
    await bot.add_cog(Wordle(bot))