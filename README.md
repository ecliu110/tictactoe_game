To Run:

```
pip install Flask
export FLASK_APP=tictactoe.py
flask run
```

Sample input from a single game:

1. Create a game

    Input: 
    ```
    curl -X POST localhost:5000/games
    ``` 

    Output:
    ```
    {
        "game_id": 1,
        "players_turn": "X",
        "status": "in progress",
        "board": [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
    }
    ```

2. Make a move on a game
    
    Each move requires a player and move with (X, Y) coordinates, with (0, 0) defined as the upper left corner, e.g.:
    
    ```
                         X-Coordinate
     
                     (0,0) | (1,0) | (2,0)
                    -----------------------
    Y-Coordinate     (0,1) | (1,1) | (2,1)
                    -----------------------
                     (0,2) | (1,2) | (2,2)
    ```

    Input Data:
    
    ```
    curl -H "Content-Type: application/json"                            \
        -X PUT -d '{"players_turn":"X","x_position":1,"y_position":2}' \
        localhost:5000/games/123
    ```
    
    Output:
    ```
    {
        "game_id": 1,
        "players_turn": "O",
        "status": "in progress",
        "board": [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", "X", " "]
        ]
    }
    ```
    
3. Check game status
    
    A game may be in the following statuses:
    
        * in progress
        * x wins
        * o wins
        * tie
    
    Input:
    
    ```
    curl localhost:5000/games/1
    ```
    
    Output:
    ```
    {
        "game_id": 1,
        "players_turn": "O",
        "status": "in progress",
        "board": [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", "X", " "]
        ]
    }
    ```
    
4. Invalid Moves

    Wrong Player Attempting to Move:
    
    ```
    curl -H "Content-Type: application/json"                            \
        -X PUT -d '{"players_turn":"X","x_position":0,"y_position":0}' \
        localhost:5000/games/1
    ```
    
    Attempting to move to an already taken position:
    
    ```
    curl -H "Content-Type: application/json"                            \
        -X PUT -d '{"players_turn":"X","x_position":2,"y_position":1}' \
        localhost:5000/games/1
    ```
    
    Attempting to move when the game is already over (Cat's Game, or a player has won)