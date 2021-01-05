import pygame
import os
import sys


FPS = 100
CONST_SPEED = 4
GRAVITY = 0.5
JUMP_HEIGHT = 13

pygame.init()
size = WIDTH, HEIGHT = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    image = load_image("mario.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
        self.floor = False
        self.flag = False
        self.grounded = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.f = GRAVITY

    def update(self):
        self.speed_y += GRAVITY

        if MOVE_RIGHT:
            self.speed_x = CONST_SPEED * 1
        elif MOVE_LEFT:
            self.speed_x = CONST_SPEED * -1
        elif not MOVE_RIGHT and not MOVE_LEFT:
            self.speed_x = 0

        self.rect = self.rect.move(self.speed_x, 0)
        if pygame.sprite.spritecollide(self, flat, 0):
            self.rect = self.rect.move(self.speed_x * -1, 0)
            self.speed_x = 0
        else:
            self.rect = self.rect.move(self.speed_x * -1, 0)

        self.rect = self.rect.move(0, self.speed_y)
        if pygame.sprite.spritecollide(self, flat, 0) and not self.floor:
            self.rect = self.rect.move(0, -1 * self.speed_y)
            self.speed_y = 0

            self.grounded = True
        else:
            self.grounded = False
            self.rect = self.rect.move(0, -1 * self.speed_y)

        if self.floor:
            self.speed_y += GRAVITY


        self.rect = self.rect.move(0, -1 * self.speed_y)
        if pygame.sprite.spritecollide(self, flat, 0):
            self.rect = self.rect.move(0, self.speed_y)
            self.floor = True
        else:
            self.floor = False
            self.rect = self.rect.move(0, self.speed_y)

        if self.grounded and JUMP and not self.floor:
            self.speed_y = -1 * JUMP_HEIGHT


        self.rect = self.rect.move(self.speed_x, self.speed_y)


class Mountain(pygame.sprite.Sprite):
    image = load_image("flat.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.mask = pygame.mask.from_surface(self.image)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.add(flat)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


flat = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
mountain = Mountain((300, 200))
mountain2 = Mountain((200, 350))
mountain3 = Mountain((0, 500))


running = True
exist = False
flag = False

JUMP = False
MOVE_LEFT = False
MOVE_RIGHT = False

while running:
    clock.tick(FPS)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                MOVE_RIGHT = True
            if event.key == pygame.K_LEFT:
                MOVE_LEFT = True
            if event.key == pygame.K_UP:
                JUMP = True
            if event.key == pygame.K_LCTRL:
                flag = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                flag = False
            if event.key == pygame.K_RIGHT:
                MOVE_RIGHT = False
            if event.key == pygame.K_LEFT:
                MOVE_LEFT = False
            if event.key == pygame.K_UP:
                JUMP = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not exist:
                Player(event.pos)
                exist = True
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()