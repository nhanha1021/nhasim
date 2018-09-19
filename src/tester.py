from models import League, Team
from tabulate import tabulate
from os import system
import json, rostertool, sys

l1 = League("LEAGUE1")
l2 = League("LEAGUE2")
l1.addTeam(Team("Team1", []))
l1.addTeam(Team("Team2", []))
l2.addTeam(Team("Team3", []))
l1.addTeam(Team("Team4", []))
print("l1 teams")
for team in l1.allTeams():
	print team.teamName
print("l2 teams")
for team in l2.allTeams():
	print team.teamName