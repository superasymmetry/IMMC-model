import math
import numpy
import random 

#Team home locations
team_locations = [
    # Oceania
    (-33.8474, 151.0634),   # Australia 1
    (-26.2348, 27.9825),
    (30.0917, 31.3211),
    (37.5683, 126.8972),
    (43.6333, -79/4186),
 
    # North America
    ( 40.895, -74.196),   # USA (NY) 2 
    ( 19.3029, -99.1505),   # Mexico 3 
    (45.424721, -75.695000), 
 
    # Central America
    ( 9.9392, -84.3046),    # Costa Rica 4
    ( 9.0333, -79.4686),    # Panama 5
 
    # South America
    (-34.5456, -58.4497),   # Argentina 6
    (-22.9122, -43.2302),   # Brazil 7
    (-34.8941, -56.1526),   # Uruguay 8
    ( 10.9187, -74.8143),   # Colombia 9
 
    # Europe
    ( 48.9245, 2.3602),     # France 10
    ( 40.4531, -3.6884),    # Spain 11
    ( 52.3144, 4.9415),     # Netherlands 12
    ( 51.5558, -0.2796),    # England 13
    ( 38.7528, -9.1847),    # Portugal 14
 
    # Africa
    ( 34.0028, -6.8443),    # Morocco 15
    ( 14.7319, -17.3725),   # Senegal 16
 
    # Asia
    ( 35.9039, 139.7149),   # Japan 17
    ( 21.0285, 105.7626),   # Vietnam 18
    ( 35.7219, 51.2753),    # Iran 19
    ( 41.0733, 28.7641),    # Turkey 20
]
 
 
#Formula from https://www.movable-type.co.uk/scripts/latlong.html
def dist(lat1,lon1,lat2,lon2):
    R = 6371 # km
    φ1 = lat1 * math.pi/180 #in radians
    φ2 = lat2 * math.pi/180
    Δφ = (lat2-lat1) * math.pi/180
    Δλ = (lon2-lon1) * math.pi/180
 
    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # in metres
    return d
 
def sus(lat1, long1, lat2, long2, nights):
    if lat1==lat2 and long1==long2:
        return 0
    d = dist(lat1,long1,lat2,long2)
    return d*(0.8)**(2*math.log(d))+nights/3 #2 flights
 
#Research-backed travel cost function
def cost(lat1,long1,lat2,long2,nights):
    if lat1==lat2 and long1==long2:
        return 0
    d = dist(lat1,long1,lat2,long2)
    return 65.87+0.23*d*2 + nights*100 #2 flights...
 
#Takes in an array of [lat1,long1,lat2,long2,nights,travellingTeam] for each FLIGHT TO A GAME...
def totalCost(dataSet):
    total=0
    for i in range(len(dataSet)):
        total+=cost(dataSet[i][0],dataSet[i][1],dataSet[i][2],dataSet[i][3],dataSet[i][4])
    return total

#Takes in an array of [lat1,long1,lat2,long2,nights,travellingTeam] for each FLIGHT TO A GAME...
def totalSus(dataSet):
    total=0
    for i in range(len(dataSet)):
        total+=sus(dataSet[i][0],dataSet[i][1],dataSet[i][2],dataSet[i][3],dataSet[i][4])
    return total
 
#Takes in an array of [lat1,long1,lat2,long2,nights,travellingTeam] for each FLIGHT TO A GAME...
#Note that lat1,long1 are the "home" place of the team
def jetlag_VAR(dataSet):
    #Takes the sum of the squares of the long differences for each team
    squaredJetLags=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(dataSet)):
        longDiff=min(abs(dataSet[i][1]-dataSet[i][3]), 24-abs(dataSet[i][1]-dataSet[i][3]))
        squaredJetLags[dataSet[i][5]]+=(1/(1+2.718281828**((-longDiff/15)+6)))*10000
    #Now we have a list of all the summed squared jetlags for each team
    #Proceed to calculate vairance of this
    newList=[]
    for a in squaredJetLags:
        if a!=0:
            newList.append(a)
    return math.sqrt(numpy.var(newList))
 
