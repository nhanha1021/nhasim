from models import DraftClass
from rostereditor import DraftShell
import rostertool

league = rostertool.loadLeague("USFL")
draft_class = DraftClass("Test Class")
draft_shell = DraftShell(league,draft_class)
draft_shell.run()