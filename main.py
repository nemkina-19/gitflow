import pygame
import os
import sys

FPS = 90
CONST_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 13

pygame.init()
size = WIDTH, HEIGHT = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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


tile_images = {
    'wall': load_image('box.png'),
}
# player_image = load_image('mario.png')

tile_width = tile_height = 50


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.speed_x = 0
        self.speed_y = 0
        self.floor = False
        self.flag = False
        self.grounded = False
        self.sheet, self.columns, self.rows = sheet, columns, rows
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.f = GRAVITY
        self.anim = 0
        self.right = False
        self.left = False

    def cut_sheet(self, sheet, columns, rows, x=0, y=1, f=False):
        if not f:
            self.rect = pygame.Rect(0, 0, (sheet.get_width() + 1) // columns,
                                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(x, y):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.speed_y += GRAVITY

        if MOVE_RIGHT:
            self.speed_x = CONST_SPEED * 1
            self.right = True
            self.left = False
        elif MOVE_LEFT:
            self.speed_x = CONST_SPEED * -1
            self.left = True
            self.right = False
        elif not MOVE_RIGHT and not MOVE_LEFT:
            self.speed_x = 0

        self.rect = self.rect.move(self.speed_x, 0)
        if pygame.sprite.spritecollide(self, flat, 0):
            self.rect = self.rect.move(self.speed_x * -1, 0)
            self.speed_x = 0
        else:
            self.rect = self.rect.move(self.speed_x * -1, 0)

        for p in flat:
            if pygame.sprite.collide_rect(self, p):

                if self.speed_y > 0:
                    self.rect.bottom = p.rect.top
                    self.grounded = True
                    self.speed_y = 0

                if self.speed_y < 0:
                    self.rect.top = p.rect.bottom
                    self.speed_y = 0

        self.rect = self.rect.move(0, self.speed_y)
        if pygame.sprite.spritecollide(self, flat, 0) and not self.floor:
            self.rect = self.rect.move(0, -1 * self.speed_y)
            self.speed_y = 0
            self.grounded = True
        else:
            self.grounded = False
            self.rect = self.rect.move(0, -1 * self.speed_y)

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

        self.anim += 1
        if abs(self.speed_y) > 1 and not self.grounded:
            if len(self.frames) < 2:
                self.frames = []
            self.cut_sheet(self.sheet, self.columns, self.rows, 6, 7, True)
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.flip(self.image, 0, 0)
            if self.left:
                self.image = pygame.transform.flip(self.image, 1, 0)
            if self.right:
                self.image = pygame.transform.flip(self.image, 0, 0)

        if self.anim % 10 == 0:
            if abs(self.speed_y) > 0.5 and not self.grounded:
                pass
            else:
                if self.speed_x == 0:
                    if len(self.frames) > 1:
                        self.frames = []
                    self.cut_sheet(self.sheet, self.columns, self.rows, 0, 1, True)
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                    if self.left:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                    if self.right:
                        self.image = pygame.transform.flip(self.image, 0, 0)
                if self.speed_x < 0:
                    if len(self.frames) == 1:
                        self.frames = []
                    self.cut_sheet(self.sheet, self.columns, self.rows, 2, 4, True)
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                    self.image = pygame.transform.flip(self.image, 1, 0)
                if self.speed_x > 0:
                    if len(self.frames) == 1:
                        self.frames = []
                    self.cut_sheet(self.sheet, self.columns, self.rows, 2, 4, True)
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                    self.image = self.frames[self.cur_frame]
                    self.image = pygame.transform.flip(self.image, 0, 0)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.add(flat)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

        # сдвинуть объект obj на смещение камеры

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

        # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(load_image("mario.png"), 20, 1, (tile_width * x, tile_width * y))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


flat = pygame.sprite.Group()

tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player = None

start_screen()

running = True
exist = False
flag = False

JUMP = False
MOVE_LEFT = False
MOVE_RIGHT = False
camera = Camera()
player, level_x, level_y = generate_level(load_level('map.txt'))

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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #  if event.button == 1 and not exist:
        # Player((100, 80))
        # exist = True
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()