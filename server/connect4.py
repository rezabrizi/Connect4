import game

class Connect4Game:
    def __init__(self, depth, bot):
        self.game = game.ConnectFour(6, 7, 2)
        self.player = 0 
        self.depth = depth
        self.bot = bot

    def move (self, column):
        outcome =  self.game.PlayToken(column)
        self.player = (self.player+1) % 2
        return outcome
        

    def bot_move(self):
        column = self.game.GetBestMove(self.depth)+1
        return self.move(column)
    

    def get_board(self):
        board = []  # Create a new, empty list for the board
        for col in self.game.board:
            board.append(col.copy())  # Copy each column manually
        
        for col in range(self.game.n):
            current_row = len(board[col])
            empty_cells = self.game.m - current_row
            for _ in range(empty_cells):
                board[col].append('X')  # Append -1 to simulate empty cells
        return board


def PrintBoard(board, m, n):
    """print the game board
    """
    for row in reversed(range(m)):
        print (' '.join(str(board[col][row]) if len(board[col]) > row else '.' for col in range(n)))

def play_game(bot, depth):
    game_over = False
    game = Connect4Game(depth)
    while (not game_over):
        
        if game.player == 0:
            print("Current board state:")
            PrintBoard(game.get_board(), 6, 7)

            column = int(input("Enter your move (1-7): ")) 

            try:
                result = game.player_move(column)
                if result != -1:
                    if (result == -2):
                        print ("Game is tied!")
                    else:
                        print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  

        if (not bot):
            print("Current board state:")
            PrintBoard(game.get_board(), 6, 7)

            column = int(input("Enter your move (1-7): ")) 

            try:
                result = game.player_move(column)
                if result != -1:
                    if (result == -2):
                        print ("Game is tied!")
                    else:
                        print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  
        
        else:
            try:
                result = game.bot_move()
                if result != -1:
                    if (result == -2):
                        print ("Game is tied!")
                    else:
                        print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  

    print("Game over!")
    PrintBoard(game.get_board(), 6, 7)
    
if __name__ == "__main__":
    play_game(True, 7)


