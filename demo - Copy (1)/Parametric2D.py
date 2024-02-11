import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -10
ortho_right = 10
ortho_top = -10
ortho_bottom = 10

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Polygons in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def plot_circle(radius=4, samples=10):
    glBegin(GL_LINE_STRIP)
    for t in np.linspace(0, 2 * np.pi, samples):
        glVertex2f(radius * np.cos(t), radius * np.sin(t))
    glEnd()


def plot_ellipse(radius_1=3, radius_2=6, samples=10):
    glBegin(GL_LINE_STRIP)
    for t in np.linspace(0, 2 * np.pi, samples):
        glVertex2f(radius_1 * np.cos(t), radius_2 * np.sin(t))
    glEnd()


def main():
    done = False
    init_ortho()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPointSize(5)
        plot_ellipse()
        pygame.display.flip()
        pygame.time.wait(100)
    pygame.quit()


if __name__ == '__main__':
    main()
