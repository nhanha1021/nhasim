from models import League, Team
from tabulate import tabulate
from game import Game
from os import system
import json, rostertool, sys

league = rostertool.loadLeague("UMASS")
puffton = league.getTeam("puffton")
pelham = league.getTeam("pelham")
game = Game(pelham, puffton)
winner = game.playGame()
print winner.teamName