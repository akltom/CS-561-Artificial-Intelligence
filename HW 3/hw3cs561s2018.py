import numpy as np
import Queue


def alignWallTransPosi():
    global row
    global column
    global terminal_position
    global terminal_number
    global wall_position
    global wall_number

    for i in range(0, terminal_number):
        curr_value = terminal_position[i]
        x_value = curr_value[0]
        temp_x = row - x_value

        y_value = curr_value[1]
        temp_y = y_value - 1
        temp_location = [temp_x, temp_y]

        terminal_position[i] = temp_location

    for j in range(0, wall_number):
        curr_value_two = wall_position[j]
        x_value_two = curr_value_two[0]
        wall_x = row - x_value_two

        y_value_two = curr_value_two[1]
        wall_y = y_value_two - 1
        wall_location = [wall_x, wall_y]

        wall_position[j] = wall_location

    #print("wall pos", "termi pos", wall_position, terminal_position)

    for k in range(0, row):
        for l in range(0, column):
            for ter in range(0, terminal_number):  # If there is terminal, assign "Exit" in grid
                if (terminal_position[ter] == [k, l]):
                    grid_world[k][l] = "Exit"
            for wal in range(0, wall_number):
                if (wall_position[wal] == [k, l]):
                    grid_world[k][l] = "None"


def generateGrid():
    global row
    global column
    global grid_world
    global terminal_number
    global terminal_position
    global wall_number
    global wall_position
    grid_world = []

    for i in range(0, row):  # Max row is 1000
        grid_world.append([])
        for j in range(0, column):  # Max column is 1000
            grid_world[i].append('0')  # Set the original utility value to string 0


def initializeGridUtility():
    global row
    global column
    global terminal_number
    global terminal_position
    global terminal_pos_reward
    global grid_world_utility
    global last_grid_world_utility

    global largest_terminal_position
    global largest_terminal_utility

    global grid_world_visit

    grid_world_utility = []
    last_grid_world_utility = []

    largest_terminal_utility = 0
    largest_terminal_position = []
    grid_world_visit = []

    for i in range(0, row):  # Max row is 1000
        grid_world_utility.append([])
        last_grid_world_utility.append([])
        grid_world_visit.append([])
        for j in range(0, column):  # Max column is 1000
            grid_world_utility[i].append(0)  # Set the original utility value to value 0
            last_grid_world_utility[i].append(0)
            grid_world_visit[i].append("F") # Initially, set all cells haven't visit before
            for ter in range(0, terminal_number): # Initialize the utility value of utility matrix
                if (terminal_position[ter] == [i, j]):
                    grid_world_utility[i][j] = terminal_pos_reward[ter]
                    last_grid_world_utility[i][j] = terminal_pos_reward[ter]


    for k in range(0, terminal_number):
        if (terminal_pos_reward[k] > largest_terminal_utility):
            largest_terminal_utility = terminal_pos_reward[k]
            largest_terminal_position = terminal_position[k]

    #print("largest terminal postion", largest_terminal_position)
    #print("largest terminal reward", largest_terminal_utility)



    # grid_world[0][2] = 1000
    # print(grid_world[0][2])


