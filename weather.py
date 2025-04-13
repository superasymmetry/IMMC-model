import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import pandas
import math

from meteostat import Point, Daily, Stations




df = pandas.DataFrame({'A': [1, 2, 3]})
list1 = df['A'].tolist()
print(list1)

print("input lat: ", end="")
#lat=float(input())
lat = 45.8
print("input long: ", end="")
#long=float(input())
long = 126.6

start=datetime(2013,1,1)
end=datetime(2023,12,31)

averageTemps=[]
place=Point(lat, long)


data = Daily(place, start, end)
data = data.fetch()
#print(data)
# Show dataframe
highs = data['tmax'].tolist()
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

for i in range(365):
    print(smoothed[i])

# graph it
x = np.arange(len(smoothed))  # X-axis as indices
y = smoothed  # Y-axis as values

plt.figure(figsize=(8, 4))
plt.scatter(x, y, color='blue', alpha=0.6)

plt.xlabel("Day")
plt.ylabel("Temp")
plt.title("Temperatures")
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.show()

rounds = [
            [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
            [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
            [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
            [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
            [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
            [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
            ]

def objective(rounds):
    even_breaks_score = [0]*20
    last_break = [0]*20

    for round in rounds:
        for team 