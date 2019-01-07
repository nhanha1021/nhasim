from models import DraftClass

draft_class = DraftClass("Test Class")
for info in draft_class.get_candidates_info():
	print info[0],info[1],info[2],info[3]

num1 = draft_class.draft_candidate(0,"Boston")
num2 = draft_class.draft_candidate(3,"New York")

for info in draft_class.get_candidates_info():
	print info[0],info[1],info[2],info[3]

print draft_class.get_draft_results()






