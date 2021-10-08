# Reinforcement Learning for Blackjack

Author: ZHA Mengyue

SID: 20668901

Math Department of HKUST

![](https://github.com/Dolores2333/Blackjack/blob/main/casino.png)

## Problem Statement

We study playing Blackjack by reinforcement learning. Prediction methods used to update q-value function for option here are Monte Carlo, Q Learning and Temporal Difference. We also test the algorithm under different combination of (M, N). M is the number of decks and N denotes N-1 palyers with 1 dealer. For each configuration, we find the optimal policy after iterations. Outcomes of three pre diction methods are compared by visualization and tables. 

Since the detailed rules in different casinos of different areas varies a lot, we describe the one we adopt in the code here. The rule we used basically follows the one in Sutton's book (Example 5.1, p.93, Chapter 5). 

### Card Count:

- 2-9: the number on the cards
- Jack, Queen, King: 10
- Ace: 1 or 11, maximizing the points player gets that no more than 21
- Jockers: not used in the Blackjack

### Game Initialization

#### Cards Initialization

We consider the case each player compete independently with the dealer. The game initialize with two cards dealt to both the players and the dealer. All cards dealt in initialization are faced up except for the second one dealt to the dealer. 

#### Instant Wins

If the palyer has 21 after initialization (an Ace and a 10-card), it's called a natural and that palyer wins unless the dealer also has a natural. In the case both some players and the dealer has a natual then the game is a draw. 

### Game On

The players turn first:

Players request additional cards one by one (Hit) until it choose to stop (Stick) or the points got after last hit exceeds 21 (Bust) and then is the next player's turn. If one player goes bust then it loses immediately or we will see later after the dealer's turn. 

If all palyers go bust then the dealder immediately wins no matter his points later. If there are some players stick successfully without an bust then the dealer's turn begins. The dealer sticks on any sum of 17 or greater and hits otherwise. Note that the dealer's strategy is fixed without any choice. 

### Game over

We compare the points for the successful players stick before a bust and the dealer to determine the final reward. If the dealer goes bust then the survival palyers wins then the  final outcome —— win, lose and draw are determined by whose final sum is closer to 2. 

#### Rewards

- win: +1
- lose: -1
- draw: 0

### Game Implementation Details

All rewards with in a game are zero and we use the discount factor $\gamma=1$ which means the terminal rewards are also the returns. 

State: 

- (players' card points, dealer's dhowing card points)

Action: 

- hit: 0
- stick: 1

Decks:

Denoted by termianl input variable M (eg. --M=2 means two decks are used in the game). If the users want to use infinite deck aka with replacement then they should type --M=0 because the code recognize 0 deck as infinite deck. 

In order to make sure that the cards are sufficient we also insert a mechanism to automatically reinitialize the decks once the number of cards left are smaller than $M * 52 * 0.6$ . BTW, infinite decks make keeping track of the already dealt cards impossible.  

## Homework Statement

Assume that in the Blackjack game, there are $m$ decks of cards, and $n$ players (a dealer vs $n-1$ players). The rules of the game are explained above. 

(1) Find the optimal policy for the Blackjack, when $m=\infty$ and $n=2$. You can use any of the methods learned so far in class (e.g. Monte Carlo, TD, or Q-Learning). If you use more than one method, do they reach the same optimal policy?

(2) Visualise the value functions and policy as done in Figures 5.1 and 5.2 in Sutton's book. 

(3) Redo (1) for different combinations of (m,n), e.g. $m=6, 3, 1$, and $n=3,4,6$. What are differences?

## Implementation

### File Structure

- main.py: main code needs terminal variable aissignment for the number of $m$ decks (--m) and the number of $n$ people (--n). One dealer and $n-1$ players. 

  NOTE: Our main.py accepts receive a list of m and n as the inputs and doing the experiments of combination of these m's and n's. Once you run the main.py, it builds several instances under corresponding INSTANCE folder where each instance is basically an experiment with a try on a set of specific hyperparameters. We list the hyperparameters below and discuss them later. 

  - m: number of decks
  - n: number of people
  - update: the method used to update the value or q value function. eg. Monte Carlo, Q Learning and Temporal Difference
  - policy: the policy improvement strategy. choices are epsilon greedy policy and the best policy. 

  Other hyperparameters are epoches, n_zeros and session. 

- config.json: stores the  configuration. This config.json is only a template. We will create new ones for experiments with different hyperparameters combination later.  
  - epochs: how many times of the Blackjack we played with the algorithm to train it. 
  - update: the method used to update the q-value function
  - name: the name of the experiment
  - policy: policy method used for the experiment
  - n_zero: a factor used to calculate the $\epsilon$ in epsilon greedy policy 
  
- deck.py: class Deck()
  - def __ init __(): initialize the $m$ decks
  - def shuffle(): suffle the decks
  - def pop(): pop up a card and delete it from the decks
  
- player.py: class Player()
  - def hit(): hit action
  - def call_points(): player return the points it got
  
- game.py: class Game()
  - def __ init __(): Initialize a game as described in the problem statement, game initialization section. 
  - def step(): given the current state and action, return the next state and reward

- utils.py
  - def MC(): Monte Carlo update function
  - def QL(): Q Learning update function
  - def TD(): Temporal Difference update function
  - def save_value(): save the Q value function in the form that every row is (player's points, dealer's points, action, value)
  - def save_win_records(): save the (state, action, value) pairs visited by a specific palyer
  
- plot.py

  - def plot_single_player(): plot the (state, action, value) pairs visited by a specific player
  - def plot_state_action_value(): plot the value function learned
  - All pics created in this section will be stored in the path HOME+STORAGE+INSTANCE+pic

### Example

1. Prepare the environment

   ```shell
   conda create -n Blackjack python=3.6
   ```

   ```shell
   conda activate Blackjack
   ```

   Now your working environment is the Blackjack now. Let's install the necessary packages. We have listed all packages in requirement.txt

   ```
   pip install -r requirement.txt
   ```

   Now your environment should be fully ready. 

2. Experiments on a single Instance 

   The following code blocks plays the Blackjack with m=2 decks and n=3 people where 2 are players and one is the dealer. 

   ```
   python main.py --m=2, --n=3
   ```

   Note that when $m=\infty$, we use --m=0 instead. 

   ```shell
   python main.py --m=0, --n=2
   ```

3. Experiments on instances of combinations of (m, n)

   Also you can test the combinations of (m, n) pairs. For example, m= 6, 3, 1 and n= 3, 4, 6

   ```shell
   python main.py --m 6 3 1 --n 3 4 6
   ```

4. Experiments on $m=\infty$

   We use --m=0 infers to use infinite decks in the game instead. 

5. The optimal policy

   We store the final Q-value function instead and the optimal poliy are derived from it by either best policy or epsilon greedy policy. 

   The value.csv are stored in thecorresponding instance folder as:

   MC_best_value.csv

   MC_epsilon_value.csv

   QL_best_value.csv

   etc.

## Tabular Summary for the Experiments

Choices for policy update: policy=['best', 'epsilon'] 

Choices for policy evaluateion(value function update): update=['MC', 'QL', 'TD']

- best: best policy evaluation
- epsilon: epsilon greedy policy evaluation
- MC: Monte Carlo
- QL: Q Learning
- TD: Temporal Difference

### Single Instance of $m=\infty$, $n=2$

| m=$\infty$, n=2       | MC       | QL       | TD       |
| --------------------- | -------- | -------- | -------- |
| best policy           | 39.9040% | 37.9700% | 37.1210% |
| epsilon greedy policy | 42.4840% | 41.3440% | 41.2620% |

#### Conclusions:

- epsilon greedy policy outperforms best policy
- The best update strategy is MC and TD has the lowest performance

### Combination of m=[6, 3, 1], n=[3, 4, 6]

We summary the performance of (update_policy) combinations in the tables below.

| MC_best | n=3      | n=4      | n=6      |
| ------- | -------- | -------- | -------- |
| m=6     | 40.0435% | 40.1663% | 39.7334% |
| m=3     | 39.7110% | 39.7077% | 39.1590% |
| m=1     | 40.5960% | 40.2913% | 39.2028% |

| MC_epsilon | n=3      | n=4      | n=6      |
| ---------- | -------- | -------- | -------- |
| m=6        | 42.0310% | 42.1147% | 42.5882% |
| m=3        | 42.4060% | 42.5710% | 42.1484% |
| m=1        | 42.5700% | 42.6407% | 42.6614% |

| QL_best | n=3      | n=4      | n=6      |
| ------- | -------- | -------- | -------- |
| m=6     | 38.935%  | 38.5240% | 38.5292% |
| m=3     | 39.1540% | 38.4173% | 38.7022% |
| m=1     | 39.5825% | 39.3437% | 38.9810% |

| QL_epsilon | n=3      | n=4      | n=6      |
| ---------- | -------- | -------- | -------- |
| m=6        | 41.3675% | 41.5430% | 41.4012% |
| m=3        | 41.5625% | 41.7900% | 41.3582% |
| m=1        | 41.8030% | 42.0723% | 41.7474% |

| TD_best | n=3      | n=4      | n=6      |
| ------- | -------- | -------- | -------- |
| m=6     | 39.3855% | 40.2017% | 39.5762% |
| m=3     | 39.9090% | 40.3023% | 39.6646% |
| m=1     | 39.4165% | 39.6960% | 40.2408% |

| TD_epsilon | n=3      | n=4      | n=6      |
| ---------- | -------- | -------- | -------- |
| m=6        | 41.4880% | 41.0790% | 41.0342% |
| m=3        | 41.1925% | 41.0230% | 41.2132% |
| m=1        | 41.6990% | 41.3067% | 41.3138% |

#### Conclusions

- epsilon greedy policy outperforms best policy
- The best update strategy is MC and TD has the lowest performance
- For MC_best, the more players are in, the less chance they will win
- For MC_epsilon, if we see the values in table as an matrix, the lower triangle part is greater than the upper triangle part. This means players enjoys greater chance to win when many players palying with few decks (**just one deck is perfect!**). 
- The conclusions for QL_best and QL_epsilon are the same with MC_epsilon. 
- For TD_best and TD_epsilon, the phenomenon in MC_epsilon is quite weak. Some combinations of $(m, n)$ in the upper triangle part are quite well. 
  - TD_best: (m=6, n=4), (m=3,n=4)
  - TD_epsilon: (m=6, n=3)

#### Testing

We provide useful test codes and print commands bracket by the annotation sign """ """ inside the code. If you would like to test the code in small sclae, you can assign epochs to be 10 and n_seros to be 2. Then release the print in lines 79-81, 159-165, 172-181, 203-212 in main.py. You may also test objects like player, deck and game in the corresponding python file after releasing the annotation on the last few lines. 

### Hyperparameters

All settable hyperparameters except for $m$ and $n$ are assigned by the instance level config.json under the instance's folder. 

Some hypperparameters has finite many choices and will be generated in the main.py when different instances are created. We will write these hyperparameters into the instance level config.json that inherited from the template config.json (under the INSTANCE folder).  

- update: choices in ['MC', 'QL', 'TD']
- name: choices in the combination of form 'update-epsilon' or 'update-best' for policy being epsilon greedy policy and best policy respectively. 
- policy: choices in ['epsilon_greedy_policy', 'best_policy']

We also has some higher level hyperparameters that are assigned in the template config.json. Note that these hyperparameters are the same for all instances created by call main.py once. They are:

- epochs: number of iterations. 
- n_zeros: a constant for determine the value of $\epsilon$ in epsilon greedy policy
- session: denotes how often we summay the performance of a given player in plot.py. For example, if session = 1000, we summary its wins losses and draws every 1000 actions. 

## Visualization

We illustrate the typical plots as examples and you want to see more, please visit the subfolder with path = STORAGE/INSTANCE/pic

### Visualization on ![](http://latex.codecogs.com/gif.latex?\m=\infty), ![](http://latex.codecogs.com/gif.latex?\n=2)

We only take the update=MC as example and you should refer to Blackjack/storage/m0n2/pic/ for outcomes for QL and TD

#### Value Function Visualization

MC_best_value visualization

![](https://github.com/Dolores2333/Blackjack/blob/main/storage/m0n2/pic/MC_bestvalue_visualization.png)

MC_epsilon_value visualization

![](https://github.com/Dolores2333/Blackjack/blob/main/storage/m0n2/pic/MC_epsilonvalue_visualization.png)

Remark

Since I forgot to add the labels for x-axis, y-axis and z-axis when doing the experiment, their position and labels are denoted by the following Pseudo Value Function Plot. All axes' arrangements in the figures of this repository follow the [left-hand rule](https://en.wikipedia.org/wiki/Fleming%27s_left-hand_rule_for_motors).  You may refer to the following pic to identify the arrangement and meaning of the x, y, z axes. 

![](https://github.com/Dolores2333/Blackjack/blob/main/axis_example.png)

#### Player Performance Visualization

##### Visualize MC

MC_best_player_1 visualization

![](https://github.com/Dolores2333/Blackjack/blob/main/storage/m0n2/pic/MC_best_player_1_performance_plot.png)

MC_epsilon_player_1 vs. MC_best_player_1 visualization

![](https://github.com/Dolores2333/Blackjack/blob/main/storage/m0n2/pic/MC_epsilon_player_1_performance_plot.png)

We see clearly that under the update rule MC, the player with epsilon greedy policy performs consistently better than they player with the deterministic best policy. The outcome shows that **expolration is important !!!**

##### Compare MC, QL, TD and best, epsilon

We have the following conclusions by observing the player performance visualization on update=[MC, QL, TD] and policy=[best, epsilon]

- epsilon greedy policy outperforms the best policy consistently no matter which update strategy we adopt.

- For a fixed policy, the performances of update strategies are MC>QL>TD

  The **reason** we guess is that since the Blackjack game has a relative small state space and action space, some advantages of MC are maximized:

  - precise real return without apprixiamtion
  - sampled long trajectories making memory on the card possible. 

## Citation

If you use my Blackjack in any context, please cite this repository:

```latex
@article{
  ZHA2021:RL_Blackjack,
  title={Reinforcement Learning for the Blackjack},
  author={ZHA Mengyue},
  year={2021},
  url={https://github.com/Dolores2333/Blackjack}
}
```

This work is done by ZHA Mengyue for Homework1 in MATH6450I Reinforcement Learning lectured by Prof Bing-yi Jing in [HKUST](https://hkust.edu.hk/). Please cite the repository if you use the code and outcomes. 

