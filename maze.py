from pygame import *
'''
'''
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    
    def update(self, kgp):
        x_shift = self.rect.x - self.speed * (kgp[K_a] - kgp[K_d])
        y_shift = self.rect.y - self.speed * (kgp[K_w] - kgp[K_s])
        self.rect.x = min(max(5, x_shift), 630)
        self.rect.y = min(max(5, y_shift), 430)


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self, _):
        if self.rect.x < 450 or self.rect.x > 600:
            self.speed *= -1
        self.rect.x += self.speed


win_width = 700
win_height = 500


window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
 

player = Player("hero.png", 100, 100, 5)
cyborg = Enemy("cyborg.png", 550, 250, 2)
final = GameSprite("treasure.png", 550, 400, 0)
updatables = [player, cyborg]
resetables = [player, cyborg, final]



 
game = True
clock = time.Clock()
FPS = 60
#музика
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    
    window.blit(background,(0, 0))

    keys_get_pressed = key.get_pressed()

    for updatable in updatables:
        updatable.update(keys_get_pressed)
    for resetable in resetables:
        resetable.reset()
    # player.update()
    # player.reset()
    # cyborg.reset()
    # final.reset()
    
    display.update()
    clock.tick(FPS)