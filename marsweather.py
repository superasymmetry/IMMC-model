from datetime import datetime
from meteostat import Point, Daily, Stations
import pandas
import math
import numpy
import random
import copy
# def swapRounds(rounds):
#     round = random.randint(0, 6)
#     x, y = random.sample(len(rounds[round])) #two teams to swap
#     rounds[round][x], rounds[round][y] = rounds[round][y], rounds[round][x]
#     return rounds
 
# def objective(schedule):
#     total_climate_suitability = 0
#     dates = []
#     for i in range(len(schedule)):
#         for arr in schedule[i]:
#             dates.append(arr[-1])
#             total_climate_suitability+=weatherSuitability(arr[-1], arr[-4], arr[-5])
#     return math.sqrt(numpy.var(dates))*0.5+total_climate_suitability*0.5

from datetime import datetime
from meteostat import Point, Daily, Stations
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import math
 
#Get data
data=open("citiesList.txt","r")
locs=data.readlines()
data.close()
for i in range(len(locs)):
    #OR: allStudents[i]=allStudents[i][0:len(allStudents[i])-1]
    locs[i]=locs[i].strip('\n')
    locs[i]=locs[i].split('\t')
    locs[i][0]=float(locs[i][0])
    locs[i][1]=float(locs[i][1])
#print(locs)
 
start=datetime(2013,1,1)
end=datetime(2023,12,31)
#Get ALL the weather data into a list........
allSmoothedWeatherData=[]
for k in range(len(locs)):
    #print("Doing:", locs[k][2])
    averageTemps=[]
 
    stations = Stations()
    stations = stations.nearby(locs[k][0],locs[k][1])
    station = stations.fetch(1)
 
 
    data = Daily(station, start, end)
    data = data.normalize()
    data = data.interpolate()
    data = data.fetch()
    #print(data)
    # Show dataframe
    highs = data['tavg'].tolist()
    #print(highs)
 
    #Take out Feburary 29
    highs.pop(1154)
    highs.pop(2615)
    for i in range(len(highs)):
        if math.isnan(highs[i]):
            highs[i]=highs[i-1]
    for i in range(365):
        s=0
        for j in range(10):
          s+=highs[i+j*365]
        avg=s/11
        #if math.isnan(avg):
        #    avg=averageTemps[i-1]
        averageTemps.append(avg)
 
    for i in range(365):
        averageTemps.append(averageTemps[i])
    for i in range(365):
        averageTemps.append(averageTemps[i])
 
    smoothed=[]
    for i in range(365, 730):
        avg=(averageTemps[i-3]+averageTemps[i-2]+averageTemps[i-1]+averageTemps[i]+averageTemps[i+1]+averageTemps[i+2]+averageTemps[i+3])/7
        smoothed.append(avg)
    allSmoothedWeatherData.append(smoothed)
    print(len(smoothed))

 
print(len(allSmoothedWeatherData))

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
 
def weatherSuitability(dayNum, lat, long):
    global allSmoothedWeatherData, locs
    #skips function if in locs
    for i in range(len(locs)):
        if dist(locs[i][0], locs[i][1], lat, long)<300:
            smoothed=allSmoothedWeatherData[i]
            return (17.5-smoothed[dayNum])**2
    start=datetime(2013,1,1)
    end=datetime(2023,12,31)
 
    averageTemps=[]
    stations = Stations()
    stations = stations.nearby(lat,long)
    station = stations.fetch(1)
    data = Daily(station, start, end)
    data = data.normalize()
    data = data.interpolate()
    data = data.fetch()
    #print(data)
    # Show dataframe
    highs = data['tavg'].tolist()
    #print(highs)
 
    #Take out Feburary 29
    highs.pop(1154)
    highs.pop(2615)
    for i in range(len(highs)):
        if math.isnan(highs[i]):
            highs[i]=highs[i-1]
    for i in range(365):
        s=0
        for j in range(10):
          s+=highs[i+j*365]
        avg=s/11
        if math.isnan(avg):
            avg=averageTemps[i-1]
        averageTemps.append(avg)
 
    for i in range(365):
        averageTemps.append(averageTemps[i])
    for i in range(365):
        averageTemps.append(averageTemps[i])
 
    smoothed=[]
    for i in range(365, 730):
        avg=(averageTemps[i-3]+averageTemps[i-2]+averageTemps[i-1]+averageTemps[i]+averageTemps[i+1]+averageTemps[i+2]+averageTemps[i+3])/7
        smoothed.append(avg)
 
    #Smoothed now contains average weather data
    for i in range(365):
        print((17.5-smoothed[i])**2)
    return (17.5-smoothed[dayNum])**2

team_locations = [ 
    # Oceania
    (-33.8474, 151.0634),   # Australia
 
    # North America
    ( 40.895, -74.196),   # USA (NY)
    ( 19.3029, -99.1505),   # Mexico
    # (), # Canada
 
    # Central America
    ( 9.9392, -84.3046),    # Costa Rica
    ( 9.0333, -79.4686),    # Panama
 
    # South America
    (-34.5456, -58.4497),   # Argentina
    (-22.9122, -43.2302),   # Brazil
    (-34.8941, -56.1526),   # Uruguay
    ( 10.9187, -74.8143),   # Colombia
 
    # Europe
    ( 48.9245, 2.3602),     # France
    ( 40.4531, -3.6884),    # Spain
    ( 52.3144, 4.9415),     # Netherlands
    ( 51.5558, -0.2796),    # England
    ( 38.7528, -9.1847),    # Portugal
    # (), # Germany
 
    # Africa
    ( 34.0028, -6.8443),    # Morocco
    ( 14.7319, -17.3725),   # Senegal
    # (), # Algeria
 
    # Asia
    ( 35.9039, 139.7149),   # Japan
    ( 21.0285, 105.7626),   # Vietnam
    ( 35.7219, 51.2753),    # Iran
    ( 41.0733, 28.7641),    # Turkey
    # (), # 
]     

