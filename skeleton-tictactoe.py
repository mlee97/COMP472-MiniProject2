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
		b_positions = [[1,1], [2,1], [3,2]]
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

		global n, b, b_positions, s, d1, d2, t, a, p_modes

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
		game_trace_file.write(F"Player 2: {p1} d={d2} a={a} e1(defensive) \n\n")
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
		global n
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

		# Output Game Board
		print()
		for y in range(0, n):
			for row in range (0, n):
				game_trace_file.write(F"\n{row}|")
				for x in range(0, n):
					game_trace_file.write(F'{self.current_state[x][y]}')
				print()
		print()

		
		
	def is_valid(self, px, py):
		global n
		if px < 0 or px >= n or py < 0 or py >= n:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		global n
		# Vertical win
		for i in range(0, n):
			if (self.current_state[0][i] != '.' and
				self.current_state[0][i] == self.current_state[1][i] and
				self.current_state[1][i] == self.current_state[2][i]):
				return self.current_state[0][i]
		# Horizontal win
		for i in range(0, 3):
			if (self.current_state[i] == ['X', 'X', 'X']):
				return 'X'
			elif (self.current_state[i] == ['O', 'O', 'O']):
				return 'O'
		# Main diagonal win
		if (self.current_state[0][0] != '.' and
			self.current_state[0][0] == self.current_state[1][1] and
			self.current_state[0][0] == self.current_state[2][2]):
			return self.current_state[0][0]
		# Second diagonal win
		if (self.current_state[0][2] != '.' and
			self.current_state[0][2] == self.current_state[1][1] and
			self.current_state[0][2] == self.current_state[2][0]):
			return self.current_state[0][2]
		# Is whole board full?
		for i in range(0, 3):
			for j in range(0, 3):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			#self.initialize_game()
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

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
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
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

