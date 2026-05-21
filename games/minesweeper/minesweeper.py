import random

game_loop = 1
player_win_lose = 0 # -1 for lose 1 for win
player_win_cond = 0
mode = -1

x_y = [0, 0]
board = []
game_board = []

def     mode_select():
    global mode

    mode = -1
    while not (mode == 0 or mode == 1 or mode == 2):
        print("0 Play game")
        print("1 Show solution")
        print("2 Exit")
        mode = int(input("Select option: 0,1 or 2: "))

def map_select():
    global mode, x_y, player_win_cond, player_win_lose
    if mode == 0 or mode == 1:
        iteration = 0
        x_y = [0, 0]
        while not (x_y[0] > 0 and x_y[0] < x_y[1] and x_y[1] >= 4):   # while not all conditions are met
            if iteration == 1:                                        # user debug output:
                if not (x_y[0] > 0 and x_y[0] < x_y[1]):
                    print("\tnumber of bombs not within range of [0..map_size]")
                if not (x_y[1] >= 4):
                    print("\tmap_size not within range of [4..finite]")
            iteration = 1                                             # ensure error message code not hit on first attempt
            nbombs_bsize = input("number-of-bombs, size-of-board: ")
            # add safety code: prevent user from adding funny values.
            x_y = nbombs_bsize.split(",")                             # split string inputs into 2 variables
            x_y = [int(i) for i in x_y]                               # convert strings to integer
            # print(bombs_size)

        player_win_lose = 0
        player_win_cond = x_y[1] * x_y[1] - x_y[0] + 1
        create_board([x_y[0], x_y[1]])                                # creates the board, places mines, and how many bombs

# You may create additional functions here:
def check_regen(p_x_y, p_bomb_size):
    global board, game_board, player_win_cond
    # loop around the square and if finds any -1 -1's then keep calling this function on it:
    i = p_x_y[1]
    j = p_x_y[0]
    if j - 1 > -1:
        if board[i][j - 1] == -1 and game_board[i][j - 1] == -1:
            player_win_cond -= 1
            game_board[i][j - 1] = 1
            check_regen([j - 1, i], p_bomb_size)
    if j + 1 < p_bomb_size[1]:
        if board[i][j + 1] == -1 and game_board[i][j + 1] == -1:
            player_win_cond -= 1
            game_board[i][j + 1] = 1
            check_regen([j + 1, i], p_bomb_size)

    if i - 1 > -1:
        if board[i - 1][j] == -1 and game_board[i - 1][j] == -1:
            player_win_cond -= 1
            game_board[i - 1][j] = 1
            check_regen([j, i - 1], p_bomb_size)
        if j - 1 > -1:
            if board[i - 1][j - 1] == -1 and game_board[i - 1][j - 1] == -1:
                player_win_cond -= 1
                game_board[i - 1][j - 1] = 1
                check_regen([j - 1, i - 1], p_bomb_size)
        if j + 1 < p_bomb_size[1]:
            if board[i - 1][j + 1] == -1 and game_board[i - 1][j + 1] == -1:
                player_win_cond -= 1
                game_board[i - 1][j + 1] = 1
                check_regen([j + 1, i - 1], p_bomb_size)

    if i + 1 < p_bomb_size[1]:
        if board[i + 1][j] == -1 and game_board[i + 1][j] == -1:
            player_win_cond -= 1
            game_board[i + 1][j] = 1
            check_regen([j, i + 1], p_bomb_size)
        if j - 1 > -1:
            if board[i + 1][j - 1] == -1 and game_board[i + 1][j - 1] == -1:
                player_win_cond -= 1
                game_board[i + 1][j - 1] = 1
                check_regen([j - 1, i + 1], p_bomb_size)
        if j + 1 < p_bomb_size[1]:
            if board[i + 1][j + 1] == -1 and game_board[i + 1][j + 1] == -1:
                player_win_cond -= 1
                game_board[i + 1][j + 1] = 1
                check_regen([j + 1, i + 1], p_bomb_size)

