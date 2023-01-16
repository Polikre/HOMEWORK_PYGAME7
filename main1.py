import pygame as p
import sys
import os


clock = p.time.Clock()
FPS = 10
WIDTH = 550
HEIGHT = 550
gravity = 0.25

p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
running = True
p.mouse.set_visible(0)
player = None
all_sprites = p.sprite.Group()
tiles_group = p.sprite.Group()
player_group = p.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = p.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    p.quit()
    sys.exit()


def start_screen():
    intro_text = [""]
    fon = p.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = p.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, p.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                terminate()
            elif event.type == p.KEYDOWN or \
                    event.type == p.MOUSEBUTTONDOWN:
                return
        p.display.flip()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(p.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(p.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_(self, key):
        min_x, min_y, max_x, max_y = 0, 0, len(map_level[0]), len(map_level)
        tmp_x = self.pos_x
        tmp_y = self.pos_y
        if key[p.K_DOWN] and self.pos_y + 1 < max_y:
            self.pos_y += 1
        elif key[p.K_UP] and self.pos_y - 1 >= min_y:
            self.pos_y -= 1
        elif key[p.K_LEFT] and self.pos_x - 1 >= min_x:
            self.pos_x -= 1
        elif key[p.K_RIGHT] and self.pos_x + 1 < max_x:
            self.pos_x += 1
        if map_level[self.pos_y][self.pos_x] == "#":
            self.pos_x = tmp_x
            self.pos_y = tmp_y
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    zn = (0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                zn = (x, y)
    Tile('empty', zn[0], zn[1])
    new_player = Player(zn[0], zn[1])
    return new_player, x, y


text = input("Название уровня\n")
try:
    map_level = load_level(text)
    start_screen()
    player, level_x, level_y = generate_level(load_level(text))
    for i in load_level("map.txt"):
        print(i)
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            key = p.key.get_pressed()
            player.update_(key)
        screen.fill((255, 255, 255))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        p.display.flip()
    p.quit()
except FileNotFoundError:
    print("Такого файла не существует")
