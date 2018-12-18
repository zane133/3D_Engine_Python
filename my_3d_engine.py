import pygame
import sys
import math
import numpy as np


VERTICES = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
EDGES = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]


def init():
    global screen, clock, cam_pos, e, cx, cy, theta

    theta = [math.radians(0), math.radians(0), math.radians(0)]
    # screen width and height
    w, h = 400, 400
    # center points
    cx, cy = w // 2, h // 2

    cam_pos = np.array([0.0, 0.0, 5.0])
    e = np.array([0, 0, 200])

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)
    pygame.font.init()


def game_input(dt):
    global cam_pos, theta
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200
            y /= 200
            theta[0] -= y
            theta[1] += x
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    cam_vector = cam_pos - np.array([0, 0, 0])
    cam_right = np.cross(np.array([0, 1, 0]), cam_vector)
    if key[pygame.K_w]:
        cam_pos -= cam_vector * dt
    if key[pygame.K_s]:
        cam_pos += cam_vector * dt
    if key[pygame.K_a]:
        cam_pos += cam_right * dt
    if key[pygame.K_d]:
        cam_pos -= cam_right * dt
    if key[pygame.K_q]:
        cam_pos[1] -= dt * 5
    if key[pygame.K_e]:
        cam_pos[1] += dt * 5


# world coordinate to screen coordinate
def w2s(world_pos):
    a = np.array(world_pos)
    # a = np.transpose([a])
    # c = np.transpose([cam_pos])
    c = cam_pos

    rx = np.array([
        [1, 0, 0],
        [0, math.cos(theta[0]), math.sin(theta[0])],
        [0, -math.sin(theta[0]), math.cos(theta[0])]
    ])
    ry = np.array([
        [math.cos(theta[1]), 0, -math.sin(theta[1])],
        [0, 1, 0],
        [math.sin(theta[1]), 0, math.cos(theta[1])]
    ])
    rz = np.array([
        [math.cos(theta[2]), math.sin(theta[2]), 0],
        [-math.sin(theta[2]), math.cos(theta[2]), 0],
        [0, 0, 1]
    ])

    d = rx.dot(ry).dot(rz).dot(a - c)

    bx = (e[2] / d[2]) * d[0] + e[0]
    by = (e[2] / d[2]) * d[1] + e[1]
    x, y = cx + int(bx), cy + int(by)
    return x, y


def update(dt):
    # draw num
    for each in VERTICES:
        font = pygame.font.Font(None, 30)
        text = font.render(str(VERTICES.index(each)), 1, (255, 255, 255))
        screen.blit(text, w2s(each))
    for edge in EDGES:
        points = []
        start, end = w2s(VERTICES[edge[0]]), w2s(VERTICES[edge[1]])
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)


if __name__ == "__main__":
    init()
    while True:
        dt = clock.tick() / 1000
        screen.fill((0, 0, 0))

        game_input(dt)

        update(dt)

        pygame.display.flip()
