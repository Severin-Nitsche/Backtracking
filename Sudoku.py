import random
import sys
import getopt

#Sudoku generator

def createSudoku():
	base = {}
	for i in range(0,9):
		base[i] = {}
		for j in range(0,9):
			base[i][j] =(j+i*3+int(i/3))%9+1
	return base;
	
def shuffle(base, n):
	for j in range(0,n):
		for i in range(0,3):
			r1 = random.randint(0,2)
			r2 = random.randint(0,2)
			temp = base[i*3+r1]
			base[i*3+r1] = base[i*3+r2]
			base[i*3+r2] = temp;
		for i in range(0,3):
			r1 = random.randint(0,2)
			r2 = random.randint(0,2)
			swap(base,r1+i*3,r2+i*3)

def swap(base,c1,c2):
	for i in range(0,9):
		temp = base[i][c1]
		base[i][c1] = base[i][c2]
		base[i][c2] = temp

def row(sudoku,n):
	for i in range(0,9):
		yield sudoku[n][i]

def col(sudoku,n):
	for i in range(0,9):
		yield sudoku[i][n];

def block(sudoku,n):
	for i in range(0,3):
		for j in range(0,3):
			yield sudoku[int(n/3)*3+i][(n%3)*3+j]

def validateCount(count):
	for i in range (1,10):
		if i in count:
			if count[i] is not 1:
				return False
	return True	
	
def count(validator,j):
	if j in validator:
		validator[j] = validator[j]+1;
	else:
		validator[j] = 1;
		
def getGroup(group):
	if group is 0:
		return row
	elif group is 1:
		return col
	elif group is 2:
		return block

def groups():
	for i in range(0,3):
		yield getGroup(i)
								
def validate(sudoku):
	for i in range(0,9):
		for group in groups():
			validator = {}
			for j in group(sudoku,i):
				count(validator,j)
			if not validateCount(validator):
				#print("failed in iteration:"+str(i)+" @ group:"+str(group))
				return False;
	return True;
	
def removeFrom(sudoku):
	while True:
		r1 = random.randint(0,8)
		r2 = random.randint(0,8)
		if sudoku[r1][r2] is not 0:
			temp = sudoku[r1][r2]
			sudoku[r1][r2] = 0
			return [r1,r2,temp]
			
def show(sudoku):
	for i in range(0,9):
		if i is not 0:
			if i%3 is 0:
				print("\n===================================")
			else:
				print("\n-----------------------------------")
		for j in range(0,9):
			if sudoku[i][j] is not 0:
				if j is not 8:
					if j%3 is 2:
						print(sudoku[i][j], end = " || ")
					else:
						print(sudoku[i][j], end = " | ")
				else:
					print(sudoku[i][j], end = " ")
			else:
				if j is not 8:
					if j%3 is 2:
						print(" ", end = " || ")
					else:
						print(" ", end = " | ")
				else:
					print(" ", end = " ")
	print("\n")
									
def solve(sudoku):
	empty = []
	for i in range(0,9):
		for j in range(0,9):
			if sudoku[i][j] is 0:
				empty.append([i,j,0])
	count = 0
	f = 0
	while True:
		while f < len(empty):
			#print(f)
			i = empty[f][0]
			j = empty[f][1]
			v = empty[f][2]
			while True:
				sudoku[i][j] = empty[f][2] + 1
				empty[f][2] = sudoku[i][j]
				if sudoku[i][j] > 9:
					empty[f][2] = 0
					sudoku[i][j] = 0
					f = f - 2
					if f < -1:
						return count
				if validate(sudoku):
					break
			f = f + 1
		#show(sudoku)
		f = len(empty) - 2
		empty[-1][2] = 0
		sudoku[empty[-1][0]][empty[-1][1]] = 0
		count = count + 1

def create(holes, shuffles):
	sudoku = createSudoku()
	shuffle(sudoku, shuffles)
	i = 0
	while i < holes:
		i = i + 1
		temp = removeFrom(sudoku)
		if solve(sudoku) is not 1:
			sudoku[temp[0]][temp[1]] = temp[2]
			i = i - 1
	return sudoku
	
#sudoku = createSudoku()
#shuffle(sudoku,100)
#for i in range(0,50):
	#removeFrom(sudoku)

try:
	opts, args = getopt.getopt(sys.argv[1:], "h:s:", ["holes=","shuffles="])
except getopt.GetoptError:
	print("usage: -h <holes> -s <shuffles>")
	sys.exit(2)

holes = 0
shuffles = 0

for opt, arg in opts:
	if opt in ("-h","--holes"):
		holes = int(arg)
	elif opt in ("-s","--shuffles"):
		shuffles = int(arg)

sudoku = create(holes,shuffles)
#print("found "+str(solve(sudoku))+" solutions")
show(sudoku)
