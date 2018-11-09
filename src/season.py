import rostertool, schedule, random
from models import League
from game import Game
from tabulate import tabulate
from os import system

def print_standings(standings):
	table = []
	for team, record in standings.items():
		table.append([team,record[0],record[1]])
	table.sort(key=lambda x:int(x[1]), reverse=True)
	rankings = {}
	for i in range(len(table)):
 		rankings[table[i][0]] = i+1
	print(tabulate(table,["Team","W","L"]))	
	print("")
	return rankings

def print_upcoming_games(cur_week, week_no,rankings):
	table = []
	for game in cur_week:
		hot = ""
		if(week_no>3):
			if((rankings[game.awayTeam.teamName]<6) and (rankings[game.homeTeam.teamName]<6)):
				hot = "Big Game!"
		table.append(["{}_{}".format(game.awayTeam.teamName,rankings[game.awayTeam.teamName]),"{}_{}".format(game.homeTeam.teamName,rankings[game.homeTeam.teamName]),hot])
	print(tabulate(table,["Away","Home",""]))

def play_week(cur_week):
	week_results = []
	for game in cur_week:
		gr = game.playGame()
		week_results.append(gr)
	return week_results

def print_week_results(week_result,rankings):
	table = []
	for gr in week_result:
		table.append(["{}_{}".format(gr.atname,rankings[gr.atname]),gr.atscore,gr.htscore,"{}_{}".format(gr.htname,rankings[gr.htname])])
	print(tabulate(table,["Away","","","Home"]))

def update_standings(standings, week_result):
	for gr in week_result:
		standings[gr.winner()][0]+=1
		standings[gr.loser()][1]+=1

league = rostertool.loadLeague("USFL")
game_results = []

schedule = schedule.make_schedule(league.allTeams())

standings = {}
for team in league.allTeams():
	standings[team.teamName] = [0,0]

week = 0;
while(week<len(schedule)):
	system("clear")
	cur_week = schedule[week]
	rankings = print_standings(standings)
	print("Week {}".format(week+1))
	print_upcoming_games(cur_week,week,rankings)
	game_results.append(play_week(cur_week))
	week_result = game_results[week]
	update_standings(standings, week_result)
	wait = raw_input()
	system("clear")
	print_standings(standings)
	print("Week {} Results".format(week+1))
	print_week_results(week_result,rankings)
	wait = raw_input()
	week += 1
