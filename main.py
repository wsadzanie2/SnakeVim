import pygame
import random
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont('', 128)
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height), RESIZABLE)


def rel_to_poz(rel_poz):
    return [rel_poz[0] * 50, rel_poz[1] * 50]
def poz_to_rel(poz):
    return [poz[0] // 50, poz[1] // 50]


class Apples:
    def __init__(self):
        self.rel_poz = random.randint(0, width // 50), random.randint(0, height // 50)
        self.poz = rel_to_poz(self.rel_poz)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.poz, (50, 50)))

    def update_poz(self):
        if not snake_head.collide_with_head(self):
            return
        while snake_head.collide_with_head(self):
            self.rel_poz = random.randint(1, width // 50) - 1, random.randint(1, height // 50) - 1
            self.poz = rel_to_poz(self.rel_poz)
        snake_head.get_last_node().add_child()
class SnakeNode:
    def __init__(self, parent, child=None, rel_poz=None):
        self.parent = parent
        self.child = child
        if rel_poz is None:
            rel_poz = [0, 0]
        self.rel_poz = rel_poz
        self.poz = rel_to_poz(rel_poz)
        self.color = (0, 255, 0)

    def collide_with_head(self, head):
        if tuple(self.rel_poz) == tuple(head.rel_poz):
            return True
        if self.child:
            return self.child.collide_with_head(head)
        return False


    def add_child(self, rel_poz=(-20, -20)):
        if self.child:
            self.get_last_node().add_child(rel_poz=rel_poz)
        self.child = SnakeNode(self, None, rel_poz)

    def get_last_node(self):
        if self.child:
            return self.child.get_last_node()
        return self

    def update_values(self):
        self.poz = rel_to_poz(self.rel_poz)
    def draw(self):
        self.update_values()
        pygame.draw.rect(screen, self.color, pygame.Rect(self.poz, (50, 50)))
        if self.child:
            self.child.draw()

    def move(self, poz):
        x, y = poz
        if self.parent is not None:
            self.rel_poz = self.parent.rel_poz.copy()
            self.parent.move(poz)
        else:
            self.rel_poz[0] += x
            self.rel_poz[1] += y
        self.rel_poz[0] %= width // 50
        self.rel_poz[1] %= height // 50


apple = Apples()

def draw_text(text, poz, color=(0, 0, 0)):
    font_thing = font.render(text, True, color)
    font_rect = font_thing.get_rect()
    font_rect.center = poz
    poz = font_rect.topleft
    screen.blit(font_thing, poz)

snake_head = SnakeNode(None, rel_poz=[0, 0])
snake_head.color = (0, 200, 0)
snake_head.direction = ''
for i in range(5):
    snake_head.get_last_node().add_child([0, i + 1])

def move_snake(direction):
    if direction == 'right':
        snake_head.get_last_node().move([1, 0])
    elif direction == 'left':
        snake_head.get_last_node().move([-1, 0])
    elif direction == 'up':
        snake_head.get_last_node().move([0, -1])
    elif direction == 'down':
        snake_head.get_last_node().move([0, 1])
run = True
clock = pygame.time.Clock()
frame = 0

while run:
    frame += 1
    dt = clock.tick(60) / 1000
    if snake_head.child.collide_with_head(snake_head):
        run = False
    if frame % 7 == 0:
        move_snake(snake_head.direction)
    screen.fill((75, 75, 75))
    if snake_head.direction == 'left':
        draw_text('h', (width // 2 - 50, height // 2), (255, 255, 255))
    else:
        draw_text('h', (width // 2 - 50, height // 2))
    if snake_head.direction == 'down':
        draw_text('j', (width // 2, height // 2 + 50), (255, 255, 255))
    else:
        draw_text('j', (width // 2, height // 2 + 50))
    if snake_head.direction == 'up':
        draw_text('k', (width // 2, height // 2 - 50), (255, 255, 255))
    else:
        draw_text('k', (width // 2, height // 2 - 50))
    if snake_head.direction == 'right':
        draw_text('l', (width // 2 + 50, height // 2), (255, 255, 255))
    else:
        draw_text('l', (width // 2 + 50, height // 2))
    snake_head.draw()
    apple.draw()
    apple.update_poz()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_l and snake_head.direction != 'left':
                snake_head.direction = 'right'
            elif event.key == K_j and snake_head.direction != 'up':
                snake_head.direction = 'down'
            elif event.key == K_h and snake_head.direction != 'right':
                snake_head.direction = 'left'
            elif event.key == K_k and snake_head.direction != 'down':
                snake_head.direction = 'up'
    pygame.display.flip()

pygame.quit()