def valueIteration(curr_row, curr_col):
    global row
    global column
    global grid_world
    global grid_world_utility
    global wall_number
    global wall_position
    global terminal_number
    global terminal_position
    global terminal_pos_reward
    global trans_walk
    global trans_run
    global reward_walk
    global reward_run
    global discount_factor

    curr_max_utility = float("-inf")  # U

    utility_this_action = 0  # U'

    # print("value iteration starts")  # Use value iteration function

    for i in range(0, 8):  # 4 run actions and 4 walk actions

        if (i == 0):  # Perform "Run Right"

            utility_this_action = 0.00000

            if (curr_col == (column - 1) or curr_col == (
                    column - 2)):  # Curr col is in the last or second last column, run right will hit outside
                utility_this_action = utility_this_action + trans_run * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + trans_run * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 2] == "Exit"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]
                    elif (grid_world[curr_row][curr_col + 2] == "None"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units right is non terminal state
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]

            # Go Up
            if (curr_row == 0 or curr_row == 1):  # Curr row = 0 or 1, mean that run up will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell
                    if (grid_world[curr_row - 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]
                    elif (grid_world[curr_row - 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units up is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]

            # Go Down
            if (curr_row == (row - 1) or curr_row == (
                    row - 2)):  # Curr row = last row or second last row, run down will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit down, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell
                    if (grid_world[curr_row + 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]
                    elif (grid_world[curr_row + 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]

            utility_this_action = utility_this_action + reward_run

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Run Right"

        if (i == 1):  # Perform "Run Left"

            utility_this_action = 0

            if (curr_col == 0 or curr_col == 1):  # Curr col = 0 or 1, run left will hit outside
                utility_this_action = utility_this_action + trans_run * discount_factor * grid_world_utility[curr_row][
                    curr_col]

            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + trans_run * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col - 2] == "Exit"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]
                    elif (grid_world[curr_row][curr_col - 2] == "None"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]

            # Go Up
            if (curr_row == 0 or curr_row == 1):  # Curr row = 0 or 1, mean that run up will absolutely hit the wall
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row - 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]
                    elif (grid_world[curr_row - 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units up is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]

            # Go Down
            if (curr_row == (row - 1) or curr_row == (
                    row - 2)):  # Curr row = last row or second last row, mean that run down will absolutely hit the wall
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row + 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]
                    elif (grid_world[curr_row + 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]

            utility_this_action = utility_this_action + reward_run

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Run Left"

        if (i == 2):  # Perform "Run Down"

            utility_this_action = 0

            if (curr_row == (row - 1) or curr_row == (
                    row - 2)):  # Curr row = last row or second last row, mean that run down will absolutely hit the wall
                utility_this_action = utility_this_action + trans_run * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit down, non terminal state
                    utility_this_action = utility_this_action + trans_run * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row + 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]
                    elif (grid_world[curr_row + 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row + 2][curr_col]

            # Go Right
            if (curr_col == (column - 1) or curr_col == (
                    column - 2)):  # Curr col is in the last or second last column, run right will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 2] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]
                    elif (grid_world[curr_row][curr_col + 2] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units right is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]

            # Go Left
            if (curr_col == 0 or curr_col == 1):  # Curr col = 0 or 1, run left will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row][curr_col - 2] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]
                    elif (grid_world[curr_row][curr_col - 2] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]

            utility_this_action = utility_this_action + reward_run

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Run Down"

        if (i == 3):  # Perform "Run Up"

            utility_this_action = 0

            if (curr_row == 0 or curr_row == 1):  # Curr row = 0 or 1, mean that run up will hit the wall
                utility_this_action = utility_this_action + trans_run * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + trans_run * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row - 2][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]
                    elif (grid_world[curr_row - 2][curr_col] == "None"):
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_run * discount_factor * \
                                              grid_world_utility[curr_row - 2][curr_col]

            # Go Right
            if (curr_col == (column - 1) or curr_col == (
                    column - 2)):  # Curr col is in the last or second last column, run right will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 2] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]
                    elif (grid_world[curr_row][curr_col + 2] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units right is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 2]

            # Go Left
            if (curr_col == 0 or curr_col == 1):  # Curr col = 0 or 1, run left will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row][curr_col - 2] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]
                    elif (grid_world[curr_row][curr_col - 2] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_run) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 2]

            utility_this_action = utility_this_action + reward_run

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Run Up"

        if (i == 4):  # Walk Right

            utility_this_action = 0

            if (curr_col == (column - 1)):  # Curr col is in the last column, run right will hit outside
                utility_this_action = utility_this_action + trans_walk * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 1] == "Exit"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]
                    elif (grid_world[curr_row][curr_col + 1] == "None"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 1 units right is non terminal state
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]

            # Go Up
            if (curr_row == 0):  # Curr row = 0 or 1, mean that run up will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell
                    if (grid_world[curr_row - 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]
                    elif (grid_world[curr_row - 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units up is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]

            # Go Down
            if (curr_row == (row - 1)):  # Curr row = last row or second last row, run down will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit down, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell
                    if (grid_world[curr_row + 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]
                    elif (grid_world[curr_row + 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]

            utility_this_action = utility_this_action + reward_walk

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Walk Right"

        if (i == 5):  # Walk Left

            utility_this_action = 0

            if (curr_col == 0):  # Curr col = 0, run left will hit outside
                utility_this_action = utility_this_action + trans_walk * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col - 1] == "Exit"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]
                    elif (grid_world[curr_row][curr_col - 1] == "None"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]

            # Go Up
            if (curr_row == 0):  # Curr row = 0 or 1, mean that run up will absolutely hit the wall
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row - 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]
                    elif (grid_world[curr_row - 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units up is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]

            # Go Down
            if (curr_row == (
                    row - 1)):  # Curr row = last row or second last row, mean that run down will absolutely hit the wall
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row + 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]
                    elif (grid_world[curr_row + 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]

            utility_this_action = utility_this_action + reward_walk

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Walk Left"

        if (i == 6):  # Walk Down

            utility_this_action = 0

            if (curr_row == (row - 1)):  # Curr row = last row, mean that run down will absolutely hit the wall
                utility_this_action = utility_this_action + trans_walk * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:  # Mean run down may or may not hit the wall
                if (grid_world[curr_row + 1][curr_col] == "None"):  # If a wall is 1 unit down, non terminal state
                    utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row + 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]
                    elif (grid_world[curr_row + 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row + 1][curr_col]

            # Go Right
            if (curr_col == (column - 1)):  # Curr col is in the last column, run right will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 1] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]
                    elif (grid_world[curr_row][curr_col + 1] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units right is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]

            # Go Left
            if (curr_col == 0):  # Curr col = 0 or 1, run left will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row][curr_col - 1] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]
                    elif (grid_world[curr_row][curr_col - 1] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]

            utility_this_action = utility_this_action + reward_walk

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Walk Down"

        if (i == 7):  # Walk Up

            utility_this_action = 0

            if (curr_row == 0):  # Curr row = 0 or 1, mean that run up will hit the wall
                utility_this_action = utility_this_action + trans_walk * discount_factor * grid_world_utility[curr_row][
                    curr_col]
            else:  # Mean run up may or may not hit the wall
                if (grid_world[curr_row - 1][curr_col] == "None"):  # If a wall is 1 unit up, non terminal state
                    utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row - 1][curr_col] == "Exit"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]
                    elif (grid_world[curr_row - 1][curr_col] == "None"):
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units down is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + trans_walk * discount_factor * \
                                              grid_world_utility[curr_row - 1][curr_col]

            # Go Right
            if (curr_col == (column - 1)):  # Curr col is in the last column, run right will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col + 1] == "None"):  # If a wall is 1 unit right, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:  # If there is no wall on the middle cell, or can be outside of grid
                    if (grid_world[curr_row][curr_col + 1] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]
                    elif (grid_world[curr_row][curr_col + 1] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units right is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col + 1]

            # Go Left
            if (curr_col == 0):  # Curr col = 0 or 1, run left will hit outside
                utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                      grid_world_utility[curr_row][curr_col]
            else:
                if (grid_world[curr_row][curr_col - 1] == "None"):  # If a wall is 1 unit left, non terminal state
                    utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                          grid_world_utility[curr_row][curr_col]
                else:
                    if (grid_world[curr_row][curr_col - 1] == "Exit"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]
                    elif (grid_world[curr_row][curr_col - 1] == "None"):
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col]
                    else:  # If 2 units left is non terminal state, or outside the grid size(treat as wall)
                        utility_this_action = utility_this_action + 0.5 * (1 - trans_walk) * discount_factor * \
                                              grid_world_utility[curr_row][curr_col - 1]

            utility_this_action = utility_this_action + reward_walk

            if (utility_this_action >= curr_max_utility):
                curr_max_utility = utility_this_action
                grid_world[curr_row][curr_col] = "Walk Up"

    grid_world_utility[curr_row][curr_col] = curr_max_utility


