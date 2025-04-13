#8-9 months is approx. 256 days... => around 70% of the year
#Call it [0,256]
#Use a sine curve with period 365, the top centered around 128
#f(x)=sin(2pi(x-36.75)/365)+1

#Takes in a location, gives high temp data

from datetime import datetime
from meteostat import Point, Daily, Stations
import pandas
import math

   
print("input lat: ", end="")
lat=float(input())
print("input long: ", end="")
long=float(input())

start=datetime(2013,1,1)
end=datetime(2023,12,31)

averageTemps=[]
#place=Point(lat, long)
stations = Stations()
stations = stations.nearby(lat,long)
station = stations.fetch(1)


data = Daily(station, start, end)
data = data.normalize()
data = data.interpolate()
data = data.fetch()
#print(data)
# Show dataframe
highs = data['tmax'].tolist()
#print(len(highs))

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
        #avg=averageTemps[i-1]
    averageTemps.append(avg)

for i in range(365):
    averageTemps.append(averageTemps[i])
for i in range(365):
    averageTemps.append(averageTemps[i])

smoothed=[]
for i in range(365, 730):
    avg=(averageTemps[i-3]+averageTemps[i-2]+averageTemps[i-1]+averageTemps[i]+averageTemps[i+1]+averageTemps[i+2]+averageTemps[i+3])/7
    smoothed.append(avg)

for i in range(365):
    print(smoothed[i])




'''
import random
#Ignore the above for now
#Try to make sets of 4

fullL=[]
for i in range(1,21):
    for j in range(1,21):
        if i<j:
            fullL.append([i,j])
            
#print(fullL)

def isGood(pairsUsed, l1):
    for i in l1:
        for j in l1:
            if ([i,j] in pairsUsed) or ([j,i] in pairsUsed):
                return False
    return True

def generateAllPairs(l1):
    out=[]
    for i in l1:
        for j in l1:
            if i<j:
                out.append([i,j])
    return out

def isPairIn(l1,pair):
    for i in l1:
        for j in l1:
            if [i,j]==pair or [j,i]==pair:
                return True
    return False

def allIn(k,a1,a2,a3,a4,a5):
    for i in k:
        if not ((i in a1) or (i in a2) or (i in a3) or (i in a4) or (i in a5)):
            return False
    return True

#Generate all possible groups of 4
k=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
allPossibles=[]
usables=[]
for a in k:
    for b in k:
        for c in k:
            for d in k:
                if a<b<c<d:
                    allPossibles.append([a,b,c,d])
                    usables.append([a,b,c,d])
print("Finished computing all possible sets of 4.")

#Now should generate a map of 6*5 sets...
pairsUsed=[]

firstSet=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]]
allSets=[firstSet]

#add pairs
for i in firstSet:
    for j in generateAllPairs(i):
        if not (j in pairsUsed):
            pairsUsed.append(j)

#Take out the sets that cannot be used
new=[]
flag=False
print(len(usables))
for i in usables:
    flag=False
    for j in pairsUsed:
        if isPairIn(i,j):
            flag=True
    if flag==False:
        new.append(i)
usables=new
print(len(usables))

#Rest of the five iterations
for i in range(5):
    #Find a way to get 5 sets of 4 from the list of usables such that all 20 are in it
    usedNums=[]
    setOfFive=[]
    setOfFive.append(usables[0])
    for i in usables[0]:
        usedNums.append(i)
    count=0
    for i in range(len(usables)):
        flag=False
        for j in usables[i]:
            if j in usedNums:
                flag=True
        if flag==False:
            setOfFive.append(usables[i])
            for j in usables[i]:
                usedNums.append(j)
            count+=1
        if count==5:
            break

    print(setOfFive)'''