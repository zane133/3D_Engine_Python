import pygame
import sys
import math
import numpy as np


VERTICES = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]

def init():
    global screen, clock, cam_pos, rx, ry, rz, e, cx, cy

    theta = [math.radians(0), math.radians(0), math.radians(0)]
    # screen width and height
    w, h = 400, 400
    # center points
    cx, cy = w // 2, h // 2
    # far and near flat
    # f, n = 1000, 500

    cam_pos = np.array([0, 0, 0])
    e = np.array([0, 0, 30])
    rx = np.array([
        [1,  0,                   0                 ],
        [0,  math.cos(theta[0]),  math.sin(theta[0])],
        [0, -math.sin(theta[0]),  math.cos(theta[0])]
    ])
    ry = np.array([
        [math.cos(theta[1]), 0, -math.sin(theta[1])],
        [0,                  1,  0                 ],
        [math.sin(theta[1]), 0,  math.cos(theta[1])]
    ])
    rz = np.array([
        [ math.cos(theta[2]), math.sin(theta[2]), 0],
        [-math.sin(theta[2]), math.cos(theta[2]), 0],
        [0,                   0,                  1]
    ])

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
    for each in VERTICES:
        a = np.array(each)
        a = np.transpose([a])
        c = np.transpose([cam_pos])
        # c = cam_pos
        d = np.dot(rx * ry * rz, (a - c))

        bx = (e[2] / d[2]) * d[0] + e[0]
        by = (e[2] / d[2]) * d[1] + e[1]
        x, y = cx + int(bx), cy + int(by)
        print(bx, by)
        # print(x, y)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)


if __name__ == "__main__":
    init()
    while True:
        dt = clock.tick() / 1000
        screen.fill((0, 0, 0))

        input()

        update()
        break
        pygame.display.flip()
