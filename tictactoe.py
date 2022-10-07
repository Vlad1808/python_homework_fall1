empty_board = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
empty_board

print('')
def place_the_board(empty_board):
    print('--------')
    print(empty_board[0] + '|' + empty_board[1] + '|' + empty_board[2])
    print('--------')
    print(empty_board[3] + '|' + empty_board[4] + '|' + empty_board[5])
    print('--------')
    print(empty_board[6] + '|' + empty_board[7] + '|' + empty_board[8])

def check_win(board):
    if (board[0] == board[1] == board[2]):
        return True
    elif (board[3] == board[4] == board[5]):
        return True
    elif (board[6] == board[7] == board[8]):
        return True
    elif (board[0] == board[3] == board[6]):
        return True 
    elif (board[1] == board[4] == board[7]):
        return True 
    elif (board[0] == board[4] == board[8]): 
        return True 
    elif (board[2] == board[4] == board[6]):
        return True 
    elif (board[0] == board[1] == board[2]):
        return True
    else: 
        return False 

move = 1
for i in range(10):
    user_input = input('Place your position:')
    if user_input in empty_board:
        if move % 2 != 0:
            player = 'X'
        else:
            player = 'O'
        for i in range(len(empty_board)):
            if empty_board[i] == user_input:
                empty_board[i] = player
            else: 
                pass
        place_the_board(empty_board)
        if check_win(empty_board):
            print('Game over ' + player + ' won')
            break
        elif move == 9:
            print('All of the positions are taken, it is a tie')
            break
        else: 
            pass
        move+=1       
    else:
        print('Your position is invalid, enter a new position')
else: 
    print('The position had been taken, choose a new one')