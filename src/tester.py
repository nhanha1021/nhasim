from models import Player
from models import Team
import rostertool
import json


# p1 = Player("John", "Shea")
# p2 = Player("Mykaela", "Lassi")
# p3 = Player("Sean", "Barker")
# p4 = Player("Jackson", "Perkins")

# roster = [p1, p2,p3,p4]

# t1 = Team("Puffton389", roster)

# rostertool.writeTeam(t1)

t1 = rostertool.loadTeam("Puffton389")
print t1.teamName
for player in t1.roster:
	print player.fullName()