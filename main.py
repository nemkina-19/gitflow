import pygame
import os
import sys
import ctypes


FPS = 50
CONST_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 13
COINS = 0

LAST = 0
START = 0

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

RED = (255, 0, 0)
YELLOW = (239, 228, 176)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


def size_screen():
    user32 = ctypes.windll.user32
    screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    size = screenSize
    return size


size_full = size_screen()
WIDTH, HEIGHT = size_full
screen = pygame.display.set_mode((size_full), pygame.FULLSCREEN)
width, height = WIDTH, HEIGHT
clock = pygame.time.Clock()
print(WIDTH, HEIGHT)


def terminate():
    pygame.quit()
    sys.exit()


def draw(screen, x, y, btn_size_x, btn_size_y, text='', color=None, options=False):
    font = pygame.font.SysFont('arial', 25)
    text1 = font.render(text, 1, BLACK)
    if text == '':
        pygame.draw.rect(screen, (0, 0, 0), (x, y, btn_size_x, btn_size_y))
    if options:
        pygame.draw.rect(screen, color, (x, y, btn_size_x, btn_size_y))
        screen.blit(text1, (x + 10, y + btn_size_y // 4))


def finish_screen():
    fon = pygame.transform.scale(load_image('img.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    end.play(loops=0)

    intro_text = [f"Вы собрали {COINS} из 20 монет!"]
    font = pygame.font.SysFont('arial', 45)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, BLUE)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 410
        intro_rect.y = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    btn_1x = 0.55 * WIDTH
    btn_1y = HEIGHT * 0.6
    btn_size_x = WIDTH * 0.125
    btn_size_y = HEIGHT * 0.1
    btn_2x = 0.3 * WIDTH
    btn_2y = HEIGHT * 0.6

    draw(screen, btn_1x, btn_1y,
         btn_size_x, btn_size_y, '', BLUE)
    draw(screen, btn_2x, btn_2y,
         btn_size_x, btn_size_y, '', RED)
    draw(screen, btn_1x + 10, btn_1y + 10, btn_size_x - 20,
         btn_size_y - 20, ' PLAY AGAIN    ', GREEN, True)
    draw(screen, btn_2x + 10, btn_2y + 10, btn_size_x - 20,
         btn_size_y - 20, '       QUIT      ', RED, True)

    pygame.mixer.music.stop()

    global MOVE_LEFT, MOVE_RIGHT, JUMP
    MOVE_RIGHT = 0
    MOVE_LEFT = 0
    JUMP = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                end.stop()
                pygame.mixer.music.load('music/joy.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(volue)
                if btn_1x <= event.pos[0] <= btn_1x + btn_size_x and btn_1y <= event.pos[1] <= btn_1y + btn_size_y:
                    # pygame.mixer.music.stop()
                    return  # начинаем игру
                elif btn_2x <= event.pos[0] <= btn_2x + btn_size_x and btn_2y <= event.pos[1] <= btn_2y + btn_size_y:
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    text_coord = 50

    # Buttons
    btn_1x = 0.75 * WIDTH
    btn_1y = HEIGHT * 0.2
    btn_size_x = WIDTH * 0.125
    btn_size_y = HEIGHT * 0.1
    btn_2x = 0.125 * WIDTH
    btn_2y = HEIGHT * 0.2

    for line in intro_text:
        string_rendered = font.render(line, 1, RED, YELLOW)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    draw(screen, btn_1x, btn_1y,
         btn_size_x, btn_size_y, '', BLUE)
    draw(screen, btn_2x, btn_2y,
         btn_size_x, btn_size_y, '', RED)
    draw(screen, btn_1x + 10, btn_1y + 10, btn_size_x - 20,
         btn_size_y - 20, '       PLAY      ', BLUE, True)
    draw(screen, btn_2x + 10, btn_2y + 10, btn_size_x - 20,
         btn_size_y - 20, '       QUIT      ', RED, True)
    pygame.mixer.music.load('music/start.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1x <= event.pos[0] <= btn_1x + btn_size_x and btn_1y <= event.pos[1] <= btn_1y + btn_size_y:
                    pygame.mixer.music.stop()
                    return  # начинаем игру
                elif btn_2x <= event.pos[0] <= btn_2x + btn_size_x and btn_2y <= event.pos[1] <= btn_2y + btn_size_y:
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)


def death_screen():
    fon = pygame.transform.scale(load_image('game_over_2.png'), (WIDTH, HEIGHT // 2))
    restart = load_image('restart.png')
    screen.blit(fon, (0, 0))
    screen.blit(restart, (width // 3, height // 2))
    pygame.display.flip()
    pygame.mixer.music.pause()
    lose.play(loops=0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if width // 3 <= event.pos[0] <= width // 3 + restart.get_width() and height // 2 <= event.pos[1] <= height // 2 + restart.get_height():
                    lose.stop()
                    pygame.mixer.music.load('music/joy.ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(volue)
                    return

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
    'ground_stay': pygame.transform.scale(load_image('grassCenter.png'), (tile_width, tile_height)),
    'coin': pygame.transform.scale(load_image('coin.png'), (tile_width, tile_height)),
    'spikes': pygame.transform.scale(load_image('spikes.png'), (tile_width, tile_height)),
    'checkpoint': pygame.transform.scale(load_image('checkpoint.png'), (tile_width, tile_height)),
    'exit': pygame.transform.scale(load_image('exit.png'), (tile_width, tile_height)),
    'right': pygame.transform.scale(load_image('signRight.png'), (tile_width, tile_height)),
    'ghost': pygame.transform.scale(load_image('sand_lol.png'), (tile_width, tile_height))
}


class Output:
    def __init__(self, screen, x, y, xs, ys):
        self.x = x
        self.y = y
        self.btn_size_x = xs
        self.btn_size_y = ys
        self.screen = screen

    def draw(self):
        font = pygame.font.Font(None, 40)
        text1 = font.render(f'Счёт: {COINS}', True, (255, 215, 0))
        screen.blit(text1, (self.x + 10, self.y + self.btn_size_y // 4))

    def draw_btn(self, text, color, x, y, btn_size_x=0, btn_size_y=0):
        font = pygame.font.Font(None, 100)
        text1 = font.render(text, True, color)
        pygame.draw.rect(screen, RED, (x, y, btn_size_x, btn_size_y))
        screen.blit(text1, (x + 10, y + btn_size_y // 4))


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

        for i in coin_group:
            if pygame.sprite.collide_rect(self, i):
                i.kill()
                global COINS
                COINS += 1
                coin.play(loops=0)

        for i in check_group:
            if pygame.sprite.collide_rect(self, i):
                global LAST, START
                if START == 0:
                    START = i
                LAST = i

        for i in spikes_group:
            if pygame.sprite.collide_rect(self, i):
                self.die()

        for i in finish_group:
            if pygame.sprite.collide_rect(self, i):
                finish_screen()
                self.rect.x = START.rect.x
                self.rect.y = START.rect.y

        for i in ghost_group:
            if pygame.sprite.collide_rect(self, i):
                i.kill()

    def die(self):
        self.rect.x = LAST.rect.x
        self.rect.y = LAST.rect.y
        self.speed_y = 0
        self.speed_x = 0
        global MOVE_LEFT, MOVE_RIGHT, JUMP
        MOVE_RIGHT = 0
        MOVE_LEFT = 0
        JUMP = 0
        death_screen()

    # Анимация
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
        if tile_type == 'coin':
            self.add(coin_group)
        if tile_type == 'spikes':
            self.add(spikes_group)
        if tile_type == 'checkpoint':
            self.add(check_group)
        if tile_type == 'exit':
            self.add(finish_group)
        if tile_type == 'ghost':
            self.add(ghost_group)


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
            elif level[y][x] == '$':
                Tile('coin', x, y)
            elif level[y][x] == '!':
                Tile('spikes', x, y)
            elif level[y][x] == '@':
                new_player = Player(load_image("mario.png"), 20, 1, (tile_width * x, tile_width * y))
            elif level[y][x] == '#':
                Tile('checkpoint', x, y)
            elif level[y][x] == '>':
                Tile('right', x, y)
            elif level[y][x] == 'E':
                Tile('exit', x, y)
            elif level[y][x] == '+':
                Tile('ghost', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


coin_group = pygame.sprite.Group()
flat = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
check_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()

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

# Music
volue = 0.3
pygame.mixer.music.load('music/joy.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volue / 2)
jump = pygame.mixer.Sound('music/jump_3.ogg')
jump.set_volume(volue / 4)
coin = pygame.mixer.Sound('music/coin.mp3')
coin.set_volume(volue)
dead = pygame.mixer.Sound('music/carumba.ogg')
lose = pygame.mixer.Sound('music/smert.ogg')
finish = pygame.mixer.Sound('music/finish_game.ogg')
end = pygame.mixer.Sound('music/fanfara.ogg')


total = Output(screen, 0, 0, 20, 20)


while running:
    clock.tick(FPS)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
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
    total.draw()
    pygame.display.flip()

pygame.quit()