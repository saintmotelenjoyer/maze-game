# -*- coding: utf-8 -*-

import random
import datetime

def makeboard(x):  # nxn matrix of large number
    M = []
    for i in range(x):
        L = []
        for i in range(x):
            L.append(99)
        M.append(L)
    return M


# get two points on opposite sides of the board i1 j1 i2 j2
def startend(M):
    a = random.getrandbits(1)
    L = []
    if a == 0:
        x1 = random.getrandbits(1)
        if x1 == 1:
            x1 = len(M) - 1
        y1 = random.randint(0, len(M) - 1)
    else:
        y1 = random.getrandbits(1)
        if y1 == 1:
            y1 = len(M) - 1
        x1 = random.randint(0, len(M) - 1)
    a = random.getrandbits(1)
    if a == 0:
        x2 = random.getrandbits(1)
        if x2 == 1:
            x2 = len(M) - 1
        y2 = random.randint(0, len(M) - 1)
    else:
        y2 = random.getrandbits(1)
        if y2 == 1:
            y2 = len(M) - 1
        x2 = random.randint(0, len(M) - 1)
    L.append(x1)
    L.append(y1)
    L.append(x2)
    L.append(y2)
    if M[x1][y1] == 0 or M[x2][y2] == 0:
        b = False
    b = djikstra(M, x1, y1, x2, y2)
    if b == False or b[x2][y2] < 4:
        return startend(M)
    else:
        return L


def djikstra(M, x1, y1, x2, y2):
    # get a list of all values adjacent to x1 y1
    n = 1
    M[x1][y1] = n
    exit = x2 * 100 + y2
    L = []  # set of checked nodes
    n = n + 1
    # set them to n+1
    if (x1 < len(M) - 1 and M[x1 + 1][y1] > n):
        M[x1 + 1][y1] = n
        L.append((x1 + 1) * 100 + y1)  # [14][6] gets you 1406, [1][1] get you 101 etc
    if (x1 > 0 and M[x1 - 1][y1] > n):
        M[x1 - 1][y1] = n
        L.append((x1 - 1) * 100 + y1)
    if (y1 < len(M) - 1 and M[x1][y1 + 1] > n):
        M[x1][y1 + 1] = n
        L.append(x1 * 100 + y1 + 1)
    if (y1 > 0 and M[x1][y1 - 1] > n):
        M[x1][y1 - 1] = n
        L.append(x1 * 100 + y1 - 1)
        # get a set of the values adjacent to the set, set them to n+1
    # repeat for about len(M)*8 times
    for i in range(len(M) * 8):
        L1 = []
        n = n + 1
        for j in L:  # turn the int stored there into an index
            if j == exit:
                return M
            x = j // 100
            y = j % 100
            if (x < len(M) - 1 and M[x + 1][y] > n):  # check neighboring indices, set to 1
                M[x + 1][y] = n
                L1.append((x + 1) * 100 + y)
            if (x > 0 and M[x - 1][y] > n):
                M[x - 1][y] = n
                L1.append((x - 1) * 100 + y)
            if (y < len(M) - 1 and M[x][y + 1] > n):
                M[x][y + 1] = n
                L1.append(x * 100 + y + 1)
            if (y > 0 and M[x][y - 1] > n):
                M[x][y - 1] = n
                L1.append(x * 100 + y - 1)
        for k in L1:
            L.append(k)
    return M


