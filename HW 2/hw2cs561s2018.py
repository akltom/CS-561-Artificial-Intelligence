
class Team:
    def __init__(self, name, pot, continent):
        self.name = name
        self.pot = pot
        self.continent = continent
        self.AFC = 0 # Asia
        self.CAF = 0 # Africa
        self.CONCACAF = 0 # North and  Central America
        self.CONMEBOL = 0 # South America
        self.OFC = 0 # Oceania
        self.UEFA = 0 # Europe

    def pot_update(self, pot):
        self.pot = pot

    def continent_update(self):
        self. UEFA += 1
    def printDetail(self):
        print(self.name)
        print(self.pot)
        print(self.continent)


# Maximum teams are 40



def backtrackingsearch(team_array, team_pot_array, team_continent_array):

    global numb_pot
    global numb_group
    global numb_team
    # team_array_left = copy.deepcopy(team_array) # An array to check the ending condition
    # And check the groups that are left
    # for each assign, we delete one group a time,





    for i in range(0, int(numb_pot)):
        curr_pot = i+ 1
        num_pot_element = team_pot_array.count(curr_pot)
        # print("ggg", num_pot_element, curr_pot, int(numb_group))
        if (num_pot_element > int(
                numb_group)):  # If in any pots, number of teams in that pot are more than group numbers
            return "No"  # return none, don't run the backtracking function

    continent_array = ["UEFA", "AFC", "CAF", "CONCACAF", "CONMEBOL", "OFC"]
    for v in continent_array:

        if (v== "UEFA" and team_continent_array.count(v) > int(numb_group)*2):

            return "No"
        if (v!="UEFA" and team_continent_array.count(v) > int(numb_group)):

            return "No"





    return backtracking(team_array, team_pot_array, team_continent_array)


def backtracking(team_array, team_pot_array, team_continent_array):

    global final_array
    global numb_group
    global numb_pot
    global pot
    global numb_team
    global count

    final_array = [[] for i in range(0, int(numb_group))]

    #print("final array test", final_array)
    current_pot = 0


    pot = [[] for i in range(int(numb_pot))]
    for a in range(0, int(numb_team)):
        count = {}
        pot[team_pot_array[a]-1].append(team_array[a])

    #print("pot", pot)

    # for ea_group in range(0, int(numb_group)): # Transverse all the pots
    for i in range(0, int(numb_group)):
        count = {}
        completed_group = dfs(team_array, team_pot_array, team_continent_array, i,  current_pot)
        #print("finish one group", final_array)
        for country in final_array[i]:

            team_used_ornot_map[country] = "Used"

    return completed_group


def dfs(teamarray, team_pot_array, team_continent_array, number_thisgroup, currentpot):
    global numb_group
    global numb_pot
    global team_continent_map
    global team_pot_map
    global numb_team
    global team_used_ornot_map
    global final_array
    global pot
    global count


    if (currentpot == int(numb_pot)):




        count_num_continent = {}
        for allteam in teamarray:  # Increase the number of team
            if count_num_continent.get(team_continent_map[allteam]):
                count_num_continent[team_continent_map[allteam]] += 1
            else:
                count_num_continent[team_continent_map[allteam]] = 1

        for allteam2 in final_array:
            for eateam in allteam2:
                count_num_continent[team_continent_map[eateam]] -= 1

        count_num_pot = {}  # increase the
        for allteam3 in teamarray:
            if count_num_pot.get(team_pot_map[allteam3]):
                count_num_pot[team_pot_map[allteam3]] += 1
            else:
                count_num_pot[team_pot_map[allteam3]] = 1

        for allteam4 in final_array:
            for eateam2 in allteam4:
                count_num_pot[team_pot_map[eateam2]] -= 1

        for p in count_num_continent:
            if (p =="UEFA"):
                if(count_num_continent[p] > (int(numb_group) - number_thisgroup - 1)*2):
                    return False
            elif (count_num_continent[p] > int(numb_group)-number_thisgroup-1):
                return False
        for n in count_num_pot:
            if (count_num_pot[n] > int(numb_group)-number_thisgroup-1):
                return False
        return True



    #print("dddd", len(pot[currentpot]))
    for eachteam in range (0, len(pot[currentpot])):



        team = pot[currentpot][eachteam]

        if (team_used_ornot_map[team] == "Used"):
            continue

        final_array[number_thisgroup].append(team)
        if count.get(team_continent_map[team]):
            count[team_continent_map[team]] += 1
        else:
            count[team_continent_map[team]] = 1

        flag = False
        if (team_continent_map[team]=='UEFA' and count['UEFA']<=2) or count[team_continent_map[team]]<=1:
            flag = dfs(teamarray, team_pot_array, team_continent_array, number_thisgroup, currentpot+1)
        if flag:
            return True
        count[team_continent_map[team]] -= 1

        final_array[number_thisgroup]= final_array[number_thisgroup][:-1]



    flag = dfs(teamarray, team_pot_array, team_continent_array, number_thisgroup, currentpot + 1)
    if flag:
        return True
    # print("count", count)

    return False
    # while True:
    #     flag = False
    #





