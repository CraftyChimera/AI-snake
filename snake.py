from random import choice
from time import sleep
import pygame

BG = (0xB4, 0xE5, 0xAF)
SCORE_BG = (0x0, 0x0, 0xFF)
OBJ = (0x0, 0x0, 0x0)
FOOD = (0xFF, 0x0, 0x0)
SCORE = (0x00, 0x00, 0x8B)
direction_vectors = [[1, 0], [0, 1], [0, -1], [-1, 0]]


digits = [
    [0xF0, 0x90, 0x90, 0x90, 0xF0],
    [0x20, 0x60, 0x20, 0x20, 0x70],
    [0xF0, 0x10, 0xF0, 0x80, 0xF0],
    [0xF0, 0x10, 0xF0, 0x10, 0xF0],
    [0x90, 0x90, 0xF0, 0x10, 0x10],
    [0xF0, 0x80, 0xF0, 0x10, 0xF0],
    [0xF0, 0x80, 0xF0, 0x90, 0xF0],
    [0xF0, 0x10, 0x20, 0x40, 0x40],
    [0xF0, 0x90, 0xF0, 0x90, 0xF0],
    [0xF0, 0x90, 0xF0, 0x10, 0xF0]
]


class App:
    def __init__(self):
        self._running = True
        self.mice = None
        self.x = 0
        self.y = 0
        self.cur_direction = 0
        self.snake = []
        self.block_size = 25
        self._display_surf = None
        self.side = 500
        self.score = 0
        self.score_area = 100
        self.block_to_remove = None
        self.block_to_add = None
        self.score_block_scale = 15

    def on_init(self):
        pygame.init()

        self._display_surf = pygame.display.set_mode(
            (self.side, self.side + self.score_area), pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)
        pygame.display.set_caption('Snake')
        self._display_surf.fill(BG)

        self.mice = self.gen_mice()
        self._running = True
        self.snake = [(self.x, self.y), (self.x+self.block_size, self.y)]
        self.x += self.block_size
        pygame.display.update()

    def on_event(self, event):

        if event.type == pygame.KEYDOWN:
            new_dir = self.cur_direction

            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                new_dir = 0

            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                new_dir = 1

            elif event.key in [pygame.K_UP, pygame.K_w]:
                new_dir = 2

            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                new_dir = 3

            elif event.key == pygame.K_q:
                self._running = False

            if abs(self.cur_direction+new_dir) != 3:
                self.cur_direction = new_dir

        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):

        self.block_to_remove = None

        self.x += direction_vectors[self.cur_direction][0] * \
            (self.block_size)
        self.x %= self.side

        self.y += direction_vectors[self.cur_direction][1] * \
            (self.block_size)
        self.y %= self.side

        if([self.x, self.y] in self.snake):
            self._running = False
            return

        if [self.x, self.y] != self.mice:
            self.block_to_remove = self.snake[0]
            self.snake = self.snake[1:]

        else:
            self.mice = self.gen_mice()
            self.score = self.score + 1

        self.snake.append([self.x, self.y])
        self.block_to_add = [self.x, self.y]

    def on_render(self):
        self.draw_score_board()
        self.draw_food()
        self.draw_snake()
        self.display_score(self.score % 10, 430, 515)
        self.display_score((self.score//10) % 10, 360, 515)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            sleep(1/30)

        self.on_cleanup()

    def draw_score_board(self):
        self._display_surf.fill(
            SCORE_BG, (0, self.side, self.side, self.score_area))

    def display_score(self, num, x, y):
        for row in range(5):
            for col in range(8):
                if digits[num][row] & (1 << (7-col)):
                    self._display_surf.fill(
                        SCORE, (x+col*self.score_block_scale, y+row*self.score_block_scale, self.score_block_scale, self.score_block_scale))

    def draw_food(self):
        self._display_surf.fill(
            FOOD, (self.mice[0], self.mice[1], self.block_size, self.block_size))

    def draw_snake(self):
        if self.block_to_remove is not None:
            self._display_surf.fill(
                BG, (self.block_to_remove[0], self.block_to_remove[1], self.block_size, self.block_size))

        self._display_surf.fill(
            OBJ, (self.block_to_add[0], self.block_to_add[1], self.block_size, self.block_size))

    def gen_mice(self):
        master_set = []
        snake_occupied = set()
        allowed_range = self.side // self.block_size

        for x in self.snake:
            snake_occupied.add(
                allowed_range*(x[0]//self.block_size) + (x[1]//self.block_size))

        for num in range(allowed_range ** 2):
            if num not in snake_occupied:
                master_set.append(num)

        gen = choice(master_set)
        gen_x = gen // allowed_range
        gen_y = gen % allowed_range
        return [self.block_size * gen_x, self.block_size * gen_y]


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
