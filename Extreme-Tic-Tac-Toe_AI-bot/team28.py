import sys
import random
import signal
from time import time
import copy

class Team28:

	def __init__(self):
		self.maxval = 1000000000
		self.default_depth = 3
		self.vari = 0
		self.cellval = (  0 , 1 , 10 , 100 , 1000 )
		self.blkval = ( 0 , 1000 , 10000 , 100000, 1000000 ) #boardmap
		self.corners = (0, 20, 200, 2000, 20000) #(0,3),(3,0),(0,0),(3,3)
		self.edges = (0, 10, 100, 1000, 10000) #(0,1),(0,2),(3,1),(3,2),(1,0),(2,0),(1,3),(2,3)
		self.startTime = 0
		self.stopTime = False
		self.timeLimit = 15
		self.best1 = 0
		self.best2 = 0
		# self.maxvalTime = 0
		#self.cnt = 0

	

	def row_col_eval(self,board):
		arr = [[ 0 for i in range(4)] for j in range(4)] #block-h
		Hval = 0
		flg = 0
		for i in range(4):
			for j in range(4):

				#rows
				flg = 1	#
				#print flg
				for u in range(4*i, 4*i+4):
					count_o = 0
					count_x = 0
					for v in range(4*j, 4*j+4):
						if board.board_status[u][v] == 'o':
							count_o+= 1
						elif board.board_status[u][v] == 'x':
							count_x+= 1
					if count_x > 0 and count_o == 0:
						arr[i][j] += self.cellval[count_x]
					elif count_x == 0 and count_o > 0 :
						arr[i][j] -= self.cellval[count_o]


				#clm
				flg = 2	#
				#print flg
				for u in range(4*j, 4*j + 4):
					count_o = 0
					count_x = 0
					for v in range(4*i , 4*i + 4):
						if board.board_status[v][u] == 'o':
							count_o+= 1
						elif board.board_status[v][u] == 'x':
							count_x+= 1
					if count_x > 0 and count_o == 0:
						arr[i][j] += self.cellval[count_x]
					elif count_x == 0 and count_o > 0 :
						arr[i][j] -= self.cellval[count_o]

				
		#rows
		for u in range(4):
			flag = 0
			count_o = 0
			count_x = 0
			ocnt = 0
			xcnt = 0
			if(u==0 or u==3):
				flag=1
			for v in range(4):
				if(flag==1 and (v==1 or v==2)):
					if(board.block_status[u][v] == 'o'):
						ocnt+=1
					elif(board.block_status[u][v] == 'x'):
						xcnt+=1

				if board.block_status[u][v] == 'o':
					count_o+= 1
				elif board.block_status[u][v] == 'x':
					count_x+= 1
			if (count_x == 0 or count_o  == 0):
				if count_x == 0 and count_o > 0 :
					Hval -= self.blkval[count_o]
				elif count_x > 0 and count_o == 0:
					Hval += self.blkval[count_x]
				for v in range(4):
					if board.block_status[u][v] == '-':
						Hval += arr[u][v]
				Hval -= self.edges[ocnt]
			Hval += self.edges[xcnt]  

		#clm
		for u in range(4):
			flag = 0
			count_o = 0
			count_x = 0
			ocnt = 0
			xcnt = 0
			if(u==0 or u==3):
				flag=1
			for v in range(4):
				if(flag==1 and (v==1 or v==2)):
					if(board.block_status[v][u] == 'o'):
						ocnt+=1
					elif(board.block_status[v][u] == 'x'):
						xcnt+=1
				if board.block_status[v][u] == 'o':
					count_o+= 1
				elif board.block_status[v][u] == 'x':
					count_x+= 1
			if (count_x == 0 or count_o  == 0):

				if count_x == 0 and count_o > 0 :
					Hval -= self.blkval[count_o]
				elif count_x > 0 and count_o == 0:
					Hval += self.blkval[count_x]
				for v in range(4):
					if board.block_status[v][u] == '-':
						Hval += arr[v][u]
			Hval -= self.edges[ocnt]
			Hval += self.edges[xcnt]

		ocnt1=0
		xcnt1=0
		if(board.block_status[0][0] == 'o'):
			ocnt1+=1
		elif(board.block_status[0][0] == 'x'):
			xcnt1+=1
		if(board.block_status[0][3] == 'o'):
			ocnt1+=1
		elif(board.block_status[0][3] == 'x'):
			xcnt1+=1
		if(board.block_status[3][0] == 'o'):
			ocnt1+=1
		elif(board.block_status[3][0] == 'x'):
			xcnt1+=1
		if(board.block_status[3][3] == 'o'):
			ocnt1+=1
		elif(board.block_status[3][3] == 'x'):
			xcnt1+=1
		Hval += self.corners[xcnt1]
		Hval -= self.corners[ocnt1]
		return Hval

	def heuristic(self,board):
		return self.row_col_eval(board) + self.diamond_eval(board)
		
	def minimax(self, board, old_move, depth, flag, alpha, beta): #converted to only depth2
		if(time() - self.startTime >= self.timeLimit - 0.01):
			print time()
			if flag == 'x':
				self.stopTime = True
				return self.best2
			elif flag == 'o':
				self.stopTime = True
				return self.best1

		status = board.find_terminal_state()

		if (depth==0) or (status[1] == 'WON') or (status[1] == 'DRAW'):
			return self.heuristic(board)

		if flag=='x':
			self.best1 = -self.maxval 
			cells = board.find_valid_move_cells(old_move)
			if len(cells) == 0:
				return self.heuristic(board)
			for cell in cells:
				board.board_status[cell[0]][cell[1]] = flag
				self.best1 = max(self.best1,self.minimax(board,(cell[0],cell[1]),depth-1,chr(ord('x')+ord('o')-ord(flag)),alpha,beta))
				board.board_status[cell[0]][cell[1]] = '-'
				if(self.stopTime == True):
					#return self.best1
					break
				alpha = max(alpha, self.best1)
				if (beta <= alpha):
					break
			return self.best1

		elif flag=='o':
			self.best2 = self.maxval 
			cells = board.find_valid_move_cells(old_move)
			if len(cells) == 0:
				return self.heuristic(board)
			for cell in cells:
				board.board_status[cell[0]][cell[1]] = flag
				self.best2 = min(self.best2,self.minimax(board,(cell[0],cell[1]),depth-1,chr(ord('x')+ord('o')-ord(flag)),alpha,beta))
				board.board_status[cell[0]][cell[1]] = '-'
				if(self.stopTime == True):
					#return self.best2
					break
				beta = min(beta, self.best2)
				if (beta <= alpha):
					break
			return self.best2
	#block_check each row 2 comp if 3rd one
	def box_check(self,board,old_move,ply): #opposite
		#(3,2) rows=> (3)*4 to (3+1)*4 
		# col=> (2)*4 to (2+1)*4
		x = old_move[0]%4 #(0,0)
		y = old_move[1]%4
		#print x 
		#print y
		bs = board.board_status
		#checking if a block has been won or drawn or not after the current move
		arr = []
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if ((bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == ply) and bs[4*x+i][4*y+3] == '-'): #== bs[4*x+i][4*y+3]):
				arr.append((4*x+i,4*y+3))
			if ((bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+3] == ply) and bs[4*x+i][4*y+2] == '-'): #== bs[4*x+i][4*y+3]):
				arr.append((4*x+i,4*y+2))
			if ((bs[4*x+i][4*y] == bs[4*x+i][4*y+3] == bs[4*x+i][4*y+2] == ply) and bs[4*x+i][4*y+1] == '-'): #== bs[4*x+i][4*y+3]):
				arr.append((4*x+i,4*y+1))
			if ((bs[4*x+i][4*y+3] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == ply) and bs[4*x+i][4*y] == '-'): #== bs[4*x+i][4*y+3]):
				arr.append((4*x+i,4*y))

			#checking col    
			#checking for vertical pattern(i'th column)
			if ((bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == ply) and bs[4*x+3][4*y+i] == '-'):
				arr.append((4*x+3,4*y+i))
				
			if ((bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+3][4*y+i] == ply) and bs[4*x+2][4*y+i] == '-'):
				arr.append((4*x+2,4*y+i))
			if ((bs[4*x][4*y+i] == bs[4*x+3][4*y+i] == bs[4*x+2][4*y+i] == ply) and bs[4*x+1][4*y+i] == '-'):
				arr.append((4*x+1,4*y+i))
			if ((bs[4*x+3][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == ply) and bs[4*x][4*y+i] == '-'): #(0,1)
				arr.append((4*x,4*y+i)) #(0,1)

		for i in range(0,2):
			for j in range(1,3): #i,j i+1,j-1 i+1,j+1, i+2,j
				if((bs[4*x+i][4*y+j] == bs[4*x+i+1][4*y+j-1] == bs[4*x+i+1][4*y+j+1] == ply) and bs[4*x+i+2][4*y+j]=='-'):
					arr.append((4*x+i+2,4*y+j))
				if((bs[4*x+i][4*y+j] == bs[4*x+i+2][4*y+j] == bs[4*x+i+1][4*y+j+1] == ply) and bs[4*x+i+1][4*y+j-1]=='-'):
					arr.append((4*x+i+1,4*y+j-1))
				if((bs[4*x+i][4*y+j] == bs[4*x+i+1][4*y+j-1] == bs[4*x+i+2][4*y+j] == ply) and bs[4*x+i+1][4*y+j+1]=='-'):
					arr.append((4*x+i+1,4*y+j+1))
				if((bs[4*x+i+2][4*y+j] == bs[4*x+i+1][4*y+j-1] == bs[4*x+i+1][4*y+j+1] == ply) and bs[4*x+i][4*y+j]=='-'):
					arr.append((4*x+i,4*y+j))
		return arr
	def move(self, board, old_move, flag):
		self.startTime = time()
		#print self.startTime
		#self.stopTime =	1
		#print "old_move:"
		#print old_move
		cells = board.find_valid_move_cells(old_move)   
		ind_row = -1
		ind_col = -1
		i_row = -1
		i_col = -1
		if (flag=='x'):
			maxval = -self.maxval 
			self.vari = 'o'

		elif (flag=='o'):
			minval = self.maxval  
			self.vari = 'x'

		
		depth = self.default_depth #3

		if old_move == (-1,-1): #if (-1,-1) len(cells) > 16
			depth = self.default_depth - 1 	#2
		flg = 0
		arr3 = []
		arr4 = []
		val1 = self.box_check(board,old_move,flag) #x game win kataniki
		if(len(val1)!=0):
			for sd1 in val1:
				if(sd1 in cells):
					arr4.append(sd1)
			if(len(arr4) != 0):
				cells = arr4
				flg = 1
				print "123there"

		else:
			val = self.box_check(board,old_move,self.vari) #o position block chesidi
			for sd in val:
				if(sd in cells):
					arr3.append(sd)
			if(len(arr3) != 0):
				cells = arr3

		for cell in cells:
			if(time() - self.startTime >= self.timeLimit - 0.01):
				break
			board.board_status[cell[0]][cell[1]] = flag
			moveval = self.minimax(board, (cell[0],cell[1]), depth, self.vari, -self.maxval, self.maxval)
			board.board_status[cell[0]][cell[1]] = '-'
			
			if flag=='x' and moveval>maxval and (not (len(self.box_check(board,(cell[0],cell[1]),self.vari))) or flg == 1): #update max value
				maxval = moveval
				ind_row = cell[0]
				ind_col = cell[1]
			elif flag == 'x' and moveval>maxval:
				maxval = moveval
				i_row = cell[0]
				i_col = cell[1]
			
			if flag=='o' and moveval<minval and (not (len(self.box_check(board,(cell[0],cell[1]),self.vari))) or flg == 1): #update min value
				minval = moveval
				ind_row = cell[0]
				ind_col = cell[1]
			elif flag == 'o' and moveval<minval:
				minval = moveval
				i_row = cell[0]
				i_col = cell[1]
		print ind_row
		print ind_col
		if(ind_row == -1 and ind_col == -1):
			return (i_row,i_col)
		else:	
			return (ind_row,ind_col)

	def diamond_eval(self, board):
		arr = [[ 0 for i in range(4)] for j in range(4)] #block-h
		Hval = 0
		for i in range(0,2): #0 and 1
			count_x = 0
			count_o = 0
			
			for j in range(1,3):	#4 outer diamonds 
				
				for u in range(0,2):
					for v in range(1,3):  # 4 diamonds inside each
						cdiam1_stat = 2
						cdiam1_count = 0
						if(board.board_status[4 * i + u][4 * j + v] == 'd' or board.board_status[4 * i + u + 1][4 * j + v - 1] == 'd' or
						   board.board_status[4 * i + u + 1][4 * j + v + 1] == 'd' or board.board_status[4 * i + u + 2][4 * j + v] == 'd'):
							cdiam1_stat = 0

						elif((board.board_status[4 * i + u][4 * j + v] == 'o' or board.board_status[4 * i + u][4 * j + v] == '-') and
							 (board.board_status[4 * i + u+1][4 * j + v-1] == 'o' or board.board_status[4 * i + u+1][4 * j + v-1] == '-') and
							 (board.board_status[4 * i + u+1][4 * j + v+1] == 'o' or board.board_status[4 * i + u+1][4 * j + v+1] == '-') and
							 (board.board_status[4 * i + u+2][4 * j + v] == 'o' or board.board_status[4 * i + u+2][4 * j + v] == '-')):
							cnt = 0
							if(board.board_status[4 * i + u][4 * j + v] == 'o'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+1][4 * j + v-1] == 'o'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+1][4 * j + v+1] == 'o'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+2][4 * j + v] == 'o'):
								cnt = cnt + 1
							cdiam1_count = cnt
							cdiam1_stat = -1

						elif((board.board_status[4 * i + u][4 * j + v] == 'x' or board.board_status[4 * i + u][4 * j + v] == '-') and
							 (board.board_status[4 * i + u+1][4 * j + v-1] == 'x' or board.board_status[4 * i + u+1][4 * j + v-1] == '-') and
							 (board.board_status[4 * i + u+1][4 * j + v+1] == 'x' or board.board_status[4 * i + u+1][4 * j + v+1] == '-') and
							 (board.board_status[4 * i + u+2][4 * j + v] == 'x' or board.board_status[4 * i + u+2][4 * j + v] == '-')):
							cnt = 0
							if(board.board_status[4 * i + u][4 * j + v] == 'x'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+1][4 * j + v-1] == 'x'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+1][4 * j + v+1] == 'x'):
								cnt = cnt + 1
							if(board.board_status[4 * i + u+2][4 * j + v] == 'x'):
								cnt = cnt + 1
							cdiam1_count = cnt
							cdiam1_stat = 1

						elif(not(board.board_status[4 * i + u][4 * j + v] == '-' or board.board_status[4 * i + u+1][4 * j + v-1] == '-' or
								 board.board_status[4 * i + u+1][4 * j + v+1] == '-' or board.board_status[4 * i + u+2][4 * j + v] == '-')):
							cdiam1_stat = 0
						# cd_won cdwts[]
						if cdiam1_stat == 1:  # x won a row
							arr[i][j] += self.cellval[cdiam1_count]
						elif cdiam1_stat == -1:  # o won a row
							arr[i][j] -= self.cellval[cdiam1_count]
						elif cdiam1_stat == 2:  # not completed
							pass

		#######################################################################################		
		for i in range(0,2): #0 and 1
			count_x = 0
			count_o = 0
			
			for j in range(1,3): #1 and 2 =>(0,1) , (0,2), (1,1), (1,2)
				diam1_stat = 2
				diam1_count = 0
				if(board.block_status[i][j] == 'd' or board.block_status[i+1][j-1] == 'd' or board.block_status[i+1][j+1] == 'd' or board.block_status[i+2][j] == 'd'):
					diam1_stat = 0

				elif((board.block_status[i][j] == 'o' or board.block_status[i][j] == '-') and (board.block_status[i+1][j-1] == 'o' or board.block_status[i+1][j-1] == '-') and
					 (board.block_status[i+1][j+1] == 'o' or board.block_status[i+1][j+1] == '-') and (board.block_status[i+2][j] == 'o' or board.block_status[i+2][j] == '-')):
					cnt = 0
					if(board.block_status[i][j] == 'o'):
						cnt = cnt + 1
					if(board.block_status[i+1][j-1] == 'o'):
						cnt = cnt + 1
					if(board.block_status[i+1][j+1] == 'o'):
						cnt = cnt + 1
					if(board.block_status[i+2][j] == 'o'):
						cnt = cnt + 1
					diam1_count = cnt
					diam1_stat = -1

				elif((board.block_status[i][j] == 'x' or board.block_status[i][j] == '-') and (board.block_status[i+1][j-1] == 'x' or board.block_status[i+1][j-1] == '-') and
					 (board.block_status[i+1][j+1] == 'x' or board.block_status[i+1][j+1] == '-') and (board.block_status[i+2][j] == 'x' or board.block_status[i+2][j] == '-')):
					cnt = 0
					if(board.block_status[i][j] == 'x'):
						cnt = cnt + 1
					if(board.block_status[i+1][j-1] == 'x'):
						cnt = cnt + 1
					if(board.block_status[i+1][j+1] == 'x'):
						cnt = cnt + 1
					if(board.block_status[i+2][j] == 'x'):
						cnt = cnt + 1
					diam1_count = cnt
					diam1_stat = 1

				elif(not(board.block_status[i][j] == '-' or board.block_status[i+1][j-1] == '-' or board.block_status[i+1][j+1] == '-' or board.block_status[i+2][j] == '-')):
					diam1_stat = 0
					diam1_count = 0
				if diam1_stat == 1:  # x won a row
					# row_count = 4 (xxxx) and r_c = 3 (x_xx)
					#d_won += self.dwts[diam1_count]
					#freedom += 1
					Hval+=self.blkval[diam1_count]
				elif diam1_stat == -1:  # o won a row
					#d_lost += self.dwts[diam1_count]
					Hval-=self.blkval[diam1_count]
				elif diam1_stat == 2:  # not completed
					#freedom += 1
					pass
				if diam1_stat == 1 or diam1_stat == -1:
					if board.block_status[i][j] == '-':
						Hval+=arr[i][j]
					if board.block_status[i+1][j-1] == '-':
						Hval+=arr[i+1][j-1]
					if board.block_status[i+1][j+1] == '-':
						Hval+=arr[i+1][j+1]
					if board.block_status[i+2][j] == '-':
						Hval+=arr[i+2][j]

		return Hval