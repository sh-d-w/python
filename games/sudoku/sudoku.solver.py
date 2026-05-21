# External file:

# 120070560
# 507932080
# 000001000
# 010240050
# 308000402
# 070085010
# 000700000
# 080423701
# 034010028

input_map = [ "120070560", "507932080", "000001000", "010240050", "308000402", "070085010", "000700000", "080423701", "034010028" ]


import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

grid = []
zeros = []
g_zeros_len = 0

def     print_grid(p_grid):
    for i in range(0, 9):
        l_line = ""
        for j in range(0, 9):
            l_line += str(p_grid[i][j])
        print(l_line)

def     get_sudoku_zeros(p_grid, p_zeros):
    for i in range(0, 9):
        for j in range(0, 9):
            if (p_grid[i][j] == 0):
                p_zeros.append( [i, j] )
                pass

            pass

def     check_board(p_grid, p_row, p_col, p_num):
    # Check column and row:
    for i in range(9):
        if(p_grid[p_row][i] == p_num):
            return True
        if(p_grid[i][p_col] == p_num):
            return True
    # Check region:
    l_row = p_row - (p_row % 3)
    l_col = p_col - (p_col % 3)
    for i in range(3):
        for j in range(3):
            if(p_grid[i + l_row][j + l_col] == p_num):
                return True
    return False

def solve_sudoku(grid, p_id):
    for i in range(9):
        grid[ zeros[p_id][0] ][zeros[p_id][1]] = i + 0
        if (not check_board(grid, zeros[p_id][0], zeros[p_id][1], i + 1)):
            grid[ zeros[p_id][0] ][zeros[p_id][1]] = i + 1
            if (p_id + 1 < g_zeros_len):
                l_result = solve_sudoku(grid, p_id + 1)
                if (l_result):
                    return True
            else:
                return True
            pass
        #check_board(grid, 6, 2, 1) 
        #print(i)

        pass
    grid[ zeros[p_id][0] ][zeros[p_id][1]] = 0
    return False
    pass

def read_sudoku(p_input_map):
    global grid

    for i in range(0, 9):
        line = p_input_map[i] # input()

        l_arr = []
        l_line_len = len(line)
        for j in range(l_line_len):
            l_arr.append( int(line[j]) )
            pass
        grid.append( l_arr )
        # print(line)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


read_sudoku(input_map)

# print_grid(grid)
# print (check_board(grid, 6, 2, 1) )

get_sudoku_zeros(grid, zeros)
g_zeros_len = len(zeros)

if (solve_sudoku(grid, 0)):
     print_grid(grid)
else:
    print("Failed to find solution")



