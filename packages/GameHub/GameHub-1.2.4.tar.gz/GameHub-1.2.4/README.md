# Game Hub

This project contains the games: rock paper scissors, hang man and tic tac toe at the 
moment. These are stored in individual files that can be played by themselves. They are
then organised in a CLI that has all of them callable via a command. A key feature is
that these commands can be called anywhere in the system after initialising the setup.py
file. The CLI can also create a repl and has other commands.

## How to use

First download it:

```
pip install gameHub
```
Now whenever you write gamehub (the name of the command group) it will show a help 
menu of all commands and command groups. You can get the commands of those command
groups by appending their name to gamehub 
```
Usage: gameHub [OPTIONS] COMMAND [ARGS]...

  the group of all the commands

Options:
  -h, --help  Show this message and exit.

Commands:
  generate   Pick Random Game to play
  last_game  Plays the last game you played
  play       Group of all games
  play_list  Play's a random game from a list
  repl       Creates a repl and a exit command
```
here you can also see the help menu of play, the group of commands that contains the
games:
```
Commands:
  hang  Plays Hangman game
  rps   Plays Rock Paper Scissors game
  tic   Plays Tic Tac Toe game
```
## The Games

* [TicTacToe](#tictactoe)
* [HangMan](#hangman)
* [Rock Paper Scissors](#rock-paper-scissors)


### TicTacToe
To play tic tac toe, you can enter either:
```
gamehub play tic
```
or, if you are in the repl
```
> play tic
```
Tic tac toe first takes three inputs from the user before it can start the game. It asks 
if you want to see the tutorial, if you want to go against the ai or another human and 
which difficulty you would like to play (if you are facing the ai).
The tutorial is a big string which shows a demonstration of the game being played.
Then it asks if you want to play against the ai or a human.

#### The AI
The ai is made up of two functions. The first one is called minimax(). 

#### Minimax

Minimax’s job is to figure out the score of a given possible move on a given board. If we
say there are three moves left, then it would create a top single branch where it’s O’s 
turn, three branches where it would be X’s turn and then two branches which lead to 
completed boards.

![Diagram](./README_resources/tictactoe_minimax_diagram.png)

Minimax would start at the top of the tree, then go down to the 1st branch, and then down 
to the first full board inside of that. Then it would evaluate that board and get a score.
The score can range from 1 to -1, with 1 meaning that x wins, -1 meaning O wins and 0 
meaning that it is a draw. This means that x will always aim for 1, and O will aim for -1.
Let’s say that we evaluated the 1st board and got 0, then we evaluated the 2nd board and 
got 1. Because the player is x, they will aim for the 2nd board, as 1 is more than 0. 
This means that now we know that if we pick the first branch, x will win. Because the 
player on the top branch is o, they now know to avoid this branch. Then we would go onto 
the second branch and evaluate the 3rd and 4th boards. Let’s say that they both have a 
score of -1. Then the best score for the second branch would be -1 and so it would be 
returned up to the top branch. Because the 2nd branch always leads to o winning (or -1) 
o will prefer to pick this one in the game. This means that the 2nd branch’s score will 
replace the 1st branch’s score. Finally, let’s say that the 5th and 6th board are -1 
and 0. X will look for the biggest number, which is 0. So that will be returned to the 
top branch, and then 0 would be compared against the best_score (-1). However, because 
0 is more than -1, it isn’t saved, and -1 continues to be the best score. Now, because 
we have finished looping through all the branches, the best score is returned and the 
function finishes. In this case, it returns -1.

#### Choose ai move

The other function is called choose_ai_move. This function loops through each of the
possible moves and then calls minimax to see what would happen if the A.I made a move
over here. Then, based on the difficulty level, it saves one to do later . The difficulty 
levels are split up into multiple parts:
 
* win  - aims for the best move
* draw - aims for draw but if can't goes for win
* lose - aims for lose but if can't goes for draw

### Hangman

To play hangman, you can enter either:
```
gamehub play hang
```
or, if you are in the repl
```
> play hang
```
Hangman takes a random word from a .txt file and then makes a hidden one from that. Then,
it makes you guess a letter of the word (or the entire word if you're feeling confident).
After that, it checks if you guessed right and if you did then it reveals a letter and if
you didn't then it takes away a chance. If you run out, then it prints that you lost and 
the word but if you won, then it prints a congratulation message. 

### Rock Paper Scissors

To play rock paper scissors, you can enter either:
```
gamehub play rps
```
or, if you are in the repl
```
> play rps
```
Rock Paper Scissors takes an input and checks if it's one of the three. It then picks
a random one as well and compares the two. After the comparison, it prints who won 

## Contributing

You can join the project but there a few standards that I would like to keep in place.
- Use single-quotes for strings unless double-quotes are necessary
- You must use tests and your code must be readable
- You must add a new issue to gitlab every time there is something you want to add/fix
- Make sure to update documentation after adding new code

## Versioning

We use the [SemVer](http://semver.org/) standard for versioning 

## Authors

* **Brooklyn Germa** - *Leader of project* - [bGerma](https://gitlab.com/bGerma)
* **Abel Germa** - *Assistance and Guidance* - [aGerma](https://gitlab.com/agerma)

## Acknowledgments

* Abel helped every step of the way
* Thanks to Mum for supplying us with Buna