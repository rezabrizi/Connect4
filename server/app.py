from flask import Flask, request, jsonify
from flask_cors import CORS
import connect4
import uuid

def PrintBoard(board, m, n):
    """print the game board"""
    for row in reversed(range(m)):
        print(' '.join(str(board[col][row]) if len(board[col]) > row else '.' for col in range(n)))

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'dev'

# In-memory storage
games = {}


@app.route("/new_game", methods=['POST'])
def new_game():
    data = request.json
    players = data.get('players', 1)
    difficulty = data.get('difficulty', 5)
    
    depth_mapping = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 5, 8: 6, 9: 6, 10: 7}
    depth = depth_mapping.get(difficulty, 4)
    
    bot = players == 1

    game_id = str(uuid.uuid4())
    games[game_id] = connect4.Connect4Game(depth=depth, bot=bot)
    
    return jsonify({'game_id': game_id, 'players': players, 'difficulty': difficulty, 'message': 'New game created successfully.'})


@app.route("/make_player_move", methods=['POST'])
def make_player_move():
    data = request.json
    game_id = data.get('game_id')
    column = data.get('column')

    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404

    game = games[game_id]
    if (game.game_over):
        return jsonify({'error': 'Game is over'}), 400


    if not (0 <= column < 7) or (len(game.game.board[column]) == 6):  # Adjust if your column indexing starts at 0
        return jsonify({'error': 'Invalid column'}), 400
    outcome, row = game.move(column)
    
    return jsonify({'outcome': outcome, 'row': 5-row, 'column': column, 'next_player': game.player})


@app.route("/make_bot_move", methods=['POST'])
def make_bot_move():
    data = request.json
    game_id = data.get('game_id')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404

    game = games[game_id]
    
    if not game.bot: 
        return jsonify({'error': 'Game is not against a bot'}), 400
    
    if game.player != 1: 
        return jsonify({'error': 'Not the bot turn'}), 400
    
    outcome, column, row = game.bot_move()
    PrintBoard(game.get_board(), 6, 7)
    print (f"BOT----column {column}----row {row}----outcome {outcome}")

    return jsonify({'outcome': outcome, 'row': 5-row, 'column': column, 'next_player': game.player})
    
    

if __name__ == '__main__':
    app.run(debug=True)
