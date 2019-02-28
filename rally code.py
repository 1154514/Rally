import pygame
pygame.init()

start = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Rally Code")


walkRight = [
pygame.image.load('/home/jorge.181316/Almus/player_12.png'),
pygame.image.load('/home/jorge.181316/Almus/player_13.png')]
walkLeft = [
pygame.image.load('/home/jorge.181316/Almus/player_14.png'), 
pygame.image.load('/home/jorge.181316/Almus/player_15.png')]
background = pygame.image.load('/home/jorge.181316/Almus/Sample.png')
char = pygame.image.load('/home/jorge.181316/Almus/player_23.png')

clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 3, 34, 54)
        
    def draw(self, start):
        if self.walkcount + 1 >= 4:
            self.walkcount = 0
        
        if not(self.standing):
            if self.left:
                start.blit(walkLeft[self.walkcount//2], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                start.blit(walkRight[self.walkcount//2], (self.x, self.y))
                self.walkcount += 1
        else: 
            if self.right:
                start.blit(walkRight[0], (self.x, self.y))
            else: 
                start.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 3, 34, 54)
        #pygame.draw.rect(start, (255,0,0), self.hitbox,2) 
         
class projectiles(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self, start):
        pygame.draw.circle(start, self.color, (self.x, self.y), self.radius)
        
class enemy(object):
    WalkRight = [
    pygame.image.load('/home/jorge.181316/Almus/zombie_walk1.png'),
    pygame.image.load('/home/jorge.181316/Almus/zombie_walk2.png')]
    WalkLeft = [
    pygame.image.load('/home/jorge.181316/Almus/zombie_skid.png'),
    pygame.image.load('/home/jorge.181316/Almus/zombie_walk2.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y + 30, 45, 70)
        self.health = 100
        self.visible = True
        
    def draw(self, start):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 2:
                self.walkcount = 0 
            if self.vel > 0:
                start.blit(self.WalkRight[self.walkcount//4], (self.x, self.y))
                self.walkcount += 1
            else:
                start.blit(self.WalkLeft[self.walkcount//4], (self.x, self.y))
                self.walkcount += 1
            pygame.draw.rect(start, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(start, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((.5) * (100 - self.health)), 10))
            self.hitbox = (self.x + 20, self.y + 30, 45, 70)
            #pygame.draw.rect(start, (255,0,0), self.hitbox,2)
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0 
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            print('hit')
    
def redrawGameWindow():
    start.blit(background, (0 ,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    start.blit(text, (390, 10))
    man.draw(start)
    goblin.draw(start)
    for bullet in bullets:
        bullet.draw(start)
        
    pygame.display.update()

font = pygame.font.SysFont('comicsans', 30, True, True)
man = player(300, 440, 2, 2)
goblin = enemy(0, 400, 2, 2, 450)
shootloop = 0
bullets = []
run = True
while run:
    clock.tick(64)
    
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shootloop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectiles(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))
        
        shootloop = 1
    
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True 
        man.left = False 
        man.standing = False
    else:
        man.standing = True
        man.walkcount = 0
    
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkcount = 0
    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * 0.5 * neg
            man.jumpcount -= 1
        else: 
            man.isJump = False
            man.jumpcount = 10
    
    redrawGameWindow()
    
pygame.quit()