# The-Game-of-Quintris
In this Problem. Quintris board starts off with a blank board. One by one, random pieces(each consisting of 5 blocks arranged in different shapes) fall from the top of the board to the bottom. As each piece falls, the player can change the shape by rotating it or flipping it horizontally, and can change its position by moving it left or right. It stops whenever it hits the ground or another fallen piece. If the piece completes an entire row, the row disappears and the player receives a point. The goal is for the player to score as many points before the board fills up
 I can use b and m keys to move the falling piece left and right, the n key to rotate, the h key to flip,and the space bar to cause the piece to fall. 
 
 # Genrating the Succesors
 First task in this problem is to generate succesors. To do that I have taken the current piece and rotated and flipped it on various ways to find all the succesors. After that I placed the place at the bottom of the board until it hit any piece and calculating the heuristic for it.

```python       
        
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
```

I used a function called movepieceleftandright() to move the modified pieces all the way to right and left. after moving them I am moving the all the way to the bottom until they hit the board. and caluclating the heuristic cost of the function. The goal is to get heuristic has low as possible.

```python
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

```
I have to optimise our heuristic as much as possible inorder to play effectively. the heuristic I used is the combination no of holes in the board, aggregate height of the board, bumpiness of the board and no of complete rows.
**No of holes**
Holes is defined as space that is under or to right or to left of a piece
I calculate the no of holes using the function below

**Branching factor**: Branching factor for this problem is 24 since there are 24 successor states.
```python
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

```
Agregate height is the sum of heights of all columns. I are also adding additional weights to the columns which nearer the end of board
 ```python
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

```
bumpiness is the sum of absolute difference between adjacent columns

noofperfectrows is the row which is totally occupied by 'x'
```python
#No of perfect lines
noofperfectrows=0
for row in range(len(state)):
	if state[row]=="xxxxxxxxxxxxxxx":
	    noofperfectrows+=1
```
I combine all this parameters to get the end heuristic
```python
heuristic= -(200+maxparam)* noofperfectrows +21.510066*sum(heights) + 1.60*noofholes + 0.884483*sum(bumpiness)+maxparam
```
**How to improve performance**
I can improve the performance by calculating the parameters using generic algorithm. I can use a neural to trained the model until it gets optimal values for the boards.I can also use expertimax to improve the accuracy.



After that I am taking the best move which has the least heuristic value and making that move.
I are using the same logic for both computer simple and computer animated
            
