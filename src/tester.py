from models import Player
from models import Team
from models import League
import rostertool
import json


# p1 = Player("John", "Shea")
# p2 = Player("Mykaela", "Lassi")
# p3 = Player("Sean", "Barker")
# p4 = Player("Jackson", "Perkins")

# roster = [p1, p2,p3,p4]

# t1 = Team("Puffton389", roster)
# t2 = Team("Frallo2", roster)

# teamRoster = [t1,t2]

# league = League("UMASS", teamRoster)

# rostertool.writeLeague(league)

league = rostertool.loadLeague("UMASS")
print league.leagueName

for team in league.teamRoster:
	print team.teamName
	for player in team.roster:
		print player.fullName()