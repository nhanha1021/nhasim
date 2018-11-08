import rostertool
import random
from models import League
from game import Game
from tabulate import tabulate
from os import system

league = rostertool.loadLeague("USFL")
game_history = []

def create_schedule(league):
 	schedule = []
 	for hteam in league.allTeams():
 		other_teams = league.allTeams()
 		other_teams.remove(hteam)
 		for ateam in other_teams:
 			schedule.append(Game(ateam,hteam))
	return schedule

schedule = create_schedule(league)
for i in range(5):
	random.shuffle(schedule)

standings = {}
for team in league.allTeams():
	standings[team.teamName] = [0,0]


def print_standings(standings):
	table = []
	for team, record in standings.items():
		table.append([team,record[0],record[1]])
	table.sort(key=lambda x:int(x[1]), reverse=True)
	print tabulate(table,["Team","W","L"])	

while(True):
	system("clear")
	print_standings(standings)
	print ""
	print("Upcoming Games:")
	for i in range(3):
		print schedule[i].get_headline()
	print ""
	if(len(schedule)<=0):
		break
	game = schedule.pop(0)
	gr = game.playGame()
	standings[gr.winner()][0]+=1
	standings[gr.loser()][1]+=1
	game_history.append(gr)
	if(raw_input()=="quit"):
		break