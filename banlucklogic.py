import random

DECK = ['AceD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 
        'AceC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 
        'AceH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 
        'AceS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']


class PlayerHand:

    card_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10
    }

    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_face(self, card):
        if card.startswith('10'):
            return '10'
        elif card.startswith('Ace'):
            return 'Ace'
        else:
            return card[:-1]
        
    def hand_size(self):
        return len(self.hand)
    
    def get_value(self):
        total = 0
        ace_count = 0
        hand_size = self.hand_size()

        for card in self.hand:
            face = self.get_face(card)
            if face == 'Ace':
                ace_count += 1
            else:
                total += self.card_values[face]

        # Ace rule based on hand size
        ace_values = [11, 10] if hand_size <= 3 else [10, 1]

        for _ in range(ace_count):
            for ace_value in ace_values:
                if total + ace_value <= 21:
                    total += ace_value
                    break
            else:
                total += min(ace_values)  # fallback

        return total

    def __str__(self):
        return f"Hand: {self.hand} | Value: {self.get_value()}"

used_deck = DECK.copy()
random.shuffle(used_deck)

player1 = PlayerHand()
player2 = PlayerHand()

for _ in range(2):
    player1.add_card(used_deck.pop())
    player2.add_card(used_deck.pop())

print(player1)
print(player2)

# For player 1
print("Do you want to draw for player 1?")
user_input = input("Y/N ")

while(user_input.lower() != 'n'):
    player1.add_card(used_deck.pop())
    print(player1)
    print("Do you want to draw?")
    user_input = input("Y/N ")
    
print("Do you want to draw for player 2?")
user_input = input("Y/N ")

while(user_input.lower() != 'n'):
    player2.add_card(used_deck.pop())
    print(player2)
    print("Do you want to draw?")
    user_input = input("Y/N ")

if player1.get_value() > player2.get_value():
    print("Player 1 wins!")
else:
    print("Player 2 wins!")

        

