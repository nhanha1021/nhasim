from models import Player
from models import Team
import rostertool
import json


p1 = rostertool.loadPlayer("John Shea")
print p1.getFullName()