def loopAllCells():
    global row
    global column
    global grid_world
    global grid_world_utility
    global last_grid_world_utility

    global largest_terminal_position
    global largest_terminal_utility
    global grid_world_visit

    flat = False

    counter_correct = 0
    run_time_counter = 0

    # q = Queue.Queue() # First In, first out BFS;
    # for zz in range(5):
    #     q.put(zz)
    #
    # while not q.empty():
    #     print q.get()
    #
    # qq = Queue.LifoQueue() # Lifoqueue: First in last out DFS
    #
    # for yy in range(5):
    #     qq.put(yy)
    #
    # while not qq.empty():
    #     print qq.get()

    adj_queue_1 = Queue.Queue() # Temp queue to store cells for construct queue 2, eventually go to 0
    adj_queue_2 = Queue.Queue() # Store all the cells in order permanently

    cell_array = []

    while (flat == False):
        # Set a checking here to check if queue2.size == row*column, then don't do the queue if and else below
        if (largest_terminal_utility == 0):  # Meaning there is no any terminal states, loop starts from left top
            for i in range(0, row):  # Loop through all cells
                for j in range(0, column):
                    if (grid_world[i][j] != 'Exit' and grid_world[i][
                        j] != 'None'):  # If grid_world[i][j] != "Exit" or "None", run the function to keep getting best action
                        last_grid_world_utility[i][j] = grid_world_utility[i][j]
                        valueIteration(i, j)
        else:  # If there are at least one terminal cell
            if (run_time_counter == 0): # First time to run the program
                ter_x = largest_terminal_position[0]
                ter_y = largest_terminal_position[1]

                # Mark down the terminal state itself
                adj_queue_1.put([ter_x, ter_y])
                adj_queue_2.put([ter_x, ter_y])
                grid_world_visit[ter_x][ter_y] = "T"

                for adj in range(0, 8): # Add the first 8 possible actions into queue
                    if (adj == 7):  # Walk Up
                        if (ter_x != 0):  # If not first row
                            if (grid_world_visit[ter_x-1][ter_y] == "F" ): # If the upper cell is never visited before
                                adj_queue_1.put([ter_x - 1, ter_y])
                                adj_queue_2.put([ter_x - 1, ter_y])
                                grid_world_visit[ter_x-1][ter_y] = "T"
                    if (adj == 6):  # Walk Down
                        if (ter_x != row -1):  # Not in last row
                            if (grid_world_visit[ter_x + 1][ter_y] == "F"):
                                adj_queue_1.put([ter_x+1,ter_y])
                                adj_queue_2.put([ter_x+1,ter_y])
                                grid_world_visit[ter_x +1][ter_y] = "T"
                    if (adj == 5): # Walk Left
                        if (ter_y != 0):  # If current column is not 0
                            if (grid_world_visit[ter_x][ter_y-1] == "F"):
                                adj_queue_1.put([ter_x,ter_y-1])
                                adj_queue_2.put([ter_x,ter_y-1])
                                grid_world_visit[ter_x][ter_y-1] = "T"
                    if (adj == 4): # Walk Right
                        if (ter_y != column -1):# Not in last column
                            if (grid_world_visit[ter_x ][ter_y+1] == "F"):
                                adj_queue_1.put([ter_x, ter_y + 1])
                                adj_queue_2.put([ter_x, ter_y + 1])
                                grid_world_visit[ter_x ][ter_y+1] = "T"
                    if (adj == 3): # Run Up
                        if (ter_x != 0 and ter_x!= 1):# Not in first row and second row
                            if (grid_world_visit[ter_x - 2][ter_y] == "F"):
                                adj_queue_1.put([ter_x-2, ter_y])
                                adj_queue_2.put([ter_x-2, ter_y])
                                grid_world_visit[ter_x - 2][ter_y] = "T"
                    if (adj == 2): # Run Down
                        if (ter_x != row -1 and ter_x!=row-2):# Not in last and second last row
                            if (grid_world_visit[ter_x +2][ter_y] == "F"):
                                adj_queue_1.put([ter_x+2, ter_y])
                                adj_queue_2.put([ter_x+2, ter_y])
                                grid_world_visit[ter_x +2][ter_y] = "T"
                    if (adj == 1): # Run Left
                        if (ter_y != 0 and ter_y!=1):# Not in first and second column
                            if (grid_world_visit[ter_x][ter_y-2] == "F"):
                                adj_queue_1.put([ter_x, ter_y-2])
                                adj_queue_2.put([ter_x, ter_y-2])
                                grid_world_visit[ter_x][ter_y-2] = "T"
                    if (adj == 0): # Run Right
                        if (ter_y != column -1 and ter_y!=column-2):# Not in last and second last column
                            if (grid_world_visit[ter_x][ter_y+2] == "F"):
                                adj_queue_1.put([ter_x, ter_y+2])
                                adj_queue_2.put([ter_x, ter_y+2])
                                grid_world_visit[ter_x][ter_y+2] = "T"
                # No need to check for other terminals, since we have something in queue1 and 2 above for sure
                aaa=adj_queue_2.qsize() # here size = 7
                #print("aa",aaa)
                adj_queue_1.get()
                while (adj_queue_2.qsize() != (row * column)): # Keep looping until we loop all the possible cells
                    next_cell = adj_queue_1.get() # Get the first cell of the queue 1
                    termin_x = next_cell[0]
                    termin_y = next_cell[1]

                    for ww in range(0, 8):
                        if (ww == 7):  # Walk Up
                            if (termin_x != 0):  # If not first row
                                if (grid_world_visit[termin_x - 1][termin_y] == "F"):
                                    adj_queue_1.put([termin_x - 1, termin_y])
                                    adj_queue_2.put([termin_x - 1, termin_y])
                                    grid_world_visit[termin_x - 1][termin_y] = "T"
                        if (ww == 6):  # Walk Down
                            if (termin_x != row - 1):  # Not in last row
                                if (grid_world_visit[termin_x + 1][termin_y] == "F"):
                                    adj_queue_1.put([termin_x + 1, termin_y])
                                    adj_queue_2.put([termin_x + 1, termin_y])
                                    grid_world_visit[termin_x + 1][termin_y] = "T"
                        if (ww == 5):  # Walk Left
                            if (termin_y != 0):  # If current column is not 0
                                if (grid_world_visit[termin_x][termin_y-1] == "F"):
                                    adj_queue_1.put([termin_x, termin_y - 1])
                                    adj_queue_2.put([termin_x, termin_y - 1])
                                    grid_world_visit[termin_x][termin_y-1] = "T"
                        if (ww == 4):  # Walk Right
                            if (termin_y != column - 1):  # Not in last column
                                if (grid_world_visit[termin_x][termin_y+1] == "F"):
                                    adj_queue_1.put([termin_x, termin_y + 1])
                                    adj_queue_2.put([termin_x, termin_y + 1])
                                    grid_world_visit[termin_x][termin_y+1] = "T"
                        if (ww == 3):  # Run Up
                            if (termin_x != 0 and termin_x != 1):  # Not in first row and second row
                                if (grid_world_visit[termin_x -2][termin_y] == "F"):
                                    adj_queue_1.put([termin_x - 2, termin_y])
                                    adj_queue_2.put([termin_x - 2, termin_y])
                                    grid_world_visit[termin_x - 2][termin_y] = "T"
                        if (ww == 2):  # Run Down
                            if (termin_x != row - 1 and termin_x != row - 2):  # Not in last and second last row
                                if (grid_world_visit[termin_x+2][termin_y] == "F"):
                                    adj_queue_1.put([termin_x + 2, termin_y])
                                    adj_queue_2.put([termin_x + 2, termin_y])
                                    grid_world_visit[termin_x + 2][termin_y] = "T"
                        if (ww == 1):  # Run Left
                            if (termin_y != 0 and termin_y != 1):  # Not in first and second column
                                if (grid_world_visit[termin_x][termin_y-2] == "F"):
                                    adj_queue_1.put([termin_x, termin_y - 2])
                                    adj_queue_2.put([termin_x, termin_y - 2])
                                    grid_world_visit[termin_x ][termin_y-2] = "T"
                        if (ww == 0):  # Run Right
                            if (termin_y != column - 1 and termin_y != column - 2):  # Not in last and second last column
                                if (grid_world_visit[termin_x][termin_y+2] == "F"):
                                    adj_queue_1.put([termin_x, termin_y + 2])
                                    adj_queue_2.put([termin_x, termin_y + 2])
                                    grid_world_visit[termin_x ][termin_y+2] = "T"

                # End of while loop

                for cell in range (0, adj_queue_2.qsize()): # For each cell in the queue
                    next_cell_Two = adj_queue_2.get()
                    cell_array.append(next_cell_Two)
                    cell_x = next_cell_Two[0]
                    cell_y = next_cell_Two[1]
                    if (grid_world[cell_x][cell_y] != 'Exit' and grid_world[cell_x][cell_y] != 'None'):  # If grid_world[x][y] != "Exit" or "None", run the function to get best action
                        valueIteration(cell_x, cell_y)

            # End of first time to run the program
            else: # Not first time to run the program
                # copy a queue 4 temp to run the for loop above
                for pp in range (0, len(cell_array)): # For each cell in the queue
                    next_cell_Three = cell_array[pp]
                    cell_x_Two = next_cell_Three[0]
                    cell_y_Two = next_cell_Three[1]

                    if (grid_world[cell_x_Two][cell_y_Two] != 'Exit' and grid_world[cell_x_Two][cell_y_Two] != 'None'):  # If grid_world[x][y] != "Exit" or "None", run the function to get best action
                        last_grid_world_utility[cell_x_Two][cell_y_Two] = grid_world_utility[cell_x_Two][cell_y_Two]
                        valueIteration(cell_x_Two, cell_y_Two)
        #End of more than one terminal cell

        for a in range(0, row):  # Compare the cells from current run and previous run
            for b in range(0, column):
                if (last_grid_world_utility[a][b] == grid_world_utility[a][b]):
                    counter_correct = counter_correct + 1

        if (counter_correct == (row * column)):  # If all cells are equal, quit the while loop

            flat = True

        counter_correct = 0
        run_time_counter = run_time_counter + 1

        # for ppppp in range (0, row):
        #     for sssss in range (0, column):
        #         if (run_time_counter==0):
        #             print("utility matrix", grid_world_utility[ppppp][sssss])
        #     if (run_time_counter==0):
        #         print("\n")

    #print("finish looping all cells")


