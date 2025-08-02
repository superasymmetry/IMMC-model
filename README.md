# IMMC-model
This code was made for the International Mathematical Modelling Challenge submission for team 2025014. The model won the Meritorious award (3rd in Canada).

## Problem Statement
The International Multi-Continental Matchmaking Committee asks us to provide an intercontinental
selection of teams (including at least two from each continent) and provide a viable tournament schedule
with groupings, date, and locations. The tasks are as follows:
1. Identify the sport and select 20 individual teams that will be competing. We have selected soccer
as the sport.
2. Develop a schedule ensuring a balanced distribution of games, travel distance, and competitive-
ness. This will be discussed throughout the methodology section.
3. Expand and generalize the model to consider additional teams and alternative sports. This
consists of essentially adding 4 teams to the league and re-running the entire model steps to
account for the 4 extra teams.

## Implementation
A double round robin tournament style was decided through a brief breakdown of the matchups needed. Although costly, it maximizes our fairness score.

The overall model design consisted of three processes: matchmaking, location optimization, and
generating the timings for the matches throughout the season. The matchmaking model assigns a
country-specific team to each placeholder team in the match groupings (refer Table 13). The location
optimization model finds the coordinates of the optimal city to host a game for a group. Lastly, the
timing model disperses the dates for each game optimally throughout the season. The outline of this
model is shown in Figure 4.

<img width="808" height="546" alt="image" src="https://github.com/user-attachments/assets/74a22aed-50ec-40e7-96fa-7b9cb2f9d9ba" />

*Our model design for combined matchmaking, location optimization, and timings*

<img width="1196" height="570" alt="image" src="https://github.com/user-attachments/assets/e3df6a52-93a8-4cd5-86d2-3e300d25f119" />

*Model design for matchmaking*

The purpose of the
matchmaking component was to generate the best groupings for the groupings approach or the best
home/away configurations for the other approach to single round-robin. This was done by finding the
matchmaking with the least total penalty (which is evaluated based on weighing various components
described in detail in our paper). 

<img width="1201" height="574" alt="image" src="https://github.com/user-attachments/assets/889ef413-c349-49af-8cec-307d6e656511" />

*Model design for match scheduling*

The timing and location optimization was based on several factors such as fairness distance/economics, fairness in jetlag, and sustainability. More detailed evaluation criteria can be found in our paper.
The weather for the matchups was
found by taking the average temperature for the week of the matchup over the past 11 years from the
Meteostat dataset, and it was evaluated based on how suitable the temperature was for a game (with the best temperature being 17.5 degrees Celsius). The break lengths is a function that calculates the
effectiveness of the break lengths in a certain schedule by considering the evenness of break lengths
and heavily discouraging consecutive groups. 

An simulated annealing process was run for thousands of iterations for each sub-model, yielding the final results, which are compiled into the infographics below.

<img width="1006" height="536" alt="image" src="https://github.com/user-attachments/assets/0850fd8c-453b-4d5f-8e9b-3447b28631d3" />

*Game locations throughout the season - date numbers labelled*

<img width="1464" height="1207" alt="image" src="https://github.com/user-attachments/assets/6b97a3ff-a6b6-4335-81b6-65b08df90ef0" />

*Match scheduling heatmap*
