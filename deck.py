# -*- coding: utf-8 _*_
# @Time : 4/10/2021 2:13 pm
# @Author: ZHA Mengyue
# @FileName: deck.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333

import random
import numpy as np


class Deck(object):
    def __init__(self, num_deck=1):
        # num_decks = 0 means infinite number of decks and the pick up is with replacement
        self.contents = ['2 of Diamonds', '2 of Hearts', '2 of Clubs', '2 of Spades', '3 of Diamonds', '3 of Hearts',\
                         '3 of Clubs', '3 of Spades', '4 of Diamonds', '4 of Hearts', '4 of Clubs', '4 of Spades',\
                         '5 of Diamonds', '5 of Hearts', '5 of Clubs', '5 of Spades', '6 of Diamonds', '6 of Hearts',\
                         '6 of Clubs', '6 of Spades', '7 of Diamonds', '7 of Hearts', '7 of Clubs', '7 of Spades',\
                         '8 of Diamonds', '8 of Hearts', '8 of Clubs', '8 of Spades', '9 of Diamonds', '9 of Hearts',\
                         '9 of Clubs', '9 of Spades', '10 of Diamonds', '10 of Hearts', '10 of Clubs', '10 of Spades',\
                         'Jack of Diamonds', 'Jack of Hearts', 'Jack of Clubs', 'Jack of Spades', 'Queen of Diamonds',\
                         'Queen of Hearts', 'Queen of Clubs', 'Queen of Spades', 'King of Diamonds', 'King of Hearts',\
                         'King of Clubs', 'King of Spades', 'Ace of Diamonds', 'Ace of Hearts', 'Ace of Clubs',\
                         'Ace of Spades']
        if num_deck is not 0:
            self.decks = [self.contents for _ in range(num_deck)]
            self.decks = list(np.concatenate(self.decks, axis=0))
        else:
            self.decks = list(self.contents)
        self.num_deck = num_deck

    def shuffle(self):
        # shuffle the cards
        random.shuffle(self.decks)

    def pop(self):
        # pop the top card out and hand it to the player
        card = self.decks.pop(0)
        # for num_deck = 0, pick up with replacement
        if self.num_deck == 0:
            self.decks = list(self.contents)
            random.shuffle(self.decks)
        return card

"""
deck = Deck(0)
card = deck.pop()
print(f'card is {card}')
print(f'length of the deck is {len(deck.decks)}')
"""