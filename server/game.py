'''
Game board (m x n)
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
1 1 . . . . .
1 0 0 0 . . .
'''

class ConnectFour:
    def __init__(self, m, n, players):
        # columns 
        self.n = n
        # rows
        self.m = m
        # whose turn it is 
        self.turn = 0
        # number of players 
        self.players = players
        # List of Lists ([] * m) for each column as there are m slots in each column 
        self.board = [[] for _ in range(n)]


    def GeneratePossibleMoves(self):
        """Find all possible columns the player can play in 

        Returns:
            list: columns with less than m tokens
        """
        possibleColumns = []
        for i in range (self.n):
            if len(self.board[i]) < self.m:
                possibleColumns.append(i)
        return possibleColumns
    

    def MakeMove(self, column):
        """Insert a token into a column and change the turn

        Args:
            column (int): the column index (0-based) to insert the current player's token to

        Returns:
            int: row index (0-based) of the column that was just inserted in
        """
        self.board[column].append(self.turn)
        self.turn = (self.turn + 1) % self.players
        return len(self.board[column])-1; 


    def UndoMove(self, column):
        """Remove a token from the  column specfied and undo the turn

        Args:
            column (int): index of the column to remove the token from
        """
        self.board[column].pop()
        self.turn = (self.turn - 1 + self.players) % self.players 
        
        
    def IsTerminalNode(self, turn, lastRow = None, lastColumn = None):
        """Check if we have reached a terminal state (winning or tie)

        Args:
            turn (int): the turn to check its win
            lastRow (int, optional): last row that was played. Defaults to None.
            lastColumn (int, optional): last col that was played. Defaults to None.

        Returns:
            int: outcome of the current game state
        """
        if (lastRow is not None and lastColumn is not None):
            if (self.__CheckWin(lastRow, lastColumn, turn)):
                return turn
        if all(len(column) == self.m for column in self.board):
            # game is a tie
            return -2
        # game is not over
        return -1
    

    def three_token_heuristic (self, turn):
        """determine if there are three tokens adjacent that can turn into winning states

        Args:
            turn (int): the turn to check for the heuristic

        Returns:
            int: three token heuristic score
        """
        count = 0 
        # Vertical checks of 3s 
        for column in self.board: 
            if 3 <= len(column) < self.m:
                three_vertical_tokens = True 
                for i in range(3): 
                    if (column[len(column)-1-i] != turn):
                        three_vertical_tokens = False
                        break
                if three_vertical_tokens: 
                    count += 30

        
        # Horizontal Checks
        for i in range (self.m):
            for j in range (self.n-3):
                if len(self.board[j]) > i:
                    three_horizontal_tokens = True
                    for k in range(3):
                        if not (len(self.board[j+k]) > i and self.board[j+k][i] == turn):
                            three_horizontal_tokens = False
                            break 
                    if three_horizontal_tokens:
                        left_empty = (j > 0 and len(self.board[j-1]) <= i)
                        right_empty = (j+3 < self.n and len(self.board[j+3]) <= i)
                        if left_empty or right_empty:
                            count += 20

        # Diagonal from buttom left to top right 
        for i in range (self.m-3):
            for j in range (self.n-3):
                if len(self.board[j]) > i:
                    three_left_diagonal_tokens = True
                    for k in range (3):
                        dr = i + k 
                        dc = j + k
                        if not(len(self.board[dc]) > dr and self.board[dc][dr] == turn):
                            three_left_diagonal_tokens = False
                            break 
                    if three_left_diagonal_tokens:
                        buttom_left_empty = (i > 0 and j > 0 and len(self.board[j-1]) <= i-1)
                        top_right_empty = (i+3 < self.m and j+3 < self.n and len(self.board[j+3]) <= i+3)
                        if buttom_left_empty or top_right_empty:
                            count += 10

        # Diagonal from top left to buttom right
        for i in range(self.m-1, 1, -1):
            for j in range (self.n-3):
                if len(self.board[j]) > i:
                    three_right_diagonal_tokens = True
                    for k in range (3):
                        dr = i-k
                        dc = j+k
                        if not (len(self.board[dc]) > dr and self.board[dc][dr] == turn):
                            three_right_diagonal_tokens = False
                            break 
                    if three_right_diagonal_tokens:
                        top_left_empty = (i+1 < self.m and j > 0 and len(self.board[j-1]) <= i+1)
                        buttom_right_empty = (i-3 >= 0 and j+3 < self.n and len(self.board[j+3]) <= i-3)
                        if top_left_empty or buttom_right_empty:
                            count += 10   
        return count                   
            

    def EvaluateBoard(self, outcome):
        """determine the board score

        Args:
            outcome (int): current terminality state of the board

        Returns:
            int: score of the current state of the board 
        """
        if outcome == 1:
            return 1000
        elif outcome == 0:
            return -1000
        elif outcome == -2:
            return 0
        else: 
            maximizer = self.three_token_heuristic (1)
            minimizer = -self.three_token_heuristic (0)
            return maximizer + minimizer


    def Minimax(self, depth, isMaximizingPlayer, alpha=float('-inf'), beta=float('inf'), lastColumn=None):      
        """Minimax recursive function

        Args:
            depth (int): current depth of the game tree
            isMaximizingPlayer (bool): whether the maximizing player is playing or not
            alpha (int, optional): alpha value used for alpha-beta pruning. Defaults to float('-inf').
            beta (int, optional): beta value used for alpha-beta pruning. Defaults to float('inf').
            lastColumn (int, optional): last column that was played. Defaults to None.

        Returns:
            int: best score of the current player's move
        """
        lastRow = len(self.board[lastColumn])-1 if lastColumn is not None else None

        lastTurn = (self.turn-1+self.players) % self.players
        terminal_state = self.IsTerminalNode(lastTurn, lastRow, lastColumn)
        if (depth == 0 or terminal_state != -1):
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
        """Determine the next best move for the AI

        Args:
            depth (int): the depth to exand the game tree to

        Returns:
            int: the column corresponding to the best move
        """
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
        """Check whether a player has won a game vertically

        Args:
            row (int): the row of the last move
            column (int): the column of the last move
            currentTurn (int): the player to check for a win

        Returns:
            bool: whether there was a vertical win
        """
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
        """Check whether a player has won a game horizontally

        Args:
            row (int): the row of the last move
            column (int): the column of the last move
            currentTurn (int): the player to check for a win

        Returns:
            bool: whether there was a horizontal win
        """
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
        """Check whether a player has won a game in the bottom left to top right direction

        Args:
            row (int): the row of the last move
            column (int): the column of the last move
            currentTurn (int): the player to check for a win

        Returns:
            bool: whether there was a bottom left to top right win
        """
        
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
        """Check whether a player has won a game in the top left to bottom right direction

        Args:
            row (int): the row of the last move
            column (int): the column of the last move
            currentTurn (int): the player to check for a win

        Returns:
            bool: whether there was a top left to bottom right win
        """
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
        """Check whether a player has won a game in any direction

        Args:
            row (int): the row of the last move
            column (int): the column of the last move
            currentTurn (int): the player to check for a win

        Returns:
            bool: whether there was a win
        """
        return self.__CheckVerticalWin (row, column, currentTurn) or self.__CheckHorizontalWin (row, column, currentTurn) or  self.__CheckLeftDiagonalWin (row, column, currentTurn) or self.__CheckRightDiagonalWin (row, column, currentTurn)


    def PlayToken(self, column) -> int:
        """Allow player to play the game

        Args:
            column (int): column index (1-based) to play

        Raises:
            ValueError: Check column validity
            ValueError: Check if a column is full

        Returns:
            int: whether the player won the game following their move
        """

        if (column < 0 or column >= self.n):
            raise ValueError("Enter a valid column")

        if (len(self.board[column]) == self.m):
            raise ValueError("Column is full")
        
        self.board[column].append(self.turn)
        row = len(self.board[column])-1

        if (self.__CheckWin(row, column, self.turn)):
            return self.turn 
        
        outcome = self.IsTerminalNode(self.turn, row, column)
        if (outcome != -1):
            return outcome
        
        self.turn = (self.turn + 1) % self.players
        return outcome
    

