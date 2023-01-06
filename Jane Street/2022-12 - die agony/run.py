import numpy as np
from sympy import pprint
rotm = [np.array([[1, 0, 0], # up
                  [0, 0, 1],
                  [0, -1,0]]),
        np.array([[0, 0, 1], # right
                  [0, 1, 0],
                  [-1,0, 0]]),
        np.array([[1, 0, 0], # down
                  [0, 0,-1],  
                  [0, 1, 0]]),
        np.array([[0, 0,-1], # left
                  [0, 1, 0],
                  [1, 0, 0]]),]
grid = [[57,  33,  132, 268, 492, 732],
        [81,  123, 240, 443, 353, 508],
        [186, 42,  195, 704, 452, 228],
        [-7,  2,   357, 452, 317, 395],
        [5,   23,  -4,  592, 445, 620],
        [0,   77,  32,  403, 337, 452]]

def finddown(m):
    # returns the index for a face being down (column that is [0,0,-1])
    for i in range(np.shape(m)[1]):
        if np.ndarray.tolist(m[:,i]) == [0,0,-1]:
            return i
    pprint(m)
    exit()

def inbounds(pos):
    global grid
    if pos[0] < 0 or pos[1] < 0:
        return False
    try:
        grid[pos[0]][pos[1]]
        return True
    except:
        return False

out = None
def recursive(pos: tuple, m: np.ndarray, faces: list,
              turn: int, score: int, pastpos: list):
    global out
    global grid
    
    pastpos.append(pos) #adds current position 

    if pos == (0,5): # at end
        print(pos, faces, turn, score, pastpos)
        out = pastpos
        return
        
    turn += 1
    oldfaces = faces.copy()
    oldpastpos = pastpos.copy()
    for i in range(4):
        faces = oldfaces.copy()
        pastpos = oldpastpos.copy()
        if i == 0:
            newpos = (pos[0]-1,pos[1]) # up
        elif i == 1:
            newpos = (pos[0],pos[1]+1) # right
        elif i == 2:
            newpos = (pos[0]+1,pos[1]) # down
        elif i == 3:
            newpos = (pos[0],pos[1]-1) # left
        
        if not inbounds(newpos):
            continue
        
        newm = rotm[i] @ m
        
        newscore = grid[newpos[0]][newpos[1]]
        fval = (newscore - score)/turn
        if int(fval) != fval: # not an int (float with trailing 0's)
            continue
        fval = int(fval)
        
        downI = finddown(newm)
        if faces[downI] == None: # face does not have a value yet
            faces[downI] = fval
        if faces[downI] != fval: # face value == expected value
            continue
        
        # good to go
        recursive(newpos, newm, faces, turn, newscore, pastpos)
    return

temp = np.identity(3, dtype= int)
initm = np.concatenate((temp,-1*temp), axis=1)
initf = [None for _ in range(6)]
recursive((5,0),initm,initf,0,0,[])


ans = 0
print("missed tiles:")
for i in range(6):
    for j in range(6):
        if (i,j) not in out:
            print(grid[i][j])
            ans += grid[i][j]
print("sum of missed tiles:",ans)