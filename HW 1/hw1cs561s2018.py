def check_available_move(matrix, player):
    all_available_moves = [] # Indicate all the available for next round
    for row in range(8):
        for column in range(8):
            if matrix[row][column] != 0 and (matrix[row][column][0] in player):  # Take whatever who are not 0, and is current player's turn
                if (player=="Star"):
                    if check_jump(player, [row, column], [row - 1, column - 1], [row - 2, column - 2], matrix) == True: all_available_moves.append([row, column, row - 2, column - 2])
                    if check_jump(player, [row, column], [row - 1, column + 1], [row - 2, column + 2], matrix) == True: all_available_moves.append([row, column, row - 2, column + 2])

                if (player=="Circle"):
                    #print("current piece is", matrix[row][column], [row, column])  # Print is for testing purpose
                    if check_jump(player, [row, column], [row + 1, column - 1], [row + 2, column - 2], matrix) == True: all_available_moves.append([row, column, row + 2, column - 2])
                    if check_jump(player, [row, column], [row + 1, column + 1], [row + 2, column + 2], matrix) == True: all_available_moves.append([row, column, row + 2, column + 2])

    for row in range(8):
        for column in range(8):
            if matrix[row][column] != 0 and (matrix[row][column][0] in player):  # Take whatever who are not 0, and is current player's turn
                if (player=="Star"):
                    if check_move(player, [row, column], [row - 1, column - 1], matrix) == True: all_available_moves.append([row, column, row - 1, column - 1])
                    if check_move(player, [row, column], [row - 1, column + 1], matrix) == True: all_available_moves.append([row, column, row - 1, column + 1])

                if (player=="Circle"):

                    if check_move(player, [row, column], [row + 1, column - 1], matrix) == True: all_available_moves.append([row, column, row + 1, column - 1])
                    if check_move(player, [row, column], [row + 1, column + 1], matrix) == True: all_available_moves.append([row, column, row + 1, column + 1])

    return all_available_moves

# Check to see if it can jump
def check_jump(player, current_posi, via, next_posi, matrix):
    x_next_posi = next_posi[0]
    y_next_posi = next_posi[1]

    x_via = via[0]
    y_via = via[1]

    x_current_posi = current_posi[0]
    y_current_posi = current_posi[1]

    # Check if the next move is outside of the 8*8 board
    if x_next_posi < 0 or x_next_posi > 7 or y_next_posi < 0 or y_next_posi > 7:
        return False

    # In row 1 to 6, Check if the next piece contain C and S piece
    if (matrix[x_next_posi][y_next_posi] != "0" and x_next_posi!=0 and x_next_posi!=7 ):
        return False

    if matrix[x_via][y_via] == "0":
        return False

    # for star piece
    if player =="Star":
        if x_next_posi > x_current_posi: return False  # Star can only move up

        if matrix[x_via][y_via] == "C1" and x_next_posi == 0 and matrix[x_next_posi][y_next_posi][0] == "C": # via is C and next piece is empty and next piece is equal to "C"
            return False
        if matrix[x_via][y_via] == "C1" and x_next_posi == 0 and matrix[x_next_posi][y_next_posi][0] == "S":
            return True
        if matrix[x_via][y_via] == "C1" and x_next_posi != 0 and x_next_posi!= 7 and x_next_posi!=6 and matrix[x_next_posi][y_next_posi][0] == "S": # via is C , next pos is not first row, and can not be start and second start row
            return False
        if matrix[x_via][y_via] == "S1":
            return False
    # for circle piece

    if player == "Circle":
        if x_next_posi < x_current_posi:
            return False # only move down
        if matrix[x_via][y_via] == "S1" and x_next_posi == 7 and matrix[x_next_posi][y_next_posi][0] == "S":
            return False
        if matrix[x_via][y_via] == "S1" and x_next_posi == 7 and matrix[x_next_posi][y_next_posi][0] == "C":
            return True
        if matrix[x_via][y_via] == "S1" and x_next_posi != 7 and x_next_posi!= 0 and x_next_posi!=1 and matrix[x_next_posi][y_next_posi][0] == "C":
            return False
        if matrix[x_via][y_via] == "C1":
            return False


    return True # can jump

