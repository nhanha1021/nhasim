import json
from models import Player, Team, League, Season

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"
OFFENSE_LABEL = "offense"
DEFENSE_LABEL = "defense"
TEAMNAME_LABEL = "teamName"
ROSTER_LABEL = "roster"
LEAGUENAME_LABEL = "leagueName"
TEAMROSTER_LABEL = "teamRoster"
SEASON_LEAGUENAME_LABEL = "leagueName"
SEASON_SCHEDULE_LABEL = "schedule"
SEASON_WEEK_LABEL = "week"
SEASON_STANDINGS_LABEL = "standings"

def _player_to_json(player):
	data = {
		FIRSTNAME_LABEL : player.firstName,
		LASTNAME_LABEL : player.lastName,
		OFFENSE_LABEL : player.offense,
		DEFENSE_LABEL : player.defense
	}
	return data

def _json_to_player(data):
	firstName = data[FIRSTNAME_LABEL]
	lastName = data[LASTNAME_LABEL]
	offense = data[OFFENSE_LABEL]
	defense = data[DEFENSE_LABEL]
	return Player(firstName,lastName, offense, defense)

def _team_to_json(team):
	data = {
		TEAMNAME_LABEL : team.teamName
	}
	roster = []
	for player in team.get_all_players():
		roster.append(_player_to_json(player))
	data[ROSTER_LABEL] = roster
	return data

def _json_to_team(data):
	team = Team(data[TEAMNAME_LABEL])
	jsonroster = data[ROSTER_LABEL]
	for jsonplayer in jsonroster:
		player = _json_to_player(jsonplayer)
		team.add_player(player)
	return team
	
def league_to_json(league):
	data = {
		LEAGUENAME_LABEL : league.leagueName
	}
	teamRoster = []
	for team in league.get_all_teams():
		teamRoster.append(_team_to_json(team))
	data[TEAMROSTER_LABEL] = teamRoster
	return data

def json_to_league(data):
	league = League(data[LEAGUENAME_LABEL])
	jsonroster = data[TEAMROSTER_LABEL]
	for jsonteam in jsonroster:
		team = _json_to_team(jsonteam)
		league.add_team(team)
	return league

def season_to_json(season):
	data = {
		SEASON_LEAGUENAME_LABEL : season.league.leagueName,
		SEASON_WEEK_LABEL : season.week,
		SEASON_SCHEDULE_LABEL : season.schedule,
		SEASON_STANDINGS_LABEL : season.standings
	}
	return data


