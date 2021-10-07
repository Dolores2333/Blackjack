# -*- coding: utf-8 _*_
# @Time : 4/10/2021 1:46 pm
# @Author: ZHA Mengyue
# @FileName: main.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333

import os
import json
import random
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
from collections import defaultdict

from deck import Deck
from game import Game
from utils import MC, QL, TD, save_value, save_win_records

from plot import plotting

# path maintenance
HOME = os.getcwd()
print(f'Current working directory: {HOME}')
STORAGE = os.path.join(HOME, 'storage')
print(f'Outcomes will be put into {STORAGE}')
if os.path.isdir(STORAGE):
    print(f'The folder for storage has been created!')
else:
    os.mkdir(STORAGE)
    print('storage initialized!')


# Random Policy Strategy
def random_policy():
    return 0 if random.random() < 0.5 else 1


# Epsilon Greedy Policy
# with prob epsilon choose randomly
# with prob i-epsilon choose the best
def epsilon_greedy_policy(epsilon, Q_sa, player, dealer):
    # exploration
    if random.random() < epsilon:
        return random_policy()
    # exploitation
    else:
        return best_policy(epsilon, Q_sa, player, dealer)


# The best policy based on the q function
def best_policy(epsilon, Q_sa, player, dealer):
    # Q_sa with key of (player_points, dealer_points, action)
    q_value_hit = Q_sa[(player, dealer, 0)]
    q_value_stick = Q_sa[(player, dealer, 1)]

    if q_value_hit > q_value_stick:
        return 0
    elif q_value_stick > q_value_hit:
        return 1
    else:
        return random_policy()


def blackjack(config, args, instance_dir):
    # Define the global variables
    # global epochs, update, name, policy, n_zeros, M, N
    epochs = config['epochs']
    update = config['update']
    name = config['name']
    policy = config['policy']
    n_zeros = config['n_zeros']
    session = config['session']
    m = args['m']
    n = args['n']
    # for test in command: print(f'epochs is {epochs}, name is {name} and M = {M}, N = {N}')

    # Define the counters
    Q_sa = defaultdict(float)
    N_s = defaultdict(int)
    N_sa = defaultdict(int)
    wins = np.zeros(n-1, dtype=int)
    win_records = [[] for _ in range(n-1)]

    npy_dir = os.path.join(instance_dir, 'npy')
    pic_dir = os.path.join(instance_dir, 'pic')

    # Training begins!
    for k in tqdm(range(epochs)):
        """
        print(f'--------Epoch {k}--------')
        """
        # Reinitialize an epoch
        # A game with M decks and N-1 players plus 1 dealer
        game = Game(m, n)
        action_list = [None for _ in range(n-1)]
        reward_list = [None for _ in range(n-1)]
        # key in keys_by_players[i] is (players[i], dealer, action_list[i])
        keys_by_players = [[] for _ in range(n-1)]
        player_points_list = game.player_points_list

        # Scan for the instance win and loss
        for j in range(n-1):
            if player_points_list[j] > 21:
                action_list[j] = 1
                reward_list[j] = -1
            if player_points_list[j] == 21:
                # dealer_real counts the real points of the dealer (two cards)
                dealer_real = game.player_list[n-1].call_points()
                if dealer_real == 21:
                    action_list[j] = 1
                    reward_list[j] = 0
                else:
                    action_list[j] = 1
                    reward_list[j] = 1

        # print(f'keys_by_players:{keys_by_players}')
        # print(f'player_points_list:{player_points_list}')
        # t indicate the num of turns

        t = 0
        while not game.terminal:
            t += 1
            # States
            # players: points of every players [list]
            # dealer: points of the dealer [int]
            players = player_points_list[:-1]
            dealer = player_points_list[-1]

            # Make sure that there are sufficient cards to pick up
            if len(game.deck.decks) < int(m * 52 * 0.6):
                game.deck = Deck(m)
                game.deck.shuffle()

            # For each player, choose the action
            for i in range(n-1):
                action = action_list[i]
                reward = reward_list[i]
                # Skip losers
                if action == 1 or reward == -1:
                    action = 1
                    action_list[i] = 1
                    continue
                # for action  == 0 or None we need to take the action
                if action is not 1:
                    # print(type(players))
                    # print(N_s)
                    epsilon = n_zeros / float(n_zeros + N_s[(players[i], dealer)])
                    # print(f'policy: {policy}')
                    # print(f'epsilon:{epsilon}')
                    # action_list[i] = exec(f'{policy}')(epsilon, Q_sa, players[i], dealer)
                    # action_list[i] = exec(f'{policy}({epsilon}, {Q_sa}, {players[i]}, {dealer})')
                    if policy == 'epsilon_greedy_policy':
                        action_list[i] = epsilon_greedy_policy(epsilon, Q_sa, players[i], dealer)
                    if policy == 'best_policy':
                        action_list[i] = best_policy(epsilon, Q_sa, players[i], dealer)
                    # then break to see the next action made by the same player rather than the next one
                    break

            # Record the keys observed
            # special consideration for the first player
            if (players[0], dealer, action_list[0]) not in keys_by_players[0] and players[0] <= 21:
                keys_by_players[0].append((players[0], dealer, action_list[0]))
            # consider player 2 to player N-1
            for i in range(1, n-1):
                if (players[i], dealer, action_list[i]) not in keys_by_players[i] and action_list[i] is not None:
                    keys_by_players[i].append((players[i], dealer, action_list[i]))

            # print the points for players
            """
            print(f'dealer in turn {t}:{dealer}')
            print(f'action_list in turn {t}:{action_list}')
            print(f'players in turn {t}:{players} before action')
            print(f'reward_list in turn {t}:{reward_list} before action')
            print(f'terminal = {game.terminal}')
            """

            # Take a step to update the state and the reward
            player_points_list, reward_list = game.step(player_points_list=player_points_list,
                                                        action_list=action_list,
                                                        reward_list=reward_list)
            # print the action being picked and the corresponding reward
            """
            players = player_points_list[:-1]
            dealer = player_points_list[-1]

            print(f'dealer after the action:{dealer}')
            print(f'players in turn {t}: {players} after action')
            print(f'reward_list in turn {t}:{reward_list} after action')
            print(f'terminal = {game.terminal}')
            print('\n')
            """

        # Now we finished a sample of trajectories
        # choose an update function to update the q-value function for prediction
        if update == 'MC':
            MC(reward_list, keys_by_players, N_s, N_sa, Q_sa)
        if update == 'QL':
            QL(reward_list, keys_by_players, N_s, N_sa, Q_sa)
        if update == 'TD':
            TD(reward_list, keys_by_players, N_s, N_sa, Q_sa)

        # After sufficient training we start to count the wins for each players
        if k > int(epochs * 0.8):
            for j in range(n-1):
                if reward_list[j] == 1:
                    wins[j] += 1

        # Record the rewards by players as win_records
        for i in range(n-1):
            win_records[i].append(reward_list[i])

        # Print the final outcome of the current epoch
        """
        players = player_points_list[:-1]
        dealer = player_points_list[-1]
        print('The final info of this game')
        print(f'action_list:{action_list}')
        print(f'reward_list:{reward_list}')
        print(f'players:{players}')
        print(f'dealer:{dealer}')
        print('--------End--------\n\n')
        """

    # Print the wins percentage averaged over players after sufficient training
    print(name + ' ' + 'Wins Averaged: %.4f%%' % ((float(np.mean(wins)) / (epochs - int(epochs * 0.8))) * 100))
    # save q value function
    value_save_flag = True
    if value_save_flag:
        save_value(Q_sa, name, instance_dir)
        save_win_records(win_records, name, npy_dir)
    # Visualization
    visual_it = True
    if visual_it:
        plotting(name, instance_dir, pic_dir, npy_dir, win_records, session)
    return None