global row
global column
global wall_number
global wall_position
global terminal_number
global terminal_position
global terminal_pos_reward
global trans_walk
global trans_run
global reward_walk
global reward_run
global discount_factor
global grid_world
global grid_world_utility
global last_grid_world_utility
global largest_terminal_utility
global largest_terminal_position
global grid_world_visit


def main():
    global row
    global column
    global wall_number
    global wall_position
    global terminal_number
    global terminal_position
    global terminal_pos_reward
    global trans_walk
    global trans_run
    global reward_walk
    global reward_run
    global discount_factor


    text_file = open("input.txt", "r")

    first_line = text_file.readline().replace('\n', '').replace('\r', '').split(',')

    row = int(first_line[0])
    column = int(first_line[1])
    #print(row)
    #print(column)
    wall_number = int(text_file.readline().replace('\n', '').replace('\r', ''))
    #print(wall_number)

    wall_position = []  # Create a array for storing wall position

    for each_wall_loc in range(wall_number):
        wall_pos_string = text_file.readline().replace('\n', '').replace('\r', '').split(',')
        wall_row = int(wall_pos_string[0])
        wall_column = int(wall_pos_string[1])
        wall_position.append([wall_row, wall_column])
        #print("wall position", wall_position[each_wall_loc])

    terminal_number = int(text_file.readline().replace('\n', '').replace('\r', ''))
    #print(terminal_number)

    terminal_position = []
    terminal_pos_reward = []

    for each_terminal_loc in range(terminal_number):
        n = 2
        terminal_pos_string = text_file.readline().replace('\n', '').replace('\r', '').split(',')
        ','.join(terminal_pos_string[:n]), ','.join(terminal_pos_string[n:])

        terminal_row = int(terminal_pos_string[0])
        terminal_column = int(terminal_pos_string[1])
        terminal_reward = float(terminal_pos_string[2])

        terminal_position.append([terminal_row, terminal_column])
        terminal_pos_reward.append(terminal_reward)
        #print("terminal position", terminal_position[each_terminal_loc])
        #print(terminal_pos_reward[each_terminal_loc])

    transition_model_string = text_file.readline().replace('\n', '').replace('\r', '').split(',')
    trans_walk = float(transition_model_string[0])
    trans_run = float(transition_model_string[1])
    #print(trans_walk, trans_run)

    reward_string = text_file.readline().replace('\n', '').replace('\r', '').split(',')
    reward_walk = float(reward_string[0])
    reward_run = float(reward_string[1])
    #print(reward_walk, reward_run)

    discount_factor_string = text_file.readline().replace('\n', '').replace('\r', '')
    discount_factor = float(discount_factor_string)
    #print(discount_factor)

    generateGrid()
    alignWallTransPosi()
    initializeGridUtility()

    loopAllCells()

    output_file = open("output.txt", "w")

    for each_row in range(0, row):
        for each_column in range(0, column):
            curr_val = grid_world[each_row][each_column]
            output_file.write(curr_val)
            if (each_column != column - 1):
                output_file.write(",")
        output_file.write("\n")

    output_file.close()

    text_file.close()


main()