def PrintBoard(board, m, n):
    """print the game board
    """
    for row in reversed(range(m)):
        print (' '.join(str(board[col][row]) if len(board[col]) > row else '.' for col in range(n)))


def play(bot):
    """game driver

    Args:
        bot (bool): wether the game is against a bot or P vs. P
    """
    cf = ConnectFour(6, 7, 2) 
    game_over = False
    current_player = 0  
    
    while not game_over:
        if current_player == 0:  
            print("Current board state:")
            PrintBoard(cf.board, cf.m, cf.n)

            column = int(input("Enter your move (1-7): ")) 
            try:
                result = cf.PlayToken(column-1)
                if result != -1:
                    if (result == -2):
                        print ("Game is tied!")
                    else:
                        print(f"Player {result} wins!")
                    game_over = True
            except ValueError as e:
                print(e)
                continue  

        elif (not bot):
            print("Current board state:")
            PrintBoard(cf.board, cf.m, cf.n)
            column = int(input("Enter your move (1-7): "))
            try: 
                result = cf.PlayToken(column)
                if (result == -2):
                    print ("Game is tied!")
                else:
                    print(f"Player {result} wins!")
                game_over = True
            except ValueError as e: 
                print(e)
                continue  
        
        else:
            print("Bot is thinking...")
            best_move = cf.GetBestMove(7)
            result = cf.PlayToken(best_move)
            print(f"Bot played in column {best_move}")
            if result != -1:
                print(f"Player {result} wins!")
                game_over = True
        current_player = (current_player+1) % 2

    print("Game over!")
    PrintBoard(cf.board, cf.m, cf.n)
    

if __name__ == "__main__":
    play(True)






