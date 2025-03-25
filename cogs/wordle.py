from discord.ext import commands
import random

WORDS = []
with open("words.txt", 'r') as file:
    WORDS = [line.strip() for line in file.readlines()]

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
    async def start(self, ctx):
        # Start the wordle game
        self.players[ctx.author.id] = {
            "attempts": 6,
            "target_word": random.choice(WORDS),
            "game_over": False
        }
        await ctx.send("Welcome to Wordle! Guess a 5-letter word.")

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
        target_word = player_data["word"]
        game_over = player_data["game_over"]

        # Validation
        guess = guess.lower()
        if len(guess) != 5 or not guess.isalpha():
            await ctx.send("Invalid guess. Please enter a 5-letter word")
            return
        
        # Check guess
        feedback = check_guess(guess, target_word)
        await ctx.send(feedback)

        # If guess is correct, end the game
        if guess == target_word:
            await ctx.send("You won!")
            game_over = True
            self.players[ctx.author.id][game_over] = game_over
            return
        
        # If guess is incorrect, decrease attempts
        attempts -= 1
        self.players[ctx.author.id][attempts] = attempts
        if attempts == 0:
            await ctx.send(f"Game over! The word was: {target_word}")
            game_over = True
            self.players[ctx.author.id][game_over] = game_over

    # Command to see how many attempts left
    @commands.command()
    async def attempts(self, ctx):
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You need to start a Wordle game with '!start_wordle' first")
            return
        
        attempts_left = self.players[ctx.author.id]["attempts"]
        await ctx.send(f"You have {attempts_left} attempts left.")


def setup(bot):
    bot.add_cog(Wordle(bot))