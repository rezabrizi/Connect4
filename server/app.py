from flask import Flask, request, jsonify, session
import connect4
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev' 

# In-memory storage
games = {} 


# API Routes

# new game takes in 2 arguments, number of players (1 or 2 for player vs bot ror player vs player) and difficulty (from 1 to 10)
@app.route("/new_game", methods=['POST'])
def new_game():
    # Extract number of players and difficulty from the request
    data = request.json
    players = data.get('players', 1)  # Default to 1 player if not specified
    difficulty = data.get('difficulty', 5)  # Default difficulty level to 5 if not specified
    
    # Map difficulty to depth for the Minimax algorithm; adjust mapping as needed
    depth_mapping = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 5, 8: 6, 9: 6, 10: 7}
    depth = depth_mapping.get(difficulty, 4)  # Default depth to 4 if not mapped
    
    bot = players == 1  # Bot is enabled if there's only 1 player

    # Create a new game instance
    game_id = str(uuid.uuid4())
    games[game_id] = connect4.Connect4Game(depth=depth, bot=bot)
    
    # Return the game ID and initial state
    initial_board = games[game_id].get_board()
    return jsonify({
        'game_id': game_id,
        'board': initial_board,
        'players': players,
        'difficulty': difficulty,
        'message': 'New game created successfully.'
    })


# this api will make a move by giving the column number 
# if the game is with a bot then we will make a bot move too unless before the player has won
@app.route("/make_move", methods=['POST'])
def make_move():
    data = request.json
    column = data.get('column')
    is_bot_move = data.get('is_bot_move', False)

    if 'game_id' not in session or session['game_id'] not in games:
        return jsonify({'error': 'Game not found'}), 404

    game_id = session['game_id']
    game = games[game_id]

    if is_bot_move:
        # Check if it's a bot's turn based on game logic
        if game.bot and game.player == 1:  # Assuming player 0 is human, 1 is bot
            outcome = game.bot_move()
        else:
            return jsonify({'error': 'Not bot\'s turn'}), 400
    else:
        if not 0 < column <= 7:
            return jsonify({'error': 'Invalid column'}), 400
        outcome = game.move(column)

    board = game.get_board()
    return jsonify({'outcome': outcome, 'board': board, 'next_player': game.player})


@app.route("/get_board", methods=['GET'])
def get_board():
    if 'game_id' not in session or session['game_id'] not in games:
        return jsonify({'error': 'Game not found'}), 404

    game_id = session['game_id']
    game = games[game_id]

    board = game.get_board()
    return jsonify({'board': board})



if __name__ == '__main__':
    app.run(debug=True)