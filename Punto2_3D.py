import numpy as np
from OpenGL.GL import *

import os

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

os.environ["SDL_VIDEO_CENTERED"] = '1'


def main():
    pygame.init()
    display = (1000, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(65, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0, -20)

def plot_parametric_mesh(points_matrix): #hace el mallado
    glPointSize(3)
    n_rows = len(points_matrix) - 1
    n_cols = len(points_matrix[0])

    # Define una nueva lista de colores con los valores que desees
    custom_colors = [
        (1.0, 0.0, 0.0),  # Rojo
        (0.0, 1.0, 0.0),  # Verde
        (0.0, 0.0, 1.0),  # Azul
        (1.0, 1.0, 0.0),  # Amarillo
        (0.0, 1.0, 1.0),  # Cian
        (1.0, 0.0, 1.0)  # Magenta
    ]

    for i in range(n_rows):
        for j in range(n_cols):
            glBegin(GL_LINES)
            glColor3fv(custom_colors[0])
            glVertex3fv(points_matrix[i][j])
            glColor3fv(custom_colors[1])
            glVertex3fv(points_matrix[i][(j + 1) % n_cols])
            glColor3fv(custom_colors[2])
            glVertex3fv(points_matrix[(i + 1) % n_rows][(j + 1) % n_cols])
            glColor3fv(custom_colors[0])
            glVertex3fv(points_matrix[i][j])
            glEnd()
            glBegin(GL_LINES)
            glColor3fv(custom_colors[3])
            glVertex3fv(points_matrix[i][j])
            glColor3fv(custom_colors[4])
            glVertex3fv(points_matrix[(i + 1) % n_rows][(j + 1) % n_cols])
            glColor3fv(custom_colors[5])
            glVertex3fv(points_matrix[(i + 1) % n_rows][j])
            glColor3fv(custom_colors[0])
            glVertex3fv(points_matrix[i][j])
            glEnd()


def generate_sphere_points(
        radius=3,
        alpha_samples=20,
        beta_samples=10
):
    point_matrix = []
    for alpha in np.linspace(0, 2 * np.pi, alpha_samples):
        point_array = []
        for beta in np.linspace(0, np.pi, beta_samples):
            point_array.append(
                (
                    radius * np.cos(alpha) * np.sin(beta),
                    radius * np.sin(alpha) * np.sin(beta),
                    radius * np.cos(beta)
                )
            )
        point_matrix.append(point_array)
    return point_matrix


main()
run = True
points_matrix = generate_sphere_points()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    glRotatef(4, 0, 1, 0);


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    plot_parametric_mesh(points_matrix)
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()
quit()
