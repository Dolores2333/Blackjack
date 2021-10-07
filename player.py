# -*- coding: utf-8 _*_
# @Time : 4/10/2021 2:12 pm
# @Author: ZHA Mengyue
# @FileName: player.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333


class Player(object):
    # Player has a name and a hand of cards
    # The points will be counted into the state
    def __init__(self, player_name):
        self.name = player_name
        self.hand = []
        self.points = 0

    def hit(self, deck):
        # Hit action
        self.hand.append(deck.pop())

    def call_points(self):
        # calculate the points got by the player
        total_points = 0
        num_aces = 0
        for card in self.hand:
            # here the points is str
            point = card.split()[0]
            if point.isdigit():
                total_points += int(point)
            elif point == 'Ace':
                total_points += 11
                num_aces += 1
            else:
                total_points += 10

        while num_aces > 0 and total_points > 21:
            num_aces -= 1
            total_points -= 10
        return total_points

    def dealer_first(self):
        # Only return thr dealer's first card  points as the state
        total_points = 0
        num_aces = 0
        card = self.hand[0]
        point = card.split()[0]
        if point.isdigit():
            total_points += int(point)
        elif point == 'Ace':
            total_points += 11
            num_aces += 1
        else:
            total_points += 10

        return total_points


"""
deck = Deck(1)
player = Player('Mengyue')
player.hit(deck)
print(player.hand)
player.points = player.call_points()
print(player.points)
"""
