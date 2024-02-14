import numpy as np
import os
from OpenGL.GL import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

os.environ["SDL_VIDEO_CENTERED"] = '1'

def main():
    pygame.init()
    display = (1000, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(85, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0, -20)


def plot_parametric_mesh(points_matrix): #hace el mallado
    glPointSize(3)
    n_rows = len(points_matrix)
    n_cols = len(points_matrix[0])


    colores = [
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
            glColor3fv(colores[0])
            glVertex3fv(points_matrix[i][j])

            glColor3fv(colores[1])
            glVertex3fv(points_matrix[i][(j + 1) % n_cols])

            glVertex3fv(points_matrix[i][(j + 1) % n_cols])
            glColor3fv(colores[2])

            glVertex3fv(points_matrix[(i + 1) % n_rows][(j + 1) % n_cols])

            glVertex3fv(points_matrix[(i + 1) % n_rows][(j + 1) % n_cols])
            glColor3fv(colores[5])
            glVertex3fv(points_matrix[(i + 1) % n_rows][j])
            glVertex3fv(points_matrix[(i + 1) % n_rows][j])

            glColor3fv(colores[0])
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


def generate_toroid_points(
        radius_1=4,
        radius_2=1,
        alpha_samples=20,
        beta_samples=20
):
    point_matrix = []
    for alpha in np.linspace(0, 2 * np.pi, alpha_samples):
        point_array = []
        for beta in np.linspace(0, 2 * np.pi, beta_samples):
            point_array.append(
                (
                    (radius_1 + radius_2 * np.cos(beta)) * np.sin(alpha),
                    (radius_1 + radius_2 * np.cos(beta)) * np.cos(alpha),
                    radius_2 * np.sin(beta)
                )
            )
        point_matrix.append(point_array)
    return point_matrix



def generate_botella_klein(alpha_samples=40, beta_samples=40):
    def kleinFlasche(u, v):
        cos = np.cos
        sin = np.sin
        pi = np.pi
        #u = u * 2
        if u < pi:
            x = 3 * cos(u) * (1 + sin(u)) + (2 * (1 - cos(u) / 2)) * cos(u) * cos(v)
            z = -8 * sin(u) - 2 * (1 - cos(u) / 2) * sin(u) * cos(v)
        else:
            x = 3 * cos(u) * (1 + sin(u)) + (2 * (1 - cos(u) / 2)) * cos(v + pi)
            z = -8 * sin(u)
        y = -2 * (1 - cos(u) / 2) * sin(v)
        return x, y, z


    point_matrix = []
    for alpha in np.linspace(0, 2 * np.pi, alpha_samples):
        point_array = []
        for beta in np.linspace(0, 2 * np.pi, beta_samples):
            point_array.append(kleinFlasche(alpha, beta))
        point_matrix.append(point_array)
    return point_matrix



main()
run = True
points_matrix = generate_botella_klein()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    glRotatef(4, 1, 0, 0);


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    plot_parametric_mesh(points_matrix)
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()
quit()