def build_parser():
    parser = ArgumentParser(description='m desks and n-1 players with 1 dealer')
    parser.add_argument('--m', type=int)
    parser.add_argument('--n', type=int)
    return parser

"""
def main():
    parser = build_parser()
    args = vars(parser.parse_args())
    m = args['M']
    n = args['N']
    INSTANCE = os.path.join(STORAGE, f'm{m}n{n}')
    PIC = os.path.join(INSTANCE, 'pic')
    NPY = os.path.join(INSTANCE, 'npy')
    if not os.path.isdir(INSTANCE):
        os.mkdir(INSTANCE)
        os.mkdir(PIC)
        os.mkdir(NPY)
    # config_dir = os.path.join(HOME, 'config.json')
    # instance_config_dir = os.path.join(INSTANCE, 'config.json')
    # copy(config_dir, instance_config_dir)
    with open('config.json') as f:
        config = json.load(f)

    blackjack(config, args, INSTANCE)
"""

def build_instances_parser():
    parser = ArgumentParser(description='Build instances for M desks and N-1 players with 1 dealer with given config')
    parser.add_argument('--m', nargs='+')
    parser.add_argument('--n', nargs='+')
    return parser


def main():
    parser = build_instances_parser()
    args = vars(parser.parse_args())
    m_list = args['m']
    n_list = args['n']
    update_list = ['MC', 'QL', 'TD']
    policy_list = ['best_policy', 'epsilon_greedy_policy']
    config_dir = os.path.join(HOME, 'config.json')
    for m in m_list:
        m = int(m)
        for n in n_list:
            n = int(n)
            for update in update_list:
                for policy in policy_list:
                    name_suffix = policy.split('_')[0]
                    name = update + '_' + name_suffix
                    INSTANCE = os.path.join(STORAGE, f'm{m}n{n}')
                    PIC = os.path.join(INSTANCE, 'pic')
                    NPY = os.path.join(INSTANCE, 'npy')
                    experiment_dir = os.path.join(INSTANCE, name)
                    if not os.path.isdir(INSTANCE):
                        os.mkdir(INSTANCE)
                        os.mkdir(PIC)
                        os.mkdir(NPY)
                    if not os.path.isdir(experiment_dir):
                        os.mkdir(experiment_dir)
                        instance_config_dir = os.path.join(experiment_dir, 'config.json')
                        with open(config_dir) as f:
                            para_dict = json.load(f)
                        para_dict['update'] = update
                        para_dict['name'] = name
                        para_dict['policy'] = policy
                        print(f'm={m} and n={n}')
                        print(para_dict)
                        """
                        if not os.path.isfile(instance_config_dir):
                            with open(instance_config_dir, 'w') as f:
                                json.dump(para_dict, f)
                        """
                        with open(instance_config_dir, 'w') as f:
                            json.dump(para_dict, f)
                        with open(instance_config_dir) as f:
                            config = json.load(f)
                        args = {'m': m,
                                'n': n}
                        blackjack(config, args, INSTANCE)


if __name__ == '__main__':
    main()
