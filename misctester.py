import math
import numpy
import statistics

#Team home locations
team_locations = [ 
    # Oceania
    (-33.8474, 151.0634),   # Australia

    # North America
    ( 40.895, -74.196),   # USA (NY)
    ( 19.3029, -99.1505),   # Mexico

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

    # Africa
    ( 34.0028, -6.8443),    # Morocco
    ( 14.7319, -17.3725),   # Senegal

    # Asia
    ( 35.9039, 139.7149),   # Japan
    ( 21.0285, 105.7626),   # Vietnam
    ( 35.7219, 51.2753),    # Iran
    ( 41.0733, 28.7641),    # Turkey
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

#Michael's sus function for one travel
def sus(lat1, long1, lat2, long2, nights):
    d = dist(lat1,long1,lat2,long2)
    if d<300:
        return 0
    return d/1000*(0.8)**(2*math.log(d))+nights/3 #2 flights

#Research-backed travel cost function
#One person on a team costs this much
def cost(lat1,long1,lat2,long2,nights):
    d = dist(lat1,long1,lat2,long2)
    if d<300:
        return 0
    return (65.87+0.23*d)*2 + nights*100 #2 flights...

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
    return total*10000

#Takes in an array of [lat1,long1,lat2,long2,nights,travellingTeam] for each FLIGHT TO A GAME...
#Note that lat1,long1 are the "home" place of the team
def jetlag_VAR(dataSet):
    #Takes the sum of the squares of the long differences for each team
    jetLags=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(dataSet)):
        longDiff=min(abs(dataSet[i][1]-dataSet[i][3]), min(abs(dataSet[i][1]-dataSet[i][3]-360), abs(dataSet[i][1]-dataSet[i][3]+360)))
        #print("longDiff:", longDiff, end=" ")
        #print("long1:", dataSet[i][1], end=" ")
        #print("long2:", dataSet[i][3], end=" ")
        
        jetLags[dataSet[i][5]]+=(1/(1+2.718281828**((-longDiff/15)+6)))*10000
        #print("jetLag:", jetLags[dataSet[i][5]])
    #Now we have a list of all the summed squared jetlags for each team
    #Proceed to calculate vairance of this
    newList=[]
    for a in jetLags:
        if a!=0:
            newList.append(a)
    return math.sqrt(numpy.var(newList))

#Takes in one GAME


#Takes in the same array as above
#Calculates the variance in costs for each team
def cost_VAR(dataSet):
    totalDists=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(dataSet)):
        #THere's a flight to and back
        totalDists[dataSet[i][5]]+=2*dist(dataSet[i][0],dataSet[i][1],dataSet[i][2],dataSet[i][3])
    
    #Calc variance of distances
    #print(totalDists)
    newList=[]
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
        #4-group
        if len(singleSet)==6:
            nights=3
        #5-group
        elif len(singleSet)==7:
            nights=5
            
        #Runs through each team. If the set is not home, create a flight
        for j in range(len(singleSet)-2):
            if not isHome(singleSet[j],lat,long):
                flights.append([team_locations[singleSet[j]][0], team_locations[singleSet[j]][1], lat, long, nights, singleSet[j]])

    return flights

#[0.15,0.05,0.4,0.4] 

def feasabilityOverall(l1):
    return (0.08436365142884102*totalCost(l1)
            + 0.03745333952951946*totalSus(l1)
            + 0.7877860183987492*cost_VAR(l1)
            + 0.09039699064289027*jetlag_VAR(l1))
'''
    return (0.033593651452160304*totalCost(l1)
            + 0.5356730767180363*totalSus(l1)
            + 0.12534125988703912*cost_VAR(l1)
            + 0.3053920119427642*jetlag_VAR(l1))
'''
#Let's suppose we have a double round-robin
#Each team goes to each other team to play
dRRGames=[]
for i in range(20):
    for j in range(20):
        if i<j:
            #Home for I
            dRRGames.append([i,j,team_locations[i][0],team_locations[i][1]])
            
            #Home for J
            dRRGames.append([i,j,team_locations[j][0],team_locations[j][1]])
