import random,pygame,os

win = pygame.display.set_mode((1000,500))
dir = os.path.dirname(os.path.realpath(__file__))
sign = pygame.image.load(dir+'\Images\sign.png')
rock = pygame.image.load(dir+'\Images\Rock.png')

WHITE = (255,255,255)
movevar = 0
changevar = 1000
enemystate = ['static'],['static']
enemyx = [500,400]
enemyy = [200,400]
plrx,plry = 0,0

def enemymove(plrx,plry):
    global enemyx,enemyy,changevar,enemystate,movevar,randdirection
    for enemynum in range(2):
        print(enemyx[enemynum],enemyy[enemynum])
        win.blit(sign, (enemyx[enemynum],enemyy[enemynum]))
        if -300 < (plrx - enemyx[enemynum]) < 300 and -300 < (plry - enemyy[enemynum]) < 300:
            if plrx < enemyx[enemynum]:
                gox = plrx - enemyx[enemynum]
            else:
                gox = enemyx[enemynum] - plrx
            if plry < enemyy[enemynum]:
                goy = plry - enemyy[enemynum]
            else:
                goy = enemyy[enemynum] - plry
            gox += 1
            goy += 1
            if gox > goy or -gox > -goy:
                if gox < 0:
                    yup = (goy/-gox) * 2
                    xup = (gox/-gox) * 2
                else:
                    yup = (goy/gox) * 2
                    xup = (gox/gox) * 2
            elif goy > gox or -goy > -gox:
                if goy < 0:
                    xup = (gox/-goy) * 2
                    yup = (goy/-goy) * 2
                else:
                    xup = (gox/goy) * 2
                    yup = (goy/goy) * 2
            else:
                xup,yup = 0,0
            print(xup,yup)
            enemyx[enemynum] += (xup / 10)
            enemyy[enemynum] += (yup / 10)
        else:
            if changevar == 2000:
                if random.randrange(0,2) == 1:
                    enemystate[enemynum][0] = random.choice(('static','wander'))
                else:
                    enemystate[enemynum][0] = enemystate[enemynum][0]
                changevar = 0
            else:
                if enemystate[enemynum][0] == 'static':
                    changevar += 1
                if enemystate[enemynum][0] == 'wander':
                    if movevar > 200:
                        movevar += 1
                    if movevar > 400:
                        movevar = 0
                    if movevar == 0:
                        randdirection = random.choice(((0,0.2,'up'),(0,-0.2,'down'),(0.2,0,'left'),(-0.2,0,'right'),(0.1,0.1,'topl'),(-0.1,0.1,'topr'),(0.1,-0.1,'botl'),(-0.1,-0.1,'botr')))
                    if movevar % 2 == 0 and movevar <= 200:
                        enemyx[enemynum] += randdirection[0]
                        enemyy[enemynum] += randdirection[1]
                    movevar += 1
                changevar += 1
    pygame.display.update()

while True:
    win.fill(WHITE)
    win.blit(rock, (plrx, plry))
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    plrx -= 10
                if event.key == pygame.K_s:
                    plry += 10
                if event.key == pygame.K_d:
                    plrx += 10
                if event.key == pygame.K_w:
                    plry -= 10
    enemymove(plrx,plry)
