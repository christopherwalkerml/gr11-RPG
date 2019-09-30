#--------------------------------------------------------------------------------------#
#Chris Walker. Final Project 11U Computer Science                                      #
#--------------------------------------------------------------------------------------#
import pygame,os,Collisions,NPCtext,random
pygame.mixer.init(frequency = 44100,size=-16,channels=1,buffer=2**12)
pygame.init()

winwidth = 896
winheight = 640
win = pygame.display.set_mode((winwidth,winheight))
#-------------------------------#
#       GLOBAL VARIABLES        #
#-------------------------------#
dir = os.path.dirname(os.path.realpath(__file__))

playerhit = pygame.mixer.Sound(dir+'\Sound\playerhit.wav')
hitsound = pygame.mixer.Sound(dir+'\Sound\enemydamage.wav')
swingsound = pygame.mixer.Sound(dir+'\Sound\swing.wav')
CocoBit50x50 = pygame.image.load(dir+'\Images\COCOBIT50x50.jpg').convert_alpha()
CocoBit50x50P2 = pygame.image.load(dir+'\Images\COCOBIT50x50P2.png').convert_alpha()
blank = pygame.image.load(dir+'\Images\Blank.png').convert_alpha()
playerspr = pygame.image.load(dir+'\Images\Rock2.png').convert_alpha()
forestrm = pygame.image.load(dir+'\Images\Forestrm1.png').convert_alpha()
textbox = pygame.image.load(dir+'\Images\Textblob.png').convert_alpha()
sign = pygame.image.load(dir+'\Images\sign.png').convert_alpha()
house1 = pygame.image.load(dir+'\Images\house1.png').convert_alpha()
housei1 = pygame.image.load(dir+'\Images\housei1.png').convert_alpha()
pausemenu = pygame.image.load(dir+'\Images\pausemenu.png').convert_alpha()
areyousure = pygame.image.load(dir+'\Images\Areyousure.png').convert_alpha()
gamesaved = pygame.image.load(dir+'\Images\gamesaved.png').convert_alpha()
grass = pygame.image.load(dir+'\Images\grass.png').convert_alpha()
shadow = pygame.image.load(dir+'\Images\shadow.png').convert_alpha()
sidebox = pygame.image.load(dir+'\Images\sidebox.png').convert_alpha()
log = pygame.image.load(dir+'\Images\log.png').convert_alpha()
rock = pygame.image.load(dir+'\Images\Rock.png').convert_alpha()
tree = pygame.image.load(dir+'\Images\Tree.png').convert_alpha()
tree1 = pygame.image.load(dir+'\Images\Tree1.png').convert_alpha()
tree2 = pygame.image.load(dir+'\Images\Tree2.png').convert_alpha()
cave = pygame.image.load(dir+'\Images\cave.png').convert_alpha()
npc1 = pygame.image.load(dir+'\Images\PCN1.png').convert_alpha()
heart = pygame.image.load(dir+'\Images\heart.png').convert_alpha()
deadheart = pygame.image.load(dir+'\Images\deadheart.png').convert_alpha()
scroll = pygame.image.load(dir+'\Images\scroll.png').convert_alpha()
gscroll = pygame.image.load(dir+'\Images\gscroll.png').convert_alpha()
plrupattack = [pygame.image.load(dir+'\Images\plrupattack'+str(x)+'.png').convert_alpha() for x in range(1,8)]
plrdownattack = [pygame.image.load(dir+'\Images\plrdownattack'+str(x)+'.png').convert_alpha() for x in range(1,8)]
plrleftattack = [pygame.image.load(dir+'\Images\plrleftattack'+str(x)+'.png').convert_alpha() for x in range(1,8)]
plrrightattack = [pygame.image.load(dir+'\Images\plrrightattack'+str(x)+'.png').convert_alpha() for x in range(1,8)]
plrdown = [pygame.image.load(dir+'\Images\plrdown'+str(x)+'.png').convert_alpha() for x in range(1,7)]
plrright = [pygame.image.load(dir+'\Images\plrright'+str(x)+'.png').convert_alpha() for x in range(1,7)]
plrleft = [pygame.image.load(dir+'\Images\plrleft'+str(x)+'.png').convert_alpha() for x in range(1,7)]
plrup = [pygame.image.load(dir+'\Images\plrup'+str(x)+'.png').convert_alpha() for x in range(1,7)]
bat = [pygame.image.load(dir+'\Images\Bat'+str(x)+'.png').convert_alpha() for x in range(1,5)]

textfont = pygame.font.Font(dir+'\Text\Fancy.ttf',18)
pixelfont = pygame.font.Font(dir+'\Text\Pixel.ttf',18)
smallpixelfont = pygame.font.Font(dir+'\Text\Pixel.ttf',14)

