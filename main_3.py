import pygame
import os
import sys

FPS = 200
CONST_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 13
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
RED = (255, 0, 0)
YELLOW = (239, 228, 176)

size = WIDTH, HEIGHT = width, height = 800, 600
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Press any button to continuie"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, RED, YELLOW)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        pygame.mixer.music.load('music/start.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
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


tile_width = tile_height = 50

tile_images = {
    'ground': pygame.transform.scale(load_image('grassCenter.png'), (tile_width, tile_height)),
    'bridge': pygame.transform.scale(load_image('boxAlt.png'), (tile_width, tile_height)),
    'grass': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),
    'ground_stay': pygame.transform.scale(load_image('grassCenter.png'), (tile_width, tile_height))
}


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
        self.jump = False

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
        if not self.grounded:
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
        if self.grounded and JUMP:
            self.speed_y = -1 * JUMP_HEIGHT

        # коллизия
        self.grounded = False
        self.rect = self.rect.move(self.speed_x, 0)
        self.isCollide(self.speed_x, 0, flat)
        self.rect = self.rect.move(0, self.speed_y)
        self.isCollide(0, self.speed_y, flat)

        # счётчик анимаций
        self.anim += 1
        if self.anim % 1000 == 0:
            self.anim //= 1000

        # различные анимации в зависимости от действий
        if self.speed_y < -1:
            self.animate('jump')
        elif self.speed_y > 1:
            self.animate('down')
        elif self.speed_x == 0:
            self.animate('0x')
        elif self.speed_x < 0:
            self.animate('-1x')
        elif self.speed_x > 0:
            self.animate('1x')

        # воспроизводим анимации
        if self.anim % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.left:
                self.image = pygame.transform.flip(self.image, 1, 0)
            elif self.right:
                self.image = pygame.transform.flip(self.image, 0, 0)

    def animate(self, animation):
        self.frames = []
        if animation == '0x':
            self.cut_sheet(self.sheet, self.columns, self.rows, 0, 1, True)
        elif animation == 'down':
            self.cut_sheet(self.sheet, self.columns, self.rows, 15, 18, True)
        elif animation == '-1x':
            self.cut_sheet(self.sheet, self.columns, self.rows, 2, 4, True)
        elif animation == '1x':
            self.cut_sheet(self.sheet, self.columns, self.rows, 2, 4, True)
        elif animation == 'jump':
            self.cut_sheet(self.sheet, self.columns, self.rows, 6, 7, True)

    def isCollide(self, sx, sy, p):
        for f in p:
            if pygame.sprite.collide_rect(self, f):
                if sy > 0:
                    self.rect.bottom = f.rect.top
                    self.grounded = True
                    self.speed_y = 0
                if sy < 0:
                    self.rect.top = f.rect.bottom
                    self.speed_y = 0
                if sx > 0:
                    self.rect.right = f.rect.left
                if sx < 0:
                    self.rect.left = f.rect.right


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'bridge' or tile_type == 'grass' or tile_type == 'ground_stay':
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
            if level[y][x] == '.':
                Tile('ground', x, y)
            elif level[y][x] == '-':
                Tile('ground_stay', x, y)
            elif level[y][x] == 'b':
                Tile('bridge', x, y)
            elif level[y][x] == '*':
                Tile('grass', x, y)
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
player, level_x, level_y = generate_level(load_level('map_1.txt'))

# Music
volue = 0.5
pygame.mixer.music.load('music/joy.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volue)
jump = pygame.mixer.Sound('music/jump_3.ogg')
jump.set_volume(volue - 0.2)


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
                jump.play(loops=0)
            if event.key == pygame.K_LCTRL:
                flag = True
            if event.key == pygame.K_F3:
                if volue > 0.3:
                    volue -= 0.1
                    pygame.mixer.music.set_volume(volue)
                    jump.set_volume(volue - 0.1)
                    print(volue)
            if event.key == pygame.K_F4:
                if volue <= 1.0:
                    volue += 0.1
                    pygame.mixer.music.set_volume(volue)
                    jump.set_volume(volue - 0.1)
                    print(volue)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                flag = False
            if event.key == pygame.K_RIGHT:
                MOVE_RIGHT = False
            if event.key == pygame.K_LEFT:
                MOVE_LEFT = False
            if event.key == pygame.K_UP:
                JUMP = False

    # изменяем ракурс камеры
    camera.update(player)

    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color(26, 21, 63))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
