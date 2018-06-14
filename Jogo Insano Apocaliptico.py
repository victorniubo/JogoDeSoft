'''
O código foi feito com base no tutorial de pygame do canal Kids Can Code do youtube,
muitas de suas "features" foram tiradas de lá porém houveram mudanças e implementações.
Entre elas:
- Movimentaçao no eixo y
- Inimigos que atiram e tem movimentaçao aleatória
- Diferentes tipos de powerup's
- Batalha com Boss
- Mecanica de batalha com boss diferente da normal
- Escolha de naves diferentes com atributos diferentes
- Meteoros com vida baseada no tamanho
- Tipos diferentes de blaster para cada nave
- Telas diferentes alem da inicial e de game over  


Autores: Giovanni Santos, Victor Niubó
    
'''

import pygame as pg
import random
import os
import sys

WIDTH = 1200
HEIGHT = 700
FPS = 60

POWERUP_TIME = 5000
# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

# Set up assets folders
# Windows: "C:\Users\ienzo\Documents/Images"
# Mac: "/Users/ienzo/Documents/Images"
game_folder = os.path.dirname(__file__)
player_folder = os.path.join(game_folder, 'Player')
mob_folder = os.path.join(game_folder, 'Mobs')
meteor_folder = os.path.join(game_folder, 'Meteors')
background_folder = os.path.join(game_folder, 'Background')
explosion_folder = os.path.join(game_folder, 'Explosions')
powerup_folder = os.path.join(game_folder, 'PowerUps')
sound_folder = os.path.join(game_folder, 'Sounds')

BOSS_HEALTH = 1000
HITPOINTS = 200
VELOCIDADE = 7
DAMAGE = 30
nave = 'nave_v.png'

# Inicializa o programa
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
fundo = pg.image.load(os.path.join(background_folder, 'fundo.png')).convert()
fundo_rect = fundo.get_rect()

pg.display.set_caption('Jogo Insano Apocalíptico')
clock = pg.time.Clock()

fonte = pg.font.match_font('space age')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(fonte, size)
    text_surface = font.render(text, True, BRANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def n_meteor():
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)

def meteor_exp_new(size):
    expl = Explosion(hit.rect.center, size)
    all_sprites.add(expl)
    hit.kill()
    n_meteor()

def kill_all():
    for mob in mobs:
        death_explosion = Explosion(mob.rect.center, 'player')
        all_sprites.add(death_explosion)
        mob.kill()
    for meteor in meteors:
        expl = Explosion(meteor.rect.center, 'G')
        all_sprites.add(expl)
        meteor.kill()

def n_mob():
    m = Mob1()
    all_sprites.add(m)
    mobs.add(m)

def n_mob2():
    m = Mob2()
    all_sprites.add(m)
    mobs.add(m)

def n_mob3():
    m = Mob3()
    all_sprites.add(m)
    mobs.add(m)

def n_boss1():
    global b, banana
    banana = True
    if ship.power_st >= 2:
        ship.velocidade = VELOCIDADE
        starpw_snd.stop()
        ship.power_st -= 1    
        tema_snd.play()
    tema_snd.stop()
    boss_snd.play()
    for mob in mobs:
        death_explosion = Explosion(mob.rect.center, 'player')
        all_sprites.add(death_explosion)
        mob.kill()
    for meteor in meteors:
        expl = Explosion(meteor.rect.center, 'G')
        all_sprites.add(expl)
        meteor.kill()
    b = Boss1()
    all_sprites.add(b)
    bosses.add(b)
    ship.velocidade = -ship.velocidade
    ship.shoot_delay = 500

def n_boss2_n_boss3():
    b2 = Boss2()
    b3 = Boss3()
    all_sprites.add(b2)
    bosses.add(b2)
    all_sprites.add(b3)
    bosses.add(b3)

