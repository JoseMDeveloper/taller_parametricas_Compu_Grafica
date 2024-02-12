import numpy as np
from OpenGL.GL import *
import pygame
from OpenGL.GLU import *
from pygame.locals import *

# Parámetros
radius = 1
eps = 2

xk = np.linspace(-radius, radius, 20)
x = np.linspace(-radius, radius, 50)


def true_fn(x, radius):
    return np.sqrt(np.where(x <= radius, radius ** 2 - x ** 2, np.nan))


def true_fn2(x, radius):
    return -(np.sqrt(np.where(x <= radius, radius ** 2 - x ** 2, np.nan)))


def euclidean_distance(x, xk):
    return np.sqrt(((x.reshape(-1, 1)) - xk.reshape(1, -1)) ** 2)


def gauss_rbf(radius, eps):
    return np.exp(-(eps * radius) ** 2)


class RBFinterp(object):
    def __init__(self, eps):
        self.eps = eps

    def fit(self, xk, yk, zk):
        self.xk = xk
        transformation = gauss_rbf(euclidean_distance(xk, xk), self.eps)
        self.w_y = np.linalg.solve(transformation, yk)
        self.w_z = np.linalg.solve(transformation, zk)

    def __call__(self, xn):
        transformation = gauss_rbf(euclidean_distance(xn, self.xk), self.eps)
        return transformation.dot(self.w_y), transformation.dot(self.w_z)


interp = RBFinterp(eps)
yk = true_fn(xk, radius)
zk = np.zeros_like(yk)
interp.fit(xk, yk, zk)

interp2 = RBFinterp(eps)
yk2 = true_fn2(xk, radius)
zk2 = np.zeros_like(yk2)
interp2.fit(xk, yk2, zk2)

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(1, 3, 1, 1)  # Rotación sobre el eje y

    # Dibujar la función verdadera
    glBegin(GL_LINE_STRIP)
    glColor3f(1, 0, 0)
    for i in range(len(x)):
        for z in range(len(x)):
            glVertex3f(x[i], true_fn(x, radius)[i], true_fn(x, radius)[z])
    glEnd()

    # Dibujar la interpolación
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)
    for i in range(len(x)):
        for z in range(len(x)):
            y_val = interp(np.array([x[i]]))
            z_val = interp(np.array([x[z]]))
            glVertex3f(x[i], y_val[0], z_val[0])
    glEnd()

    # Dibujar puntos de muestra
    glBegin(GL_POINTS)
    glColor3f(0, 1, 0)
    for i in range(len(xk)):
        glVertex3f(xk[i], yk[i], zk[i])
    glEnd()

    # Dibujar la parte de abajo del círculo

    # Dibujar la función verdadera
    glBegin(GL_LINE_STRIP)
    glColor3f(1, 0, 0)
    for i in range(len(x)):
        for z in range(len(x)):
            glVertex3f(x[i], true_fn2(x, radius)[i], true_fn(x, radius)[z])
    glEnd()

    # Dibujar la interpolación
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)
    for i in range(len(x)):
        for z in range(len(x)):
            y_val = interp2(np.array([x[i]]))
            z_val = interp(np.array([x[z]]))
            glVertex3f(x[i], y_val[0], z_val[0])
    glEnd()

    # Dibujar puntos de muestra
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0)
    for i in range(len(xk)):
        glVertex3f(xk[i], yk2[i], zk2[i])
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
