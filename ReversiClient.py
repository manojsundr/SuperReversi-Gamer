from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import pygame
pygame.init()
p = 0
width,height,d,q,count = 533,570,0,0,[0 for i in range(8)]
board = [[False for i in range(8)] for i in range(8)]
board[3][3],board[4][4],board[4][3],board[3][4] = "w","w","b","b"
turn = ["b","w"]
x_2,y_2 = 0,0
#Board definition
class BoxesGame(ConnectionListener):
	#Images and graphics sources
	def Network_close(self, data):
		exit()
		pass
	def Network_theirturn(self, data):
		global d
		connection.Pump()
		self.Pump()
		self.surround_check(data["x_2"],data["y_2"])
		self.change_color(data["x_2"],data["y_2"])
		self.screen.fill((51,102,0),(0,550,500,570))
		myfont = pygame.font.SysFont(None, 20)
		d = 1-d
		global board
		count_w,count_b = 0,0
		for item in board:
			count_w += item.count("w")
			count_b += item.count("b")
		if self.color_player == 0 and d == 0:
			label = myfont.render( "Your Turn",1,(0,0,0))
			self.screen.blit(label,(0,550))
			label = myfont.render( "You: "+str(count_b),1,(0,0,0))
			self.screen.blit(label,(300,550))					
			label = myfont.render( "Opponent: "+str(count_w),1,(255,255,255))
			self.screen.blit(label,(400,550))					
		elif self.color_player == 1 and d == 1:	
			label = myfont.render( "Your Turn",1,(255,255,255))
			self.screen.blit(label,(0,550))
			label = myfont.render( "You: "+str(count_w),1,(255,255,255))
			self.screen.blit(label,(300,550))					
			label = myfont.render( "Opponent: "+str(count_b),1,(0,0,0))
			self.screen.blit(label,(400,550))	
	def Network_startgame(self, data):
		self.running=True
		self.num=data["player"]
		self.gameid=data["gameid"]
		self.color_player = data["cindex"]
		self.screen.fill((51,102,0),(0,550,500,570))
		myfont = pygame.font.SysFont(None, 20)
		if self.color_player == 0:
			label = myfont.render( "Your Turn",1,(0,0,0))
			self.screen.blit(label,(0,550))
			label = myfont.render( "You: 2",1,(0,0,0))
			self.screen.blit(label,(300,550))
			label = myfont.render( "Opponent: 2",1,(255,255,255))
			self.screen.blit(label,(400,550))
		else:	
			label = myfont.render( "Opponent's Turn",1,(255,255,255))
			self.screen.blit(label,(0,550))
			label = myfont.render( "Opponent: 2",1,(0,0,0))
			self.screen.blit(label,(400,550))
			label = myfont.render( "You: 2",1,(255,255,255))
			self.screen.blit(label,(300,550))
										
	def Network_place(self, data):
        #self.placeSound.play()
        #get attributes
		x = data["x"]
		y = data["y"]
		
	def Network_yourturn(self, data):
        #torf = short for true or false
		self.color = data["torf"]
			
	def initGraphics(self):
		self.normallinev=pygame.image.load("images/line3.png")
		self.normallineh=pygame.transform.rotate(pygame.image.load("images/line3.png"), -90)
		self.white = pygame.image.load("images/w.png")
		self.black = pygame.image.load("images/b.png")
		self.green = pygame.image.load("images/green.png")
	#Class initialization	
	def __init__(self):
		self.justplaced=10
		global d,q,count,board
		d,q,count= 0,0,[0 for i in range(8)]
		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption("reversi")
		board = [[False for i in range(8)] for i in range(8)]
		board[3][3],board[4][4],board[4][3],board[3][4] = "w","w","b","b"
		self.boardh = [[False for x in range(9)] for y in range(9)]
		self.boardv = [[False for x in range(9)] for y in range(9)]
		self.initGraphics()
		self.color = True
		self.owner=[[0 for x in range(8)] for y in range(8)]
		self.me=0
		self.otherplayer=0
		self.didiwin=False
		self.running=False
		address=raw_input("Address of Server: ")
		try:
			if not address:
				host, port="localhost", 8000
			else:
				host,port=address.split(":")
			self.Connect((host, int(port)))
		except:
			print "Error Connecting to Server"
			print "Usage:", "host:port"
			print "e.g.", "localhost:31425"
			exit()
        print "Boxes client started"	
	#Construct Board	
	def drawBoard(self):
		for x in range(9):
			for y in range(9):
				if not self.boardh[y][x]:
					self.screen.blit(self.normallineh, [(x)*59, (y)*66.3])
		for x in range(9):
			for y in range(9):
				if not self.boardv[y][x]:
					self.screen.blit(self.normallinev, [(x)*66.3, (y)*59])			
		#Initial black and white configuration
		myfont = pygame.font.SysFont(None, 24)
		self.screen.blit(self.white, [208.9,208.9])
		self.screen.blit(self.black, [275.2,208.9])
		self.screen.blit(self.white, [275.2,275.2])
		self.screen.blit(self.black, [208.9,275.2])
	def surround_check(self,a,b):
		global board,d,count
		t = 0
		count = [0 for i in range(8)]
		self.screen.fill((51,102,0),(0,550,400,700))
		if b<8 and a<8:
			p = 1		
			if board[b][a] == False:
				#Up
				w = b-1
				if w>0:
					while w>=0:
						if w>7 or w<0:
							break
						if board[w][a] == turn[1-d] and w!=0:
							count[0] += 1
							w -= 1
						elif board[w][a] == turn[d] and count[0]!=0:
							t = 1		
							break
						else:
							count[0] = 0
							break
				if t!=1:
					count[0] = 0						
				#Down
				t = 0
				w = b+1
				if w<7:			
					while w<8:
						if w>7 or w<0:
							break
						if board[w][a] == turn[1-d] and w!=7:
							count[1] += 1
							w += 1
						elif board[w][a] == turn[d] and count[1]!=0:
							t = 1
							break
						else:
							count[1] = 0
							break
				if t!=1:
					count[1] = 0					
				#Left
				t = 0
				w = a-1
				if w>0:			
					while w>=0:
						if w>7 or w<0:
							break
						if board[b][w] == turn[1-d] and w!=0:
							count[2] += 1
							w -= 1
						elif board[b][w] == turn[d] and count[2]!=0:
							t = 1
							break
						else:
							count[2] = 0
							break
				if t!=1:
					count[2] = 0					
				#Right
				t = 0
				w = a+1
				if w<7:			
					while w<8:
						if w>7 or w<0:
							break
						if board[b][w] == turn[1-d] and w!=7:
							count[3] += 1
							w += 1
						elif board[b][w] == turn[d] and count[3]!=0:
							t = 1 
							break
						else:
							count[3] = 0
							break
				if t!=1:
					count[3] = 0						
				#Left-Upper Diagonal
				w,x,t = a-1,b-1,0
				if w>0 and x>0:
					while w*x >=0:
						if w>7 or w<0 or x>7 or x<0:
							break
						if board[x][w] == turn[1-d] and (x!=0 or w!=0):
							count[4] += 1
							w -= 1
							x -= 1
						elif board[x][w] == turn[d] and count[4]!=0:
							t = 1
							break
						else:
							count[4] = 0
							break
				if t!=1:
					count[4] = 0			
				#Right-Lower Diagonal
				w,x,t = a+1,b+1,0
				if w<7 and x<7:
					while w*x <=49:
						if w>7 or w<0 or x>7 or x<0:
							break
						if board[x][w] == turn[1-d] and (x!=7 or w!=7):
							count[5] += 1
							w += 1
							x += 1
						elif board[x][w] == turn[d] and count[5]!=0:
							t = 1							
							break
						else:
							count[5] = 0
							break
				if t!=1:
					count[5] = 0				
				#Left Lower Diagonal
				w,x,t = a-1,b+1,0
				if w>0 and x<7:
					while w*x >=0:
						if w>7 or w<0 or x>7 or x<0:
							break
						if board[x][w] == turn[1-d] and (w!=0 or x!=7):
							count[6] += 1
							w -= 1
							x += 1
						elif board[x][w] == turn[d] and count[6]!=0:
							t = 1
							break
						else:
							count[6] = 0
							break
				if t!=1:
					count[6] = 0				
				#Right Upper Diagonal
				w,x,t = a+1,b-1,0
				if w<7 and x>0:
					while w*x >=0:
						if w>7 or w<0 or x>7 or x<0:
							break
						if board[x][w] == turn[1-d] and (w!=7 or x!=0):
							count[7] += 1
							w += 1
							x -= 1
						elif board[x][w] == turn[d] and count[7]!=0:
							t = 1
							break
						else:
							count[7] = 0
							break
				if t!=1:
					count[7] = 0			
		return sum(count)
	def change_color(self,a,b):
		global count,d,turn,board
		#UP
		if count[0] >0:
			for i in range(b-count[0],b+1):
				board[i][a] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(a)+10,66.3*(i)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(a)+10,66.3*(i)+10])
				pygame.display.flip()
		#DOWN
		if count[1]>0:
			for i in range(b,b+1+count[1]):
				board[i][a] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(a)+10,66.3*(i)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(a)+10,66.3*(i)+10])
				pygame.display.flip()	
		#LEFT
		if count[2]>0:
			for i in range(a-count[2],a+1):
				board[b][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(b)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(b)+10])
				pygame.display.flip()	
		#RIGHT
		if count[3]>0:
			for i in range(a,a+1+count[3]):
				board[b][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(b)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(b)+10])
				pygame.display.flip()
		#LUD
		if count[4]>0:
			i,j,k = a-count[4],b-count[4],0
			while k<=count[4]:
				board[j][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(j)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(j)+10])
				pygame.display.flip()	
				i +=1 
				j += 1
				k += 1
		#RLD
		if count[5]>0:
			i,j,k = a,b,0
			while k<=count[5]:
				board[j][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(j)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(j)+10])
				pygame.display.flip()
				i +=1 
				j += 1
				k += 1
		#LLD
		if count[6]>0:
			i,j,k = a-count[6],b+count[6],0
			while k<=count[6]:
				board[j][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(j)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(j)+10])
				pygame.display.flip()
				i +=1 
				j -= 1
				k += 1
		#RUD
		if count[7]>0:
			i,j,k = a+count[7],b-count[7],0
			while k<=count[7]:
				board[j][i] = turn[d]
				self.screen.blit(pygame.image.load("images/green.png"),[66.3*(i)+10,66.3*(j)+10])
				self.screen.blit(pygame.image.load("images/"+turn[d]+".png"),[66.3*(i)+10,66.3*(j)+10])
				pygame.display.flip()
				i -=1 
				j += 1
				k += 1
		count = [0 for i in range(8)]
	def check_zero_moves(self):
		global initial,d,count,board
		a = d
		c = 0
		initial = board
		for i in range(8):
			for j in range(8):
				board = initial
				d = a
				count = [0 for k in range(8)]						 		
				if board[j][i] == False:
					if self.surround_check(i,j) != 0:
						c += 1
						break
		if c == 0:
			return 0
		else:
			return 1
		board = initial
		d = a
		count = [0 for i in range(8)]
	def game_finish(self):
		global d
		c = 0
		if self.check_zero_moves() == 0:
			d = 1-d
			if self.check_zero_moves() == 0:
				d = 1-d
				return True
			else:
				return False
		else:
			return False	
																			
	def gameBoard(self):
		#sleep to make the game 60 fps
		#self.clock.tick(60) 
		#clear the screen
		self.screen.fill((51,102,0))
		self.drawBoard()																																										
	def label_print(self):
		self.screen.fill((51,102,0),(0,550,500,570))
		myfont = pygame.font.SysFont(None, 20)
		global board
		count_w,count_b = 0,0
		for item in board:
			count_w += item.count("w")
			count_b += item.count("b")
		if d == 1 and self.color_player == 0:				
			label = myfont.render( "Opponent's Turn",1,(255,255,255))
			self.screen.blit(label,(0,550))
			label = myfont.render( "You: "+str(count_b),1,(0,0,0))
			self.screen.blit(label,(300,550))					
			label = myfont.render( "Opponent: "+str(count_w),1,(255,255,255))
			self.screen.blit(label,(400,550))					
		elif d == 0 and self.color_player == 1:
			label = myfont.render( "Opponent's Turn",1,(0,0,0))
			self.screen.blit(label,(0,550))
			label = myfont.render( "You: "+str(count_w),1,(255,255,255))
			self.screen.blit(label,(300,550))					
			label = myfont.render( "Opponent: "+str(count_b),1,(0,0,0))
			self.screen.blit(label,(400,550))
			
	def update(self):
		self.Pump()
		connection.Pump()
		global old,d,board
		clock = pygame.time.Clock()			
		for event in pygame.event.get():
			#quit if the quit button was pressed
			if event.type == pygame.QUIT:	
				exit()
			else:
				if pygame.mouse.get_pressed()[0] and d == self.color_player:
					self.x = int(pygame.mouse.get_pos()[0]/67)
					self.y = int(pygame.mouse.get_pos()[1]/68.3)
					if self.x<8 and self.y<8 and self.surround_check(self.x,self.y) > 0:							
						self.surround_check(self.x,self.y)
						self.change_color(self.x,self.y)
						connection.Send({"action": "receive", "x":self.x, "y":self.y,"num":self.num,"gameid":self.gameid})
						d = 1-d
						if not self.check_zero_moves():
							d = 1-d
							if not self.check_zero_moves():
								self.winner()
								break
						self.label_print()
						pygame.display.update()
						clock.tick(30)
						break	
					elif self.x<8 and self.y<8 and self.surround_check(self.x,self.y) == 0 and self.check_zero_moves()>0:
						self.label_print()			
						pygame.display.update()
						clock.tick(30)
						break												
			pygame.display.flip()
	def Network_win(self, data):
		self.owner[data["x"]][data["y"]]="win"
		self.boardh[data["y"]][data["x"]]=True
		self.boardv[data["y"]][data["x"]]=True
		self.boardh[data["y"]+1][data["x"]]=True
		self.boardv[data["y"]][data["x"]+1]=True
		#add one point to my score
		self.me+=1
	def Network_lose(self, data):
		self.owner[data["x"]][data["y"]]="lose"
		self.boardh[data["y"]][data["x"]]=True
		self.boardv[data["y"]][data["x"]]=True
		self.boardh[data["y"]+1][data["x"]]=True
		self.boardv[data["y"]][data["x"]+1]=True
        #add one to other players score
		self.otherplayer+=1			
	def start_game(self):
		self.gameBoard()
		self.Pump()
		connection.Pump()
		while 1:
			self.update()	
bg=BoxesGame()
bg.start_game()			
