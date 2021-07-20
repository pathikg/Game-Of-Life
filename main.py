import pygame
import random
import sys

# reference : https://www.youtube.com/watch?v=FWSR_7kZuYg&t=2060s

random.seed(69)
pygame.init()


class Game:
    def __init__(self, width, height, cell_width, cell_height):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Of Life")
        self.colors = ['black', 'white']
        self.num_rows = height // cell_height
        self.num_cols = width // cell_width
        self.grid = self.makeGrid()
        self.start_pressed = False

    # intro before game starts
    def intro(self, x, y):
        width = 240
        height = 40
        if self.width // 2 + width // 2 > x > self.width // 2 - width // 2 and self.height // 2 + height // 2 > y > self.height // 2 - height // 2:
            self.start_pressed = True
        else:
            font = pygame.font.SysFont('roboto', 60)
            text = font.render("Don't Hover !", True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (self.width // 2, self.height // 2)

            font2 = pygame.font.SysFont('roboto', 30)
            text2 = font2.render("Made by Pathik Ghugare", True, (255, 255, 255), (0, 0, 0))
            textRect2 = text2.get_rect()
            textRect2.center = (self.width // 2, self.height-50)

            font3 = pygame.font.SysFont('roboto', 100)
            text3 = font3.render("Game Of Life", True, (0, 0, 0), (255, 255, 255))
            textRect3 = text2.get_rect()
            textRect3.center = (self.width // 2 - 100, 100)

            self.screen.blit(text, textRect)
            self.screen.blit(text2, textRect2)
            self.screen.blit(text3, textRect3)

            # pygame.draw.rect(self.screen, 'white',
            #                  ((self.width // 2 - width // 2, self.height // 2 - height), (width, height)))

    # to create empty grid
    def makeGrid(self):
        a = [[0] * self.num_cols for i in range(self.num_rows)]
        return a

    def initGrid(self):
        for c, i in enumerate(range(0, self.height, self.cell_height)):
            for d, j in enumerate(range(0, self.width, self.cell_width)):
                color = random.choice(self.colors)
                self.grid[c][d] = self.colors.index(color)
        return self.grid

    def drawLines(self):
        for i in range(0, self.height, self.cell_height):
            pygame.draw.line(self.screen, 'black', (0, i), (self.width, i))
        for i in range(0, self.width, self.cell_width):
            pygame.draw.line(self.screen, 'black', (i, 0), (i, self.height))

    def drawGrid(self):
        for c, i in enumerate(range(0, self.height, self.cell_height)):
            for d, j in enumerate(range(0, self.width, self.cell_width)):
                color_index = self.grid[c][d]
                color = self.colors[color_index]
                pygame.draw.rect(self.screen, color, ((j, i), (self.cell_width, self.cell_height)))
        self.drawLines()

    def updateGrid(self):
        # initialising next generation
        nxt = self.makeGrid()
        for c, i in enumerate(range(0, self.height, self.cell_height)):
            for d, j in enumerate(range(0, self.width, self.cell_width)):
                state = self.grid[c][d]
                neighbors = self.countNeighbours(c, d)
                if state == 0 and neighbors == 3:
                    nxt[c][d] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    nxt[c][d] = 0
                else:
                    nxt[c][d] = state
        self.grid = nxt

    def countNeighbours(self, x, y):
        s = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                s += self.grid[(x + i + self.num_rows) % self.num_rows][(y + j + self.num_cols) % self.num_cols]
        s -= self.grid[x][y]  # not considering the element around which we are counting neighbours
        return s


# will use this to set FPS
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_WIDTH = CELL_HEIGHT = 10

board = Game(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
grid = board.initGrid()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    if board.start_pressed:
        board.drawGrid()
        board.updateGrid()
    else:
        x, y = pygame.mouse.get_pos()
        board.intro(x, y)

    # Updating the entire window
    pygame.display.update()
    # 60 FPS
    clock.tick(60)
