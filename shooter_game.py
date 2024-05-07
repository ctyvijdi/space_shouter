#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as timer
mixer.init()
font.init()

mixer.music.load('space.ogg')
kick = mixer.Sound("fire.ogg")
window = display.set_mode((1000,700))
display.set_caption('Shooter')
bg = transform.scale(image.load('galaxy.jpg'),(1000,800))
game = True
clock = time.Clock()
FPS = 120
finish = False
a = 0
b = 0
font2 = font.SysFont('Arial',36)
#!
class Game_Sprite(sprite.Sprite):
    def __init__(self,x,y,name,speed,waith,heigth):
        super().__init__()
        self.image = transform.scale(image.load(name),(waith,heigth))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def start(self):
        self.rect.x = 300
        self.rect.y = 550

class Player(Game_Sprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 900:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        ammo = Ammo(self.rect.x + 35,self.rect.y - 50,"bullet.png",5,30,60)
        ammors.add(ammo)

class Enemy(Game_Sprite):
    def update(self):
        global a
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.rect.y = -100
            self.rect.x = randint(100,900)
            a += 1
class Ammo(Game_Sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()
class asteroid(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
                self.rect.y = -100
                self.rect.x = randint(100,900)
#?
player = Player(300,550,"rocket.png",10,100,100)
enemys = sprite.Group()
ammors = sprite.Group()
asteroids = sprite.Group()
for i in range(5):    
    enemy = Enemy(randint(100,900),100,"ufo.png",randint(2,5),126,66)
    enemys.add(enemy)
for i in range(2):
    asteroid1 = asteroid(randint(100,900),100,"asteroid.png",randint(2,5),126,66)
    asteroids.add(asteroid1)
mixer.music.play()
font1 = font.SysFont("Arial", 50)
font3 = font.SysFont("Arial", 150)

lvl1 = font2.render("Уничтоженных:", True,(255,100,0))
lvl2 = font2.render("Пропущенных:", True,(255,100,255))
win = font3.render("YOU WIN!", True,(255,100,0))
lose = font3.render("YOU LOSE!", True,(100,215,0))
contin = font1.render("Want continue? Press F or Press ESC to Exit", True,(151,255,0))
reload1 = font1.render("Wait Reload...", True,(255,0,0))


res_time = False
num_fire = 0

#TODO
t = 4
while game:
    clock.tick(FPS)
    for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if res_time == False:
                        player.fire()
                        num_fire += 1
                if e.key == K_ESCAPE:
                    game = False
                if e.key == K_f and finish == True:
                    a = 0
                    b = 0
                    t = 4
                    num_fire = 0
                    res_time = False
                    finish = False
                    del asteroids
                    del enemys
                    asteroids = sprite.Group()
                    for i in range(2): 
                        asteroid1 = asteroid(randint(100,900),-100,"asteroid.png",randint(2,5),126,66)
                        asteroids.add(asteroid1)
                    enemys = sprite.Group()    
                    for i in range(5):   
                        enemy = Enemy(randint(100,900),-100,"ufo.png",randint(2,5),126,66)
                        enemys.add(enemy)
                    player.start()

                
    if finish != True:

        window.blit(bg,(0,0))
        window.blit(lvl1, (0, 0))
        window.blit(font1.render(str(b), True,(255,100,0)), (235, 0))
        window.blit(lvl2, (0, 50))
        window.blit(font1.render(str(a), True,(255,100,255)), (230, 50))
        window.blit(font1.render(str(t), True,(255,100,255)), (900, 0))
        

        player.reset()
        player.update()

        enemys.update()
        enemys.draw(window)

        asteroids.update()
        asteroids.draw(window)

        ammors.update()
        ammors.draw(window)
        sprintes_list1 = sprite.spritecollide(player,asteroids, True)
        for e in event.get():
            if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        if num_fire <= 5 and res_time == False:
                            player.fire()
                            num_fire += 1
                    if num_fire >= 6 and res_time == False:
                        res_time = True
                        st_time = timer()
        if num_fire >= 6 and res_time == True:
            st_time1 = timer()
            if st_time1 - st_time >= 3:
                res_time = False
                num_fire = 0
            else:
                window.blit(reload1,(400,650))
        for e in sprintes_list1:
            t -= 1
            asteroid1 = asteroid(randint(100,900),-100,"asteroid.png",randint(2,5),126,66)
            asteroids.add(asteroid1)
            
        sprintes_list1 = sprite.spritecollide(player,enemys, True)
        for d in sprintes_list1:
            t -= 1
            enemy = Enemy(randint(100,900),-100,"ufo.png",randint(2,5),126,66)
            enemys.add(enemy)

        sprintes_list2 = sprite.groupcollide(enemys, ammors, True, True)
        for ammo in sprintes_list2:
            enemy = Enemy(randint(100,900),-100,"ufo.png",randint(2,5),126,66)
            enemys.add(enemy)
            b += 1
            if b >= 10:
                window.blit(win, (300, 300))
                window.blit(contin, (200, 450))
                finish = True
        if a >= 5:
            window.blit(lose, (300, 300))
            window.blit(contin, (200, 450))
            finish = True
        if t <= 0:
            window.blit(lose, (300, 300))
            window.blit(contin, (200, 450))
            finish = True

        



    display.update()
        