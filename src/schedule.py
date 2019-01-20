import random

def make_schedule(t):

	def get_matches(t):

		def rotate(t0):
			t = t0[1:]
			end = t.pop(len(t)-1)
			t.insert(0,end)
			t.insert(0,t0[0])
			return t

		original_matches = []
		for w in range(len(t)-1):
			a = t[:len(t)/2]
			h = t[len(t)/2:]
			h.reverse()
			week = []
			for i in range(len(a)):
				week.append([a[i],h[i]])
			original_matches.append(week)
			t = rotate(t)
		
		reverse_matches = []
		for week in original_matches:
			w = []
			for game in week:
				w.append([game[1],game[0]])
			reverse_matches.append(w)

		matches = original_matches + reverse_matches
		return matches

	#shuffle the order of teams
	random.shuffle(t)
	#get matches
	schedule = get_matches(t)
	#shuffle the weeks
	for i in range(5):
		random.shuffle(schedule)
	#append keys to end of each matchup and convert to tuple
	for w in range(len(schedule)):
		for g in range(len(schedule[w])):
			schedule[w][g].insert(2,(w,g))
			schedule[w][g] = tuple(schedule[w][g])

	return schedule