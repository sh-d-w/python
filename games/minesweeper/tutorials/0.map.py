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