l1=generateListofFlights(dRRGames)
print("TOTAL FOR DRR:")
print(feasabilityOverall(l1))

dRRGames=[]
for i in range(20):
    for j in range(20):
        if i<j:
            if (j-i)%2==0:
                #Home for I
                dRRGames.append([i,j,team_locations[i][0],team_locations[i][1]])
            else:
                #Home for J
                dRRGames.append([i,j,team_locations[j][0],team_locations[j][1]])
l1=generateListofFlights(dRRGames)
print("TOTAL FOR SRR:")
print(feasabilityOverall(l1))


#Now let's do groups of 4/5 - is it better?
#The groups are:
initialGrps=[
    [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
    [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
    [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
    [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
    [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
    [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
    ]

#Get available game coords
data=open("citiesList.txt","r")
locs=data.readlines()
data.close()
for i in range(len(locs)):
    #OR: allStudents[i]=allStudents[i][0:len(allStudents[i])-1]
    locs[i]=locs[i].strip('\n')
    locs[i]=locs[i].split('\t')
    locs[i][0]=float(locs[i][0])
    locs[i][1]=float(locs[i][1])

#locs=[[float lat,long,String name],[lat,long,name],[...]...]
    
#Input is a list of team numbers, e.g. [1,3,6,8]
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

print(locs[findOptLoc([0,13,15,17])])
bestLoc=locs[findOptLoc([0,13,15,17])]

altLat=25.2
altLong=51.4

#print(cost(21.0285, 105.7626, bestLoc[0],bestLoc[1],3))
#print(cost(21.0285, 105.7626, altLat,altLong,3))


#print("Best Cost:", totalCost(generateListofFlights([[0,13,15,17, bestLoc[0], bestLoc[1]]])))  
#print("Alt Cost:", totalCost(generateListofFlights([[0,13,15,17,altLat,altLong]]))) 
#
#print("B cVAR:", cost_VAR(generateListofFlights([[0,13,15,17,bestLoc[0], bestLoc[1]]])))  #
#print("A cVAR:", cost_VAR(generateListofFlights([[0,13,15,17,altLat,altLong]])))  # 

#print("B tVAR:", jetlag_VAR(generateListofFlights([[0,13,15,17,bestLoc[0], bestLoc[1]]])))  # 
#print("A tVAR:", jetlag_VAR(generateListofFlights([[0,13,15,17,altLat,altLong]])))  # 

#print("B sus:", totalSus(generateListofFlights([[0,13,15,17,bestLoc[0], bestLoc[1]]])))  # 
#print("A sus:", totalSus(generateListofFlights([[0,13,15,17,altLat,altLong]])))  # 


#SIMMING
#Samples from a poisson distribution
#Where t1L and t2L are lambda values (mean goals scored)
def simOneGame(t1, t1L, t2, t2L, scoresList):
    t1Goals=numpy.random.poisson(lam=t1L, size=1)[0]
    t2Goals=numpy.random.poisson(lam=t2L, size=1)[0]
    if t1Goals>t2Goals:
        scoresList[t1]+=3
    elif t1Goals<t2Goals:
        scoresList[t2]+=3
    else:
        scoresList[t1]+=1
        scoresList[t2]+=1

def simGroup(group, scoresList):
    ls=[0.85,1.08,1.03,1.05,0.74,1.73,2.08,1.51,1.45,1.86,1.61,1.75,1.40,1.74,0.87,1.33,1.00,0.56,0.72,0.97]
    for i in group:
        for j in group:
            if i<j:
                simOneGame(i,ls[i],j,ls[j],scoresList)
    
#Games is an list of objects [int team1,int team2,lat,long] (single games)
#OR [int team1, team2, team3, team4, lat, long] for grps of 4
#OR [team1...5, lat, long] for grps of 5
def sim(games):
    points=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Data from WIkipedia
    ls=[0.85,1.08,1.03,1.05,0.74,1.73,2.08,1.51,1.45,1.86,1.61,1.75,1.40,1.74,0.87,1.33,1.00,0.56,0.72,0.97]
    for i in range(len(games)):
        simGroup(games[i][0:len(games[i])-2],points)
    print(points)
    return points
    