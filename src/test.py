def three_token_heuristic (turn, board, n, m):
    count = 0 
    
        # Vertical checks of 3s 
    for column in board: 
        if 3 <= len(column) < m:
            three_vertical_tokens = True 
            for i in range(3): 
                if (column[len(column)-1-i] != turn):
                    three_vertical_tokens = False
                    break
            if three_vertical_tokens: 
                count += 10

    
    # Horizontal Checks
    for i in range (m):
        for j in range (n-3):
            if len(board[j]) > i:
                three_horizontal_tokens = True
                for k in range(3):
                    if not (len(board[j+k]) > i and board[j+k][i] == turn):
                        three_horizontal_tokens = False
                        break 
                if three_horizontal_tokens:
                    left_empty = (j > 0 and len(board[j-1]) <= i)
                    right_empty = (j+3 < n and len(board[j+3]) <= i)
                    if left_empty or right_empty:
                        count += 10

    # Diagonal from buttom left to top right 
    for i in range (m-3):
        for j in range (n-3):
            if len(board[j]) > i:
                three_left_diagonal_tokens = True
                for k in range (3):
                    dr = i + k 
                    dc = j + k
                    if not(len(board[dc]) > dr and board[dc][dr] == turn):
                        three_left_diagonal_tokens = False
                        break 
                if three_left_diagonal_tokens:
                    buttom_left_empty = (i > 0 and j > 0 and len(board[j-1]) <= i-1)
                    top_right_empty = (i+3 < m and j+3 < n and len(board[j+3]) <= i+3)
                    if buttom_left_empty or top_right_empty:
                        count += 10

    # Diagonal from top left to buttom right
    for i in range(m-1, 1, -1):
        for j in range (n-3):
            if len(board[j]) > i:
                three_right_diagonal_tokens = True
                for k in range (3):
                    dr = i-k
                    dc = j+k
                    if not (len(board[dc]) > dr and board[dc][dr] == turn):
                        three_right_diagonal_tokens = False
                        break 
                if three_right_diagonal_tokens:
                    top_left_empty = (i+1 < m and j > 0 and len(board[j-1]) <= i+1)
                    buttom_right_empty = (i-3 >= 0 and j+3 < n and len(board[j+3]) <= i-3)
                    if top_left_empty or buttom_right_empty:
                        count += 10   
    return count                   
            

if __name__ == "__main__":
    board = [
        [1, 0, 1],
        [],
        [0, 0, 0, 1],
        [0, 0, 1],
        [0, 1],
        [0],
        [],
    ]
    print (three_token_heuristic (1, board, 7, 6))