def check_move(player, current_posi, next_posi, matrix):
    x_next_posi = next_posi[0]
    y_next_posi = next_posi[1]

    x_current_posi = current_posi[0]
    y_current_posi = current_posi[1]

    if x_next_posi < 0 or x_next_posi > 7 or y_next_posi < 0 or y_next_posi > 7:
        return False

    if player == "Star":
        if x_next_posi > x_current_posi: return False # only move up
        if (x_next_posi == 0 and matrix[x_next_posi][y_next_posi] == "C1"):
            return False
        if (x_next_posi!= 0 and matrix[x_next_posi][y_next_posi] != "0"): # if next row is 1 to 6, and the next piece is not "0"
            return False
    # for Circle
    if player == "Circle":
        if x_next_posi < x_current_posi: return False # circle's column value can be be go up, can not go down
        if (x_next_posi == 7 and matrix[x_next_posi][y_next_posi] == "S1"):
            return False
        if (x_next_posi!=7 and matrix[x_next_posi][y_next_posi] != "0"): # if next row is 1 to 6, and the next piece is not "0"
            return False

    return True # can move

def move(current_posi, next_posi, matrix, player, num_nodes_para):
    global num_nodes
    x_next_posi = next_posi[0]
    y_next_posi = next_posi[1]
    num_nodes = num_nodes_para

    x_current_posi = current_posi[0]
    y_current_posi = current_posi[1]
    if (abs(x_next_posi - x_current_posi) == 1): #if we made a move
        if (player == "Star"):
            if (x_next_posi != 0):
                matrix[x_next_posi][y_next_posi] = matrix[x_current_posi][y_current_posi]  # make the move
                matrix[x_current_posi][y_current_posi] = "0"  # delete the source
            if (x_next_posi == 0): # first row
                num_piece_thisbox = matrix[x_next_posi][y_next_posi]
                num_piece_thisbox = num_piece_thisbox.replace('S', '')  # replace S
                #print("testingggggg", matrix[x_next_posi][y_next_posi], x_next_posi, y_next_posi, matrix[x_current_posi][y_current_posi], x_current_posi, y_current_posi)
                int_num_piece_thisbox = int(num_piece_thisbox)
                int_num_piece_thisbox = int_num_piece_thisbox + 1
                new_num_piece_thisbox = str(int_num_piece_thisbox)
                new_num_piece_thisbox = new_num_piece_thisbox[:0] + 'S' + new_num_piece_thisbox[0:]
                matrix[x_next_posi][y_next_posi] = new_num_piece_thisbox  # make the move
                matrix[x_current_posi][y_current_posi] = "0"
        if (player == "Circle"):
            if (x_next_posi != 7):
                matrix[x_next_posi][y_next_posi] = matrix[x_current_posi][y_current_posi]  # make the move
                matrix[x_current_posi][y_current_posi] = "0"  # delete the source
            if (x_next_posi == 7):
                num_piece_thisbox = matrix[x_next_posi][y_next_posi]
                num_piece_thisbox = num_piece_thisbox.replace('C', '')  # replace S
                int_num_piece_thisbox = int(num_piece_thisbox)
                int_num_piece_thisbox = int_num_piece_thisbox + 1
                new_num_piece_thisbox = str(int_num_piece_thisbox)
                new_num_piece_thisbox = new_num_piece_thisbox[:0] + 'C' + new_num_piece_thisbox[0:]
                matrix[x_next_posi][y_next_posi] = new_num_piece_thisbox  # make the move
                matrix[x_current_posi][y_current_posi] = "0"

    if (x_current_posi - x_next_posi) % 2 == 0:  # we made a jump...
            if (player == "Star"):
                if (x_next_posi != 0):
                    matrix[x_next_posi][y_next_posi] = matrix[x_current_posi][y_current_posi]  # make the move
                    matrix[(x_current_posi + x_next_posi) / 2][
                        (y_current_posi + y_next_posi) / 2] = "0"  # delete the jumped piece
                    matrix[x_current_posi][y_current_posi] = "0"
                if (x_next_posi == 0): #go to the last row
                    num_piece_thisbox = matrix[x_next_posi][y_next_posi]
                    num_piece_thisbox = num_piece_thisbox.replace('S', '')  # replace S
                    int_num_piece_thisbox = int(num_piece_thisbox)
                    int_num_piece_thisbox = int_num_piece_thisbox + 1
                    new_num_piece_thisbox = str(int_num_piece_thisbox)
                    new_num_piece_thisbox = new_num_piece_thisbox[:0] + 'S' + new_num_piece_thisbox[0:]
                    matrix[x_next_posi][y_next_posi] = new_num_piece_thisbox  # make the move
                    matrix[(x_current_posi + x_next_posi) / 2][(y_current_posi + y_next_posi) / 2] = "0"  # delete the jumped piece
                    matrix[x_current_posi][y_current_posi] = "0"
            if (player == "Circle"):
                if (x_next_posi != 7):
                    matrix[x_next_posi][y_next_posi] = matrix[x_current_posi][y_current_posi]  # make the move
                    matrix[(x_current_posi + x_next_posi) / 2][
                        (y_current_posi + y_next_posi) / 2] = "0"  # delete the jumped piece
                    matrix[x_current_posi][y_current_posi] = "0"
                if (x_next_posi == 7): #go to the last row
                    num_piece_thisbox = matrix[x_next_posi][y_next_posi]
                    #print("matrix at this point",matrix)
                    #print("next piece is",num_piece_thisbox)
                    num_piece_thisbox = num_piece_thisbox.replace('C', '')  # replace S
                    #print("testing", matrix[x_next_posi][y_next_posi], x_next_posi, y_next_posi, matrix[x_current_posi][y_current_posi], x_current_posi, y_current_posi)
                    #print(num_piece_thisbox)
                    int_num_piece_thisbox = int(num_piece_thisbox)
                    int_num_piece_thisbox = int_num_piece_thisbox + 1
                    new_num_piece_thisbox = str(int_num_piece_thisbox)
                    new_num_piece_thisbox = new_num_piece_thisbox[:0] + 'C' + new_num_piece_thisbox[0:]
                    matrix[x_next_posi][y_next_posi] = new_num_piece_thisbox  # make the move
                    matrix[(x_current_posi + x_next_posi) / 2][(y_current_posi + y_next_posi) / 2] = "0"  # delete the jumped piece
                    matrix[x_current_posi][y_current_posi] = "0"

    return matrix,(current_posi, next_posi)