tempkills,tempsign = 0,0
loop = 0
turned = 0
opened = False
questpage = False
den = 0
housevar = 0
hitcontr = 0
plrhit = False
colv,colsw = 0,True
idling = True
dead = False
plrinvincible = 0
dranx,drany,hranx,hrany = 0,0,0,0
dmg,crit,encords,dmgcontr = 0,False,(0,0),0
sprite = 0
clock = pygame.time.Clock()
direction = 'down'
blitlist,interactables = [],[]
colvar = 0
colswitch,inspeech,fade,alpha = True,-1,True,0
movevar = 0
changevar = 1000
enemylist = [1700,1500,'static',10,'bat',True,0,50,0,0],[1400,1800,'wander',10,'bat',True,0,120,0,0],[1550,1900,'static',10,'bat',True,0,0,0,0],[1600,1100,'wander',10,'bat',True,0,576,0,0]
deathvar = 0

BLACK = (0,0, 0)
WHITE = (255,255,255)
RED   = (255,0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
LGREEN = (66,244,95)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
#-----------------------------#
#   IMPORTANT  FUNCTIONS      #
#-----------------------------#
def redraw(interacted,plrspr):
    global plrx,plry,interactables,blitlist,paused,fade,alpha,moving,newarea,area,atk,kills,dmg,crit,encords,dmgcontr,damage,dranx,drany,shoes
    global colv,idling,colv,colsw,plrhit,hitcontr,hranx,hrany,health,housevar,questpage,opened,turned,loop,tempkills,tempsign
    tempsign = len(signlist)
    tempkills = kills
    if area == 'village1':
        win.blit(forestrm,(plrx + (winwidth/2), plry + (winheight/2)))  #if the area is village1 (the main area), do all of this stuff
        tempplr = 0
        for x,z in enumerate(blitlist):
            if (-z[2] - z[3]) >= plry:
                win.blit(z[0],(z[1] + plrx + (winwidth/2),z[2] + plry + (winheight/2))) #blit all the objects that are behind the player
        tpos = centerpic(plrspr)
        if plrinvincible > 0:
            if plrinvincible % 3 == 0:      #if the player was hit by a mob recently, make him invincible for a short period, and show it
                plrspr = blank
        win.blit(shadow, ((winwidth/2) - 14,(winheight/2) + 20))    #blit the shadow for the player
        if plrspr == plrupattack[0] or plrspr == plrupattack[1] or plrspr == plrupattack[2] or plrspr == plrupattack[3] or plrspr == plrupattack[4] or plrspr == plrupattack[5] or plrspr == plrupattack[6]:
            win.blit(plrspr, (tpos[0], tpos[1] - 16))   #these are the attack animations. The depend on the direction of the player
        elif plrspr == plrleftattack[0] or plrspr == plrleftattack[1] or plrspr == plrleftattack[2] or plrspr == plrleftattack[3] or plrspr == plrleftattack[4] or plrspr == plrleftattack[5] or plrspr == plrleftattack[6]:
            win.blit(plrspr, (tpos[0] - 26, tpos[1]))
        elif plrspr == plrrightattack[0] or plrspr == plrrightattack[1] or plrspr == plrrightattack[2] or plrspr == plrrightattack[3] or plrspr == plrrightattack[4] or plrspr == plrrightattack[5] or plrspr == plrrightattack[6]:
            win.blit(plrspr, (tpos[0] + 26, tpos[1]))
        else:
            win.blit(plrspr, (tpos[0], tpos[1]))
        for x,z in enumerate(blitlist):
            if (-z[2] - z[3]) < plry:
                win.blit(z[0],(z[1] + plrx + (winwidth/2),z[2] + plry + (winheight/2))) #blit all the objects that are infront of the player
        if newarea != area:
            blitlist = []
            interactables = []
            createcollide(area)
            fade = True
            music(dir+'\Sound\Villagesong.mp3',-1)  #start to play this beutiful melody if the area is being entered
            if newarea == 'house1':
                plrx,plry = -1976,-1950 #if player came from the house, he will start infront of the house
            elif newarea == 'cave1':
                plrx,plry = -1840,-486 #if they came from cave, they will start infron of cave
    elif area == 'house1':
        win.blit(housei1,(plrx + (winwidth/2), plry + (winheight/2)))
        for x,z in enumerate(blitlist):
            win.blit(z[0],(z[1] + plrx + (winwidth/2),z[2] + plry + (winheight/2)))
        if newarea != area:
            blitlist = []
            interactables = []
            createcollide(area) #create all the collisions and blits for the house
            fade = True
            music(dir+'\Sound\housesong.mp3',-1)
            if newarea != '':
                plrx,plry = -348,-380#if the game hasnt been played yet, start at this point
        if housevar == 250:
            if health < 5:
                health += 1 #heal the player by 1 heart in the house after every 250 frames. The house heals
            housevar = 0
        housevar += 1
        atk = False #attacking is not possible in the house or cave
        tpos = centerpic(playerspr)
        win.blit(plrspr, (tpos[0], tpos[1]))
    elif area == 'cave1':
        win.blit(cave,(plrx + (winwidth/2), plry + (winheight/2)))
        for x,z in enumerate(blitlist):
            win.blit(z[0],(z[1] + plrx + (winwidth/2),z[2] + plry + (winheight/2))) #same thing for the cave. Collisions, etc
        if newarea != area:
            blitlist = []
            interactables = []
            createcollide(area)
            fade = True
            if newarea != '':
                music(dir+'\Sound\cavesong.mp3',-1)
                plrx,plry = -400,-420
        atk = False
        tpos = centerpic(playerspr)
        win.blit(plrspr, (tpos[0], tpos[1]))
    #checkcollide(plrx,plry,True)             #remove the '#' to see collision rectangles ######################
    enemymove(plrx,plry)
    if damage[0] > 0:
        if dmgcontr < 20:   #if the player hit something, display it on the enemy. If it was a crit, make it yellow. do this for 20 frames
            dmgcontr += 1
            if damage[1]:
                colr = YELLOW
            else:
                colr = WHITE
            if dmgcontr == 1:
                dranx = random.randrange(-20,21)    #display it at a 'random' position relative to the enemy
                drany = random.randrange(-20,21)
            win.blit(smallpixelfont.render(str(damage[0]), False, colr), (damage[2][0] + 10 + dranx, damage[2][1] + 15 + drany))
        else:
            damage = (0, False, (damage[2]))
            dmgcontr = 0
    if plrhit or hitcontr > 0:
        hitcontr += 1
        if hitcontr == 1:
            hranx = random.randrange(-20,21)    #if the player was hit, display a red -1 'randomly' relative to the player for 20 frames
            hrany = random.randrange(-20,21)
        win.blit(smallpixelfont.render('-1', False, RED), (winwidth/2 + hranx, winheight/2 + hrany))
        plrhit = False
        if hitcontr == 20:
            hitcontr = 0
    if paused:  
        paused = pause(paused)  #if the game is paused, show the menu
    if newarea == area:
        if interacted != -1:  #this puts text on the screen if the player is in the speech event
            if interactables[interacted][2] != 'DOOR':
                for texts in npctext[interacted]: #this puts text in the screen in order from the NPCtext file. Each NPC has it's own value, and therefore, it's own text
                    speech(texts)
            if area == 'village1':
                if interacted == 2 or interacted == 3 or interacted == 4 or interacted == 5:
                    if interacted not in signlist:
                        signlist.append(interacted)
            elif area == 'cave1':
                if interacted == 1:
                    shoes = True
    newarea = area
    if fade:
        moving = False  #if rooms are changing, make it fade in, and make moving false
        fadesurface = pygame.Surface((winwidth,winheight))
        fadesurface.set_alpha(225 - alpha)
        win.blit(fadesurface,(0,0))
        alpha += 10
        if alpha > 255:
            fade = False
            moving = True
            alpha = 0
    for h in range(5):
        win.blit(deadheart,(20 + (h * 34), 20)) #display all the hearts. Dead are under the alive ones, but are covered
    for h in range(health):
        win.blit(heart,(20 + (h * 34), 20))
    ppos = centerpic(sidebox)
    win.blit(sidebox, (770, ppos[1]))
    win.blit(pixelfont.render('Signs', False, WHITE), (winwidth - 100,ppos[1]))
    win.blit(pixelfont.render(str(len(signlist)) + '/4', False, WHITE), (winwidth - 80,ppos[1] + 25))   #display the sidebar of stats
    win.blit(pixelfont.render('Kills', False, WHITE), (winwidth - 100,ppos[1] + 65))
    win.blit(pixelfont.render(str(kills), False, WHITE), (winwidth - 80,ppos[1] + 90))
    if len(signlist) == 4 and tempsign != len(signlist):
        opened = False
    if kills == 15 and tempkills != kills:
        opened = False
    if questpage:
        opened = True
        ppos = centerpic(textbox)
        win.blit(textbox, (ppos[0],ppos[1]))
        tpos = centertext('QUESTS',textfont)
        text = spacetext('QUESTS')
        if len(signlist) == 4 and kills >= 15:
            colr = LGREEN
        else:
            colr = BLACK
        win.blit(textfont.render(text, False, colr), (tpos[0], tpos[1] - 50))
        tpos = centertext('Talk to all 4 signs', textfont)
        text = spacetext('Talk to all 4 signs')
        if len(signlist) == 4:
            colr = LGREEN
        else:
            colr = BLACK
        win.blit(textfont.render(text, False, colr), (tpos[0], tpos[1]))
        tpos = centertext('Kill 15 Bats', textfont)
        text = spacetext('Kill 15 Bats')
        if kills >= 15:
            colr = LGREEN
        else:
            colr = BLACK
        win.blit(textfont.render(text, False, colr), (tpos[0], tpos[1] + 50))
    win.blit(scroll, (winwidth - 40, 14))
    if len(signlist) == 4 or kills >= 15:
        if opened == False:
            turned += 1
            if turned <= 50:
                win.blit(gscroll, (winwidth - 40, 14))
            if turned == 100:
                turned = 0
    win.blit(smallpixelfont.render('Q', False, WHITE), (winwidth - 30, 20))
    if dead:
        win.fill(BLACK)
        tpos = centertext('You Died...',pixelfont)
        text = spacetext('You Died...')
        win.blit(pixelfont.render(text, False, WHITE), (tpos[0],tpos[1]))   #this is the death screen
        tpos = centertext('Press SPACE to restart',pixelfont)
        text = spacetext('Press SPACE to restart')
        if colv < 255 and colsw:
            colv += 5
        if colv == 255:
            colsw = False
        if colsw == False:  #this makes the colour changing text
            colv -= 5
        if colv == 0:
            colsw = True
        win.blit(pixelfont.render(text, False, (colv,colv,colv)), (tpos[0],tpos[1] + 50))
    pygame.display.update()
    win.fill(BLACK)

def enemymove(plrx,plry):
    global enemylist,changevar,enemystate,randdirection,sprite,deathvar,kills   #this function has control over the enemies movements
    for enemynum in range(len(enemylist)):
        if enemylist[enemynum][3] <= 0 and enemylist[enemynum][5] == True:  #if they are dead, make them blink, and unhittable. Increase the kill stat
            if deathvar % 10 == 0 or deathvar % 5 == 0:
                win.blit(bat[sprite//10], (enemylist[enemynum][0] + plrx + (winwidth/2),enemylist[enemynum][1] + plry + (winheight/2)))
                win.blit(shadow, (enemylist[enemynum][0] + plrx + 20 + (winwidth/2),enemylist[enemynum][1] + plry + 64 + (winheight/2)))
                if deathvar == 50:
                    enemylist[enemynum][5] = False
                    deathvar = 0
                    kills += 1
            deathvar += 1
        elif enemylist[enemynum][5]:
            win.blit(bat[sprite//10], (enemylist[enemynum][0] + plrx + (winwidth/2),enemylist[enemynum][1] + plry + (winheight/2)))
            win.blit(shadow, (enemylist[enemynum][0] + plrx + 20 + (winwidth/2),enemylist[enemynum][1] + plry + 64 + (winheight/2)))
            if enemylist[enemynum][7] == 2000:
                if random.randrange(0,2) == 1:
                    enemylist[enemynum][2] = random.choice(('static','wander')) #choose a state for a mob 'randomly'
                else:
                    enemylist[enemynum][2] = enemylist[enemynum][2]
                enemylist[enemynum][7] = 0
            else:
                if enemylist[enemynum][2] == 'static':  #if the mob is static, they will not move, but count down till they get a chance at changing states
                    enemylist[enemynum][7] += 1
                if enemylist[enemynum][2] == 'wander':  #if the mob is in the wander state, every 200 frames, it will move. Every 200 frames it wont move.
                    if enemylist[enemynum][6] > 200:
                       enemylist[enemynum][6] += 1
                    if enemylist[enemynum][6] > 400:
                        enemylist[enemynum][6] = 0
                    if enemylist[enemynum][6] == 0:     #every 400 frames, it will change direction to travel
                        randdirection = random.choice(((0,0.6,'up'),(0,-0.6,'down'),(0.6,0,'left'),(-0.6,0,'right'),(0.3,0.3,'topl'),(-0.3,0.3,'topr'),(0.3,-0.3,'botl'),(-0.3,-0.3,'botr')))
                        enemylist[enemynum][8] = randdirection[0]
                        enemylist[enemynum][9] = randdirection[1]
                    if enemylist[enemynum][6] % 2 == 0 and movevar <= 200:
                        enemylist[enemynum][0] += enemylist[enemynum][8]
                        enemylist[enemynum][1] += enemylist[enemynum][9]
                    enemylist[enemynum][6] += 1
                enemylist[enemynum][7] += 1
    if sprite <= 30:
        sprite += 1
    if sprite == 31:
        sprite = 0

def blit(image, posx, posy,area,past):        #this function blits images on to the screen. I have it this way because when the player moves, all of these images need to move too. They are moved in the 'redraw' function.
    global blitlist
    win.blit(image,(posx,posy))
    blitlist.append([image, posx, posy, past])

def createcollide(rm):    #this function creates collisions and interactables depending on the room. It is called when a room is entered.
    global collidelist,npctext,area
    if rm == 'village1':
        househalf = 200
        rockhalf,loghalf,grasshalf = 10,10,0
        treehalf,tree1half,tree2half = 90,90,156 #these 'halves' are to determine when the object should blit infron of the player
        blit(house1, 1794, 1710, area,househalf),blit(rock, 1682, 1980, area,rockhalf),blit(log, 1544, 1780, area,loghalf),blit(tree, 1420, 1600, area,treehalf),blit(tree1, 1540, 1600, area,tree1half),blit(tree2, 1450, 1580, area,tree2half)
        blit(tree, 1400, 1680, area,treehalf),blit(tree1, 1700, 1940, area,tree1half),blit(tree2, 1800, 1480, area,tree2half),blit(tree2, 1000, 1820, area,tree2half)
        blit(grass,1532,1868,area,grasshalf),blit(grass,1548,1868,area,grasshalf),blit(grass,1516,1884,area,grasshalf),blit(grass,1532,1884,area,grasshalf),blit(grass,1548,1884,area,grasshalf),blit(grass,1564,1884,area,grasshalf)
        blit(tree2, 1500, 900, area, tree2half),blit(tree1, 1900, 800, area, tree1half),blit(tree, 2100, 1200, area, treehalf)
        for z in range(5):
            blit(grass,1578,1884 + (z * 16),area,grasshalf)
            for x in range(5):
                blit(grass,1500 + (x * 16), 1900 + (z * 16),area,grasshalf)
        for z in range(7):
            for x in range(7):
                blit(grass,1800 + (x * 16), 1100 + (z * 16),area,grasshalf)
        blit(grass,2000,1200,area,grasshalf),blit(grass,2016,1200,area,grasshalf),blit(grass,2000,1216,area,grasshalf),blit(grass,2016,1216,area,grasshalf)
        collidelist = Collisions.collidelist
        addinteract(1960,1922,'DOOR',blank,'village1'),addinteract(1826,464,'DOOR',blank,'village1'),addinteract(2060,1690,'NPC',sign,'village1')
        addinteract(2220,660,'NPC',sign,'village1'),addinteract(1100,500,'NPC',sign,'village1'),addinteract(2030,1940,'NPC',sign,'village1')
        npctext = NPCtext.npctext
        area = 'village1'
    if rm == 'house1':
        collidelist = Collisions.collidelisthouse1
        addinteract(330,420,'DOOR',blank,'house1'),addinteract(172,240,'NPC',blank,'house1'),addinteract(172,270,'NPC',blank,'house1')
        npctext = NPCtext.npctexthouse1
        area = 'house1'
    if rm == 'cave1':
        collidelist = Collisions.collidelistcave1
        blit(npc1,560,250,area,10)
        addinteract(384,392,'DOOR',blank,'cave1'),addinteract(562,290,'NPC',blank,'cave1')
        npctext = NPCtext.npctextcave1
        area = 'cave1'

def pause(paused):  #this is the pause menu
    global inGame
    surf = pygame.Surface((winwidth,winheight))
    surf.set_alpha(150)
    win.blit(surf,(0,0))
    pauseopts,quitopts = 0,1
    while paused:
        ppos = centerpic(pausemenu)
        win.blit(pausemenu, (ppos[0], ppos[1]))
        pygame.draw.rect(win, WHITE, (340, 250 + (pauseopts * 60), 200, 4))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    #if the player hits w, it will move the option up/down
                if event.key == pygame.K_w:
                    pauseopts -= 1
                elif event.key == pygame.K_s:
                    pauseopts += 1
                elif event.key == pygame.K_ESCAPE:  #this will exit the pause menu
                    paused = False
                    return paused
                elif event.key == pygame.K_SPACE:   #this will select the option being hovered on
                    if pauseopts == 0:
                        paused = False
                        return paused
                    elif pauseopts == 1:    #this will save the game. It will save X cord of plr, Y cord of plr, the area, the signs they have interacted with,
                        ppos = centerpic(gamesaved) #the number of kills, if or not they have shoes, and their health
                        win.blit(gamesaved, (ppos[0], ppos[1])) #blits 'game saved'
                        pygame.display.update()
                        file = open('save.txt','w')
                        file.write(str(plrx)),file.write('\n'),file.write(str(plry)),file.write('\n'),file.write((area)),file.write('\n'),
                        for s in range(len(signlist)):
                            if signlist[s] == int(signlist[s]):
                                file.write(str(signlist[s],))
                        file.write('\n'),file.write(str(kills)),file.write('\n'),file.write(str(shoes)),file.write('\n'),file.write(str(health))
                        file.close()
                        pygame.time.delay(1000)
                    elif pauseopts == 2:
                        print('not implemented yet, but options')   #this is for a future update. yes. a future update.
                    elif pauseopts == 3:
                        choice = True
                        while choice:
                            ppos = centerpic(areyousure)    #this is for exiting the game. It will first prompt you, and ask if you are sure
                            win.blit(areyousure, (ppos[0], ppos[1]))
                            pygame.draw.rect(win, WHITE, (395 + (quitopts * 70), 360, 30, 4))
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_d:
                                        quitopts += 1
                                    elif event.key == pygame.K_a:
                                        quitopts -= 1
                                    elif event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                                        if quitopts == 0:
                                            inGame = False
                                            return
                                        else:
                                            quitopts = 1
                                            choice = False
                            if quitopts == -1:
                                quitopts = 1
                            if quitopts == 2:
                                quitopts = 0
                            pygame.display.update()
        if pauseopts == -1:
            pauseopts = 3
        if pauseopts == 4:
            pauseopts = 0
        pygame.display.update()

def speech(text):
    print(text)
    speed,idling,y = 1,True,0
    win.blit(textbox, (30,15))
    texts = text.split('//')    #Gosh Mr Jones, I hate the way you did this, but it works so much better hahaha
    for z in texts:
        y += 30
        tpos = centertext(z,pixelfont)
        twid = (winwidth - 2*tpos[0]) / len(z)
        for v in range(len(z)): #this function is what blits the text when talking to NPCs
            win.blit(pixelfont.render(z[v], False, BLACK), (60 + (v * twid), y))
            pygame.time.delay(speed * 100)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        speed = 0
    while idling:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    idling = False
        
#-----------------------------------#
#           CHECK FUNCTIONS         #
#-----------------------------------#

def checkcollide(plrx, plry,show=False):       #this functions checks if a player hits a collision wall every time the player moves. If they did, it well send a 'False' to the movement manager, which will deal with it from there
    collisions = []
    for x in range(len(collidelist)):
        if show:
            pygame.draw.rect(win, collidelist[x][0], (-collidelist[x][1] + plrx + (winwidth/2), -collidelist[x][2] + plry + (winheight/2), collidelist[x][3], collidelist[x][4]))
        if (plrx + 10) >= collidelist[x][1] - collidelist[x][3] and (plrx - 10) <= collidelist[x][1] and (plry - 22) >= collidelist[x][2] - collidelist[x][4] and (plry - 26) <= collidelist[x][2]:
            return False
    return True

def addinteract(x,y,kind,img,area):  #this adds interactables to the world. It appends them to an array, blits them on the screen, and adds a collision box to them.
    interactables.append([x,y,kind])
    blit(img,x,y,area,10)
    if kind == 'NPC':
        collidelist.append([RED,-x,-y,32,32])
    elif kind == 'DOOR':
        collidelist.append([BLUE,-x,-y,32,32])

def interact():    #when space is pressed, this function is called. It will call an interaction, depending on the interacted object 'kind'.
    for z in range(len(interactables)): #this tests if theres an interactable object within a few feet of the player
        if (interactables[z][0] + plrx + (winwidth/2)) < ((winwidth/2) + 14) and (interactables[z][0] + plrx + (winwidth/2)) > ((winwidth/2) - 48) and (interactables[z][1] + plry + (winheight/2)) < ((winheight/2) + 35) and (interactables[z][1] + plry + (winheight/2)) > ((winheight/2) - 15):
            return z
    return -1

#-----------------------------------#
#           RANDOM FUNCTIONS        #
#-----------------------------------#

def titletext(title,speed,click,bitbybit,font,colvar):     #make text for a title. Inputs: (String,Int for display speed, if req click to proceed, if instant blit, fade variable)
    win.fill(BLACK)
    tpos = centertext(title,font)
    if speed != 0:
        for x in range(len(title)):             #if blit letter by letter
            twid = (winwidth - 2*tpos[0]) / len(title)
            win.blit(font.render(title[x], False, WHITE), (tpos[0] + (x * twid), tpos[1]))
            pygame.time.delay(speed * 100)
            pygame.display.update()
    else:                                       #if instant blit
        text = spacetext(title)
        win.blit(font.render(text, False, WHITE), (tpos[0], tpos[1]))
    if click:                                   #if req click to proceed title
        idling = True
        while idling:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        idling = False
            pygame.time.delay(10)
            colvar = fading(colvar)
            win.blit(font.render('Hit Space To Continue...', False, (colvar,colvar,colvar)), (winwidth - 390,winheight - 50))
            pygame.display.update()

def shaketext(text,font):   #this is useless currently, but will be used for future updates. It just shakes the text around 'randomly'
    tpos = centertext(text,font)
    text = spacetext(text)
    for x in range(0,20):
        rval = random.randrange(2,6)
        win.blit(font.render(text, False, WHITE), (tpos[0] + rval, tpos[1] - rval))
        pygame.time.delay(25)
        pygame.display.update()
        win.fill(BLACK)

def fadeout(drawtext,font,picture = blank, pposx = 0,pposy = 0):
    fadesurface = pygame.Surface((winwidth,winheight))     #make a surface called fadesurface
    titletext(drawtext,0,False,False,font,colvar)    #make the centered title text
    ppos = centerpic(picture)                   #get a centered picture's position
    fadesurface.fill(BLACK)                     #make the fade surface black
    for alpha in range(0,300):                  #start the fade
        fadesurface.set_alpha(alpha)
        titletext(drawtext,0,False,False,font,colvar)
        win.blit(picture, (pposx,pposy))
        win.blit(fadesurface,(0,0))
        pygame.time.delay(5)
        pygame.display.update()
        win.fill(WHITE)

def centertext(text,font):   #Center the text in the middle of the screen.
    text = spacetext(text)
    text = font.render(text, True, WHITE)
    tpos = ((winwidth/2) - (text.get_rect().width / 2), (winheight/2) - (text.get_rect().height / 2))   #gets half the height, half the width, and takes away half the
    return tpos                                                                                             #size of the rect from it to center it

def picfade(picture,speed): #Make a picture go from top to bottom, and fade from white to none, to black.
    fadesurface = pygame.Surface((winwidth,winheight))
    fadesurface.fill((WHITE))
    ppos = centerpic(picture)
    for alpha in range(0,225):  #Fade from white to picture
        fadesurface.set_alpha(225 - alpha)
        win.blit(picture, (ppos[0],ppos[1] - 500 + (speed * alpha)))
        win.blit(fadesurface,(0,0))
        pygame.time.delay(5)
        pygame.display.update()
        win.fill(WHITE)
    fadesurface.fill(BLACK)
    for alpha in range(0,300):  #Fades to black from picture
        fadesurface.set_alpha(alpha)
        win.blit(picture, (ppos[0],ppos[1] - 500 + (speed * (225 + alpha))))
        win.blit(fadesurface,(0,0))
        pygame.time.delay(5)
        pygame.display.update()
        win.fill(WHITE)

def centerpic(pic): #Center a picture in the middle of the screen
    ppos = ((winwidth/2) - (pic.get_rect().width / 2), (winheight/2) - (pic.get_rect().height / 2))
    return ppos

def fading(colvar):   #Make a fade from black to white and back again
    global colswitch
    if colvar < 255 and colswitch:
        colvar += 5
    if colvar == 255:
        colswitch = False
    if colswitch == False:
        colvar -= 5
    if colvar == 0:
        colswitch = True
    return colvar

def music(song,loop=0):    #Play a sound/song with input of the sound file
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loop)

def spacetext(text):
    text = (text.replace("", "  ")[1: -1])
    return text

def load(reset): #this loads from a file.
    global shoes,plrx,plry,area,newarea,kills,signlist,health,plrinvincible
    plrinvincible = 1
    values,nextlist = [],[]
    savefile = open('save.txt','r')
    for lines in savefile:
        values.append(lines.split())
    if values == [] or reset == True:    #if nothing is in the save file, create stuff'
        logo()
        shoes = False
        plrx,plry = -550,-390
        area,newarea = 'house1',''
        kills = 0
        signlist = []
        health = 5
        intro()
    else:   #if there is stuff in the save file, load it
        plrx,plry,area,newarea,asignlist,kills,health = int(values[0][0]), int(values[1][0]), values[2][0], '', values[3], int(values[4][0]), int(values[6][0])
        if values[5] == ['False']:
            shoes = False
        elif values[5] == ['True']:
            shoes = True
        signlist = []
        asignlist = str(asignlist)
        if len(asignlist) != 0:
            for x in range(len(asignlist)):
                nextlist.append(asignlist[x])
            for z in range(len(nextlist)):
                if nextlist[z].isdigit():
                    signlist.append(int(nextlist[z]))   #signs were the most annoying part of this, since they were in a list
        else:
            signlist = []

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/##/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
#-------------------------------------------#
#                   STORY                   #
#-------------------------------------------#

def logo():    #this is the logo at the beginning of the game
    titletext('CocoBit Games',0,False,False,pixelfont,colvar)
    ppos = centerpic(CocoBit50x50)
    win.blit(CocoBit50x50, (ppos[0],ppos[1] + 50))
    pygame.display.update()
    pygame.time.wait(2000)
    win.fill(BLACK)
    titletext('CocoBit Games',0,False,False,pixelfont,colvar)
    win.blit(CocoBit50x50P2, (ppos[0],ppos[1] + 50))
    pygame.display.update()
    music(dir+'\Sound\COCOBITCRUNCH.wav')
    pygame.time.wait(2000)
    fadeout('CocoBit Games',pixelfont,CocoBit50x50P2, ppos[0],ppos[1] + 50)
    ppos = centerpic(playerspr)
    win.fill(BLACK)
    pygame.display.update()

def intro():    #this is the speech that shows at the beginning of the game
    speech('ARYA:Welcome!//This is the land of//Noname! I will be your guide!//Use SPACEBAR to continue')
    speech('ARYA:Use the WASD keys//to move around!')
    speech('ARYA:The SPACEBAR is your//interaction button! Use//it to interact with NPCs//and to chat!')
    speech('ARYA:If you have found the//SHOES,you can press//and hold Left SHIFT to//sprint!')
    speech('ARYA:Press Q to open the//quests menu! Try to//complete them all!')
    speech('ARYA:The house is also a//safe zone,where you can//regenerate life! Just//stand around for a bit!')
    speech('ARYA:Press ESC to open the//game menu!')
    speech('ARYA:Lastly,the ENTER key//is your attack key!//It only works outside//though. That way its safe!')
    speech('ARYA:Cmon,go ahead!')

#-------------------------------#
#           STARTING            #
#-------------------------------#
inGame = True
moving,paused,shoes = True,False,False
plrvar,plrspr = 0,plrdown[0]
interacted = -1
plratkvar = 0
atk = False
damage = (0, False, (0,0))
load(False)
createcollide(area)
redraw(interacted,plrspr)
while inGame:
    if moving:
        keys = pygame.key.get_pressed()  #checking pressed keys and making sure no collision occurs
        xvar,yvar = 0,0
        if shoes:
            if keys[pygame.K_LSHIFT]:
                speed = 3
            else:
                speed = 2
        else:
            speed = 2
        if keys[pygame.K_s] and checkcollide(plrx,plry) != False and atk == False:  #this moves the player, and makes sure no collisions are occurring.
            yvar -= speed
            direction = 'down'
        if keys[pygame.K_w] and checkcollide(plrx,plry) != False and atk == False:  #it also changes the direction the player is facing for attacking and sprite changes
            yvar += speed
            direction = 'up'
        if keys[pygame.K_a] and checkcollide(plrx,plry) != False and atk == False:
            xvar += speed
            direction = 'left'
        if keys[pygame.K_d] and checkcollide(plrx,plry) != False and atk == False:
            xvar -= speed
            direction = 'right'
        if checkcollide(plrx + xvar,plry + yvar) == False and atk == False:
            if checkcollide(plrx  + xvar,(plry - speed)) == True: #trouble shoot by putting 8 coords around the dot and see which one is free
                yvar -=speed
            elif checkcollide((plrx - speed + xvar),plry + yvar) == True:   #this checks 8 positions around the player, and takes whichever one is free
                xvar -= speed
            elif checkcollide(plrx + xvar,(plry + speed) + yvar) == True:
                yvar += speed
            elif checkcollide((plrx + speed) + xvar,plry + yvar) == True:
                xvar += speed
            elif checkcollide((plrx + speed) + xvar,(plry + speed) + yvar) == True:
                yvar += speed
                xvar += speed
            elif checkcollide((plrx - speed) + xvar,(plry - speed) + yvar) == True:
                xvar -= speed
                yvar -= speed
            elif checkcollide((plrx - speed) + xvar,(plry + speed) + yvar) == True:
                yvar += speed
                xvar -= speed
            elif checkcollide((plrx + speed) + xvar,(plry - speed) + yvar) == True:
                xvar += speed
                yvar -= speed
        if plrvar != 50:
            if plrx != (plrx+xvar) or plry != (plry+yvar):
                plrvar += 1
            else:
                plrvar = 0
        else:
            plrvar = 0
        if not atk:
            if direction == 'up':
                plrspr = plrup[plrvar//10]  #this is the move animation. It takes a direction, and changes the player sprite
            elif direction == 'down':
                plrspr = plrdown[plrvar//10]
            elif direction == 'left':
                plrspr = plrleft[plrvar//10]
            elif direction == 'right':
                plrspr = plrright[plrvar//10]
        if atk:
            plratkvar += 1
            if direction == 'up':   #the same thing for attacking
                plrspr = plrupattack[plratkvar//3]
            elif direction == 'down':
                plrspr = plrdownattack[plratkvar//3]
            elif direction == 'left':
                plrspr = plrleftattack[plratkvar//3]
            elif direction == 'right':
                plrspr = plrrightattack[plratkvar//3]
        if plratkvar == 18:
            plratkvar = 0
            atk = False
        plrx += xvar
        plry += yvar
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    #if the spacebar is pressed, the interaction event will be called to check if an interaction occurred.
                if event.key == pygame.K_SPACE:
                    interacted = interact()
                    if len(interactables) != 0 and interacted != -1:
                        if interactables[interacted][2] == 'DOOR':  #if the interaction is a kind 'DOOR', then the area changes.
                            area = npctext[interacted]
                if event.key == pygame.K_RETURN and atk == False:
                    if area == 'village1':
                        swingsound.play()
                    if direction == 'up':
                        hitrect = pygame.Rect(winwidth/2 - 16, winheight/2 - 48, 32, 64)    #this is the attacking mechanism. It draws a rect, and check for
                    elif direction == 'down':                                                   #the collision of another mob inside of it
                        hitrect = pygame.Rect(winwidth/2 - 16, winheight/2 + 16, 32, 64)
                    elif direction == 'left':
                        hitrect = pygame.Rect(winwidth/2 - 64, winheight/2 - 16, 64, 32)
                    elif direction == 'right':
                        hitrect = pygame.Rect(winwidth/2 + 0, winheight/2 - 16, 64, 32)
                    for ens in range(len(enemylist)):
                        if enemylist[ens][5]:
                            if hitrect.colliderect(pygame.Rect(enemylist[ens][0] + plrx + (winwidth/2) + 16,enemylist[ens][1] + plry + (winheight/2) + 16, 32, 48)):
                                if enemylist[ens][3] >= 0:
                                    encords = (enemylist[ens][0] + plrx + (winwidth/2) + 16, enemylist[ens][1] + plry + (winheight/2) + 16)
                                    dmg = random.randrange(1,6)
                                    if dmg == 1:
                                        dmg = 8
                                        crit = True #this is the damage value when hitting a mob.
                                    else:
                                        crit = False
                                    enemylist[ens][3] -= dmg
                                    hitsound.play()
                                    damage = (dmg, crit, (encords))
                    atk = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                elif event.key == pygame.K_q:
                    if questpage == False:
                        questpage = True
                    else:
                        questpage = False
        for ens in range(len(enemylist)):   #if the player is inside the rect of a mob, and the mob is alive (not blinking away or dead), damage the player
            if enemylist[ens][5]:               #for 1 heart
                if enemylist[ens][3] > 0:
                    if (pygame.Rect(winwidth/2 - 16, winheight/2 - 16, 32, 32)).colliderect(pygame.Rect(enemylist[ens][0] + plrx + (winwidth/2) + 16,enemylist[ens][1] + plry + (winheight/2) + 16, 32, 48)) or plrinvincible > 0:
                        if plrinvincible == 0:
                            health -= 1
                            playerhit.play()
                            plrhit = True
                        plrinvincible += 1
                        if plrinvincible == 150:
                            plrinvincible = 0
                        if health == 0:
                            music(dir+'\Sound\deathsong.mp3',-1)
    if health == 0:
        dead = True
        moving = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    load(True)
                    dead = False
                    moving = True
    for e in range(len(enemylist)):
        if enemylist[e][5] == False and den == 1000:    #if an enemy is dead, it will respawn when death enemy variable is 1000. Only 1 will respawn at a time.
            enemylist[e][3] = 10                            #this will prevent too many mobs spawning at once. Less overwhelming. Easier for Mr Jones :)
            enemylist[e][5] = True
            den += 1
    den += 1
    if den > 1000:
        den = 0
    redraw(interacted,plrspr)
    interacted = -1
    clock.tick(80)
pygame.quit()
