class ConnectFour:

    def __init__(self, m, n, players):
        self.n = n
        self.m = m
        self.turn = 0
        self.players = players
        self.board = [[] for _ in range(n)]

    def GeneratePossibleMoves(self):
        possibleColumns = []
        for i in range (self.n):
            if len(self.board[i]) < self.m:
                possibleColumns.append(i)
        return possibleColumns
    
    def MakeMove(self, column):
        # Simulate making a move for the current player in the given column.

        self.board[column].append(self.turn)
        self.turn = (self.turn + 1) % self.players
        return len(self.board[column])-1; 


    def UndoMove(self, column):
        # Remove the last token from the given column and switch the turn back.
        self.board[column].pop()
        self.turn = (self.turn - 1 + self.players) % self.players 
        
    def IsTerminalNode(self, lastRow = None, lastColumn = None):
        # Check if the game has ended (win, loss, draw).
        if (lastRow is not None and lastColumn is not None):
            if (self.__CheckWin(lastRow, lastColumn)):
                # someone won
                return self.turn
        if all(len(column) == self.m for column in self.board):
            # game is a tie
            return -1
        # game is not over
        return -2 


    def EvaluateBoard(self, lastRow = None, lastColumn = None):
        # Evaluate and return the score of the board.
        outcome = self.IsTerminalNode(lastRow, lastColumn)
        if outcome == 1:
            return 10
        elif outcome == 0:
            return -10
        else:
            return 0


    def Minimax(self, depth, isMaximizingPlayer, alpha=float('-inf'), beta=float('inf'), lastColumn=None):
        # Implement the minimax algorithm.
        lastRow = len(self.board[lastColumn])-1 if lastColumn is not None else None 
        terminal_state = self.IsTerminalNode(lastRow, lastColumn)
        if (depth == 0 or terminal_state != -2):
            return self.EvaluateBoard(lastRow, lastColumn)
        
        if isMaximizingPlayer: 
            maxEval = float('-inf')
            for column in self.GeneratePossibleMoves():
                row = self.MakeMove(column)
                eval = self.Minimax(depth-1, False, alpha, beta, column)
                self.UndoMove(column)
                maxEval = max(eval, maxEval)
                alpha = max (alpha, eval)
                if beta <= alpha: 
                    break 
            return maxEval
        else:
            maxEval = float('inf')
            for column in self.GeneratePossibleMoves():
                row = self.MakeMove(column)
                eval = self.Minimax(depth-1, True, alpha, beta, column)
                self.UndoMove(column)
                maxEval = min(eval, maxEval)
                beta = min (eval, beta)
                if beta <= alpha:
                    break
            return maxEval

    def GetBestMove(self, depth):
        # Use the minimax algorithm to find and return the best move.
        bestScore = float('-inf')
        bestMove = None 
        for column in self.GeneratePossibleMoves():
            row = self.MakeMove(column)
            score = self.Minimax(depth-1, False, float('-inf'), float('inf'), column)
            self.UndoMove(column)
            if score > bestScore:
                bestScore = score
                bestMove = column
        return bestMove


    def __CheckVerticalWin(self, row, column) -> bool:
        if (row < 3):
            return False
        verticalStreak = 0
        for dy in range (4):
            ny = row - dy 
            if (self.board[column][ny] == self.turn):
                verticalStreak += 1 
            else: 
                break
        
        return (verticalStreak == 4)

    def __CheckHorizontalWin(self, row, column) -> bool:

        horizontalStreak = 0
        for d in range (-3, 4):
            nx = column + d

            if 0 <= nx < self.n and len(self.board[nx]) > row:
                if self.board[nx][row] == self.turn:
                    horizontalStreak += 1
                    if horizontalStreak == 4:
                        return True
                else:
                    horizontalStreak = 0
            else:
                horizontalStreak = 0 
        return False

    def __CheckLeftDiagonalWin(self, row, column) -> bool:

        leftDiagonalStreak = 0 
        for d in range (-3, 4):
            ny = row + d 
            nx = column - d 

            if 0 <= nx < self.n and 0 <= ny < len(self.board[nx]):
                if self.board[nx][ny] == self.turn:
                    leftDiagonalStreak += 1
                    if leftDiagonalStreak == 4:
                        return True
                else:
                    leftDiagonalStreak = 0 
            else:
                leftDiagonalStreak = 0
        return False

    def __CheckRightDiagonalWin(self, row, column) -> bool:
        rightDiagonalStreak = 0 
        for d in range (-3, 4):
            ny = row + d 
            nx = column + d 

            if 0 <= nx < self.n and 0 <= ny < len(self.board[nx]):
                if self.board[nx][ny] == self.turn:
                    rightDiagonalStreak += 1
                    if rightDiagonalStreak == 4:
                        return True
                else:
                    rightDiagonalStreak = 0 
            else:
                rightDiagonalStreak = 0
        return False

    def __CheckWin(self, row, column) -> bool:
        return self.__CheckVerticalWin (row, column) or self.__CheckHorizontalWin (row, column) or  self.__CheckLeftDiagonalWin (row, column) or self.__CheckRightDiagonalWin (row, column)

    def PlayToken(self, column) -> int:
        
        column -= 1

        if (column < 0 or column >= self.n):
            raise ValueError("Enter a valid column")

        if (len(self.board[column]) == self.m):
            raise ValueError("Column is full")
        
        self.board[column].append(self.turn)
        row = len(self.board[column])-1

        if (self.__CheckWin(row, column)):
            return self.turn 

        self.turn = (self.turn + 1) % self.players
        return -1
    


def human_vs_bot_game():
    cf = ConnectFour(6, 7, 2)  # Initializes the Connect Four game
    game_over = False
    current_player = 0  # Start with the human player
    
    while not game_over:
        if current_player == 0:  # Human player's turn
            print("Current board state:")
            for row in reversed(range(cf.m)):
                print(' '.join(str(cf.board[col][row]) if len(cf.board[col]) > row else '.' for col in range(cf.n)))
            column = int(input("Enter your move (1-7): ")) # Human input, adjust for 0-indexed
            try:
                result = cf.PlayToken(column)
                if result != -1:
                    print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  # Ask for input again if there was an error
        else:  # Bot's turn
            print("Bot is thinking...")
            best_move = cf.GetBestMove(10) + 1 # You can adjust depth based on difficulty
            result = cf.PlayToken(best_move)
            print(f"Bot played in column {best_move + 1}")
            if result != -1:
                print(f"Player {result} wins!")
                game_over = True

        # Switch turns
        current_player = (current_player + 1) % 2

    print("Game over!")
    # Optionally print the final board state here

if __name__ == "__main__":
    human_vs_bot_game()