##========================================
## Minimax Algorithm

#global current_depth
global max_scores
global two_pass
global num_nodes
global original_player
global optimal_path


def maxvalue(alpha_para, beta_para, player, algorithm_para, depth_limit, matrix, moves, row_values, two_pass_para, num_nodes_para, original_player_para, optimal_path_para, current_depth_para):
    #global current_depth
    global max_scores
    global two_pass
    global num_nodes
    global original_player
    global optimal_path

    alpha = alpha_para
    beta = beta_para
    algorithm = algorithm_para
    current_depth = current_depth_para
    optimal_path = optimal_path_para
    original_player = original_player_para
    num_nodes = num_nodes_para
    two_pass = two_pass_para
    this_moves = moves
    #print("max function current depth", current_depth)
    #print("max function moves", this_moves)
    local_max = float('-inf')

    #print("current player in max function is", player)

    if(this_moves == []):  # this moves is a array of available moves, if it is [], then we pass, dont_run any functions

        copy_matrix = [['0'] * 8 for k in range(8)]

        for a in range(8):
            for b in range(8):
                copy_matrix[a][b] = matrix[a][b]

        two_pass = two_pass + 1
        num_nodes = num_nodes + 1


        #print("testing", optimal_path)
        if two_pass >= 2:  # If there are two continue pass, game over
            #print("two pass value max value function is,", two_pass)
            this_scores = calculateScores(original_player, copy_matrix, row_values, this_moves)
            if this_scores > local_max:
                #optimal_path.append("pass")  #
                local_max = this_scores
            return local_max

        if (player == "Circle"): new_player = "Star"
        if (player == "Star"): new_player = "Circle"



        check_player_has_piece = 0
        for row in range(8):
            for column in range(8):
                if (new_player == "Star"):
                    if (copy_matrix[row][column][0] == "S"):
                        check_player_has_piece = check_player_has_piece + 1
                if (new_player == "Circle"):
                    if (copy_matrix[row][column][0] == "C"):
                        check_player_has_piece = check_player_has_piece + 1

        if check_player_has_piece > 0: # if the next player has piece to move, game continue
            if (current_depth == int(depth_limit)):  # If we need to stop
                #print("i am the king", original_player, copy_matrix, row_values, this_moves)
                this_scores = calculateScores(original_player, copy_matrix, row_values, this_moves)
                if current_depth == 1:
                    optimal_path.append("pass")
                    optimal_path.append(copy_matrix)
                if this_scores > local_max:

                    local_max = this_scores

            if (current_depth < int(depth_limit)):  # If we can go deeper
                avil_moves_for_next_depth = check_available_move(copy_matrix, new_player)  # Check the next move for the first moved piece   [1,4,0,5]         , 1,4,0,3
                if current_depth == 1:
                    optimal_path.append("pass")
                    optimal_path.append(copy_matrix)
                #print("i am in depth 3", local_max)
                min_function_scores = minvalue(alpha, beta, new_player, algorithm, depth_limit, copy_matrix, avil_moves_for_next_depth, row_values, two_pass, num_nodes, original_player, optimal_path, current_depth+1)  # how to do max of this?# else:
                if min_function_scores > local_max:

                    local_max = min_function_scores


        if check_player_has_piece == 0:  # if the next player has no piece to move, this is a terminal node
            this_scores = calculateScores(original_player, copy_matrix, row_values, this_moves)
            if this_scores > local_max:
                local_max = this_scores

        return local_max

    else:

        for i in range(len(this_moves)):
            two_pass = 0


            copy_matrix = [['0']*8 for k in range(8)]

            for a in range(8):
                for b in range(8):
                    copy_matrix[a][b] = matrix[a][b]

            num_nodes = num_nodes + 1
            the_matrix, position = move((this_moves[i][0], this_moves[i][1]), (this_moves[i][2], this_moves[i][3]), copy_matrix, player, num_nodes)  # make move on new board, now i move multiple pieces on the board

            if (player == "Circle"): new_player = "Star"
            if (player == "Star"): new_player = "Circle"

            #print("max function after make move", copy_matrix)

            # Check if new player has piece to play or not
            check_player_has_piece = 0
            for row in range(8):
                for column in range(8):
                    if (new_player == "Star"):
                        if (copy_matrix[row][column][0] == "S"):
                            check_player_has_piece = check_player_has_piece + 1
                    if (new_player == "Circle"):
                        if (copy_matrix[row][column][0] == "C"):
                            check_player_has_piece = check_player_has_piece + 1

            if check_player_has_piece > 0: # if the next player still have pieces to move
                if (current_depth == int(depth_limit)):  # If we need to stop

                    this_scores = calculateScores(original_player, copy_matrix, row_values, this_moves)

                    if this_scores > local_max:
                        if current_depth == 1:
                            optimal_path.append(position)
                            optimal_path.append(the_matrix)
                            #print("get the best position 1111111", optimal_path)
                        local_max = this_scores

                    if (algorithm == "ALPHABETA"):
                        if local_max > alpha:
                            alpha = local_max

                        if beta <= alpha:
                            break

                if (current_depth < int(depth_limit)):                 # If we can go deeper
                        avil_moves_for_next_depth = check_available_move(copy_matrix,new_player)  # Check the next move for the first moved piece   [1,4,0,5]         , 1,4,0,3
                        #if (avil_moves_for_next_depth == []):

                        #print("max function next avail move ", avil_moves_for_next_depth) #[1,4,05], 1,4,0,3
                        #print("current delth 1 local max", local_max)
                        min_function_scores = minvalue(alpha, beta, new_player, algorithm, depth_limit, copy_matrix, avil_moves_for_next_depth, row_values, two_pass, num_nodes, original_player, optimal_path, current_depth+1)   # how to do max of this?

                        if min_function_scores > local_max:
                            if current_depth == 1:
                                optimal_path.append(position)
                                optimal_path.append(the_matrix)
                                #print("get the best position kkkkkkk1",optimal_path )

                            local_max = min_function_scores

                        if (algorithm == "ALPHABETA"):
                            if local_max > alpha:
                                alpha = local_max

                            if beta <= alpha:
                                break

            if check_player_has_piece == 0: # if the next player has no piece to move, this is a terminal node
                this_scores = calculateScores(original_player, copy_matrix, row_values, this_moves)

                if this_scores > local_max:
                    if current_depth == 1:
                        optimal_path.append(position)
                        optimal_path.append(the_matrix)


                    local_max = this_scores

                #print("local max",local_max)
                if (algorithm == "ALPHABETA"):
                    if local_max > alpha:

                        alpha = local_max

                    if beta <= alpha:

                        break

        return local_max # only return local max when i finish tranverse for loop

