import random
from math import *

def getFirstName():

	firstNames = []
	with open("../res/malenames.txt",'r') as f:
		firstNames = list(f)
		firstNames = [x.strip() for x in firstNames]
	x = random.random()*100
	f = 0
	if(x<66.6):
		f = int(1.5*x)
	else:
		f = int(exp(x/14.5))
	return firstNames[f]

def getLastName():

	lastNames = []
	with open("../res/lastnames.txt",'r') as f:
		lastNames = list(f)
		lastNames = [x.strip() for x in lastNames]
	x = random.random()*100
	f = 0
	if(f<77.7):
		f=int(6.4365*x)
	else:
		f=int(exp(x/12.5))
	return lastNames[f]

def getFullName():

	name = getFirstName()+" "+getLastName()
	return name

