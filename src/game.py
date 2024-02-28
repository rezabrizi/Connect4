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

        self.board[column].append(self.turn)
        self.turn = (self.turn + 1) % self.players
        return len(self.board[column])-1; 


    def UndoMove(self, column):
        self.board[column].pop()
        self.turn = (self.turn - 1 + self.players) % self.players 
        
        
    def IsTerminalNode(self, currentTurn, lastRow = None, lastColumn = None):
        if (lastRow is not None and lastColumn is not None):
            if (self.__CheckWin(lastRow, lastColumn, currentTurn)):
                return currentTurn
        if all(len(column) == self.m for column in self.board):
            # game is a tie
            return -1
        # game is not over
        return -2 


    def EvaluateBoard(self, outcome):
        if outcome == 1:
            return 10
        elif outcome == 0:
            return -10
        else:
            return 0


    def Minimax(self, depth, isMaximizingPlayer, alpha=float('-inf'), beta=float('inf'), lastColumn=None):      
        lastRow = len(self.board[lastColumn])-1 if lastColumn is not None else None

        lastTurn = (self.turn-1+self.players) % self.players
        terminal_state = self.IsTerminalNode(lastTurn, lastRow, lastColumn)
        if (depth == 0 or terminal_state != -2):
            return self.EvaluateBoard(terminal_state)

        if isMaximizingPlayer: 
            maxEval = float('-inf')
            for column in self.GeneratePossibleMoves():
                self.MakeMove(column)
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
                self.MakeMove(column)
                eval = self.Minimax(depth-1, True, alpha, beta, column)
                self.UndoMove(column)
                maxEval = min(eval, maxEval)
                beta = min (eval, beta)
                if beta <= alpha:
                    break
            return maxEval

    def GetBestMove(self, depth):
        bestScore = float('-inf')
        bestMove = None 
        # this will return a list of columns after the last player made a move
        for column in self.GeneratePossibleMoves():
            self.MakeMove(column)
            score = self.Minimax(depth-1, False, float('-inf'), float('inf'), column)
            self.UndoMove(column)
            if score > bestScore:
                bestScore = score
                bestMove = column
        return bestMove

    def __CheckVerticalWin(self, row, column, currentTurn) -> bool:
        if (row < 3):
            return False
        verticalStreak = 0
        for dy in range (4):
            ny = row - dy 
            if (self.board[column][ny] == currentTurn):
                verticalStreak += 1 
            else: 
                break
        
        return (verticalStreak == 4)

    def __CheckHorizontalWin(self, row, column, currentTurn) -> bool:

        horizontalStreak = 0
        for d in range (-3, 4):
            nx = column + d

            if 0 <= nx < self.n and len(self.board[nx]) > row:
                if self.board[nx][row] == currentTurn:
                    horizontalStreak += 1
                    if horizontalStreak == 4:
                        return True
                else:
                    horizontalStreak = 0
            else:
                horizontalStreak = 0 
        return False

    def __CheckLeftDiagonalWin(self, row, column, currentTurn) -> bool:

        leftDiagonalStreak = 0 
        for d in range (-3, 4):
            ny = row + d 
            nx = column - d 

            if 0 <= nx < self.n and 0 <= ny < len(self.board[nx]):
                if self.board[nx][ny] == currentTurn:
                    leftDiagonalStreak += 1
                    if leftDiagonalStreak == 4:
                        return True
                else:
                    leftDiagonalStreak = 0 
            else:
                leftDiagonalStreak = 0
        return False

    def __CheckRightDiagonalWin(self, row, column, currentTurn) -> bool:
        rightDiagonalStreak = 0 
        for d in range (-3, 4):
            ny = row + d 
            nx = column + d 

            if 0 <= nx < self.n and 0 <= ny < len(self.board[nx]):
                if self.board[nx][ny] == currentTurn:
                    rightDiagonalStreak += 1
                    if rightDiagonalStreak == 4:
                        return True
                else:
                    rightDiagonalStreak = 0 
            else:
                rightDiagonalStreak = 0
        return False

    def __CheckWin(self, row, column, currentTurn) -> bool:
        return self.__CheckVerticalWin (row, column, currentTurn) or self.__CheckHorizontalWin (row, column, currentTurn) or  self.__CheckLeftDiagonalWin (row, column, currentTurn) or self.__CheckRightDiagonalWin (row, column, currentTurn)

    def PlayToken(self, column) -> int:
        
        column -= 1

        if (column < 0 or column >= self.n):
            raise ValueError("Enter a valid column")

        if (len(self.board[column]) == self.m):
            raise ValueError("Column is full")
        
        self.board[column].append(self.turn)
        row = len(self.board[column])-1

        if (self.__CheckWin(row, column, self.turn)):
            return self.turn 

        self.turn = (self.turn + 1) % self.players
        return -1
    
    def PrintBoard(self):
        for row in reversed(range(self.m)):
            print (' '.join(str(self.board[col][row]) if len(self.board[col]) > row else '.' for col in range(self.n)))

def play(bot):
    cf = ConnectFour(6, 7, 2) 
    game_over = False
    current_player = 0  
    
    while not game_over:
        if current_player == 0:  
            print("Current board state:")
            cf.PrintBoard()

            column = int(input("Enter your move (1-7): ")) 
            try:
                result = cf.PlayToken(column)
                if result != -1:
                    print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  

        elif (not bot):
            print("Current board state:")
            cf.PrintBoard()
            column = int(input("Enter your move (1-7): "))
            try: 
                result = cf.PlayToken(column)
                if result != -1:
                    print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e: 
                print(e)
                continue  
        
        else:
            print("Bot is thinking...")
            best_move = cf.GetBestMove(11)
            best_move += 1
            result = cf.PlayToken(best_move)
            print(f"Bot played in column {best_move + 1}")
            if result != -1:
                print(f"Player {result} wins!")
                game_over = True

        current_player = (current_player + 1) % 2

    print("Game over!")
    cf.PrintBoard()
    

if __name__ == "__main__":
    play(True)






