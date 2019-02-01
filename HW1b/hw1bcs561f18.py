import numpy as np

ap = 0
gsize = 0
psize = 0
scooters = 0
# A function to check if a queen can
# be placed on grid[row][col].
def notAttacked(grid, row, col, gridsize):
 
    # Check row
    for r in range(gridsize):
        if grid[r][col] !=0 :
            return False
    # Check column
    for c in range(gridsize):
        if grid[row][c] !=0 :
            return False
 
    # Check upper left diagonal
    for i,j in zip(range(row,-1,-1), range(col,-1,-1)):
        if grid[i][j] !=0 :
            return False
 
    # Check lower left diagonal
    for i,j in zip(range(row,gridsize,1), range(col,-1,-1)):
        if grid[i][j] != 0:
            return False
        
    # Check upper right diagonal
    for i,j in zip(range(row,-1,-1), range(col,gridsize,1)):
        if grid[i][j] !=0 :
            return False
 
    # Check lower right diagonal
    for i,j in zip(range(row,gridsize,1), range(col,gridsize,1)):
        if grid[i][j] !=0 :
            return False
 
    return True

def assignOfficers(list, k, count, grid):
    global ap
    if count == psize:
        #calc sum
        sum = 0
        for i in range(gsize):
            for j in range(gsize):
                sum+=grid[i,j]
        if sum>ap:
            ap = sum
        return
    else:
        for j in range(k,gsize*gsize,1):
            if notAttacked(grid,list[j][0],list[j][1], gsize):
                count+=1
                grid[list[j][0], list[j][1]] = list[j][2]
                assignOfficers(list,j+1,count,grid)
                grid[list[j][0], list[j][1]] = 0
                count-=1
def main():
    lineno= 0
    global ap
    with open('input.txt') as ip:
        for line in ip:
            lineno+=1
            if lineno == 1:
                #grid size
                global gsize 
                gsize = int(line.strip())
                #gsize= 3
                a = np.zeros(gsize*gsize).astype(int)
            elif lineno == 2:
                #number of officers
                global psize 
                #psize = 2
                psize = int(line.strip())
            elif lineno == 3:
                #number of scooters
                global scooters
                scooters = int(line.strip())
            else:
                #activity frequency
                pos = tuple(line.strip().split(","))
                a[gsize * int(pos[1]) + int(pos[0])]+=1
                #a = [1, 2, 3, 4, 100, 6, 0, 6, 8]
    print a 
    l = list()
    for index in range(len(a)):
        l.append((index/gsize, index%gsize, a[index]))

    l.sort(key=lambda t: t[2], reverse=True)
    #print(l)
    l3 = list()
    conflict_l=list()
    for i in range(0,(gsize*gsize),1):
        count=1
        grid = np.zeros((gsize,gsize)).astype(int)
        grid[l[i][0], l[i][1]]= l[i][2]
        assignOfficers(l3,i+1,count,grid)
    op = open("output.txt","w")
    print (ap)
    op.write("%i"%ap)
    op.close()
main()