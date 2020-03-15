import boto3
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# importing the tools required for the Poisson regression model
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson, skellam

epl_1819 = pd.read_csv("https://s3.amazonaws.com/foot365predictiondata/E0.csv")
epl_1819 = epl_1819[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
epl_1819 = epl_1819.rename(columns={'FTHG': 'HomeGoals', 'FTAG': 'AwayGoals'})
epl_1819.head()

epl_1819 = epl_1819[:-10]
epl_1819.mean()

# construct Poisson  for each mean goals value
poisson_pred = np.column_stack([[poisson.pmf(i, epl_1819.mean()[j]) for i in range(8)] for j in range(2)])

# plot histogram of actual goals
plt.hist(epl_1819[['HomeGoals', 'AwayGoals']].values, range(9),
         alpha=0.7, label=['Home', 'Away'], normed=True, color=["#FFA07A", "#20B2AA"])

# add lines for the Poisson distributions
pois1, = plt.plot([i - 0.5 for i in range(1, 9)], poisson_pred[:, 0],
                  linestyle='-', marker='o', label="Home", color='#CD5C5C')
pois2, = plt.plot([i - 0.5 for i in range(1, 9)], poisson_pred[:, 1],
                  linestyle='-', marker='o', label="Away", color='#006400')

leg = plt.legend(loc='upper right', fontsize=13, ncol=2)
leg.set_title("Poisson           Actual        ", prop={'size': '14', 'weight': 'bold'})

plt.xticks([i - 0.5 for i in range(1, 9)], [i for i in range(9)])
plt.xlabel("Goals per Match", size=13)
plt.ylabel("Proportion of Matches", size=13)
plt.title("Number of Goals per Match (EPL 2018/19 Season)", size=14, fontweight='bold')
plt.ylim([-0.004, 0.4])
plt.tight_layout()
plt.show()

# probability of draw between home and away team
skellam.pmf(0.0, epl_1819.mean()[0], epl_1819.mean()[1])

# probability of home team winning by one goal
skellam.pmf(1, epl_1819.mean()[0], epl_1819.mean()[1])

skellam_pred = [skellam.pmf(i, epl_1819.mean()[0], epl_1819.mean()[1]) for i in range(-6, 8)]

plt.hist(epl_1819[['HomeGoals']].values - epl_1819[['AwayGoals']].values, range(-6, 8),
         alpha=0.7, label='Actual', normed=True)
plt.plot([i + 0.5 for i in range(-6, 8)], skellam_pred,
         linestyle='-', marker='o', label="Skellam", color='#CD5C5C')
plt.legend(loc='upper right', fontsize=13)
plt.xticks([i + 0.5 for i in range(-6, 8)], [i for i in range(-6, 8)])
plt.xlabel("Home Goals - Away Goals", size=13)
plt.ylabel("Proportion of Matches", size=13)
plt.title("Difference in Goals Scored (Home Team vs Away Team)", size=14, fontweight='bold')
plt.ylim([-0.004, 0.26])
plt.tight_layout()
plt.show()

fig, (ax1, ax2) = plt.subplots(2, 1)

chel_home = epl_1819[epl_1819['HomeTeam'] == 'Chelsea'][['HomeGoals']].apply(pd.value_counts, normalize=True)
chel_home_pois = [poisson.pmf(i, np.sum(np.multiply(chel_home.values.T, chel_home.index.T), axis=1)[0]) for i in
                  range(6)]
sun_home = epl_1819[epl_1819['HomeTeam'] == 'Liverpool'][['HomeGoals']].apply(pd.value_counts, normalize=True)
sun_home_pois = [poisson.pmf(i, np.sum(np.multiply(sun_home.values.T, sun_home.index.T), axis=1)[0]) for i in range(6)]

chel_away = epl_1819[epl_1819['AwayTeam'] == 'Chelsea'][['AwayGoals']].apply(pd.value_counts, normalize=True)
chel_away_pois = [poisson.pmf(i, np.sum(np.multiply(chel_away.values.T, chel_away.index.T), axis=1)[0]) for i in
                  range(6)]
sun_away = epl_1819[epl_1819['AwayTeam'] == 'Liverpool'][['AwayGoals']].apply(pd.value_counts, normalize=True)
sun_away_pois = [poisson.pmf(i, np.sum(np.multiply(sun_away.values.T, sun_away.index.T), axis=1)[0]) for i in range(6)]

ax1.bar(chel_home.index - 0.4, chel_home.values, width=0.4, color="#034694", label="Chelsea")
ax1.bar(sun_home.index, sun_home.values, width=0.4, color="#EB172B", label="Liverpool")
pois1, = ax1.plot([i for i in range(6)], chel_home_pois,
                  linestyle='-', marker='o', label="Chelsea", color="#0a7bff")
pois1, = ax1.plot([i for i in range(6)], sun_home_pois,
                  linestyle='-', marker='o', label="Liverpool", color="#ff7c89")
leg = ax1.legend(loc='upper right', fontsize=12, ncol=2)
leg.set_title("Poisson                 Actual                ", prop={'size': '14', 'weight': 'bold'})
ax1.set_xlim([-0.5, 7.5])
ax1.set_ylim([-0.01, 0.65])
ax1.set_xticklabels([])
# mimicing the facet plots in ggplot2 with a bit of a hack
ax1.text(7.65, 0.585, '                Home                ', rotation=-90,
         bbox={'facecolor': '#ffbcf6', 'alpha': 0.5, 'pad': 5})
ax2.text(7.65, 0.585, '                Away                ', rotation=-90,
         bbox={'facecolor': '#ffbcf6', 'alpha': 0.5, 'pad': 5})

ax2.bar(chel_away.index - 0.4, chel_away.values, width=0.4, color="#034694", label="Chelsea")
ax2.bar(sun_away.index, sun_away.values, width=0.4, color="#EB172B", label="Liverpool")
pois1, = ax2.plot([i for i in range(6)], chel_away_pois,
                  linestyle='-', marker='o', label="Chelsea", color="#0a7bff")
pois1, = ax2.plot([i for i in range(6)], sun_away_pois,
                  linestyle='-', marker='o', label="Liverpool", color="#ff7c89")
ax2.set_xlim([-0.5, 7.5])
ax2.set_ylim([-0.01, 0.65])
ax1.set_title("Number of Goals per Match (EPL 2016/17 Season)", size=14, fontweight='bold')
ax2.set_xlabel("Goals per Match", size=13)
ax2.text(-1.15, 0.9, 'Proportion of Matches', rotation=90, size=13)
plt.tight_layout()
plt.show()

goal_model_data = pd.concat([epl_1819[['HomeTeam', 'AwayTeam', 'HomeGoals']].assign(home=1).rename(
    columns={'HomeTeam': 'team', 'AwayTeam': 'opponent', 'HomeGoals': 'goals'}),
    epl_1819[['AwayTeam', 'HomeTeam', 'AwayGoals']].assign(home=0).rename(
        columns={'AwayTeam': 'team', 'HomeTeam': 'opponent', 'AwayGoals': 'goals'})])

poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                        family=sm.families.Poisson()).fit()
poisson_model.summary()