def draw_hitpoints_bar(surf, x, y, porcentagem):
    if porcentagem < 0:
        porcentagem = 0

    bar_lengh = HITPOINTS
    bar_height = 30
    fill = porcentagem
    rect_fora = pg.Rect(x, y, bar_lengh, bar_height)
    rect_dentro = pg.Rect(x, y, fill, bar_height)
    if porcentagem > bar_lengh/2 and porcentagem <= bar_lengh:
        pg.draw.rect(surf, VERDE, rect_dentro)
    elif porcentagem > bar_lengh / 5 and porcentagem <= bar_lengh/2:
        pg.draw.rect(surf, AMARELO, rect_dentro)
    elif porcentagem > 0 and porcentagem <= bar_lengh/5:
        pg.draw.rect(surf, VERMELHO, rect_dentro)
    pg.draw.rect(surf, BRANCO, rect_fora, 2)

def draw_hitpoints_bar_boss(surf, x, y, porcentagem):
    if porcentagem < 0:
        porcentagem = 0

    bar_lengh = WIDTH - 200
    bar_height = 20
    fill = (porcentagem / BOSS_HEALTH) * bar_lengh
    rect_fora = pg.Rect(x, y, bar_lengh, bar_height)
    rect_dentro = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, VERMELHO, rect_dentro)
    pg.draw.rect(surf, BRANCO, rect_fora, 2)