#Takes in the same array as above
#Calculates the variance in costs for each team
def cost_VAR(dataSet):
    totalDists=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(dataSet)):
        #THere's a flight to and back
        totalDists[dataSet[i][5]]+=2*dist(dataSet[i][0],dataSet[i][1],dataSet[i][2],dataSet[i][3])
    #Calc variance of distances
    #print(totalDists)
    newList = []
    for a in totalDists:
        if a!=0:
            newList.append(a)
    return math.sqrt(numpy.var(newList))
 
#Is the game home for that team?
def isHome(team, lat, long):
    global team_locations
    if dist(team_locations[team][0],team_locations[team][1],lat,long)<200:
        return True
    return False

def findOptLoc(teams):
    global locs, team_locations
    #We are going to minimize the sum of the distances + VAR of the distances
    #Just look through every possible loc
    #First set minSum to infinity
    minSum=10000000000000.0
    bestLoc=-1
    numTeams=len(teams)
    for i in range(len(locs)):
        game=teams.copy()
        game.append(locs[i][0])
        game.append(locs[i][1])
        l1=generateListofFlights([game])
        k=feasabilityOverall(l1)
        if k<minSum:
            bestLoc=i
            minSum=k
    game=teams.copy()
    game.append(locs[i][0])
    game.append(locs[i][1])
    l1=generateListofFlights([game])
    k=feasabilityOverall(l1)
    return bestLoc

def feasabilityOverall(l1):
    return (0.08436365142884102*totalCost(l1)
            + 0.03745333952951946*totalSus(l1)
            + 0.7877860183987492*cost_VAR(l1)
            + 0.09039699064289027*jetlag_VAR(l1))
 
#Games is an list of objects [int team1,int team2,lat,long] (single games)
#OR [int team1, team2, team3, team4, lat, long] for grps of 4
#OR [team1...5, lat, long] for grps of 5
#Generates a list of one-way flights [lat1,long1,lat2,long2,nights,travellingTeam]
#Basically formats the games data into flights data for the functions above
def generateListofFlights(games):
    global team_locations
    flights=[]
    nights=1
    for i in range(len(games)):
        nights=1
        singleSet=games[i]
        lat=singleSet[-2]
        long=singleSet[-1]
        if len(singleSet)==6:
            nights=3
        elif len(singleSet)==7:
            nights=5
        #Runs through each team. If the set is not home, create a flight
        for j in range(len(singleSet)-2):
            if not isHome(singleSet[j],lat,long):
                flights.append([team_locations[singleSet[j]][0], team_locations[singleSet[j]][1], lat, long, nights, singleSet[j]])
 
    return flights

def ipf(a, b, c, d, tolerance=1e-4, target=[0.15, 0.05, 0.4, 0.4]):
        '''
        a, b, c, d - total scores of the four factors
        tolerance - the error threshold for convergence
        target - desired target proportions for the contributions of the factors
        '''
        weights = target.copy()
        while True:
            c_i = [a * weights[0], b * weights[1], c * weights[2], d * weights[3]]
            c_total = sum(c_i)
            p_i = [c_i[i] / c_total for i in range(len(c_i))]

            weights = [weights[i] * target[i] / p_i[i] for i in range(len(weights))]

            denom = sum(weights)
            weights = [w / denom for w in weights]

            diff = sum(abs(p_i[i] - target[i]) for i in range(len(target)))
            if diff < tolerance:
                break

        return weights
 
# generates a random initial grouping
def generate_initial():
    global locs, team_locations
    teams = list(range(24))
    random.shuffle(teams)
    dataset = []
    # rounds = [
    #         [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
    #         [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
    #         [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
    #         [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
    #         [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
    #         [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
    #         ]
    rounds = [
            [[0,1,2,3,20],[4,5,6,7,20],[8,9,10,11,20],[12,13,14,15,20],[16,17,18,19,20]],
            [[0,5,10,15,21],[4,9,14,19,21],[8,13,18,3,21],[12,17,2,7,21],[16,1,6,11,21]],
            [[0,9,18,7,22],[4,13,2,11,22],[8,17,6,15,22],[12,1,10,19,22],[16,5,14,3,22]],
            [[0,13,6,19,23],[4,17,10,3,23],[8,1,14,7,23],[12,5,18,11,23],[16,9,2,15,23]],
            [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
            [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]],
            [[20,21,22,23]]
        ]
    for round in rounds:
        for group in round:
            # appends a list in the dataset format
            temp = [teams[i] for i in group]
            locindex = findOptLoc(temp)  # Find location based on the group, not all teams
            temp.append(locs[locindex][0])  # lat
            temp.append(locs[locindex][1])  # long
            dataset.append(temp)
    return dataset


