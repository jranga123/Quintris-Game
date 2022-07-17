
# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
from queue import PriorityQueue 

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves
        
            

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    
    
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, quintris):
        
        def down1(quintris):
            while not quintris.check_collision(*quintris.state, quintris.piece, quintris.row+1, quintris.col):
              quintris.row += 1
        
        
        def calculatecost(state):
            
            
            #calculating the heights of the boards
            heights=[]
            maxparam=0
            depth=0
            for col in range(len(state[0])):
                height=0
                for row in range(len(state)):
                    if state[row][col]=="x":
                        height=(len(state)-row)
                        depth=depth+row
                        

                        break
                heights.append(height)
                maxheight=max(heights)
                if maxheight>19:
                    maxparam=100*sum(list(filter(lambda x:x>19,heights)))
                if maxheight>22:
                    maxparam+=1000*sum(list(filter(lambda x:x>22,heights)))
                if maxheight>23:
                    maxparam+=100000*sum(list(filter(lambda x:x>23,heights)))
           
            bumpiness=( [ abs(heights[i]-heights[i-1]) for i in range(1,len(heights)) ])
            
            
            #No of perfect lines
            noofperfectrows=0
            for row in range(len(state)):
                if state[row]=="xxxxxxxxxxxxxxx":
                    noofperfectrows+=1
            
            #calculating the no of holes
            noofholes=0
            for row in range(len(state)):
                for col in range(len(state[0])):
                    if (state[row][col]==" "):
                        try:
                            noofholes=noofholes+(1 if state[row-1][col]=='x' else 0)
                        except:
                            p=0
                        try:
                            
                            noofholes=noofholes+(1 if state[row][col+1]=='x' else 0)
                        except:
                            p=0
                        try:
                            noofholes=noofholes+(1 if state[row][col-1]=='x' else 0)
                        except:
                            p=0
            
            heuristic= -(200+maxparam)* noofperfectrows +21.510066*sum(heights) + 1.60*noofholes + 0.884483*sum(bumpiness)+maxparam
            # print("Noofperfectlines:",noofperfectrows)
            # print("height:",height)
            # print("noofholes:",noofholes)
            # print("bumpiness:",sum(bumpiness))
            # print(heuristic)
            #print("-----stop------")
            return heuristic
            
            
                    
                
                
            
        
        # Function to move piece all the way to left and right 
        def movepieceleftandright(quintris,fringe,path):
            
           
            c_current_board=quintris.state
            c_current_row=quintris.row
            c_current_col=quintris.col
            c_current_piece=quintris.piece
            down1(quintris)
                
            
            m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
            

            cost=calculatecost(m[0])
            fringe.put((cost,path))
            quintris.state=c_current_board
            quintris.piece=c_current_piece
            quintris.row=c_current_row
            
            
            
            #print("------------------------moving left----------------------------------")
            
            leftpath=path
            
            for i in range(c_current_col):
                quintris.left()
                down1(quintris)
                leftpath=leftpath+"b"
                m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                
                cost=calculatecost(m[0])
                fringe.put((cost,leftpath))
                quintris.state=c_current_board
                quintris.piece=c_current_piece
                
                
                quintris.row=c_current_row
                
               
                
                
                
            #resetting the position of the board
            quintris.state=c_current_board
            quintris.piece=c_current_piece
            quintris.col=c_current_col
            quintris.row=c_current_row
        
            #print("------------------------moving right----------------------------------")
            
            rightpath=path
            for i in range(c_current_col,15-len(max(quintris.piece))+1):
                quintris.right()
                down1(quintris)
                rightpath=rightpath+"m"
                m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                
                cost=calculatecost(m[0])
                fringe.put((cost,rightpath))
                quintris.row=c_current_row
                
                
                
            #resetting the position of the board    
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            return fringe
            
            
            
       
        
        ############################# Main Code ##########################################
        
        
        
        
        fringe=PriorityQueue()
        path=""
        
        #Storing current board params
        current_board=quintris.state
        current_row=quintris.row
        current_col=quintris.col
        current_piece=quintris.piece
        fringe=movepieceleftandright(quintris,fringe,path)

        
        #Horizontaly flipping the piece
        #print("-------------Horizontal flip--------------------------")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        
        
        quintris.hflip()
       
        #printstate(quintris.state[0])
        fringe=movepieceleftandright(quintris,fringe,"h")
    
        
        
        # #Rotating the board by 90 degrees
        #print("-------------rotating 90--------------------------")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        
        
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"n")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        #print("-------------fliping and rotating 90--------------------------")
        quintris.hflip()
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"hn")
        
        
        
        
        #Rotating the board by 180 degrees
        #print("-------------rotating 180--------------------------")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        
        
        quintris.rotate()
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"nn")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        #print("-------------fliping and rotating 180--------------------------")
        quintris.hflip()
        quintris.rotate()
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"hnn")
        
    
        
        #rotating the board by 270 degrees
        #print("-------------rotating 270--------------------------")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        
        quintris.rotate()
        quintris.rotate()
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"nnn")
        
        #resetting the position of the board
        quintris.state=current_board
        quintris.piece=current_piece
        quintris.col=current_col
        quintris.row=current_row
        #print("-------------fliping and rotating 270--------------------------")
        quintris.hflip()
        quintris.rotate()
        quintris.rotate()
        quintris.rotate()
        fringe=movepieceleftandright(quintris,fringe,"hnnn")
        
        
        k=fringe.get()
        
        return k[1]
    
        ######################################## End of Computer Simple #################################### 
    
     
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        
        def down1(quintris):
                while not quintris.check_collision(*quintris.state, quintris.piece, quintris.row+1, quintris.col):
                  quintris.row += 1
           
            
            
        def calculatecost(state):
            
            heights=[]
            maxparam=0
            depth=0
            for col in range(len(state[0])):
                height=0
                for row in range(len(state)):
                    if state[row][col]=="x":
                        height=(len(state)-row)
                        depth=depth+row
                        

                        break
                heights.append(height)
                maxheight=max(heights)
                if maxheight>19:
                    maxparam=100*sum(list(filter(lambda x:x>19,heights)))
                if maxheight>22:
                    maxparam+=1000*sum(list(filter(lambda x:x>22,heights)))
                if maxheight>23:
                    maxparam+=100000*sum(list(filter(lambda x:x>23,heights)))
            
            bumpiness=( [ abs(heights[i]-heights[i-1]) for i in range(1,len(heights)) ])
            
            
            #No of perfect lines
            noofperfectrows=0
            for row in range(len(state)):
                if state[row]=="xxxxxxxxxxxxxxx":
                    noofperfectrows+=1
            
            #calculating the no of holes
            noofholes=0
            for row in range(len(state)):
                for col in range(len(state[0])):
                    if (state[row][col]==" "):
                        try:
                            noofholes=noofholes+(1 if state[row-1][col]=='x' else 0)
                        except:
                            p=0
                        try:
                            
                            noofholes=noofholes+(1 if state[row][col+1]=='x' else 0)
                        except:
                            p=0
                        try:
                            noofholes=noofholes+(1 if state[row][col-1]=='x' else 0)
                        except:
                            p=0
            
            
            heuristic= -(200+maxparam)* noofperfectrows +21.510066*sum(heights) + 1.60*noofholes + 0.884483*sum(bumpiness)+maxparam
            #heuristic= -k* noofperfectrows +8.510066*sum(heights) + 1.40*noofholes + 0.884483*sum(bumpiness)+maxparam
            # print("Noofperfectlines:",noofperfectrows)
            # print("height:",height)
            # print("noofholes:",noofholes)
            # print("bumpiness:",sum(bumpiness))
            # print(heuristic)
            # print("-----stop------")
            return heuristic
            
            
                    
                
                
            
        
        
        def movepieceleftandright(quintris,fringe,path):
            
            #quintris.print_board(True)
            c_current_board=quintris.state
            c_current_row=quintris.row
            c_current_col=quintris.col
            c_current_piece=quintris.piece
            down1(quintris)
                
            
            m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
            

            cost=calculatecost(m[0])
            fringe.put((cost,path))
            quintris.state=c_current_board
            quintris.piece=c_current_piece
            quintris.row=c_current_row
            
            
            
            #print("------------------------moving left----------------------------------")
            
            leftpath=path
            
            for i in range(c_current_col):
                quintris.left()
                down1(quintris)
                leftpath=leftpath+"b"
                m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
               
                cost=calculatecost(m[0])
                fringe.put((cost,leftpath))
                quintris.state=c_current_board
                quintris.piece=c_current_piece
                
                
                quintris.row=c_current_row
                
                
            quintris.state=c_current_board
            quintris.piece=c_current_piece
            quintris.col=c_current_col
            quintris.row=c_current_row
        
            #print("------------------------moving right----------------------------------")
            
            rightpath=path
            for i in range(c_current_col,15-len(max(quintris.piece))+1):
                quintris.right()
                down1(quintris)
                rightpath=rightpath+"m"
                m=quintris.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)
                
                cost=calculatecost(m[0])
                fringe.put((cost,rightpath))
                quintris.row=c_current_row
                
                
                
            #resetting the position of the board    
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            return fringe
            
                
            
        
        while 1:
            #time.sleep(0.1)
            
            
            
            ############################# Main Code ##########################################
            
            
            
            
            fringe=PriorityQueue()
            path=""
            
            #Storing current board params
            current_board=quintris.state
            current_row=quintris.row
            current_col=quintris.col
            current_piece=quintris.piece
            fringe=movepieceleftandright(quintris,fringe,path)
    
            
            #Horizontaly flipping the piece
            #print("-------------Horizontal flip--------------------------")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            
            quintris.hflip()
           
           
            fringe=movepieceleftandright(quintris,fringe,"h")
        
                
            
            
            
            
            
            # #Rotating the board by 90 degrees
            #print("-------------rotating 90--------------------------")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"n")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            #print("------------- fliping and rotating 90--------------------------")
            quintris.hflip()
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"hn")
            
            
            
            
            # #Rotating the board by 180 degrees
            #print("-------------rotating 180--------------------------")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            
            quintris.rotate()
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"nn")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            #print("-------------fliping and rotating 180--------------------------")
            quintris.hflip()
            quintris.rotate()
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"hnn")
            
        
            
            #rotating the board by 270 degrees
            #print("-------------rotating 270--------------------------")
            
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            quintris.rotate()
            quintris.rotate()
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"nnn")
            
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            #print("-------------fliping and rotating 270--------------------------")
            quintris.hflip()
            quintris.rotate()
            quintris.rotate()
            quintris.rotate()
            fringe=movepieceleftandright(quintris,fringe,"hnnn")
            
            
            k=fringe.get()
            #resetting the position of the board
            quintris.state=current_board
            quintris.piece=current_piece
            quintris.col=current_col
            quintris.row=current_row
            
            
            commandpath = k[1]
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            
            for i in range(len(commandpath)+1):
                if i==len(commandpath):
                    quintris.down()
                    
                else:
                    commands[commandpath[i]]()
                    

            


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



