import rostertool, random
from game import Game

def shift(array):
	start = array.pop(0)
	array.append(start)

def sort_matches(teams_a, teams_h):
	if((len(teams_a)==0) or (len(teams_h)==0)):
		return
	group = []
	for i in range(len(teams_a)):
		for j in range(len(teams_a)):
			group.append(Game(teams_a[j],teams_h[j]))
		shift(teams_a)
	teams_a1 = teams_a[:len(teams_a)/2]
	teams_a2 = teams_a[len(teams_a)/2:]
	teams_h1 = teams_h[:len(teams_h)/2]
	teams_h2 = teams_h[len(teams_h)/2:]
	group.append([sort_matches(teams_a1,teams_a2),sort_matches(teams_h1,teams_h2)])
	return group

def get_matches(teams): 
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
	L1_1_1_1 = L1_1_1[len(L1_1_1)-1][0]
	L1_1_1_2 = L1_1_1[len(L1_1_1)-1][1]
	L1_1_2_1 = L1_1_2[len(L1_1_2)-1][0]
	L1_1_2_2 = L1_1_2[len(L1_1_2)-1][1]
	L1_2_1_1 = L1_2_1[len(L1_2_1)-1][0]
	L1_2_1_2 = L1_2_1[len(L1_2_1)-1][1]
	L1_2_2_1 = L1_2_2[len(L1_2_2)-1][0]
	L1_2_2_2 = L1_2_2[len(L1_2_2)-1][1]

	A = L1[:len(L1)-1]
	B = L1_1[:len(L1_1)-1]
	C = L1_2[:len(L1_1)-1]
	D = L1_1_1[:len(L1_1_1)-1]
	E = L1_1_2[:len(L1_1_2)-1]
	F = L1_2_1[:len(L1_2_1)-1]
	G = L1_2_2[:len(L1_2_2)-1]
	H = L1_1_1_1[:len(L1_1_1_1)-1]
	I = L1_1_1_2[:len(L1_1_1_2)-1]
	J = L1_1_2_1[:len(L1_1_2_1)-1]
	K = L1_1_2_2[:len(L1_1_2_2)-1]
	L = L1_2_1_1[:len(L1_2_1_1)-1]
	M = L1_2_1_2[:len(L1_2_1_2)-1]
	N = L1_2_2_1[:len(L1_2_2_1)-1]
	O = L1_2_2_2[:len(L1_2_2_2)-1]

	weeks = []
	weeks.append(A[0:8])
	weeks.append(A[8:16])
	weeks.append(A[16:24])
	weeks.append(A[24:32])
	weeks.append(A[32:40])
	weeks.append(A[40:48])
	weeks.append(A[48:56])
	weeks.append(A[56:64])
	weeks.append(B[0:4]+C[0:4])
	weeks.append(B[4:8]+C[4:8])
	weeks.append(B[8:12]+C[8:12])
	weeks.append(B[12:16]+C[12:16])
	weeks.append(D[0:2]+E[0:2]+F[0:2]+G[0:2])
	weeks.append(D[2:4]+E[2:4]+F[2:4]+G[2:4])
	weeks.append(H+I+J+K+L+M+N+O)
 	return weeks

def make_schedule(teams):
	random.shuffle(teams)
	ta = teams[:len(teams)/2]
	tb = teams[len(teams)/2:]
	t = ta+tb
	random.shuffle(ta)
	random.shuffle(tb)
	rt = tb+ta
	schedule = get_matches(t) + get_matches(rt)
	random.shuffle(schedule)
	return schedule