import random

WORDS = []
with open("words.txt", 'r') as file:
    WORDS = [line.strip() for line in file.readlines()]

TARGET_WORD = random.choice(WORDS)

# Function to check a guess
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

# Game loop
attempts = 6
print("🎯 Welcome to Wordle! Guess a 5-letter word.")

while attempts > 0:
    guess = input(f"\nAttempts left ({attempts}). Enter your guess: ").lower()

    if len(guess) != 5 or not guess.isalpha():
        print("❌ Invalid guess. Please enter a 5-letter word.")
        continue

    feedback = check_guess(guess, TARGET_WORD)
    print(f"🔎 {feedback}")

    if guess == TARGET_WORD:
        print("🎉 Congratulations! You guessed the word!")
        break

    attempts -= 1

if attempts == 0:
    print(f"💀 Game Over! The word was: {TARGET_WORD}")
