import pygame
import random

pygame.init()
FPS = 1000
pygame.font.init()
font_size = 34
font = pygame.font.Font('font_3.ttf', font_size)



class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.pallete = {2: (255, 255, 224), 4: (255, 228, 181), 8: (255, 218, 185), 16: (255, 192, 203),
                        32: (221, 160, 221), 64: (135, 206, 235), 128: (32, 178, 170), 256: (154, 205, 50),
                        512: (255, 160, 122), 1024: (219, 112, 147), 2048: (230, 230, 250), 0: (255, 255, 255)}
        # настройка внешнего вида

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                x = self.left + i * self.cell_size
                y = self.top + j * self.cell_size
                pygame.draw.rect(screen, self.pallete[self.field[j][i]], pygame.Rect(x, y,
                                        self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y,
                                        self.cell_size, self.cell_size), 1)
                if self.field[j][i] != 0:
                    screen.blit(font.render(f'{self.field[j][i]}', True, [0, 0, 0]), (
                    (x + cell_size / 2) - font_size  * len(str(self.field[j][i])) / 3.5,
                    y + cell_size / 2 - font_size / 3))

    def add_new_plate(self):
        x_pos = random.randint(0, 3)
        y_pos = random.randint(0, 3)
        while self.field[y_pos][x_pos] != 0:
            x_pos = random.randint(0, 3)
            y_pos = random.randint(0, 3)
        self.field[y_pos][x_pos] = 2

    def create_field(self):
        self.field = [[0] * width for _ in range(height)]

    def compress(self):
        changed = False
        new_field = [[0, 0, 0, 0] for i in range(4)]
        for x_pos in range(4):
            pos = 0
            for y_pos in range(4):
                if self.field[x_pos][y_pos] != 0:
                    new_field[x_pos][pos] = self.field[x_pos][y_pos]
                    if y_pos != pos:
                        changed = True
                    pos += 1
        return new_field, changed

    def merge(self):
        changed = False
        for x_pos in range(4):
            for y_pos in range(3):
                if self.field[x_pos][y_pos] == self.field[x_pos][y_pos + 1] and self.field[x_pos][y_pos] != 0:
                    self.field[x_pos][y_pos] = self.field[x_pos][y_pos] * 2
                    self.field[x_pos][y_pos + 1] = 0
                    changed = True
        return changed

    def reverse(self):
        new_field = []
        for x_pos in range(4):
            new_field.append([])
            for y_pos in range(4):
                new_field[x_pos].append(self.field[x_pos][3 - y_pos])
        return new_field

    def transpose(self):
        new_field = []
        for x_pos in range(4):
            new_field.append([])
            for y_pos in range(4):
                new_field[x_pos].append(self.field[y_pos][x_pos])
        return new_field

    def move_left(self):
        self.field, changed1 = self.compress()
        changed2 = self.merge()
        self.changed = changed1 or changed2
        self.field, temp = self.compress()
        self.add_new_plate()

    def move_right(self):
        self.field = self.reverse()
        self.move_left()
        self.field = self.reverse()


    def move_up(self):
        self.field = self.transpose()
        self.move_left()
        self.field = self.transpose()

    def move_down(self):
        self.field = self.transpose()
        self.move_right()
        self.field = self.transpose()


size = width, height = 1280, 1024
screen = pygame.display.set_mode(size)

field = Field(4, 4)
cell_size = 120
field.set_view(width / 2 - cell_size * 2, height / 2 - cell_size * 2, cell_size)
field.create_field()
field.add_new_plate()
running = True
while running:
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            field.move_right()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            field.move_left()
        if pygame.key.get_pressed()[pygame.K_UP]:
            field.move_up()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            field.move_down()
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    field.render(screen)
    pygame.display.flip()
