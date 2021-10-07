# -*- coding: utf-8 _*_
# @Time : 4/10/2021 11:36 pm
# @Author: ZHA Mengyue
# @FileName: utils.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333

import os
import numpy as np
import pandas as pd


def MC(reward_list, keys_by_players, N_s, N_sa, Q_sa):
    for i in range(len(reward_list)):
        if reward_list[i] is not None:
            # Update counters
            for key in keys_by_players[i]:
                N_s[key[:-1]] += 1
                N_sa[key] += 1

                # Update Q-value function
                alpha = 1.0 / N_sa[key]
                Q_sa[key] += alpha * (reward_list[i] - Q_sa[key])


def QL(reward_list, keys_by_players, N_s, N_sa, Q_sa):
    for i in range(len(reward_list)):
        if reward_list[i] is not None:
            for j, key in enumerate(keys_by_players[i]):
                N_s[key[:-1]] += 1
                N_sa[key] += 1

                # Update Q-value function
                alpha = 1.0 / N_sa[key]
                old = Q_sa[key]
                if j < len(keys_by_players[i]) - 1:
                    """
                    hit = keys_by_players[i, j+1][:2] + (1, )
                    stick = keys_by_players[i, j+1][:2] + (0, )
                    """
                    keys_by_current_player = keys_by_players[i]
                    # print(keys_by_current_player)
                    next_state = keys_by_current_player[j+1][:-1]
                    hit = (next_state[0], next_state[1], 0)
                    stick = (next_state[0], next_state[1], 1)
                    """
                    print(f'This is hit in QL:{hit}')
                    print(f'This is stick in QL:{stick}')
                    """
                    max_value = max(Q_sa[hit], Q_sa[stick])
                    new = 0.8 * max_value

                else:
                    new = 0
                Q_sa[key] = (1-alpha) * old + alpha * (reward_list[i] + new)


def TD(reward_list, keys_by_players, N_s, N_sa, Q_sa):
    for i in range(len(reward_list)):
        if reward_list[i] is not None:
            for j, key in enumerate(keys_by_players[i]):
                N_s[key[:-1]] += 1
                N_sa[key] += 1

                # Update Q-value function
                alpha = 1.0 / N_sa[key]
                old = Q_sa[key]
                if j < len(keys_by_players[i]) - 1:
                    keys_by_current_player = keys_by_players[i]
                    new = 0.8 * Q_sa[keys_by_current_player[j+1]]
                else:
                    new = 0
                Q_sa[key] = (1-alpha) * old + alpha * (reward_list[i] + new)


def save_value(Q_sa, name, instance_dir):
    # Q_sa: (player, dealer, action) ——> value
    value_list = list(Q_sa.items())
    file_name = name + '_value.csv'
    file_dir = os.path.join(instance_dir, file_name)
    record_list = []
    # print(value_list)

    for i in range(len(value_list)):
        # each record of the form [player, dealer, action, value]
        record_list.append([value_list[i][0][0],
                            value_list[i][0][1],
                            value_list[i][0][2],
                            value_list[i][1]])
    value_frame = pd.DataFrame(record_list, columns=['player', 'dealer', 'action', 'value'])
    value_frame.to_csv(file_dir, index=False)
    return None


def save_win_records(win_records, name, npy_dir):
    win_records_npy = np.array(win_records)
    file_name = name + '_win_records.npy'
    file_dir = os.path.join(npy_dir, file_name)
    np.save(file_dir, win_records_npy)