def create_board(p_x_y):
    global board, game_board

    # initialize empty board:
    i = 0
    board = []
    while i < p_x_y[1]:
        arr = []
        j = 0
        while j < p_x_y[1]:
            arr.append(-1)
            j += 1
        board.append(arr)
        i += 1

    # initialize bombs in random array locations
    l_bombs = p_x_y[0]
    while l_bombs > 0:
        l_x = random.randint(0, p_x_y[1] - 1)
        l_y = random.randint(0, p_x_y[1] - 1)
        if board[l_y][l_x] != '*':
            board[l_y][l_x] = '*'
            l_bombs -= 1

    # initialize empty player positions board:
    i = 0
    game_board = []
    while i < p_x_y[1]:
        arr = []
        j = 0
        while j < p_x_y[1]:
            l_value = -1

            if board[i][j] == '*':          # if mine then remove from user click options
                l_value = 0
            arr.append(l_value)
            j += 1
        game_board.append(arr)
        i += 1

    # loop through and if bomb then loop around it and increments the area around it by 1
    i = 0
    while i < p_x_y[1]:
        j = 0
        while j < p_x_y[1]:
            if board[i][j] == '*':
                if j - 1 > -1:
                    if board[i][j - 1] != '*':
                        board[i][j - 1] += 1
                if j + 1 < p_x_y[1]:
                    if board[i][j + 1] != '*':
                        board[i][j + 1] += 1

                if i - 1 > -1:
                    if board[i - 1][j] != '*':
                        board[i - 1][j] += 1
                    if j - 1 > -1:
                        if board[i - 1][j - 1] != '*':
                            board[i - 1][j - 1] += 1
                    if j + 1 < p_x_y[1]:
                        if board[i - 1][j + 1] != '*':
                            board[i - 1][j + 1] += 1

                if i + 1 < p_x_y[1]:
                    if board[i + 1][j] != '*':
                        board[i + 1][j] += 1
                    if j - 1 > -1:
                        if board[i + 1][j - 1] != '*':
                            board[i + 1][j - 1] += 1
                    if j + 1 < p_x_y[1]:
                        if board[i + 1][j + 1] != '*':
                            board[i + 1][j + 1] += 1

            j += 1
        i += 1
    # pass

def print_board(p_x_y, p_bombs):
    i = 0
    l_print_string = " "
    while i < p_x_y[1]:
        l_print_string += "  " + str(i)
        i += 1
    print(l_print_string)

    # print ---------
    i = 0
    l_print_string = "-"
    while i < p_x_y[1]:
        l_print_string += "---"
        i += 1
    l_print_string += "---"
    print(l_print_string)

    # print the board values
    i = 0
    l_print_string = ""
    while i < p_x_y[1]:
        l_print_string = str(i) + " |"
        j = 0
        while j < p_x_y[1]:
            if board[i][j] == '*' and not p_bombs:
                l_print_string += " " + " |" 
            elif game_board[i][j] == 1 and (not p_bombs):
                l_print_string += str(board[i][j] + 1) + " |"
            elif game_board[i][j] == -1 and (not p_bombs):
                l_print_string += " " + " |"
            elif (board[i][j] == -1):
                l_print_string += " " + " |"
            elif board[i][j] == '*' and p_bombs:
                l_print_string += "*" + " |"           
            else:
                l_print_string += str(board[i][j] + 1) + " |"
            j += 1
        print(l_print_string)
        i += 1
 
    # print ---------
    i = 0
    l_print_string = "-"
    while i < p_x_y[1]:
        l_print_string += "---"
        i += 1
    l_print_string += "---"
    print(l_print_string)
# Additional Functions above this comment



# Implement your Minesweeper Solution Below:
def play(dim_size, num_bombs):
    #Edit the code Below Here
    global player_win_lose, player_win_cond, board, game_board, game_loop, mode
    while game_loop:
        # Show solution:
        if mode == 1:
            print_board(x_y,  True)
            mode_select()
        # Play game:
        if mode == 0:
            while player_win_lose == 0:
                print_board(x_y, mode == 1)                                         # print the board (the user sees)
                # print_board([num_bombs, dim_size], True)                          # print the board (debug interface)

                # print(dim_size, " test ", player_win_cond)                        #   (debug player win condition code)
                row_col = input("Input as row,col a block to search: ")             
                # add safety code: prevent user from adding funny values.
                row_col = row_col.split(",")                                        # split string inputs into 2 variables
                row_col = [int(i) for i in row_col]                                 # convert strings to integer

                if row_col[0] >= 0 and row_col[1] >= 0 and row_col[0] < x_y[1] and row_col[1] < x_y[1]:
                    if game_board[row_col[1]][row_col[0]] == 0:
                        player_win_lose = -1                                        # player loses
                    elif game_board[row_col[1]][row_col[0]] == -1:
                        if board[row_col[1]][row_col[0]] == -1:
                            check_regen(row_col, [num_bombs, dim_size])             # loop around the square and if finds any -1 -1's then keep calling this function on it:
                        player_win_cond -= 1
                        game_board[row_col[1]][row_col[0]] = 1                      # sucessfully reveal block
                if player_win_cond == 0:
                    player_win_lose = 1                                             # player wins

            if player_win_lose == -1:
                print("You have LOST the game!")
            elif player_win_lose == 1:
                print("CONGRATULATIONS! You have WON the game!")
            mode_select()                                                           # switch modes
            if mode == 0 or mode == 1:
                map_select()                                                        # generate new map data and reset settings
            if mode == 2:
                game_loop = 0
        # print("play: reached")

    # pass
    #Edit the code Above Here
#play Function Ends Here

if __name__=='__main__':
    mode_select()                                                               # switch modes
    map_select()                                                                # generate new map data and reset settings
    play(x_y[1], x_y[0])                                                        # required play algorithm