def generate_dataset(teams):
    dataset = []
    rounds = [
            [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
            [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
            [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
            [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
            [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
            [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
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

def isHome(team, lat, long):
    global team_locations
    if dist(team_locations[team][0],team_locations[team][1],lat,long)<200:
        return True
    return False

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

def feasabilityOverall(l1):
    return (0.08436365142884102*totalCost(l1)
            + 0.03745333952951946*totalSus(l1)
            + 0.7877860183987492*cost_VAR(l1)
            + 0.09039699064289027*jetlag_VAR(l1))

def sus(lat1, long1, lat2, long2, nights, epsilon = 1e-6):
    if lat1==lat2 and long1==long2:
        return 0
    d = dist(lat1,long1,lat2,long2)
    d = max(d, epsilon)
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


def breaks_variance(schedule):
    """
    Given a schedule (list of flights), this function computes the break variance for each team.
    Each flight is assumed to be a list where:
      - flight[-1] is the date (an integer, e.g., day of season),
      - flight[5] is the team ID.
    For each team, we collect its game dates, sort them, compute the differences
    between consecutive dates (the "breaks"), then compute the variance of those breaks.
    Returns the average standard deviation (sqrt(variance)) of the breaks across teams.
    """
    team_dates = {}
    for flight in schedule:
        team = flight[5]
        date = flight[-1]
        if team not in team_dates:
            team_dates[team] = []
        team_dates[team].append(date)
    
    break_std_list = []
    for team, dates in team_dates.items():
        if len(dates) < 2:
            continue  # Not enough games to compute breaks
        dates.sort()
        breaks = [dates[i+1] - dates[i] for i in range(len(dates) - 1)]
        mean_break = sum(breaks) / len(breaks)
        var_break = sum((b - mean_break)**2 for b in breaks) / len(breaks)
        break_std = math.sqrt(var_break)
        break_std_list.append(break_std)
    
    if not break_std_list:
        return 0
    # Return the average standard deviation of breaks over all teams.
    print(f"breaks variance: {sum(break_std_list) / len(break_std_list)}")
    return sum(break_std_list) / len(break_std_list)

# Your climate suitability function should be defined elsewhere.
# For this example, assume weatherSuitability(date, param1, param2) is available.

def objective(schedule):
    """
    The new objective function computes:
      - The average standard deviation of team breaks (from breaks_variance), and
      - The total climate suitability summed over all flights.
    These two are then weighted (here equally) to produce the overall objective.
    """
    total_climate_suitability = 0
    for flight in schedule:
        # We assume flight[-1] is the date and flight[-4] and flight[-3] contain parameters
        # needed for the weatherSuitability function.
        print("flights: ", flight[-1], flight[-3], flight[-2])
        ws = weatherSuitability(flight[-1], flight[-3], flight[-2])
        if math.isnan(ws):
            ws = 10000
        total_climate_suitability += ws
        print(f"weathersuitability: {ws, total_climate_suitability}")
    
    break_std = breaks_variance(schedule)
    # Weighting: 50% on break variance and 50% on climate suitability.
    return break_std * 0.5 + total_climate_suitability * 0.5



def get_neighbor(schedule, temperature):
    neighbor = copy.deepcopy(schedule)
    day = random.randint(int(-temperature)-1, int(temperature-1))
    x = random.randint(0, len(schedule)-1)
    schedule[x][-1] += day
    schedule[x][-1] %= 256
    schedule[x][-1] += 63
    return neighbor

def optimize_timings(n_iter = 10, temp = 200, alpha = 0.13):
    # initialize
    teams = [5, 2, 0, 17, 18, 19, 13, 11, 10, 14, 6, 3, 15, 9, 8, 16, 1, 4, 12, 7]
    current_schedule = generate_dataset(teams)
    print(f"current schedule: {current_schedule}")
    for arr in current_schedule:
        print(arr)
        arr.append(random.randint(63, 318)) # put a random date
    print(f"initialized array: {current_schedule}")
    
    current_cost = objective(current_schedule)
    best_schedule, best_cost = current_schedule, current_cost

    T = temp
    for i in range(n_iter):
        candidate_schedule = get_neighbor(current_schedule, T)
        candidate_cost = objective(candidate_schedule)
        # print(f"candidate schedule: {candidate_schedule}")
        T = temp * (alpha ** i)  # Cooling schedule

        if candidate_cost < current_cost or random.random() < math.exp((current_cost - candidate_cost) / T):
            current_schedule, current_cost = candidate_schedule, candidate_cost
            if candidate_cost < best_cost:
                best_schedule, best_cost = candidate_schedule, candidate_cost

        print(f"Iteration {i}, Temp: {T:.2f}, Best Cost: {best_cost:.2f}")
    return best_schedule, best_cost


# print("input lat: ", end="")
# lat=float(input())
# print("input long: ", end="")
# long=float(input())
# print("input dayNum: ", end="")
# dayNum=int(input())
 
# print(weatherSuitability(dayNum,lat,long))

data=open("citiesList.txt","r")
locs=data.readlines()
data.close()
for i in range(len(locs)):
    #OR: allStudents[i]=allStudents[i][0:len(allStudents[i])-1]
    locs[i]=locs[i].strip('\n')
    locs[i]=locs[i].split('\t')
    locs[i][0]=float(locs[i][0])
    locs[i][1]=float(locs[i][1])

print("findoptloc:", findOptLoc(teams = [5, 2, 0, 17, 18, 19, 13, 11, 10, 14, 6, 3, 15, 9, 8, 16, 1, 4, 12, 7]))

print(optimize_timings())