def minvalue(alpha_para, beta_para, player, algorithm_para, depth_limit, matrix, moves, row_values, two_pass_para, num_nodes_para, original_player_para, optimal_path_para, current_depth_para):
    #global current_depth
    global max_scores
    global two_pass
    global num_nodes
    global original_player
    global optimal_path

    alpha = alpha_para
    beta = beta_para
    algorithm = algorithm_para
    optimal_path = optimal_path_para
    original_player = original_player_para
    num_nodes = num_nodes_para
    two_pass = two_pass_para
    #current_depth = current_depth + 1
    current_depth = current_depth_para
    #print("Min function current depth ", current_depth)
    local_min = float('inf')


    if (moves == []):  # pass, dont run make_run function

        copy_matrix = [['0'] * 8 for k in range(8)]
        # print("copy_matrix2222", copy_matrix2)
        for a in range(8):
            for b in range(8):
                copy_matrix[a][b] = matrix[a][b]

        num_nodes = num_nodes + 1
        #print("num node", num_nodes)
        two_pass = two_pass + 1


        if two_pass >= 2:  # If there are two continue pass, game over
            this_scores = calculateScores(original_player, copy_matrix, row_values, moves)
            if this_scores < local_min:

                local_min = this_scores

            return local_min

        #print("two pass value min value function is,", two_pass)

        if (player == "Circle"): new_player = "Star"
        if (player == "Star"): new_player = "Circle"

        # Check if new player has piece to play or not
        check_player_has_piece = 0
        for row in range(8):
            for column in range(8):
                if (new_player == "Star"):
                    if (copy_matrix[row][column][0] =="S"):
                        check_player_has_piece = check_player_has_piece+1
                if (new_player =="Circle"):
                    if (copy_matrix[row][column][0] =="C"):
                        check_player_has_piece = check_player_has_piece+1


        if check_player_has_piece > 0: # if the next player has piece to move, game continuous
            if (current_depth == int(depth_limit)):  # If we need to stop tranverse this node
                this_scores = calculateScores(original_player, copy_matrix, row_values, moves)
                if this_scores < local_min:
                    local_min = this_scores

            if (current_depth < int(depth_limit)):  # If we can go deeper

                avil_moves_for_next_depth = check_available_move(copy_matrix, new_player)  # Check the next move for the first moved piece   [1,4,0,5]         , 1,4,0,3
                #print(avil_moves_for_next_depth)
                max_function_scores = maxvalue(alpha, beta, new_player, algorithm, depth_limit, copy_matrix, avil_moves_for_next_depth,row_values, two_pass, num_nodes, original_player, optimal_path, current_depth+1)  # how to do max of this?# else:
                #print("ccccccccccc")
                if max_function_scores < local_min:


                    local_min = max_function_scores

        if check_player_has_piece == 0: # if next player can not move, game over, return
            this_scores = calculateScores(original_player, copy_matrix, row_values, moves)
            if this_scores < local_min:

                local_min = this_scores

        return local_min
    else:

        #print("testing in min fuunction moves",moves)
        for i in range(len(moves)):
                two_pass = 0
                #print("enter for loop", two_pass, player)
                num_nodes = num_nodes + 1

                copy_matrix = [['0'] * 8 for k in range(8)]

                for a in range(8):
                    for b in range(8):
                        copy_matrix[a][b] = matrix[a][b]

                the_matrix, position = move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), copy_matrix, player, num_nodes) #[]01 05   #0103

                #print("position in min function", position)


                # Swipe to next player's turn
                if (player == "Circle"): new_player = "Star"
                if (player == "Star"): new_player = "Circle"

                # Check if new player has piece to play or not
                check_player_has_piece = 0
                for row in range(8):
                    for column in range(8):
                        if (new_player == "Star"):
                            if (copy_matrix[row][column][0] == "S"):
                                check_player_has_piece = check_player_has_piece + 1
                        if (new_player == "Circle"):
                            if (copy_matrix[row][column][0] == "C"):
                                check_player_has_piece = check_player_has_piece + 1

                if check_player_has_piece > 0: # if the next player has piece to move, game continuous

                    if (current_depth == int(depth_limit)):
                        this_scores = calculateScores(original_player, copy_matrix, row_values, moves)
                        if this_scores < local_min:

                            local_min = this_scores

                        if (algorithm == "ALPHABETA"):
                            if local_min < beta:
                                beta = local_min

                            if beta <= alpha:
                                break

                    if (current_depth < int(depth_limit)):  # Check if we still need to tranverse to deeper depth
                        avil_moves_for_next_depth = check_available_move(copy_matrix,new_player)  # Check the next move for the first moved piece   [1,4,0,5]         , 1,4,0,3

                        #print("min function local min", local_min)
                        max_function_scores = maxvalue(alpha, beta, new_player, algorithm, depth_limit, copy_matrix, avil_moves_for_next_depth, row_values, two_pass, num_nodes, original_player, optimal_path, current_depth+1)  # how to do max of this?

                        if max_function_scores < local_min:
                            local_min = max_function_scores

                        if (algorithm == "ALPHABETA"):
                            if local_min < beta:
                                beta = local_min

                            if beta <= alpha:
                                break


                if check_player_has_piece == 0:
                    this_scores = calculateScores(original_player, copy_matrix, row_values, moves)
                    if this_scores < local_min:
                        #optimal_path.append(moves[i])
                        local_min = this_scores

                    if (algorithm == "ALPHABETA"):
                        if local_min < beta:
                            beta = local_min

                        if beta <= alpha:
                            break


        return local_min



