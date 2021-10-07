# -*- coding: utf-8 _*_
# @Time : 6/10/2021 2:16 pm
# @Author: ZHA Mengyue
# @FileName: plot.py
# @Software: Blackjack
# @Blog: https://github.com/Dolores2333

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def plot_single_player(name, win_records, pic_dir, k, session, i):
    """

    :param win_record: win_records[i] stores the record for player i
    :param path: the given path to save the fig
    :param k: the index of the figure
    :param session: summary after a session finished
    :param i: visualizing the i-th player
    :return: None
    """
    win_list = []
    loss_list = []
    draw_list = []
    win_record = win_records[i]
    file_name = name + f'_player_{i+1}_performance_plot.png'
    file_dir = os.path.join(pic_dir, file_name)
    for j in range(int(len(win_record)/session)):
        win_list.append(win_record[j * session: (j + 1) * session].count(1))
        loss_list.append(win_record[j * session: (j + 1) * session].count(-1))
        draw_list.append(win_record[j * session: (j + 1) * session].count(0))
    plt.figure(k, figsize=(15, 5))
    plt.title(f'Performance by {i+1}-th player', size=14)
    plt.ylabel(f'Summary by session of {session} actions', size=14)
    plt.xlabel(f'Session')
    plt.plot([x for x in np.arange(len(win_list))], win_list, color='r', label='win')
    plt.plot([x for x in np.arange(len(loss_list))], loss_list, color='g', label='loss')
    plt.plot([x for x in np.arange(len(draw_list))], draw_list, color='b', label='draw')
    plt.legend(loc='best')
    plt.savefig(file_dir)


def plot_policy_comparison(name, k, i, npy_dir, pic_dir):
    """

    :param epsilon_record:
    :param best_record:
    :param k: index of the figure
    :param i: player
    :param path:
    :return:
    """
    method = name.split('_')[0]
    epsilon_name = method + '_epsilon_win_records.npy'
    best_name = method + '_best_win_records.npy'
    epsilon_dir = os.path.join(npy_dir, epsilon_name)
    best_dir = os.path.join(npy_dir, best_name)
    epsilon_records = list(np.load(epsilon_dir))
    best_records = list(np.load(best_dir))
    epsilon_record = list(epsilon_records[i])
    best_record = list(best_records[i])
    win = []
    loss = []
    draw = []
    win.append(epsilon_record.count(1))
    win.append(best_record.count(1))
    loss.append(epsilon_record.count(-1))
    loss.append(best_record.count(-1))
    draw.append(epsilon_record.count(0))
    draw.append(best_record.count(0))
    """
    print(win)
    print(loss)
    print(draw)
    """
    data = [win, loss, draw]
    color_idx = ['r', 'g', 'b']
    x_axis = ['epsilon greedy', 'best policy']
    fig = plt.figure(k, figsize=(5, 12))
    plt.ylabel('Counts for games', size=15)
    plt.xticks([0.05, 0.2], x_axis)
    p = [0, 0, 0]
    for j in range(3):
        p[j] = plt.bar([0, 0.15], data[i], width=.1, color=color_idx[j],
                       bottom = np.sum(data[:j], axis=0), alpha=.7)
    fig.legend((p[0], p[1], p[2]), ('win', 'loss', 'draw'))
    file_name = method + f'_policy_comparison_for_player_{i}.png'
    file_dir = os.path.join(pic_dir, file_name)
    plt.savefig(file_dir)


def plot_state_action_value(name, instance_dir, pic_dir):
    # We consider point from 4 to 21, totally 18 states
    v = np.zeros((33, 33))
    records_name = name + '_value.csv'
    records_dir = os.path.join(instance_dir, records_name)
    # print(os.path.isfile(records_dir))
    q = pd.read_csv(records_dir)
    # q.drop(0)
    # print(q.head())
    q = q.values
    """
    q = []
    
    with open(path, 'rb') as f:
        for line in f:
            q.append(f)
    q.remove(['player', 'dealer', 'action', 'value'])
    """
    q_dict = {}
    for j in q:
        j = list(j)
        # print(f'This is j:{j}')
        j[0] = int(j[0])
        j[1] = int(j[1])
        j[2] = int(j[2])
        j[3] = float(j[3])
        q_dict[(j[0], j[1], j[2])] = j[3]

    for player in range(33):
        for dealer in range(33):
            hit_key = (player, dealer, 0)
            stick_key = (player, dealer, 1)
            if hit_key not in q_dict.keys():
                value_HIT = 0
                q_dict[hit_key] = value_HIT
            else:
                value_HIT = q_dict[hit_key]
            if stick_key not in q_dict.keys():
                value_STICK = 0
                q_dict[stick_key] = value_STICK
            else:
                value_STICK = q_dict[stick_key]

            if value_HIT > value_STICK:
                v[player-4][dealer-4] = value_HIT
                del q_dict[stick_key]
            else:
                v[player-4][dealer-4] = value_STICK
                del q_dict[hit_key]

    x = []
    y = []
    z = list(q_dict.values())
    for i in range(33 * 33):
        x.append(list(q_dict)[i][0])
        y.append(list(q_dict)[i][1])

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cmap = cm.get_cmap('coolwarm')
    ax.plot_trisurf(y, x, z, cmap=cmap, linewidth=0)
    file_name = name + 'value_visualization.png'
    file_dir = os.path.join(pic_dir, file_name)
    plt.savefig(file_dir)
    # plt.show()


def plotting(name, instance_dir, pic_dir, npy_dir, win_records, session):
    plot_single_player(name=name,
                       win_records=win_records,
                       pic_dir=pic_dir,
                       k=0,
                       session=session,
                       i=0)
    """
    plot_policy_comparison(name= name,
                           k=1,
                           i=1,
                           npy_dir=npy_dir,
                           pic_dir=pic_dir)
    """
    plot_state_action_value(name=name,
                            instance_dir=instance_dir,
                            pic_dir=pic_dir)
    return None

