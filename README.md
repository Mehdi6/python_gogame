# Implementation of the Go Game
This is an implementation of the Go game using Python programming language. The code implements a friendly UI with a very simple design, using the famous python GUI library PyQt.

## Understading the game, it's rules and how it's played

Go ("encircling game") is an abstract strategy board game for two players, in which the aim is to surround more territory than the opponent. 
The game was invented in China over 3,000 years ago, and is therefore believed to be the oldest board game continuously played today. It was considered one of the four essential arts of the cultured aristocratic Chinese scholars in antiquity. Despite its relatively simple rules, Go is very complex, even more so than chess. 

Computers have only recently been capable of beating human masters. Have a look at the following for more details: https://deepmind.com/research/alphago/
*****

- Initial Board Layout: We will use a 7x7 board to ensure quick game play and reduced complexity. Go is commonly played on a 13x13 and 19x19 grid. Black goes first. Stones are placed on the grid intersections. 

- Movement: Black plays first, with black and white taking turns. A stone can be placed at any unoccupied intersection of the board with limited exceptions. 

- Suicide Rule: You cannot place a stone which will immediately have no liberties.

- KO Rule (Eternity Rule): Previous game states are not allowed. Keep a list of previous game states which must be checked before stones are placed https://youtu.be/JWdgqV-8yVg?t=7m35s 

- Determining a Winner: When a player thinks their territories are all safe, and they cannot gain any more territory, reduce their opponent's territory or capture more strings, instead of playing a stone on the board they pass and hand a stone to your opponent as a prisoner. Two consecutive passes terminates the game. 
i)  Awarding of Points: (1) stones captured (2) territory controlled by a colour
ii) Additional Rules and Information: 
-- A detailed set of rules is available here https://www.britgo.org/intro/intro2.html 
-- A cartoon tutorial is available at https://www.britgo.org/cartoons/index.html 
-- A well-structured version of the rules is available here https://en.wikipedia.org/wiki/Rules_of_Go 
-- An extensive list of GO terms available at https://en.wikipedia.org/wiki/List_of_Go_terms 
-- There is a lot of additional information on Go some of it code related at 
https://senseis.xmp.net/ 
iii)  Interesting Situations
-- Seki (Impasse): A board position may arise where a play can capture opponents’ piece, but the opponent can immediately recapture a string of pieces. Whoever goes first loses. https://youtu.be/JWdgqV-8yVg?t=11m12s 
-- Having eyes is a strong position 
vi) Handicaps
-- You may implement this as an advanced task, but you will need to do more research. Typically, white gets 7.5 points for going 2nd. The .5 point is to avoid a tie. 

## Technical details

There are four major files:

- board.py: this is the file where the board, which is a grid of n by n squares, is implemented.
- score_board.py: is meant to hold the code for a side barre which is enriched with information to follow players score.
- game_logic.py: we managed to put here the score computation methods and logic.
- go.py: in this file, we have the board and score board put together in order to form the full board.

Requirements:

- the only library needed is PyQt, once installed correctly you can run the code.

## Issue Reporting

If you have found a bug or feature request, please report them at the repository issues section.

## License 

MIT

## Acknowledgements

In this exercice, we have used different resources to manage the implementation of the game. We thank the community of programmers that keep sharing valuable information in order to solve implementation problems. 
