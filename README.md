# Hanabi_Intro_To_AI

## Hanabi Game 

Hanabi is a cooperative card game created by French game designer Antoine Bauza and published in 2010. Players are aware of other players' cards but not their own, and attempt to play a series of cards in a specific order to set off a simulated fireworks show.

#### Game Rules

The game of Hanabi is played with 50 cards. Each card consists of a number and a color. There are 5
different colors available (red, green, yellow, blue, white). The numbers on the cards range from 1 to 5
(1’s three times per color, 2’s 3’s 4’s two times per color and one 5 for each color). The aim of the game
is to create a firework, which can be achieved by playing cards in the correct order. There is a pile for
each color on the game board, hence you can make only one pile for each color. You can play all of your
hand cards, but only if the color matches the one on the game board and the number is the successor of
this card the turn is successful meaning that if there is a red 1 on the board you only can play a red 2
otherwise you will lose a live (collect a red coin). When you lose all of your lives (collected 3 red coins)
the game is over and the fireworks explodes. Based on the amount of cards the final score is calculated.
Other then usual card games you see all cards of your play mates, but not your own cards. Therefore it is
necessary to share information about the cards which your other players have, so they can be sure about
what cards they have. In each turn a player can do 3 different types of actions. Either playing a card
in his hand, discarding a card to the discard pile, where everyone can see it or he can give a hint to an
other player. If a cards is played or discarded the player draws a new card from the deck. If the deck is
empty every player has one remaining turn left, then the game is over. A hint is either about the color or
number of a players Hand. For example player A has the hand [ 3R | 2G | 1G | 5G ] player B could
give him the hint that he has 1 card with the number 3 or 3 cards which are green and so on. The player
which receives the hint, will know which cards are effected by the hint. Hints can only be done if there
are blue coins left. In the beginning of the game there are 8 blue coins, if hint is performed a blue coins is
deducted. If a card is discarded a blue coin is added. Also if a stack of cards reaches 5 (the highest card)
there is also a blue coin added.

## How to run the code.

The game simulation and the agents run on Python 3.

In order to install the requirements run

`pip install requirements.txt`

The repository contains two entry points of execution.
1. main.py runs a single game 
2. game_runner.py executes 100 times a single game and show the statistic such as: average score, average number of plays, average remaining lives and reason the state in which each game finished.

Be aware that the game_runner can take from 1-2h to execute 100 games in the **Charlie** agent.

#### Game configuration.

The repository allows several configurations that can be seen at the `.env` file in the root of the project.

Each player can have a different name that will be shown in terminal when executing the game.

Each player can also be assigned a human player, or an AI agent. AI-agents available are:
1. **Alpha**. Plays random actions on its turn.
2. **Beta**. Uses an evaluation function and chooses the action that would bring the highest value to the game-state.
3. **Charlie**. Uses an evaluation function and a Tree-sarch algorithm to identify the best play.

The evaluation function used in **Charlie** can be configured as well in the `.env` file. All variables that contains "_VALUE" will weight higher different state of the game.

For example increasing "LIVE_VALUE" will make the agent choose actions that would not involve losing lives. And if we lower the value agents would take a more risky behavior.
    
## Agent results.

Here is a list of the scores obtained with each of the agents.

1. Alpha - 1.2
2. Beta - 9.24
3. Charlie - 13.59