def minimax(player, algorithm_para, depth_limit, matrix, row_values):
    #global current_depth
    current_depth = 0
    global two_pass
    two_pass = 0
    global num_nodes
    num_nodes = 1 # the initial number of node = 1 (the root)
    global original_player
    original_player = player
    global optimal_path
    optimal_path = []
    algorithm = algorithm_para

    beta = float('inf')
    alpha = float('-inf')


    moves = check_available_move(matrix, player)  # get the first available moves for player


    scores = maxvalue(alpha, beta, player, algorithm, depth_limit, matrix, moves, row_values, two_pass, num_nodes, original_player, optimal_path, current_depth+1)
    #print("final number of nodes", num_nodes)

    display_row_one = []
    display_row_one_store = []
    if optimal_path[0] != "pass":
        if (optimal_path[0][0][0] == 0):
            display_row_one.extend("H")
        if (optimal_path[0][0][0] == 1):
            display_row_one.extend("G")
        if (optimal_path[0][0][0] == 2):
            display_row_one.extend("F")
        if (optimal_path[0][0][0] == 3):
            display_row_one.extend("E")
        if (optimal_path[0][0][0] == 4):
            display_row_one.extend("D")
        if (optimal_path[0][0][0] == 5):
            display_row_one.extend("C")
        if (optimal_path[0][0][0] == 6):
            display_row_one.extend("B")
        if (optimal_path[0][0][0] == 7):
            display_row_one.extend("A")


        the_row_int = optimal_path[0][0][1] + 1
        the_row_str = str(the_row_int)
        display_row_one.extend(the_row_str)


        if (optimal_path[0][1][0] == 0):
            display_row_one.extend("H")
        if (optimal_path[0][1][0] == 1):
            display_row_one.extend("G")
        if (optimal_path[0][1][0] == 2):
            display_row_one.extend("F")
        if (optimal_path[0][1][0] == 3):
            display_row_one.extend("E")
        if (optimal_path[0][1][0] == 4):
            display_row_one.extend("D")
        if (optimal_path[0][1][0] == 5):
            display_row_one.extend("C")
        if (optimal_path[0][1][0] == 6):
            display_row_one.extend("B")
        if (optimal_path[0][1][0] == 7):
            display_row_one.extend("A")

        the_row_int_two = optimal_path[0][1][1] + 1
        the_row_str_two = str(the_row_int_two)
        display_row_one.extend(the_row_str_two)

        display_row_one_store.append(display_row_one[0] + display_row_one[1] + "-"+ display_row_one[2] + display_row_one[3])


    direction = ''
    if optimal_path[0] != "pass":
        direction = display_row_one_store[0]

    if optimal_path[0] == "pass":
        direction = optimal_path[0]


    #if optimal_path[0] != "pass":
        #print("testing: optimal path", optimal_path[0], optimal_path[0][0][0], optimal_path[0][0][1], optimal_path[0][1][0], optimal_path[0][1][1], optimal_path[1])

    #if optimal_path[0] == "pass":
        #print("optimal path 0", optimal_path[0], optimal_path[1])

    this_moves=[]
    next_move_scores = calculateScores(player, optimal_path[1], row_values, this_moves)

    return direction, next_move_scores, scores, num_nodes



