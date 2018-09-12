from models import Player
from models import Team
from models import League
import rostertool, randomname
import json

leagueName = "USFL"
teamNames = ["Boston","New York","Philadelphia","New Jersey",
"Washington","Miami","Chicago","Cleveland",
"Los Angeles","San Francisco","San Diego","Seattle",
"Texas","Colorado","Phoenix","San Antonio"]

teamRoster = []

for name in teamNames:
	roster = []
	for i in range(10):
		roster.append(rostertool.createRandomPlayer())
	teamRoster.append(Team(name,roster))

league = League(leagueName, teamRoster)
rostertool.writeLeague(league)


