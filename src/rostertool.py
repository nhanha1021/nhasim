from models import Player, Team, League, Season
from game import GameResult
import json

LEAGUE_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/data/"

def _to_league_file_name(name):
	return name.replace(" ","")+"_league.json"

def _to_season_file_name(name):
	return name.replace(" ","")+"_season.json"

def write_league(league):
	data = _league_to_json(league)
	filename = _to_league_file_name(league.get_league_name())
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def load_league(leagueName):
	filename = _to_league_file_name(leagueName)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return _json_to_league(data)

def write_season(season):
	data = _season_to_json(season)
	filename = _to_season_file_name(season.league.get_league_name())
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data,datafile)

def load_season(season_name):
	filename = _to_season_file_name(season_name)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return _json_to_season(data) 

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
SEASON_RESULTS_LABEL = "results"
GR_AWAY_TEAM = "away_team"
GR_HOME_TEAM = "home_team"
GR_AWAY_SCORE = "away_score"
GR_HOME_SCORE = "home_score"
GR_AWAY_EVENTS = "away_events"
GR_HOME_EVENTS = "home_events"

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
	
def _league_to_json(league):
	data = {
		LEAGUENAME_LABEL : league.leagueName
	}
	teamRoster = []
	for team in league.get_all_teams():
		teamRoster.append(_team_to_json(team))
	data[TEAMROSTER_LABEL] = teamRoster
	return data

def _json_to_league(data):
	league = League(data[LEAGUENAME_LABEL])
	jsonroster = data[TEAMROSTER_LABEL]
	for jsonteam in jsonroster:
		team = _json_to_team(jsonteam)
		league.add_team(team)
	return league

def _season_to_json(season):
	data = {
		SEASON_LEAGUENAME_LABEL : season.league.leagueName,
		SEASON_WEEK_LABEL : season.week,
		SEASON_SCHEDULE_LABEL : season.schedule,
		SEASON_STANDINGS_LABEL : season.standings,
		SEASON_RESULTS_LABEL : []
	}
	for week in season.results:
		week_results = []
		for result in week:
			week_results.append(_game_result_to_json(result))
		data[SEASON_RESULTS_LABEL].append(week_results)	
	return data

def _json_to_season(data):
	league = load_league(data[SEASON_LEAGUENAME_LABEL])
	schedule = data[SEASON_SCHEDULE_LABEL]
	week = data[SEASON_WEEK_LABEL]
	season = Season(league, schedule, week)
	season.standings = data[SEASON_STANDINGS_LABEL]
	results = []
	for jsonweek in data[SEASON_RESULTS_LABEL]:
		week_results = []
		for jsonresult in jsonweek:
			week_results.append(_json_to_game_result(jsonresult))
		results.append(week_results)
	season.results = results
	return season

def _game_result_to_json(game_result):
	data = {
		GR_AWAY_TEAM : _team_to_json(game_result.away_team),
		GR_AWAY_SCORE : game_result.away_score,
		GR_AWAY_EVENTS : game_result.away_events,
		GR_HOME_TEAM : _team_to_json(game_result.home_team),
		GR_HOME_SCORE : game_result.home_score,
		GR_HOME_EVENTS : game_result.home_events
	}
	return data

def _json_to_game_result(data):
	away_team = _json_to_team(data[GR_AWAY_TEAM])
	away_score = data[GR_AWAY_SCORE]
	away_events = data[GR_AWAY_EVENTS]
	home_team = _json_to_team(data[GR_HOME_TEAM])
	home_score = data[GR_HOME_SCORE]
	home_events = data[GR_HOME_EVENTS]
	return GameResult(away_team, away_score, away_events, home_team, home_score, home_events)


