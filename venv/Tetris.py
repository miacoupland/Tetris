import pygame
import random

#CREDIT TO: Timur Bakibayev at gitconnected https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
#Programme made with this tutorial and expanded to add functionality, making the game more similar to the original NES game
#made colours specific to piece type

#piece colours
colours = [
    (0,0,0),
    (52, 235, 235),#cyan i piece
    (25, 68, 255),#blue j piece
    (255, 155, 25),#orange l piece
    (144, 25, 255),#purple t piece
    (247, 255, 25),#yellow o piece
    (56, 255, 25),#green s piece
    (255, 36, 36),#red z piece
]

class Figure:
    x = 0
    y = 0

    # the main list contains figure types the the inner list is their rotations
    # the numbers represent the positions in a 4x4 matrix where the figure is solid
    # [1, 5, 9, 13] represents a line.
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],#I piece
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],#J piece
        [[1, 2, 6, 10],[5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],#L piece
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],#T piece
        [[1, 2, 5, 6]],#o piece
        [[1, 5, 6, 10], [2, 3, 5, 6,]], #S piece
        [[1, 5, 4, 8], [1, 2, 6, 7]]#Z piece
    ]

    # type and colour is randomly picked
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.colour = self.type + 1 # +1 to avoid i piece disappearing when setting colours
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris:
    level = 2
    score = 0
    state = "start" #says if we're playing or not
    # field of the game, with 0s where it is empty and colours
    # where colours there are figures, aside from the active piece
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    #a new field is created with the size height x width
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    #makes a new figure at coordinates 3,0
    def new_figure(self):
        self.figure = Figure(3, 0)

    #check each cell in the 4x4 matrix of the figure. see if it is out
    #of bounds or if it is touching a busy field. if there is no colour,
    #there is no issue.
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y] [j + self.figure.x] > 0:
                        intersection = True
        return intersection

    #check if we are allowed to move or rotate the figure. if it moves
    #down and intersects, we reach the bottom and need to lock it into place
    def lock(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.colour
        self.break_lines()
        self.new_figure()
        if self.intersects():
            game.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    #start of moving methods
    #each method remembers the last position, changes coordinates
    #and if there is an intersection, returns to the previous state
    #this goes down until it reaches the bottom or a figure
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.lock()

    #sends piece down one
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.lock()

    #sends piece to the specified side
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    #rotates piece
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

#initialise game
pygame.init()

#define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

#set game size
size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

#loop until closes
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()

    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colours[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colours[game.figure.colour],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calbiri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 40, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0,0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

quit()