poisson_model.predict(pd.DataFrame(data={'team': 'Chelsea', 'opponent': 'Liverpool',
                                         'home': 1}, index=[1]))

poisson_model.predict(pd.DataFrame(data={'team': 'Liverpool', 'opponent': 'Chelsea',
                                         'home': 0}, index=[1]))


def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam,
                                                           'opponent': awayTeam, 'home': 1},
                                                     index=[1])).values[0]
    away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam,
                                                           'opponent': homeTeam, 'home': 0},
                                                     index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in
                 [home_goals_avg, away_goals_avg]]
    return (np.outer(np.array(team_pred[0]), np.array(team_pred[1])))


simulate_match(poisson_model, 'Chelsea', 'Liverpool', max_goals=3)

chel_sun = simulate_match(poisson_model, "Leicester", "Chelsea", max_goals=10)
# leicester win
np.sum(np.tril(chel_sun, -1))

# draw
np.sum(np.diag(chel_sun))

# chelsea win
np.sum(np.triu(chel_sun, 1))

s3 = boto3.client('s3')
finalWeek = [{"Home": "Brighton", "Away": "Man City"},
             {"Home": "Burnley", "Away": "Arsenal"},
             {"Home": "Crystal Palace", "Away": "Bournemouth"},
             {"Home": "Fulham", "Away": "Newcastle"},
             {"Home": "Leicester", "Away": "Chelsea"},
             {"Home": "Liverpool", "Away": "Wolves"},
             {"Home": "Man United", "Away": "Cardiff"},
             {"Home": "Southampton", "Away": "Huddersfield"},
             {"Home": "Tottenham", "Away": "Everton"},
             {"Home": "Watford", "Away": "West Ham"}]
result = {}
for i in finalWeek:
    print(i["Home"], i["Away"])
    match = simulate_match(poisson_model, i["Home"], i["Away"], max_goals=12)
    result[i["Home"] + " vs " + i["Away"]] = {"Home Wins": str(int(np.sum(np.tril(match, -1)) * 100)) + "%",
                                              "Draws": str(int(np.sum(np.diag(match)) * 100)) + "%",
                                              "Away Wins": str(int(np.sum(np.triu(match, 1)) * 100)) + "%"}

print(json.dumps(result))
with open('data.json', 'w') as f:
    f.write(json.dumps(result))

s3.upload_file('data.json', 'foot365predictionresult', 'data.json')
