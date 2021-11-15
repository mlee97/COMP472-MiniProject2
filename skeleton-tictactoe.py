# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

# Row/Column size
n = 0
# Size of blocks
b = 0
# Positions of the blocks 
b_positions = []
# The winning line-up size
s = 0
# Maximum depth of the adversarial search for player 1 and for player 2
d1 = 0
d2 = 0
# Maximum allowed time (in seconds) for your program to return a move
t = 0 
# Boolean to force the use of either minimax (FALSE) or alphabeta (TRUE)
a = False
# Play modes
p1 = ""
p2 = ""

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend

	def initialize_params(self):
		global n, b, b_positions, s, d1, d2, t, a, p1, p2
		
		n = 5 #int(input('enter the row/column size of the board: '))
		b = 3 #int(input('enter the number of blocks: '))
		b_positions = [[0,0], [2,1], [3,3]]
		#for i in range(b):
		#	x_position = int(input(F'enter the positions of the x-coordinate of block {i+1}: '))
		#	y_position = int(input(F'enter the positions of the y-coordinate of block {i+1}: '))
		#	b_positions.append([x_position, y_position])

		s = 3 #int(input('enter the winning line-up size: '))
		d1 = 2 #int(input('enter the maximum depth of the adversarial search for player 1: '))
		d2 = 2 #int(input('enter the maximum depth of the adversarial search for player 2: '))
		t = 2 #int(input('enter the maximum allowed time (in seconds) for your program to return a move: '))
		a = False #bool(input('enter boolean to force the use of either minimax (FALSE) or alphabeta (TRUE): '))
		p1 = "Human" #(input('enter the play mode of Player 1 (Human or AI): '))
		p2 = "AI" #(input('enter the play mode of Player 2 (Human or AI): '))



		
	def initialize_game(self):

		global n, b, b_positions, s, d1, d2, t, a, p1, p2

		# Ask user to specify all input parameters
		self.initialize_params()

		# Open Text File for the Game Trace
		open(F'gameTrace-{n}{b}{s}{t}.txt', 'w').close()
		game_trace_file = open(F'gameTrace-{n}{b}{s}{t}.txt', 'a')
		
		# Output the parameters
		game_trace_file.write(F'n={n} b={b} s={s} t={t} \n')

		# Output the position of the blocks
		game_trace_file.write(F'blocs={b_positions} \n\n')

		# Output player information

		game_trace_file.write(F"Player 1: {p1} d={d1} a={a} e1(regular) \n")
		game_trace_file.write(F"Player 2: {p2} d={d2} a={a} e1(defensive) \n\n")
		game_trace_file.close()

		# Specify the rows and columns
		rows, columns = (n, n)
		# Initialize nxn board with periods
		self.current_state = [['.']*columns for _ in range(rows)]

		# Set blocks on board
		for i in range(len(b_positions)):
			x = b_positions[i][0]
			y = b_positions[i][1] 
		
			self.current_state[x][y] = "*"

		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		global n, b, s, t
		game_trace_file = open(F'gameTrace-{n}{b}{s}{t}.txt', 'a')

		# Output Letters for Columns
		ch = 'A'
		game_trace_file.write("\n  ")
		for i in range (0, n):
			game_trace_file.write(ch)
			ch = chr(ord(ch) + 1)

		# Output Line
		str = "\n +"
		for i in range(0, n):
			str += "-"
		
		game_trace_file.write(str)

		row_count = 0

		# Output Game Board
		print()
		for x in range(0, n):
			game_trace_file.write(F"\n{row_count}|")
			row_count = row_count + 1
			for y in range(0, n):
				game_trace_file.write(F'{self.current_state[x][y]}')
			print()
		print()
		game_trace_file.close()

		
		
	def is_valid(self, px, py):
		global n
		if px < 0 or px >= n or py < 0 or py >= n:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		global n, s
		count = 0
		# Vertical win
		for y in range (0, n):
			for x in range(0, n):

				# If coordinate is empty or has block, do nothing
				if(self.current_state[x][y] == "." or self.current_state[x][y] == "*"):
					count = 0
				# Start counter at 1 everytime we return to the top
				elif (x==0):
					count = 1
				# If the state of the current index is the same as the previous one, increment counter 
				elif (self.current_state[x][y] == self.current_state[x-1][y]):
					count = count + 1
				# If the state of the current index is different as the previous one, return to 1
				else:
					count = 1
				# If the counter is equal to s, found a vertical s
				if(count == s):
					return self.current_state[x][y]

		# Horizontal win
		for x in range (0, n):
			for y in range(0, n):

				# If coordinate is empty or has block, do nothing
				if(self.current_state[x][y] == "." or self.current_state[x][y] == "*"):
					count = 0
				# Start counter at 1 everytime we return to start of a row
				elif (y==0):
					count = 1
				# If the state of the current index is the same as the previous one, increment counter 
				elif (self.current_state[x][y] == self.current_state[x][y-1]):
					count = count + 1
				# If the state of the current index is different as the previous one, return to 1
				else:
					count = 1
				# If the counter is equal to s, found a horizontal s
				if(count == s):
					return self.current_state[x][y]

		# Diagonal win

		cols = [[] for _ in range(n)]
		rows = [[] for _ in range(n)]
		fdiag = [[] for _ in range(n + n - 1)]
		bdiag = [[] for _ in range(len(fdiag))]
		min_bdiag = -n + 1

		for x in range(n):
			for y in range(n):
				fdiag[x+y].append(self.current_state[y][x])
				bdiag[x-y-min_bdiag].append(self.current_state[y][x])

		for x in range(0, len(fdiag)):
			count = 0
			# Find diagonal wins, only look at diagonals that are at least s-long
			if(len(fdiag[x]) >= s):
				for y in range(0, len(fdiag[x])):
					# If coordinate is empty or has block, do nothing
					if(fdiag[x][y] == "." or fdiag[x][y] == "*"):
						count = 0
					# Start counter at 1 everytime we return to start of a row
					elif (y==0):
						count = 1
					# If the state of the current index is the same as the previous one, increment counter 
					elif (fdiag[x][y] == fdiag[x][y-1]):
						count = count + 1
					# If the state of the current index is different as the previous one, return to 1
					else:
						count = 1
					# If the counter is equal to s, found a horizontal s
					if(count == s):
						return fdiag[x][y]
			if(len(bdiag[x]) >= s):
				for y in range(0, len(bdiag[x])):
					# If coordinate is empty or has block, do nothing
					if(bdiag[x][y] == "." or bdiag[x][y] == "*"):
						count = 0
					# Start counter at 1 everytime we return to start of a row
					elif (y==0):
						count = 1
					# If the state of the current index is the same as the previous one, increment counter 
					elif (bdiag[x][y] == bdiag[x][y-1]):
						count = count + 1
					# If the state of the current index is different as the previous one, return to 1
					else:
						count = 1
					# If the counter is equal to s, found a horizontal s
					if(count == s):
						return bdiag[x][y]

		# Is whole board full?
		for i in range(0, n):
			for j in range(0, n):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		game_trace_file = open(F'gameTrace-{n}{b}{s}{t}.txt', 'a')
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				game_trace_file.write('\n\nThe winner is X!')
			elif self.result == 'O':
				game_trace_file.write('\n\nThe winner is O!')
			elif self.result == '.':
				game_trace_file.write("\n\nIt's a tie!")
			#self.initialize_game()
		game_trace_file.close()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			p_column = int(input('enter the column [A, B, ..., N]: '))
			p_row = int(input('enter the row [0, 1, ... n-1]: '))
			if self.is_valid(p_column, p_row):
				return (p_column, p_row)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn
	
	# Heuristic #1. Simple, but fast to compute.
	def e1(self, x, y):
		global n
		node = self.current_state[x][y]
		count = 0
		adversary_count = 0

		# Only perform if it isn't the first row
		if(x!=0):

			if(self.current_state[x-1][y]==self.player_turn or self.current_state[x-1][y]=='.'):
				count = count + 1
			else:
				adversary_count = adversary_count + 1

			# Only perform if it isn't in the first column
			if(y!=0):
				if(self.current_state[x-1][y-1]==self.player_turn or self.current_state[x-1][y]=='.'):
					count = count + 1
				else:
					adversary_count = adversary_count + 1

			# Only perform if it isn't in the last column
			if(y!=n-1):
				if(self.current_state[x-1][y+1]==self.player_turn or self.current_state[x-1][y]=='.'):
					count = count + 1
				else:
					adversary_count = adversary_count + 1

				if(self.current_state[x][y+1]==self.player_turn or self.current_state[x-1][y]=='.'):
					count = count + 1
				else:
					adversary_count = adversary_count + 1
		
		# Ignore anything below if looking in last row
		if(x!=n-1):
			if(self.current_state[x+1][y]==self.player_turn or self.current_state[x-1][y]=='.'):
				count = count + 1
			else:
				adversary_count = adversary_count + 1
			if(y!=0):
				if(self.current_state[x+1][y-1]==self.player_turn or self.current_state[x-1][y]=='.'):
					count = count + 1
				else:
					adversary_count = adversary_count + 1
			if(y!=n-1):
				if(self.current_state[x+1][y+1]==self.player_turn or self.current_state[x-1][y]=='.'):
					count = count + 1
				else:
					adversary_count = adversary_count + 1
		
		# Look to the left if not in first column
		if(y!=0):
			if(self.current_state[x][y-1]==self.player_turn or self.current_state[x-1][y]=='.'):
				count = count + 1
			else:
				adversary_count = adversary_count + 1
		
		# Look to the right if not in last column
		if(y!=n-1):
			if(self.current_state[x][y+1]==self.player_turn or self.current_state[x-1][y]=='.'):
				count = count + 1
			else:
				adversary_count = adversary_count + 1

		if(self.player_turn == 'X'):
			return 7-count+adversary_count
		else:
			return -7+count+adversary_count
		
	
	"""
	Heuristic #2. Sophisticated, but slow to compute.

	1. Counts the # of consecutive X or O in a row, column and diagonal (including blank tiles), where the search span = s.
	2. Counts the # of surrounding blanks (including the player's piece).
	3. Counts the # consecutive pieces of the opponenent. This heuristic also prevents the other from winning.
	
	Parameters:
	- x: x position on the board.
	- y: y position on the board.
	"""
	def e2(self, x, y):
		global n, s
		consecutive_piece_count, blank_tile_count, adversary_consecutive_piece_count = 0
		lhs_out_of_bound = y-s+1 < 0
		rhs_out_of_bound = y+s-1 >= n

		# Count the the # of consecutive X or O in a row, column and diagonal (including blank tiles), where the search span = s
		
		# First, check the rows:
		for i in range (-s+1, s):
			for j in range (0, s):
				# Ignore all cases that are out of bounds
				if (lhs_out_of_bound or rhs_out_of_bound):
					pass # Do nothing
				
				elif(j==0):
					if(self.current_state[x][y+i] == self.player_turn):
						consecutive_piece_count = consecutive_piece_count + 1
					
				else:
					print('hi')

			

	def e3(self, x, y):
		global n, s
		blank_tile_count = 0
		vertical_consecutive_piece_count, horizontal_consecutive_piece_count, fdiag_consecutive_piece_count, bdiag_consecutive_piece_count = 1,1,1,1
		ad_vertical_consecutive_piece_count, ad_horizontal_consecutive_piece_count, ad_fdiag_consecutive_piece_count, ad_bdiag_consecutive_piece_count = 0,0,0,0
		continue_left = True
		continue_right = True
		continue_up = True
		continue_down = True
		continue_top_left_diag = True
		continue_top_right_diag = True
		continue_bottom_left_diag = True
		continue_bottom_right_diag = True

		# Count the the # of consecutive X or O in a row, column and diagonal (including blank tiles), where the search span = s
		
		# First, check the consective pieces of the current player:
		for i in range (1, s):

			#Find Bounds
			lhs = y-i >= 0
			rhs = y+i < n
			upper_bound = x-i >= 0
			lower_bound = x+i < n

			# Check horizontal directions
			if(continue_left and lhs):
				if(self.current_state[x][y-i]==self.player_turn):
					horizontal_consecutive_piece_count = horizontal_consecutive_piece_count + 1
				elif(self.current_state[x][y-i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_left == False
					
			if(continue_right and rhs):
				if(self.current_state[x][y+i]==self.player_turn):
					horizontal_consecutive_piece_count = horizontal_consecutive_piece_count + 1
				elif(self.current_state[x][y+i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_right == False
			
			#Automatic win detected
			if(horizontal_consecutive_piece_count >= s):
					if(self.player_turn=='O'):
						return 1
					else:
						return -1
					
			# Check vertical directions
			if(continue_up and upper_bound):
				if(self.current_state[x-i][y]==self.player_turn):
					vertical_consecutive_piece_count = vertical_consecutive_piece_count + 1
				elif(self.current_state[x-i][y]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_up == False
					
			if(continue_down and lower_bound):
				if(self.current_state[x+i][y]==self.player_turn):
					vertical_consecutive_piece_count = vertical_consecutive_piece_count + 1
				elif(self.current_state[x+i][y]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_down == False
			
			#Automatic win detected
			if(vertical_consecutive_piece_count >= s):
				if(self.player_turn=='O'):
					return 1
				else:
					return -1
				
			# Check diagonal directions
			if(continue_top_left_diag and lhs and upper_bound):
				if(self.current_state[x-i][y-i]==self.player_turn):
					fdiag_consecutive_piece_count = fdiag_consecutive_piece_count + 1
				elif(self.current_state[x-i][y-i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_top_left_diag == False
			
			if(continue_top_right_diag and rhs and upper_bound):
				if(self.current_state[x-i][y+i]==self.player_turn):
					bdiag_consecutive_piece_count = bdiag_consecutive_piece_count + 1
				elif(self.current_state[x-i][y+i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_top_right_diag == False
			
			if(continue_bottom_left_diag and lhs and lower_bound):
				if(self.current_state[x+i][y-i]==self.player_turn):
					bdiag_consecutive_piece_count = bdiag_consecutive_piece_count + 1
				elif(self.current_state[x+i][y-i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_bottom_left_diag == False
			
			if(continue_bottom_right_diag and rhs and lower_bound):
				if(self.current_state[x+i][y+i]==self.player_turn):
					fdiag_consecutive_piece_count = fdiag_consecutive_piece_count + 1
				elif(self.current_state[x+i][y+i]=='.'):
					blank_tile_count = blank_tile_count + 1
				# If blocked, stop search in this direction
				else:
					continue_bottom_right_diag == False
			
			#Automatic win detected
			if(fdiag_consecutive_piece_count >= s):
				if(self.player_turn=='O'):
					return 1
				else:
					return -1

			#Automatic win detected
			if(bdiag_consecutive_piece_count >= s):
				if(self.player_turn=='O'):
					return 1
				else:
					return -1
		 
		# Defensive strategy: Count the # of opponent pieces in range of s that contains 2 or more of their pieces. This prevents the other from winning.
		# Formula: 2*s  * (number of consec opponent pieces - 1)
		if self.player_turn == 'X':
			opponent = 'O'
		else:
			opponent = 'X'

		# Reset all continue boolean variables
		continue_left = True
		continue_right = True
		continue_up = True
		continue_down = True
		continue_top_left_diag = True
		continue_top_right_diag = True
		continue_bottom_left_diag = True
		continue_bottom_right_diag = True
			
		for i in range (1, s):
			# Check horizontal directions
			if(continue_left and lhs):
				if(self.current_state[x][y-i]!=self.player_turn):
					ad_horizontal_consecutive_piece_count = ad_horizontal_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_left == False
					
			if(continue_right and rhs):
				if(self.current_state[x][y+i]!=self.player_turn):
					ad_horizontal_consecutive_piece_count = ad_horizontal_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_right == False
					
			# Check vertical directions
			if(continue_up and upper_bound):
				if(self.current_state[x-i][y]!=self.player_turn):
					ad_vertical_consecutive_piece_count = ad_vertical_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_up == False
					
			if(continue_down and lower_bound):
				if(self.current_state[x+i][y]!=self.player_turn):
					ad_vertical_consecutive_piece_count = ad_vertical_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_down == False
				
			# Check diagonal directions
			if(continue_top_left_diag and lhs and upper_bound):
				if(self.current_state[x-i][y-i]!=self.player_turn):
					ad_fdiag_consecutive_piece_count = ad_fdiag_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_top_left_diag == False
			
			if(continue_top_right_diag and rhs and upper_bound):
				if(self.current_state[x-i][y+i]!=self.player_turn):
					ad_bdiag_consecutive_piece_count = ad_bdiag_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_top_right_diag == False
			
			if(continue_bottom_left_diag and lhs and lower_bound):
				if(self.current_state[x+i][y-i]!=self.player_turn):
					ad_bdiag_consecutive_piece_count = ad_bdiag_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_bottom_left_diag == False
			
			if(continue_bottom_right_diag and rhs and lower_bound):
				if(self.current_state[x+i][y+i]!=self.player_turn):
					ad_fdiag_consecutive_piece_count = ad_fdiag_consecutive_piece_count + 1
				# If blocked, stop search in this direction
				else:
					continue_bottom_right_diag == False
				
		if(horizontal_consecutive_piece_count >= s or 
		vertical_consecutive_piece_count >= s or 
		fdiag_consecutive_piece_count >= s or 
		bdiag_consecutive_piece_count >= s):
			if(self.player_turn == 'X'):
				return -1
			else:
				return 1
		else:
			value = horizontal_consecutive_piece_count + vertical_consecutive_piece_count + fdiag_consecutive_piece_count + bdiag_consecutive_piece_count
			ad_value = ad_horizontal_consecutive_piece_count + ad_vertical_consecutive_piece_count + ad_fdiag_consecutive_piece_count + ad_bdiag_consecutive_piece_count
			heuristic_value = 6*(4*(2*s-1))-(3*value) - (blank_tile_count) - (2*s  * (ad_value - 1))
			if(self.player_turn == 'X'):
				return heuristic_value
			else:
				return -heuristic_value

	def minimax(self, max=False, e1=True):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		global n

		if e1:
			value = 8 # Worst value for X, -1 is win for X
			if max:
				value = -8 # Worst value for O, 1 is win for O
		else:
			value = 6*(4*(2*s-1))
			if max:
				value = -6*(4*(2*s-1))
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						if(e1 == True):
							v = self.e1(i, j)
						else:
							v = self.e3(i, j)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						if(e1 == True):
							v = self.e1(i, j)
						else:
							v = self.e3(i, j)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, max=False, e1=True):
		global n, s
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		if e1:
			alpha = -8
			beta = 8
			value = 8
			if max:
				value = -8
		else:
			alpha = -6*(4*(2*s-1))
			beta = 6*(4*(2*s-1))
			value = 6*(4*(2*s-1))
			if max:
				value = -6*(4*(2*s-1))

		x = None
		y = None
		result = self.is_end()

		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)

		for i in range(0, n):
			for j in range(0, n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						#(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if(e1 == True):
							v = self.e1(i, j)
						else:
							v = self.e3(i, j)
						if v > value:
							# v > -8
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						#(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if(e1 == True):
							v = self.e1(i, j)
						else:
							v = self.e3(i, j)
						if v < value:
							# v < 8
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		global n, b, s, t
	
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			game_trace_file = open(F'gameTrace-{n}{b}{s}{t}.txt', 'a')
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False, e1=True)
				else:
					(_, x, y) = self.minimax(max=True, e1=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False, e1=True)
				else:
					(m, x, y) = self.alphabeta(max=True, e1=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						game_trace_file.write(F'\nEvaluation time: {round(end - start, 7)}s\n')
						game_trace_file.write(F'Recommended move: x = {x}, y = {y}\n')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						game_trace_file.write(F'\nEvaluation time: {round(end - start, 7)}s\n')
						game_trace_file.write(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}\n')
			self.current_state[x][y] = self.player_turn
			self.switch_player()
			game_trace_file.close()

def main():
	g = Game(recommend=True)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	#g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