def draw_image(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_bg_screen():
    win_snd.stop()
    screen.blit(fundo, fundo_rect)
    menu_snd.play(-1)
    draw_text(screen, 'JOGO INSANO APOCALÍPTICO', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Setas para se movimentar, espaço para atirar', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Pressione espaço para começar', 18, WIDTH / 2, HEIGHT * 3/4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            keystate = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()                
            elif event.type == pg.KEYDOWN:
                if keystate[pg.K_SPACE]:
                    waiting = False

def show_choose_ship_screen():
    global nave, HITPOINTS, VELOCIDADE, DAMAGE
    screen.blit(fundo, fundo_rect)
    draw_text(screen, 'ESCOLHA SUA', 100, WIDTH / 2, HEIGHT * 1 / 6)
    draw_text(screen, 'NAVE', 100, WIDTH / 2, HEIGHT * 2 / 6)
    draw_image(screen, WIDTH / 2-260, HEIGHT / 2, big_ship1_img)
    draw_image(screen, WIDTH / 2-60, HEIGHT / 2, big_ship2_img)
    draw_image(screen, WIDTH / 2+150, HEIGHT / 2, big_ship3_img)
    draw_text(screen, '1', 50 , WIDTH / 2 - 200, HEIGHT * 3/4 - 50)
    draw_text(screen, '+ Ataque', 20 , WIDTH / 2 - 200, HEIGHT * 3/4 )
    draw_text(screen, '2', 50 , WIDTH / 2 , HEIGHT * 3/4 - 50)
    draw_text(screen, '+ Vida', 20 , WIDTH / 2, HEIGHT * 3/4 )
    draw_text(screen, '3', 50 , WIDTH / 2 + 210, HEIGHT * 3/4 - 50)
    draw_text(screen, '+ Velocidade', 20 , WIDTH / 2 + 210, HEIGHT * 3/4 )
    draw_image(screen, 10, HEIGHT - 40, powerup_imgs_c['shield'])
    draw_text(screen, ': GANHA VIDA', 30, 170, HEIGHT - 40)
    draw_image(screen, 10, HEIGHT - 80, powerup_imgs_c['star'])
    draw_text(screen, ': INVENCIBILIDADE', 30, 213, HEIGHT - 80)
    draw_image(screen, 10, HEIGHT - 120, powerup_imgs_c['gun'])
    draw_text(screen, ': TIRO DUPLO', 30, 174, HEIGHT - 120)
    draw_text(screen, 'P.U. COMUNS', 30, 135, HEIGHT - 160)
    draw_text(screen, 'P.U. RAROS', 30, WIDTH / 2 + 420, HEIGHT - 160)
    draw_image(screen, 900, HEIGHT - 80, powerup_imgs_r['things'])
    draw_text(screen, ': TIRO TRIPLO', 30, 1070, HEIGHT - 80)
    draw_image(screen, 900, HEIGHT - 120, powerup_imgs_r['pill'])
    draw_text(screen, ': VIDA EXTRA', 30, 1062, HEIGHT - 120)

    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            keystate = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()  
                sys.exit()              
            if event.type == pg.KEYDOWN:
                if keystate[pg.K_1]:
                    HITPOINTS = 200
                    VELOCIDADE = 7
                    DAMAGE = 30
                    nave = 'nave_v.png'
                    waiting = False
                               
                if keystate[pg.K_2]:
                    HITPOINTS = 300
                    VELOCIDADE = 5
                    DAMAGE = 20
                    nave = 'nave_v2.png'
                    waiting = False

                if keystate[pg.K_3]:
                    HITPOINTS = 125
                    VELOCIDADE = 10
                    DAMAGE = 25
                    nave = 'nave_v3.PNG'
                    waiting = False

    ship = Ship(HITPOINTS, VELOCIDADE, DAMAGE, nave)
    return ship        

def show_go_screen():
    tema_snd.stop()
    death_snd.play()
    draw_text(screen, 'GAME OVER', 150, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Pressione R para jogar novamente', 25, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    waiting = True
    waiting2 = False
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            keystate = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()  
                sys.exit()              
            elif event.type == pg.KEYDOWN:
                if keystate[pg.K_r]:
                    waiting = False
                    death_snd.stop()

def show_win_screen():
    boss_snd.stop()
    win_snd.play()
    draw_text(screen, 'CONGRATULATIONS', 95, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Pressione R para jogar novamente', 25, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            keystate = pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()  
                sys.exit()              
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    death_snd.stop()
                    waiting = False

class Ship(pg.sprite.Sprite):
    def __init__(self, HITPOINTS, VELOCIDADE, DAMAGE, nave):
        pg.sprite.Sprite.__init__(self)
        if nave == 'nave_v.png':
            self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, nave)).convert(), (90,80))
            self.image.set_colorkey(PRETO)
        elif nave == 'nave_v2.png':
            self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, nave)).convert(), (100,90))
            self.image.set_colorkey(BRANCO)
        else:
            self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, nave)).convert(), (60,50))
            self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hitpoints = HITPOINTS
        self.shoot_delay = 350
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power_g = 1
        self.power_time = pg.time.get_ticks()
        self.power_st = 1
        self.power_g2 = 1
        self.velocidade = VELOCIDADE


    def update(self):
        if self.power_g >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power_g -= 1
            self.power_time = pg.time.get_ticks()

        if self.power_st >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.velocidade = VELOCIDADE
            starpw_snd.stop()
            self.power_st -= 1
            self.power_time = pg.time.get_ticks()    
            tema_snd.play()

        if self.power_g2 >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power_g2 -= 1
            self.power_time = pg.time.get_ticks()

        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False

        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RIGHT]:
            self.speedx = self.velocidade
        if keystate[pg.K_DOWN]:
            self.speedy = self.velocidade
        if keystate[pg.K_UP]:
            self.speedy = -self.velocidade
        if keystate[pg.K_LEFT]:
            self.speedx = -self.velocidade
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT * 2)

    def powerup_gun(self):
        powerup_snd.play()
        if self.power_g2 == 1:
            self.power_g = 2
            self.power_time = pg.time.get_ticks()

    def powerup_star(self):
        self.velocidade = VELOCIDADE * 2 - 4 
        starpw_snd.stop()
        tema_snd.stop()
        starpw_snd.play()
        self.power_st = 2
        self.power_time = pg.time.get_ticks()
        
    def powerup_gun2(self):
        powerup_snd.play()
        if self.power_g ==1:
            self.power_g2 = 2
            self.power_time = pg.time.get_ticks()
        if self.power_g >= 2:
            self.power_g -= 1
            self.power_g2 = 2
            self.power_time = pg.time.get_ticks()
        
    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power_g == 1 and self.power_g2 == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                laser_snd.play()

            if self.power_g >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser_snd.play()

            if self.power_g2 >= 2:
                bullet = Bullet_1(self.rect.centerx, self.rect.top)
                bullet1 = Bullet_2(self.rect.right, self.rect.centery)
                bullet2 = Bullet_3(self.rect.left, self.rect.centery)
                all_sprites.add(bullet)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser_snd.play()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_ship1
        #self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'laserBlue.png')).convert(), (2000 ,1))
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet_1(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_ship1_1
        #self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'laserBlue.png')).convert(), (2000 ,1))
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet_2(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_ship1_1
        #self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'laserBlue.png')).convert(), (2000 ,1))
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 3

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class Bullet_3(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_ship1_1
        #self.image = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'laserBlue.png')).convert(), (2000 ,1))
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = -3

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class PowerUp(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'star'])
        self.image = powerup_imgs_c[self.type]
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp_R(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['things', 'pill'])
        self.image = powerup_imgs_r[self.type]
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Mob1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = mob1_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -200)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,3)
        self.shoot_delay = random.randrange(600,1000)
        self.last_shot = pg.time.get_ticks()
        self.last_show = pg.time.get_ticks()
        self.hitpoints = 90

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pg.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.shoot()

        if self.speedx == 0:
            self.speedx = 3
        if self.rect.right > WIDTH:
            self.speedx = random.randrange(-4,-2)
        if self.rect.left < 0:
            self.speedx = random.randrange(2,4)
        if self.rect.bottom > HEIGHT/2:
            self.speedy = random.randrange(-4,-2)
            self.speedx = random.randrange(-4,4)
        if self.rect.top < 0:
            self.speedy = random.randrange(2,4)
            self.speedx = random.randrange(-4,4)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:  
            self.last_shot = now
            bullet = BulletMob1(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            bulletsmobs.add(bullet)

    def draw_health(self):
        if self.hitpoints > 50:
            color = VERDE
        if self.hitpoints > 20:
            color = AMARELO
        else:
            color = VERMELHO

        width = int(self.rect.width * self.hitpoints / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.hitpoints <= 100:
            pg.draw.rect(self.image, color, self.health_bar)

class BulletMob1(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob1
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

class Mob2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = mob2_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -200)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,3)
        self.shoot_delay = random.randrange(600,1000)
        self.last_shot = pg.time.get_ticks()
        self.hitpoints = 90
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pg.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.shoot()

        if self.speedx == 0:
            self.speedx = 3
        if self.rect.right > WIDTH:
            self.speedx = random.randrange(-4,-2)
        if self.rect.left < 0:
            self.speedx = random.randrange(2,4)
        if self.rect.bottom > HEIGHT/2:
            self.speedy = random.randrange(-4,-2)
            self.speedx = random.randrange(-4,4)
        if self.rect.top < 0:
            self.speedy = random.randrange(2,4)
            self.speedx = random.randrange(-4,4)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay: 
            self.last_shot = now 
            bullet1 = BulletMob2(self.rect.left, self.rect.centery)
            bullet2 = BulletMob2(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bulletsmobs.add(bullet1)
            bulletsmobs.add(bullet2)

class BulletMob2(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob2
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

class Mob3(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = mob3_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -200)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,3)
        self.shoot_delay = 1500
        self.last_shot = pg.time.get_ticks()
        self.last_show = pg.time.get_ticks()
        self.hitpoints = 90

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pg.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.shoot()

        if self.speedx == 0:
            self.speedx = 3
        if self.rect.right > WIDTH:
            self.speedx = random.randrange(-4,-2)
        if self.rect.left < 0:
            self.speedx = random.randrange(2,4)
        if self.rect.bottom > HEIGHT/2:
            self.speedy = random.randrange(-4,-2)
            self.speedx = random.randrange(-4,4)
        if self.rect.top < 0:
            self.speedy = random.randrange(2,4)
            self.speedx = random.randrange(-4,4)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:  
            self.last_shot = now
            bullet = BulletMob3_1(self.rect.centerx, self.rect.bottom)
            bullet1 = BulletMob3_2(self.rect.right, self.rect.centery)
            bullet2 = BulletMob3_3(self.rect.left, self.rect.centery)
            all_sprites.add(bullet)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bulletsmobs.add(bullet)
            bulletsmobs.add(bullet1)
            bulletsmobs.add(bullet2)


    def draw_health(self):
        if self.hitpoints > 50:
            color = VERDE
        if self.hitpoints > 20:
            color = AMARELO
        else:
            color = VERMELHO

        width = int(self.rect.width * self.hitpoints / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.hitpoints <= 100:
            pg.draw.rect(self.image, color, self.health_bar)

class BulletMob3_1(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob3
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

class BulletMob3_2(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob3
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = 3

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class BulletMob3_3(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob3
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = -3

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class Boss1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = boss1_img
        self.image.set_colorkey(PRETO)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = - 500
        self.speedy = 1
        self.hitpoints = BOSS_HEALTH
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.last_explosion = pg.time.get_ticks()


    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay: 
            self.last_shot = now
            self.shoot()
        self.rect.y += self.speedy
        if self.rect.bottom == 200:
            self.speedy = 0

    def shoot(self):
        if self.hitpoints > 0:
            bullet = BulletBoss1(random.randrange(self.rect.left,self.rect.right), random.randrange(self.rect.top, self.rect.bottom))
            all_sprites.add(bullet)
            bulletsbosses.add(bullet)

class BulletBoss1(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob1
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(3,10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class BulletBoss1_killer(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_mob1
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = random.randrange(-4,4)
        self.speedy = random.randrange(-10,-3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT + 50:
            self.kill()

        if self.rect.left < -50:
            self.kill()

        if self.rect.right > WIDTH + 50:
            self.kill()

class Boss2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_str = boss2_img
        self.image_str.set_colorkey(PRETO)
        self.image = self.image_str.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = 300
        self.rect.y = - 500
        self.speedy = 1
        self.hitpoints = 3000
        self.shoot_delay = 300
        self.last_shot = pg.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = 5
        self.last_update = pg.time.get_ticks()       

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.bottom >= 400:
            self.speedy = 0

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.image_str, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Boss3(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_str = boss3_img
        self.image_str.set_colorkey(PRETO)
        self.image = self.image_str.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 300
        self.rect.y = - 500
        self.speedy = 1
        self.hitpoints = 3000
        self.shoot_delay = 300
        self.last_shot = pg.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = -5
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.bottom >= 400:
            self.speedy = 0

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.image_str, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Meteor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_str = random.choice(lista_meteor)
        self.image_str.set_colorkey(PRETO)
        self.image = self.image_str.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -300
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8,8)
        self.last_update = pg.time.get_ticks()
        self.hitpoints = 30

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.image_str, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 100 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, - 40)
            self.speedy = random.randrange(1,8)

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosions[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosions[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load nas imagens
mob1_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'enemyRed1.png')).convert(), (100,90))
mob2_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'enemyGreen3.png')).convert(), (100,90))
mob3_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'enemyBlue4.png')).convert(), (100,90))
bullet_mob1 = pg.image.load(os.path.join(mob_folder, 'laserRed08.png')).convert()
bullet_mob2 = pg.image.load(os.path.join(mob_folder, 'laserRed07.png')).convert()
bullet_mob3 = pg.image.load(os.path.join(mob_folder, 'laserRed10.png')).convert()
big_ship1_img = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'nave_v.png')).convert(), (120,110))
big_ship1_img.set_colorkey(PRETO)
big_ship2_img = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'nave_v2.png')).convert(), (120,110))
big_ship2_img.set_colorkey(BRANCO)
big_ship3_img = pg.transform.scale(pg.image.load(os.path.join(player_folder, 'nave_v3.png')).convert(), (120,110))
big_ship3_img.set_colorkey(PRETO)
if nave == 'nave_v.png':
    bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserBlue01.png')).convert()
    bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserBlue10.png')).convert()