# backforce , use two for loop, first for is for all group, second for is for all pots


#  return True


global numb_group
global numb_pot

global numb_team
global team_continent_map
global team_pot_map
global team_used_ornot_map
global final_array
global pot
global count
def main():
    text_file = open("input.txt", "r")

    global numb_group
    global numb_pot

    global numb_team
    global team_continent_map
    global team_pot_map
    global team_used_ornot_map
    global final_array

    group_count = text_file.readline().replace('\n', '').replace('\r', '')
    #print("The group count is", group_count)
    numb_group = group_count

    pot_count = text_file.readline().replace('\n', '').replace('\r', '')
    #print("The pot count is", pot_count)
    numb_pot = pot_count

    line_counter = 0
    pot_ranking_array = []
    continent_array = []
    pot_ranking_array_final = []
    continent_array_final = []
    temp2=[]

    for eachLine in text_file:
        line_counter += 1
        if (line_counter <= int(pot_count)):
            pot_ranking_array.append(eachLine)
        else:
            continent_array.append(eachLine)

    for x in range(0, int(pot_count)):
        temp_ranking_array = (pot_ranking_array[x].replace('\n', '').replace('\r', '').split(','))
        # print(temp_ranking_array)
        pot_ranking_array_final.append(temp_ranking_array)

    for y in range(0, 6):
        temp_continent_array = (continent_array[y].replace('\n', '').replace('\r', '').split(','))
        temp2.append(temp_continent_array)

        context = temp2[y][0].split(":")


        if (context[0] == "AFC"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)

        if (context[0] == "CAF"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)

        if (context[0] == "OFC"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)

        if (context[0] == "CONCACAF"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)
        if (context[0] == "CONMEBOL"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)
        if (context[0] == "UEFA"):
            temp_array = []
            for p in range(0, len(context)):
                temp_array.append(context[p])

            if (len(temp_continent_array) > 1):  # If there are more than 1 team
                for u in range(1, len(temp_continent_array)):
                    temp_array.append(temp_continent_array[u])
            continent_array_final.append(temp_array)

        context = []

    #print("final_test", continent_array_final)

    # print("pot ranking array reword", pot_ranking_array_final)

    # print("continent array reword", continent_array_final)

    curr_pot = 0  # Current pot index
    num_teams = 0
    team_array = []
    team_pot_array = []

    for num_pot in range(0, int(pot_count)):
        num_teams_curr_pot = len(pot_ranking_array_final[curr_pot])  # Number of teams in the current pot
        num_teams += num_teams_curr_pot

        for each_team_curr_pot in range(0, num_teams_curr_pot):  # For each team in the current pot
            team_array.append(pot_ranking_array_final[curr_pot][each_team_curr_pot])
            team_pot_array.append(curr_pot + 1)

        curr_pot = curr_pot + 1

    numb_team = num_teams
    #print("num of team", num_teams)
    #print("total array", team_array)
    #print("team pot array", team_pot_array)

    afc_array = []
    caf_array = []
    ofc_array = []
    concacaf_array = []
    conmebol_array = []
    uefa_array = []

    team_continent_array = []

    for each_continent in range(0, 6):  # Six Continent
        if continent_array_final[each_continent][0] == "AFC":
            for each_afc_team in range(0, len(continent_array_final[each_continent])):  # For each team in AFC
                afc_array.append(continent_array_final[each_continent][each_afc_team])

        if continent_array_final[each_continent][0] == "CAF":
            for each_caf_team in range(0, len(continent_array_final[each_continent])):
                caf_array.append(continent_array_final[each_continent][each_caf_team])
        if continent_array_final[each_continent][0] == "OFC":
            for each_ofc_team in range(0, len(continent_array_final[each_continent])):
                ofc_array.append(continent_array_final[each_continent][each_ofc_team])
        if continent_array_final[each_continent][0] == "CONCACAF":
            for each_concacaf_team in range(0, len(continent_array_final[each_continent])):
                concacaf_array.append(continent_array_final[each_continent][each_concacaf_team])
        if continent_array_final[each_continent][0] == "CONMEBOL":
            for each_conmebol_team in range(0, len(continent_array_final[each_continent])):
                conmebol_array.append(continent_array_final[each_continent][each_conmebol_team])
        if continent_array_final[each_continent][0] == "UEFA":
            for each_uefa_team in range(0, len(continent_array_final[each_continent])):
                uefa_array.append(continent_array_final[each_continent][each_uefa_team])

    del afc_array[0]
    del caf_array[0]
    del ofc_array[0]
    del concacaf_array[0]
    del conmebol_array[0]
    del uefa_array[0]
    #  print("afcarray", afc_array)
    #  print("cafarray", caf_array) # Could be None
    #  print("ofcarray", ofc_array)
    #  print("concacafarray", concacaf_array)  # Could be None
    #  print("conmebolarray", conmebol_array)
    #  print("uefaarray", uefa_array)  # Could be None

    for team in team_array:  # For each countries ex. Russia, Brazil.......

        for afc_team in afc_array:
            if team == afc_team:
                team_continent_array.append("AFC")
                break

        for caf_team in caf_array:
            if team == caf_team:
                team_continent_array.append("CAF")
                break
        for ofc_team in ofc_array:
            if team == ofc_team:
                team_continent_array.append("OFC")
                break
        for concacaf_team in concacaf_array:
            if team == concacaf_team:
                team_continent_array.append("CONCACAF")
                break
        for conmebol_team in conmebol_array:
            if team == conmebol_team:
                team_continent_array.append("CONMEBOL")
                break
        for uefa_team in uefa_array:
            if team == uefa_team:
                team_continent_array.append("UEFA")
                break

    #print("team continent", team_continent_array)

    # for each_team in range(0, len(team_array)):

    #   team_obj = Team(team_array[each_team], team_pot_array[each_team], team_continent_array[each_team])
    # team_obj.printDetail()

    team_continent_map = {}

    for i in range(0, numb_team):
        team = team_array[i]
        team_continent_map[team] = team_continent_array[i]

    #print("team continent map", team_continent_map)

    team_used_ornot_map = {}
    for y in range (0, numb_team):
        team3 = team_array[y]
        team_used_ornot_map[team3] = "Not"

    #print("team used or not", team_used_ornot_map)

    team_pot_map = {}

    for z in range(0, numb_team):
        team2 = team_array[z]
        team_pot_map[team2] = team_pot_array[z]

    #print("team pot map", team_pot_map)
    #print("team continent map", team_continent_map)

    final_output = backtrackingsearch(team_array, team_pot_array, team_continent_array)

    output_file = open("output.txt", "w")

    output=[]


    if (final_output == "No"):
        #print("The final solution is",final_output)
        output_file.write("No")
    else:
        output_file.write("Yes" + "\n")
        for group_index in range(0, len(final_array)):
            # print("group index", group_index)

            team_index = 0
            for thisteam in final_array[group_index]:
                #print("ggg", team_index+1, len(final_array[group_index]))
                if (team_index+1 == len(final_array[group_index])):
                    output_file.write(thisteam)
                else:
                    output_file.write(thisteam + ",")
                team_index = team_index+1
                # print("one", one_group)

            output_file.write("\n")
        #print("The final solution is", final_array)


    output_file.close()

    text_file.close()
main()
