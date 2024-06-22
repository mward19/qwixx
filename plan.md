# Qwixx

First, develop a text based interface for the game. The web interface can come later. Gotta get excited, yanno?

## State variables and such

- Game state
  - Players
  - Whose turn (one of the players)
  - Current roll
    - White
    - White
    - Red
    - Yellow
    - Green
    - Blue
  - Locked colors (when length is >=, game over)
  - Game over (bool)

- Player
  - Board
    - Composed of Squares
  - Turn
    - White dice choice
    - Colored dice choice

- Game loop
  - [Add ability to choose player name]
  - Randomly select player order, place in list
  - Begin game
    - Display current player's board.
    - Use carriage return to simulate the dice rolling
    - Press enter or space to stop rolling
    - Choose roll
      * Let player choose which dice to use, or penalty. Regex to validate
      * Update and print board.
      * If undo, repeat. If next player, break.
    - If four penalties, end game. 
    - If two rows locked, end game.
    - Else repeat with next player.
  - Calculate scores with the element of surprise. Podium
  