elif nave == 'nave_v2.png':
    bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserGreen01.png')).convert()
    bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserGreen10.png')).convert()
else:
    bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserBlue01.png')).convert()
    bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserBlue10.png')).convert()


boss1_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'boss1.png')).convert(), (921, 500))
boss2_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'boss2.png')).convert(), (550, 550))
boss3_img = pg.transform.scale(pg.image.load(os.path.join(mob_folder, 'boss3.png')).convert(), (550, 550))
lista_meteor = []
lista_meteoros = ['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png', 'meteorGrey_big4.png',
                   'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png', 'meteorGrey_small2.png',
                   'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png']

for meteoro in lista_meteoros:
    lista_meteor.append(pg.image.load(os.path.join(meteor_folder, meteoro)).convert())

explosions = {}
explosions['G'] = []
explosions['P'] = []
explosions['U'] = []
explosions['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(os.path.join(explosion_folder, filename)).convert()
    img.set_colorkey(PRETO)
    img_G = pg.transform.scale(img, (75,75))
    explosions['G'].append(img_G)
    img_P = pg.transform.scale(img, (32,32))
    explosions['P'].append(img_P)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pg.image.load(os.path.join(explosion_folder, filename)).convert()
    img.set_colorkey(PRETO)
    explosions['player'].append(img)
    img_U = pg.transform.scale(img, (900,500))
    explosions['U'].append(img_U)

powerup_imgs_c = {}
powerup_imgs_r = {}
powerup_imgs_c['shield'] = pg.image.load(os.path.join(powerup_folder, 'shield_gold.png')).convert()
powerup_imgs_c['gun'] = pg.image.load(os.path.join(powerup_folder, 'bolt_gold.png')).convert()
powerup_imgs_c['star'] = pg.image.load(os.path.join(powerup_folder, 'star_gold.png')).convert()
powerup_imgs_r['things'] = pg.image.load(os.path.join(powerup_folder, 'things_gold.png')).convert()
powerup_imgs_r['pill'] = pg.image.load(os.path.join(powerup_folder, 'pill_yellow.png')).convert()

# Load nos sons
menu_snd = pg.mixer.Sound(os.path.join(sound_folder, 'temaJogo1.ogg'))
tema_snd = pg.mixer.Sound(os.path.join(sound_folder, 'temaJogo2.ogg'))
boss_snd = pg.mixer.Sound(os.path.join(sound_folder, 'boss1.ogg'))
expl_death_snd = pg.mixer.Sound(os.path.join(sound_folder, 'expl_death.ogg'))
laser_snd = pg.mixer.Sound(os.path.join(sound_folder, 'laser_snd.ogg'))
laser2_snd = pg.mixer.Sound(os.path.join(sound_folder, 'laser2_snd.ogg'))
powerup_snd = pg.mixer.Sound(os.path.join(sound_folder, 'powerup.ogg'))
starpw_snd = pg.mixer.Sound(os.path.join(sound_folder, 'starpw.ogg'))
death_snd = pg.mixer.Sound(os.path.join(sound_folder, 'death.ogg'))
win_snd = pg.mixer.Sound(os.path.join(sound_folder, 'win.ogg'))


# Loop
Game_over = True
Rodando = True
waiting2 = True
banana = False
abobora = False
while Rodando:
    if Game_over:
        banana = False
        abobora = False
        show_bg_screen()
        ship = show_choose_ship_screen()
        menu_snd.stop()
        tema_snd.play()
        mini_ship1_img = pg.transform.scale(pg.image.load(os.path.join(player_folder, nave)).convert(), (50, 45))
        if nave == 'nave_v2.png':
            mini_ship1_img.set_colorkey(BRANCO)
        else:
            mini_ship1_img.set_colorkey(PRETO)
        if nave == 'nave_v.png':
            bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserPink01.png')).convert()
            bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserPink10.png')).convert()
        elif nave == 'nave_v2.png':
            bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserGreen01.png')).convert()
            bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserGreen10.png')).convert()
        else:
            bullet_ship1 = pg.image.load(os.path.join(player_folder, 'laserBlue01.png')).convert()
            bullet_ship1_1 = pg.image.load(os.path.join(player_folder, 'laserBlue10.png')).convert()
        Game_over = False
        waiting2 = False
        screen.blit(fundo, fundo_rect)
        all_sprites = pg.sprite.Group()
        ships = pg.sprite.Group()
        mobs = pg.sprite.Group()
        bosses = pg.sprite.Group()
        bulletsbosses = pg.sprite.Group()
        bulbosskill = pg.sprite.Group()
        bullets = pg.sprite.Group()
        powerups = pg.sprite.Group()
        meteors = pg.sprite.Group()
        bulletsmobs = pg.sprite.Group()
        all_sprites.add(ship)
        ships.add(ship)
        boss = Boss1()
        
        for e in range(6):
            n_meteor()
            
        for e in range(2):
            n_mob()

        score = 0
        
    # Mantem o loop rodando na velocidade certa
    clock.tick(FPS)
    
    # Processo (eventos)
    for event in pg.event.get():
        keystate = pg.key.get_pressed()
        if event.type == pg.QUIT:
            Rodando = False
        if event.type == pg.KEYDOWN:
            if keystate[pg.K_m]:
                n_boss2_n_boss3()
            if keystate[pg.K_z]:
                ship.powerup_gun()
            if keystate[pg.K_x]:
                ship.powerup_gun2()
            if keystate[pg.K_c]:
                ship.powerup_star()
            if keystate[pg.K_b]:
                n_boss1()
            if keystate[pg.K_k]:
                kill_all()

    # Update
    all_sprites.update()
    mobs.update()

    # Colisão meteoros com tiros
    hits = pg.sprite.groupcollide(meteors, bullets, False, True)
    for hit in hits:
        if score < 7500:
            if hit.radius > 40:
                hit.hitpoints -= 10
                expl = Explosion(hit.rect.center, 'P')
                all_sprites.add(expl)
                if hit.hitpoints <= 0:
                    score += 55 - hit.radius
                    meteor_exp_new('G')                              
            if hit.radius < 40 and hit.hitpoints > 20:
                hit.hitpoints -= 15
                expl = Explosion(hit.rect.center, 'P')
                all_sprites.add(expl)
                if hit.hitpoints <= 0:
                    score += 55 - hit.radius        
                    meteor_exp_new('G')
            if hit.radius == 37:
                hit.hitpoints -= 15
                expl = Explosion(hit.rect.center, 'P')
                all_sprites.add(expl)
                if hit.hitpoints <= 0:
                    score += 55 - hit.radius
                    meteor_exp_new('P')
            if hit.radius < 20:
                hit.hitpoints -= 30
                if hit.hitpoints <= 0:
                    score += 55 - hit.radius
                    meteor_exp_new('P')
            x = random.random()
            if  x > 0.99:
                pups = PowerUp_R(hit.rect.center)
                all_sprites.add(pups)
                powerups.add(pups)
            elif  x > 0.95:
                pups = PowerUp(hit.rect.center)
                all_sprites.add(pups)
                powerups.add(pups)
        if score > 7500:
            score = 7500
            n_boss1()

    # Colisão mobs com tiros
    hits = pg.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.hitpoints -= DAMAGE        
        expl = Explosion(hit.rect.center, 'P')
        all_sprites.add(expl)
        if hit.hitpoints <= 0:
            score += 300
            if score >= 0 and score <= 2500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob()
            if score > 2500 and score <= 5000:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob2()
            if score > 5000 and score < 7500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob3()
            if score > 7500:
                score = 7500
                n_boss1()
               
    # Colisão nave com PowerUps
    hits = pg.sprite.spritecollide(ship, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            powerup_snd.play()
            ship.hitpoints += random.randrange(40, 60)
            if ship.hitpoints >= HITPOINTS:
                ship.hitpoints = HITPOINTS
        if hit.type == 'gun':
            ship.powerup_gun()
        
        if hit.type == 'star':
            ship.powerup_star()
            
        if hit.type == 'things':
            ship.powerup_gun2()
            
        if hit.type == 'pill':
            if ship.lives < 4:
                powerup_snd.play()
                ship.lives += 1

    # Colisão de tiros dos mobs com a nave
    
    hits = pg.sprite.groupcollide(bulletsmobs, ships, True, False)
    for hit in hits:
        if ship.power_st == 1:
            ship.hitpoints -= 50
            expl = Explosion(hit.rect.center, 'P')
            all_sprites.add(expl)
            if ship.hitpoints <= 0:
                death_explosion = Explosion(ship.rect.center, 'player')
                all_sprites.add(death_explosion)
                expl_death_snd.play()
                ship.hide()
                ship.lives -= 1
                ship.hitpoints = HITPOINTS
        if ship.power_st >= 2:
            expl = Explosion(hit.rect.center, 'P')
            all_sprites.add(expl)
            
    # Colisão de mobs com a nave
    hits = pg.sprite.spritecollide(ship, mobs, True , pg.sprite.collide_circle)
    for hit in hits:
        if ship.power_st == 1:
            ship.hitpoints -= HITPOINTS / 3
            score += 300
            if score >= 0 and score <= 2500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                expl_death_snd.play()
                hit.kill()
                n_mob()
            if score > 2500 and score <= 5000:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob2()
            if score > 5000 and score < 7500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob3()
            if score > 7500:
                score = 7500
                n_boss1()
            if ship.hitpoints <= 0:
                death_explosion = Explosion(ship.rect.center, 'player')
                all_sprites.add(death_explosion)
                expl_death_snd.play()
                ship.hide()
                ship.lives -= 1
                ship.hitpoints = HITPOINTS
        if ship.power_st >= 2:
            score += 300
            if score >= 0 and score <= 2500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                expl_death_snd.play()
                hit.kill()
                n_mob()
            if score > 2500 and score <= 5000:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob2()
            if score > 5000 and score < 7500:
                death_explosion = Explosion(hit.rect.center, 'player')
                all_sprites.add(death_explosion)
                hit.kill()
                expl_death_snd.play()
                n_mob3()
            if score > 7500:
                score = 7500
                n_boss1()
            

    # Colisão de meteoros com a nave
    hits = pg.sprite.spritecollide(ship, meteors, True, pg.sprite.collide_circle)
    for hit in hits:
        if ship.power_st == 1:
            ship.hitpoints -= hit.radius
            expl = Explosion(hit.rect.center, 'P')
            all_sprites.add(expl)
            n_meteor()
            if ship.hitpoints <= 0:
                now = pg.time.get_ticks()
                death_explosion = Explosion(ship.rect.center, 'player')
                all_sprites.add(death_explosion)
                expl_death_snd.play()
                ship.hide()
                ship.lives -= 1
                ship.hitpoints = HITPOINTS
        if ship.power_st >= 2:
            score += 300
            expl = Explosion(hit.rect.center, 'P')
            all_sprites.add(expl)
            n_meteor()

    # Colisão dos tiros com o Boss
    hits = pg.sprite.groupcollide(bullets, bosses, True, False)
    for hit in hits:       
        b.hitpoints -= 5
        expl = Explosion(hit.rect.center, 'P')
        all_sprites.add(expl)

    # Colisão dos tiros do boss com a nave
    hits = pg.sprite.groupcollide(bulletsbosses, ships, True, False)
    for hit in hits:
        ship.hitpoints -= HITPOINTS / 4
        expl = Explosion(hit.rect.center, 'P')
        all_sprites.add(expl)
        if ship.hitpoints <= 0:
            death_explosion = Explosion(ship.rect.center, 'player')
            all_sprites.add(death_explosion)
            expl_death_snd.play()
            ship.hide()
            ship.lives -= 1
            ship.hitpoints = HITPOINTS

    # Colisão dos tiros do boss com tiros da nave
    hits = pg.sprite.groupcollide(bulletsbosses, bullets, False, True)
    for hit in hits:
        bullet = BulletBoss1_killer(hit.rect.centerx, hit.rect.centery)
        bulbosskill.add(bullet)
        all_sprites.add(bullet)
        hit.kill()

    # Colisão dos tiros matatadores de boss com boss
    hits = pg.sprite.groupcollide(bulbosskill, bosses, True, False)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'G')
        all_sprites.add(expl)
        b.hitpoints -= 25
        score += random.randrange(45,55)
        if b.hitpoints <= 0:
            abobora = True
            b.kill()
            morri = Explosion(b.rect.center, 'U')
            all_sprites.add(morri)
            expl_death_snd.play()
            boss_snd.stop()
    if abobora:
        if not morri.alive():
            show_win_screen()
            Game_over = True

    # Mostra a tela de GAMEOVER caso as vidas cheguem a zero
    if ship.lives == 0:# and not death_explosion.alive():
        kill_all()
        ship.kill()
        boss_snd.stop()
        if not death_explosion.alive():
            show_go_screen()
            Game_over = True

    # Desenha
    screen.fill(PRETO)
    screen.blit(fundo, fundo_rect)
    all_sprites.draw(screen)
    mobs.draw(screen)
    draw_text(screen, str(score), 50, WIDTH / 2, 10)
    draw_hitpoints_bar(screen, 5, 5, ship.hitpoints)
    draw_lives(screen, WIDTH - 200, 5, ship.lives, mini_ship1_img)
    if banana:
        draw_hitpoints_bar_boss(screen, 100, 50, b.hitpoints)

    # *Depois* de desenhar tudo, flipa o display
    pg.display.flip()

pg.quit()