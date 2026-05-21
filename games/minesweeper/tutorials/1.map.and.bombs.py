import random       # to be able to use random.randint functionalities

# initialize empty board:

board = []

i = 0
while i < 5:
    arr = []
    j = 0
    while j < 5:
        arr.append(0)
        j += 1
    board.append(arr)
    i += 1

# print what the array contains:
print("Print Empty minesweeper map: ")
i = 0
while i < 5:
    print (board[i])
    i += 1

# initialize mines in random array locations
mines = 3
while mines > 0:
    x = random.randint(0, 5 - 1)
    y = random.randint(0, 5 - 1)
    if board[y][x] != '*':
        board[y][x] = '*'
        mines -= 1

# print what the array contains:
print()
print("Print minesweeper map with bombs: ")
i = 0
while i < 5:
    print (board[i])
    i += 1
