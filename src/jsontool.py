import json
from models import Player
from models import Team
from models import League

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"
OFFENSE_LABEL = "offense"
DEFENSE_LABEL = "defense"
TEAMNAME_LABEL = "teamName"
ROSTER_LABEL = "roster"
LEAGUENAME_LABEL = "leagueName"
TEAMROSTER_LABEL = "teamRoster"

def PlayerToJson(player):
	data = {
		FIRSTNAME_LABEL : player.firstName,
		LASTNAME_LABEL : player.lastName,
		OFFENSE_LABEL : player.offense,
		DEFENSE_LABEL : player.defense
	}
	return data

def JsonToPlayer(data):
	firstName = data[FIRSTNAME_LABEL]
	lastName = data[LASTNAME_LABEL]
	offense = data[OFFENSE_LABEL]
	defense = data[DEFENSE_LABEL]
	return Player(firstName,lastName, offense, defense)

def TeamToJson(team):
	data = {
		TEAMNAME_LABEL : team.teamName
	}
	roster = []
	for player in team.get_all_players():
		roster.append(PlayerToJson(player))
	data[ROSTER_LABEL] = roster
	return data

def JsonToTeam(data):
	team = Team(data[TEAMNAME_LABEL])
	jsonroster = data[ROSTER_LABEL]
	for jsonplayer in jsonroster:
		player = JsonToPlayer(jsonplayer)
		team.add_player(player)
	return team
	
def LeagueToJson(league):
	data = {
		LEAGUENAME_LABEL : league.leagueName
	}
	teamRoster = []
	for team in league.get_all_teams():
		teamRoster.append(TeamToJson(team))
	data[TEAMROSTER_LABEL] = teamRoster
	return data

def JsonToLeague(data):
	league = League(data[LEAGUENAME_LABEL])
	jsonroster = data[TEAMROSTER_LABEL]
	for jsonteam in jsonroster:
		team = JsonToTeam(jsonteam)
		league.add_team(team)
	return league