def makepoints(M, x1, y1, x2, y2):
    # get n random value pairs within M where n=len(M)/3
    L = []
    L1 = []
    Lf = []
    for i in range(len(M) // 3):
        x = random.randint(0, len(M) - 1)
        y = random.randint(0, len(M) - 1)
        while M[x][y] == 0:
            x = random.randint(0, len(M) - 1)
            y = random.randint(0, len(M) - 1)
        L.append(x * 100 + y)
    # re-sort them in order of distance from start
    for i in range(len(L)):
        d = ((L[i] / 100 - x1) * (L[i] / 100 - x1) + (L[i] % 100 - y1) * (L[i] % 100 - y1)) ** 0.5
        L1.append(d)
    for i in range(len(L)):
        j = min(L1)
        k = L1.index(j)
        Lf.append(L[k])
        L1.remove(j)
        L1.insert(k, 9999)
    L = Lf
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] > 0:
                M[i][j] = 99
    djikstra(M, x1, y1, L[0] // 100, L[0] % 100)
    for i in range(len(L) - 1):
        for d in range(len(M)):
            for e in range(len(M)):
                if M[d][e] > 0:
                    M[d][e] = 99
    return L


def getapath(M, SE):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] > 0:
                M[i][j] = 99
    M = djikstra(M, SE[0], SE[1], SE[2], SE[3])
    P = []
    t = SE[2] * 100 + SE[3]
    n = M[SE[2]][SE[3]]
    s = SE[0] * 100 + SE[1]
    if n == 99:
        return False
    tempL = t
    S = [100, -100, 1, -1]
    while t // 100 > len(M) - 1 or t // 100 < 0 or t % 100 > len(M) - 1 or t % 100 < 0:
        t = tempL - random.choice(S)
    P.append(t)
    while t != s:
        oops = 0
        while M[t // 100][t % 100] != n - 1:
            t = tempL - random.choice(S)
            oops = oops + 1
            if oops > 100:
                return False
            while t // 100 > len(M) - 1 or t // 100 < 0 or t % 100 > len(M) - 1 or t % 100 < 0:
                t = tempL - random.choice(S)
                oops = oops + 1
                if oops > 100:
                    return False
        tempL = t
        P.append(t)
        n = n - 1
    return P


def path(M, SE, L):
    # se and l will be in different formats
    # se[0] and se[1] are start, L//100 and L%100 are next point
    # start with 2 and 3, go all the way through L, then do 0 1
    # getapath goes from last 2 inputs to first 2 inputs
    P = []
    if len(L) == 0:
        newL = [SE[0], SE[1], SE[2], SE[3]]
        PATH = getapath(M, newL)
        if PATH == False:
            return False
        for n in PATH:
            P.append(n)
        return P
    elif len(L) == 1:
        newL = [L[0] // 100, L[0] % 100, SE[2], SE[3]]
        PATH = getapath(M, newL)
        if PATH == False:
            return False
        for n in PATH:
            P.append(n)
        newL = [SE[0], SE[1], L[0] // 100, L[0] % 100]
        PATH = getapath(M, newL)
        if PATH == False:
            return False
        for n in PATH:
            P.append(n)
        return P
    newL = [L[-1] // 100, L[-1] % 100, SE[2], SE[3]]
    PATH = getapath(M, newL)
    if PATH == False:
        return False
    for n in PATH:
        P.append(n)
    else:
        for i in range(1, len(L) - 1):
            newL = [L[-i - 1] // 100, L[-i - 1] % 100, L[-i] // 100, L[-i] % 100]
            PATH = getapath(M, newL)
            if PATH == False:
                return False
            for n in PATH:
                P.append(n)
        newL = [L[0] // 100, L[0] % 100, L[1] // 100, L[1] % 100]
        PATH = getapath(M, newL)
        if PATH == False:
            return False
        for n in PATH:
            P.append(n)
        newL = [SE[0], SE[1], L[0] // 100, L[0] % 100]
        PATH = getapath(M, newL)
        if PATH == False:
            return False
        for n in PATH:
            P.append(n)
        return P


def deadends(M, P):
    Z = []
    for i in range(len(M)):
        for j in range(len(M)):
            M[i][j] = 0
            Z.append(i * 100 + j)
    for i in P:
        x = i // 100
        y = i % 100
        M[x][y] = 1
        if i in Z:
            Z.remove(i)
    n = 1
    # pick a random index with value 0, set a 1-valued index next to it to n+1
    # continue until no more dead ends to make
    S = [100, -100, 1, -1]
    # while (len(Z)>0 or oops<len(M)):#may want a method for in case sections get blocked off
    USED = []
    for i in range(15):  # change this condition after subsequent code works
        r = random.choice(P)
        while r in USED:
            r = random.choice(P)
        tempr = r
        USED.append(r)
        # add either 100, 1, -100, -1 to r
        # check if new r>0, <lenM, in zeros
        # if so, give r value of n+1, increment n, check spaces next to new r
        # if r+100, r+1, r-100, r-1 all dead ends, pick a new point
        stop = False
        while (stop == False):
            stop = True
            if r - 100 > 0 and r - 100 in Z:
                stop = False
            elif r % 100 - 1 > 0 and r - 1 in Z:
                stop = False
            elif r // 100 + 1 < len(M) and r + 100 in Z:
                stop = False
            elif r % 100 + 1 < len(M) and r + 1 in Z:
                stop = False
            # now that r has been confirmed to not be a dead end, do stuff
            if stop == False:
                r = tempr + random.choice(S)
                while r // 100 > len(M) - 1 or r // 100 < 0 or r % 100 > len(M) - 1 or r % 100 < 0 or r not in Z:
                    r = tempr + random.choice(S)
                M[r // 100][r % 100] = n + 1
                Z.remove(r)
                n = n + 1
                tempr = r
        n = 1
        
    return M


def fillzeros(M):
    # for all indices in M
    # if n=0 add to a list
    # for all indices in list
    # pick a random index next to them <lenL and >=0
    # get n from random index
    # assign the list index n+1
    return M


        

dt1 = datetime.datetime.now()
M = makeboard(10)
L = startend(M)
print(L)
P = makepoints(M, L[0], L[1], L[2], L[3])
print(P)
PATH = path(M, L, P)
# print(PATH)
for i in range(len(M)):
    for j in range(len(M)):
        M[i][j] = 0

for i in PATH:
    x = i // 100
    y = i % 100
    M[x][y] = 1
dt2 = datetime.datetime.now()
M = deadends(M, PATH)
for i in range(len(M)):
    print(M[i])

print(dt2 - dt1)
s=dt2.microsecond

import pygame

pygame.init()

size=width, height=500, 500

screen = pygame.display.set_mode(size)
ground=pygame.image.load("ground.png")
groundrect=ground.get_rect()
wall=pygame.image.load("wall.png")
wallrect=wall.get_rect()
player=pygame.image.load("player.png")
playerrect=player.get_rect()
playerrect.update(250, 250, 20, 40)
px=playerrect.topleft[0]
py=playerrect.topleft[1]
screen.blit(player, playerrect)
truex=L[1]*120
truey=L[0]*120

#so window size stays constant and is redrawn as player moves, but maze size varies
#paths between walls should be wider than the walls, 80px good for tessellation reasons
#so size =(wall size + path size)*len(M)
gamewon=False

while gamewon==False:
    pi=py//120
    pj=px//120
    #step 1 cover everything in ground tiles

    #step 2 look at matrix indices
    ##use truex truey that update w player movement to get i j
    i=truey//120
    j=truex//120
    if i==L[2] and j==L[3]:
        gamewon=True
    WALLS=[]
    #TODO: make this happen less often, like every half second or something
    timer=datetime.datetime.now().microsecond
    if timer%500==2:
        for num in range(-10, 10):
            for num2 in range(-10, 10):
                if i+(num2/1.5)>=0 and j+(num/1.5)>=0 and i+(num2/1.5)<len(M) and j+(num/1.5)<len(M):
                    groundrect.topleft = (210 + num * 80, 210 + num2 * 80)
                    screen.blit(ground, groundrect)
        for a in range(-5, 5):
            for b in range(-5, 5):
                #corners, 1 corner should be enough since the index below & right of it is guaranteed calculated
                if i + a >= 0 and i + a <= len(M) and j + b >= 0 and j + b <= len(M):
                    wallrect.topleft = (px + b * 120 - 40 - 3, py + a * 120 - 40 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                #generates the rest of the maze walls, doesn't cover some edge cases like main path folding back on itself
                #need to repeatedly make copies of wall
                if i + a>=0 and i + a<len(M) and j + b>=0 and j + b<len(M):
                    if i+a<len(M)-1:
                       if (M[i + a][j+b] !=1 or  M[i + a + 1][j+b] !=1) and M[i + a + 1][j+b] != (M[i + a][j+b]+1) and M[i + a+1][j+b] !=(M[i + a][j+b]-1):
                            wallrect.topleft = (px + b * 120 - 3, py + a * 120 + 80 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                            wallrect.topleft = (px + b * 120 + 40 - 3, py + a * 120 + 80 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                    if i+a>0:
                        if (M[i + a][j+b] !=1 or  M[i + a - 1][j+b] !=1) and M[i + a - 1][j + b] != (M[i + a][j+b] + 1) and M[i + a-1][j+b] != (M[i + a][j+b]-1):
                            wallrect.topleft = (px + b * 120 - 3, py + a * 120 - 40 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                            wallrect.topleft = (px + b * 120 + 40 - 3, py + a * 120 - 40 - 3 )
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                    if j+b<len(M)-1:
                        if (M[i + a][j+b] !=1 or  M[i + a][j+b+1] !=1) and M[i + a][j+b+1] != M[i + a][j+b] + 1 and M[i + a][j+b+1] != M[i + a][j+b] - 1:
                            wallrect.topleft = (px + b * 120 + 80 - 3, py + a * 120 - 3 )
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                            wallrect.topleft = (px + b * 120 + 80 - 3, py + a * 120 + 40 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                    if j+b>0:
                        if (M[i + a][j+b] !=1 or  M[i + a][j+b-1] !=1) and M[i + a][j+b-1] != M[i + a][j+b] + 1 and M[i + a][j+b-1] != M[i + a][j+b] - 1:
                            wallrect.topleft = (px + b * 120 - 40 - 3, py + a * 120 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                            wallrect.topleft = (px + b * 120 - 40 - 3, py + a * 120 + 40 - 3)
                            screen.blit(wall, wallrect)
                            WALLS.append(wallrect)
                if i + a == 0 and j + b >= -1 and j + b < len(M):
                    wallrect.topleft = (px + b * 120 - 3, py + a * 120 - 40 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                    wallrect.topleft = (px + b * 120 + 40 - 3, py + a * 120 - 40 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                if j + b == 0 and i + a >= -1 and i + a < len(M):
                    wallrect.topleft = (px + b * 120 - 40 - 3, py + a * 120 + 120 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                    wallrect.topleft = (px + b * 120 -40 - 3, py + a * 120 + 120 + 40 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                if i + a == len(M)-1 and j + b >= 0 and j + b < len(M)-1:
                    wallrect.topleft = (px + b * 120 - 3, py + a * 120 + 80 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                    wallrect.topleft = (px + b * 120 +40 - 3, py + a * 120 + 80 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                if j + b == len(M)-1 and i + a >= 0 and i + a < len(M)-1:
                    wallrect.topleft = (px + b * 120 + 80 - 3, py + a * 120 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
                    wallrect.topleft = (px + b * 120 + 80 - 3, py + a * 120 + 40 - 3)
                    screen.blit(wall, wallrect)
                    WALLS.append(wallrect)
        screen.blit(player, playerrect)
        pygame.display.flip()

    #step 2: take input for player movement, update px, py, truex, truey
    WASD= pygame.key.get_pressed()
    canmove=True
    m=5
    if WASD[pygame.K_w]:
        for wall in WALLS:
            if wall.bottom<playerrect.top:
                if playerrect.colliderect(wall):
                    canmove=False
        if canmove:
            playerrect.move(0, -m)
            truey-=m
        #move player up
    canmove = True
    if WASD[pygame.K_a]:
        for wall in WALLS:
            if wall.right<playerrect.left:
                if playerrect.colliderect(wall):
                    canmove=False
        if canmove:
            playerrect.move(-m, 0)
            truex-=m
        #move player left
    canmove = True
    if WASD[pygame.K_s]:
        for wall in WALLS:
            if wall.top<playerrect.bottom:
                if playerrect.colliderect(wall):
                    canmove=False
        if canmove:
            playerrect.move(0, m)
            truey+=m
        #move player down
    canmove = True
    if WASD[pygame.K_d]:
        for wall in WALLS:
            if wall.left<playerrect.right:
                if playerrect.colliderect(wall):
                    canmove=False
        if canmove:
            playerrect.move(m, 0)
            truex+=m
        #move player right
    screen.blit(player, playerrect)
    pygame.display.flip()
