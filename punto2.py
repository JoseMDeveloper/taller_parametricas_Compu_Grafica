import numpy as np
import pygame
import scipy.interpolate as interpolate
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


def calculate_coordinates():
    samples = 100
    x_coord = np.linspace(0, 2 * np.pi, samples)
    y_coord = np.linspace(0, 2 * np.pi, samples)

    x_flat, y_flat = np.meshgrid(x_coord, y_coord)
    z_flat = np.sin(x_flat) * np.cos(y_flat)  # Genera una superficie para z en función de x y y

    x_grid, y_grid = np.meshgrid(x_coord, y_coord)
    z_gridded = interpolate.griddata((x_flat.flatten(), y_flat.flatten()), z_flat.flatten(), (x_grid, y_grid),
                                     method='linear')

    return z_gridded


def plot_circle(z_gridded, radius=5, samples=10):
    glBegin(GL_LINE_STRIP)
    for row in z_gridded:
        for t in row:
            glVertex2f(radius * np.cos(t), radius * np.sin(t))
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
        z_gridded = calculate_coordinates()
        plot_circle(z_gridded)
        pygame.display.flip()
        pygame.time.wait(100)
    pygame.quit()


if __name__ == '__main__':
    main()

