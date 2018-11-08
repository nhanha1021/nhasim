import rostertool
from models import League

def shift(array):
	start = array.pop(0)
	array.append(start)

def sort_matches(teams_a, teams_h):
	if((len(teams_a)==0) or (len(teams_h)==0)):
		return
	group = []
	for i in range(len(teams_a)):
		for j in range(len(teams_a)):
			group.append((teams_a[j],teams_h[j]))
		shift(teams_a)
	teams_a1 = teams_a[:len(teams_a)/2]
	teams_a2 = teams_a[len(teams_a)/2:]
	teams_h1 = teams_h[:len(teams_h)/2]
	teams_h2 = teams_h[len(teams_h)/2:]
	group.append([sort_matches(teams_a1,teams_a2),sort_matches(teams_h1,teams_h2)])
	return group

def make_schedule(teams): 
	teams_a = teams[:len(teams)/2]
	teams_h = teams[len(teams)/2:]
	group = [sort_matches(teams_a, teams_h)]

	L1 = group[0]
	L1_1 = L1[len(L1)-1][0]
	L1_2 = L1[len(L1)-1][1]
	L1_1_1 = L1_1[len(L1_1)-1][0]
	L1_1_2 = L1_1[len(L1_1)-1][1]
	L1_2_1 = L1_2[len(L1_2)-1][0]
	L1_2_2 = L1_2[len(L1_2)-1][1]

	A = L1[:len(L1)-1]
	B = L1_1[:len(L1_1)-1]
	C = L1_2[:len(L1_1)-1]
	D = L1_1_1[:len(L1_1_1)-1]
	E = L1_1_2[:len(L1_1_2)-1]
	F = L1_2_1[:len(L1_2_1)-1]
	G = L1_2_2[:len(L1_2_2)-1]

	groups = [A,B,C,D,E,F,G]
	games = []
	weeks = []

	for g in groups:
		for item in g:
			games.append(item)

	while(len(games)>0):
	 	week = []
	 	for i in range(4):
	 		week.append(games.pop(0))
	 	weeks.append(week)

 	return weeks

league = rostertool.loadLeague("USFL")
teams = league.allTeams();
teams = teams[:len(teams)/2]
s = make_schedule(teams)
for i in range(len(s)):
	print("Week: {}".format(i))
	for game in s[i]:
		print("{} @ {}".format(game[0].teamName, game[1].teamName))






