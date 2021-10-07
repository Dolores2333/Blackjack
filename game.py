# -*- coding: utf-8 _*_
# @Time : 4/10/2021 3:12 pm
# @Author: ZHA Mengyue
# @FileName: game.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333

from player import Player
from deck import Deck


def whether_terminal(action_list, reward_list, num_player):
    flag = True
    for i in range(num_player):
        if action_list[i] is None:
            flag = False
        if action_list[i] == 0 and (reward_list[i] != -1):
            flag = False
    return flag


class Game:
    def __init__(self, m, n):
        self.terminal = False
        self.num_player = n-1
        self.num_deck = m
        self.deck = Deck(self.num_deck)
        self.deck.shuffle()
        # self.player_list with i-th item to be the i-th player instance
        self.player_list = []
        # player_points with the i-th item to be the points for i-th player
        self.player_points_list = []
        # Create N-1 players with 2 cards and points calculated
        for i in range(self.num_player):
            name = f'player{i}'
            self.player = Player(name)
            self.player.hit(self.deck)
            self.player.hit(self.deck)
            self.player_points = self.player.call_points()
            self.player_list.append(self.player)
            self.player_points_list.append(self.player_points)

        # Create a dealer with 2 cards but only one card showed
        self.dealer = Player('dealer')
        self.dealer.hit(self.deck)
        self.dealer.hit(self.deck)
        self.dealer_points = self.dealer.dealer_first()
        # Now the player_list has N-1 players and one dealer instance
        self.player_list.append(self.dealer)
        self.player_points_list.append(self.dealer_points)

    def step(self, player_points_list, action_list, reward_list):
        """ Given the current state and action, Return the next state and reward
        :param player_points_list: current state
        :param action_list: current action
        :param reward_list: current reward
        :return: next state and reward
        """

        if not self.terminal:
            # The players' turn
            for i in range(self.num_player):
                if action_list[i] == 0:
                    self.player_list[i].hit(self.deck)
                    self.player_points_list[i] = self.player_list[i].call_points()
                    if self.player_points_list[i] > 21:
                        reward_list[i] = -1
                    break
                elif action_list[i] == 1:
                    if self.player_points_list[i] > 21:
                        reward_list[i] = -1

                    self.terminal = whether_terminal(action_list, reward_list, num_player=self.num_player)

                    # Next we calculate the poker chip once the game terminates
                    if self.terminal:
                        # First is the dealer's turn
                        # The dealer should show both two cards got in the initialization now
                        self.player_points_list[self.num_player] = self.player_list[self.num_player].call_points()
                        while player_points_list[self.num_player] < 17:
                            self.player_list[self.num_player].hit(self.deck)
                            self.player_points_list[self.num_player] = self.player_list[self.num_player].call_points()

                        # Find the winner
                        # Note that now all dealer's cards are shown
                        dealer_points = self.player_points_list[self.num_player]
                        if dealer_points > 21:
                            for j in range(self.num_player):
                                if self.player_points_list[j] <= 21:
                                    reward_list[j] = 1
                        else:
                            for j in range(self.num_player):
                                if player_points_list[j] < dealer_points:
                                    reward_list[j] = -1
                                elif player_points_list[j] == dealer_points:
                                    reward_list[j] = 0
                                elif player_points_list[j] > dealer_points:
                                    reward_list[j] = 1
                                # Fixation: for those player > 21 the reward should be -1
                                if player_points_list[j] > 21:
                                    reward_list[j] = -1

        return self.player_points_list, reward_list


"""
game = Game(2, 3)
print(game.player_list)
print(game.player_points_list)
"""
