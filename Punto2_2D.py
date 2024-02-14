import numpy as np
from OpenGL.GL import *
import pygame
from OpenGL.GLU import *
from pygame.locals import *

# Parámetros
radius = 2  # Puedes ajustar el radio según sea necesario
eps = 2

xk = np.linspace(-radius, radius, 55)
x = np.linspace(-radius, radius, 200)


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

    def fit(self, xk, yk):
        self.xk = xk
        transformation = gauss_rbf(euclidean_distance(xk, xk), self.eps)
        self.w_ = np.linalg.solve(transformation, yk)

    def __call__(self, xn):
        transformation = gauss_rbf(euclidean_distance(xn, self.xk), self.eps)
        return transformation.dot(self.w_)


interp = RBFinterp(eps)
yk = true_fn(xk, radius)
interp.fit(xk, yk)

interp2 = RBFinterp(eps)
yk2 = true_fn2(xk, radius)
interp2.fit(xk, yk2)

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

    # Dibujar la función verdadera
    glBegin(GL_LINE_STRIP)
    glColor3f(1, 0, 0)
    for i in range(len(x)):
        glVertex3f(x[i], true_fn(x, radius)[i], 0)
    glEnd()

    # Dibujar la interpolación
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)
    for i in range(len(x)):
        glVertex3f(x[i], interp(x)[i], 0)
    glEnd()

    # Dibujar puntos de muestra
    glBegin(GL_POINTS)
    glColor3f(0, 1, 0)
    for i in range(len(xk)):
        glVertex3f(xk[i], true_fn(xk, radius)[i], 0)
    glEnd()

    # Dibujar la parte de abajo del circulo

    # Dibujar la función verdadera
    glBegin(GL_LINE_STRIP)
    glColor3f(1, 0, 0)
    for i in range(len(x)):
        glVertex3f(x[i], true_fn2(x, radius)[i], 0)
    glEnd()

    # Dibujar la interpolación
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)
    for i in range(len(x)):
        glVertex3f(x[i], interp2(x)[i], 0)
    glEnd()

    # Dibujar puntos de muestra
    glBegin(GL_POINTS)
    glColor3f(1, 1, 0)
    for i in range(len(xk)):
        glVertex3f(xk[i], true_fn2(xk, radius)[i], 0)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
