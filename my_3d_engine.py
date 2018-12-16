import pygame
import sys
import numpy as np


VERTICES = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]


def init():
    global screen, clock
    # screen width and height
    w, h = 400, 400
    # center points
    cx, cy = w // 2, h // 2
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()


def input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def update():
    pygame.draw.circle(screen, (255,255,255), (50,50), 50)


if __name__ == "__main__":
    init()
    while True:
        dt = clock.tick() / 1000
        screen.fill((0, 0, 0))

        input()

        update()

        pygame.display.flip()