# generates dataSet from a new arrangement of teams
def generate_dataset(teams):
    dataset = []
    # rounds = [
    #         [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
    #         [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
    #         [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
    #         [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
    #         [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
    #         [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
    #         ]
    rounds = [
            [[0,1,2,3,20],[4,5,6,7,20],[8,9,10,11,20],[12,13,14,15,20],[16,17,18,19,20]],
            [[0,5,10,15,21],[4,9,14,19,21],[8,13,18,3,21],[12,17,2,7,21],[16,1,6,11,21]],
            [[0,9,18,7,22],[4,13,2,11,22],[8,17,6,15,22],[12,1,10,19,22],[16,5,14,3,22]],
            [[0,13,6,19,23],[4,17,10,3,23],[8,1,14,7,23],[12,5,18,11,23],[16,9,2,15,23]],
            [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
            [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]],
            [[20,21,22,23]]
        ]
    for round in rounds:
        for group in round:
            # appends a list in the dataset format
            # print(f"group: {group}")
            temp = [teams[i] for i in group]
            # print(f"temp: {temp}")
            locindex = findOptLoc(temp)  # Find location based on the group, not all teams
            temp.append(locs[locindex][0])  # lat
            temp.append(locs[locindex][1])  # long
            dataset.append(temp)
    return dataset
    
# get neighbor
def get_neighbor(teams):
    team = teams.copy()
    i, j = random.sample(range(len(teams)), 2)
    team[i], team[j] = team[j], team[i]
    return team

def objective(teams):
    weights = [0.08436365142884102, 0.03745333952951946, 0.7877860183987492, 0.09039699064289027]
    # print(f"schedule: {teams}")
    dataset = generate_dataset(teams)
    # print(f"schedule dataset: {dataset}")
    return totalCost(generateListofFlights(dataset))*weights[0]+totalSus(generateListofFlights(dataset))*weights[1]+cost_VAR(generateListofFlights(dataset))*weights[2]+jetlag_VAR(generateListofFlights(dataset))*weights[3]

def optimize(n_iter=24000, temp=1200, alpha=0.995):
    current_schedule = list(range(24))
    random.shuffle(current_schedule)
    # current_schedule = generate_initial()
    # print(f"current schedule {current_schedule}")
    current_cost = objective(current_schedule)
    best_schedule, best_cost = current_schedule, current_cost

    for i in range(n_iter):
        candidate_schedule = get_neighbor(current_schedule)
        candidate_cost = objective(candidate_schedule)
        # print(f"candidate schedule: {candidate_schedule}")
        T = temp * (alpha ** i)  # Cooling schedule

        if candidate_cost < current_cost or random.random() < math.exp((current_cost - candidate_cost) / T):
            current_schedule, current_cost = candidate_schedule, candidate_cost
            if candidate_cost < best_cost:
                best_schedule, best_cost = candidate_schedule, candidate_cost

        print(f"Iteration {i}, Temp: {T:.2f}, Best Cost: {best_cost:.2f}")

    return best_schedule, best_cost


data=open("citiesList.txt","r")
locs=data.readlines()
data.close()
for i in range(len(locs)):
    locs[i]=locs[i].strip('\n')
    locs[i]=locs[i].split('\t')
    locs[i][0]=float(locs[i][0])
    locs[i][1]=float(locs[i][1])
print(optimize())


# sampleGameSet=[[0,1,-25.274398, 133.775136],[1,2,13.3,15.5],[0,1,2,3,45.0,45.0]]
# print(generateListofFlights(sampleGameSet))
# print(totalCost(generateListofFlights(sampleGameSet)))
# print(totalSus(generateListofFlights(sampleGameSet)))
# print(cost_VAR(generateListofFlights(sampleGameSet)))
# print(jetlag_VAR(generateListofFlights(sampleGameSet)))

# print(ipf(13845.418694451222,10395.602379723927,3953.8658107496963,34456.90152052008))