def calculateScores(player, this_matrix, row_values, moves): #moves may not be necesary to calculate scores
    global max_scores
    max_scores = 0
    factor = 7
    this_scores = 0 # this scores = star scores - circle scores , or the other way around
    star_scores = 0
    circle_scores = 0
    for row in range(8):
        for column in range(8):
            if (this_matrix[row][column] == "0"): # For all 0
                star_scores = star_scores + 0
                circle_scores = circle_scores + 0

            if (row == 0 and this_matrix[row][column] != "0"): # To calculate points for # of pieces in row 0 for star

                num_piece_thisbox = this_matrix[row][column]
                if (this_matrix[row][column][0] == "S"):

                    num_piece_thisbox = num_piece_thisbox.replace('S', '') # replace S
                    int_num_piece_thisbox = int(num_piece_thisbox)
                    star_scores = star_scores + int_num_piece_thisbox * (int(row_values[factor - row]))







            if (row == 7 and this_matrix[row][column] != "0"): # To calculate points for # of pieces in the row 7 for circle

                num_piece_thisbox = this_matrix[row][column]

                if (this_matrix[row][column][0] == "C"):
                    num_piece_thisbox = num_piece_thisbox.replace('C', '')  # replace C
                    int_num_piece_thisbox = int(num_piece_thisbox)
                    circle_scores = circle_scores + int_num_piece_thisbox * (int(row_values[row]))

            if (row != 0 and this_matrix[row][column] != "0"): # For all S1 other than top and bottom row
                #num_piece_thisbox = this_matrix[row][column]
                if (this_matrix[row][column] == "S1"):
                    star_scores = star_scores + int(row_values[factor - row])


            if (row!= 7 and this_matrix[row][column] != "0"): # For all C1 other than top and bottom row
                #num_piece_thisbox = this_matrix[row][column]
                if (this_matrix[row][column] == "C1"):
                    circle_scores = circle_scores + int(row_values[row])

    if (player == "Circle"):
        this_scores = circle_scores - star_scores

    if (player == "Star"):
        this_scores = star_scores - circle_scores


    #print("calculate the scores",this_scores, star_scores, circle_scores)

    if (this_scores > max_scores):  # not that here does not compare if the scores are the same
        max_scores = this_scores

    return this_scores
##================================
## Implemmentation Main
def main():

    text_file = open("input.txt", "r")

    player = text_file.readline().replace('\n', '').replace('\r', '')
    algorithm = text_file.readline().replace('\n', '').replace('\r', '')
    depth_limit = text_file.readline().replace('\n', '').replace('\r', '')

    #print(player)
    #print(algorithm)
    #print(depth_limit)

    matrix_with_rowvalues = []
    matrix = []
    for eachLine in text_file:
          line = [str(x) for x in eachLine.replace('\n', '').replace('\r', '').split(',')]
          matrix_with_rowvalues.append(line)

    row_values = matrix_with_rowvalues[8]
    for row in range(0,8):
        matrix.append(matrix_with_rowvalues[row])


    #print(matrix)
    #print(row_values)


    local_first_move, local_first_move_scores, local_scores, local_num_nodes = minimax(player, algorithm, depth_limit, matrix, row_values)
    #print("main final score",local_first_move ,local_first_move_scores, local_scores, local_num_nodes)


    output_file = open("output.txt", "w")

    output_file.write(local_first_move + "\n" + str(local_first_move_scores) + "\n" + str(local_scores) + "\n" + str(local_num_nodes))

    output_file.close()

    text_file.close()


main()


