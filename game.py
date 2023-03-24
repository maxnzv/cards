#!/usr/bin/env python3
import random

# Define the deck of cards
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
deck = [(value, suit) for value in values for suit in suits]
random.shuffle(deck)

# Deal 6 cards to each player
player1_hand = [deck.pop() for _ in range(6)]
player2_hand = [deck.pop() for _ in range(6)]
trump = deck.pop ()
trump_suit = trump[1]

# Initialize the table
table = []

def draw_card(player_hand):
    ''' draws a card from deck if it's not empty or gives the player a last card which is trump '''
    if len (player_hand) < 6:
        if len(deck) > 0:
            player_hand.append(deck.pop())
        elif len (trump) == 1:
            player_hand.append (trump.pop ())

def pick_card(player_hand, can_take=True):
    ''' asks player to pick a card from his hand to start a round or beat the card on the table '''
    while True:
        try:
            query = "Pick a card to play (enter index number from 1 to {})"
            if can_take:
                query += " or type 'take' to take the table"
            query += ":"
            choice = input(query.format(len(player_hand)))
            if choice == 'take' and can_take:
                return None
            card_index = int(choice)
            if card_index < 1 or card_index > len(player_hand):
                raise ValueError
            break
        except ValueError:
            print("Invalid input.")
            print (query.format(len(player_hand)))
    return player_hand.pop(card_index - 1)

def header(player_hand):
    ''' prints a header before a player's turn '''
    print("Your hand:")
    for i, card in enumerate(player_hand, 1):
        print(f"{i}. {card[0]} of {card[1]}")
    print(f"Table: {table}")

def play_turn(player_hand, opponent_hand, opponent_num):
    # Print player's hand and ask for card to play
    header(player_hand)
    played_card = pick_card(player_hand, False)

    # Play a card
    table.append(played_card)

    # Print opponent's hand and ask for card to play
    print("Try to beat the table, player {}".format(opponent_num))
    header(opponent_hand)
    card = pick_card(opponent_hand)

    # The opponent gave up
    if card is None:
        opponent_hand.extend(table)
        table.clear()
        draw_card(player_hand)
        print("The other player cannot beat your card.")
        return True

    # Determine if the other player can beat the played card
    can_beat = False
    if card[1] == trump_suit and played_card[1] != trump_suit:
        can_beat = True
    elif card[1] == played_card[1] and values.index(card[0]) > values.index(played_card[0]):
        can_beat = True

    # Update the table and hands based on whether the opponent can beat the played card
    if can_beat:
        print("The other player beats your card.")
        table.clear()
        draw_card(player_hand)
        draw_card(opponent_hand)
        return False
    else:
        opponent_hand.extend(table)
        opponent_hand.append(card)
        table.clear()
        draw_card(player_hand)
        print("The other player cannot beat your card.")
        return True

# Start the game
draw_card(player1_hand)
draw_card(player2_hand)
player_turn = 1
while len(player1_hand) > 0 and len(player2_hand) > 0:
    print ("Player {} turn".format (player_turn))
    print ("The trump suit is {} and trump card is {}".format (trump_suit, trump))
    if player_turn == 1:
        if play_turn(player1_hand, player2_hand, 2):
            player_turn = 1
        else:
            player_turn = 2
    else:
        if play_turn(player2_hand, player1_hand, 1):
            player_turn = 2
        else:
            player_turn = 1

if len(player1_hand) == 0:
    print("Player 1 wins!")
elif len(player2_hand) == 0:
    print("Player 2 wins!")
else:
    print("No more cards in the deck. It's a tie!")
