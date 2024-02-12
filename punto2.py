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

def heart_equation(t, a=1):
    x = a * 16 * np.sin(t)**3
    y = a * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    return x, y

def true_fn(x, radius):
    t = np.linspace(0, np.pi, len(x))
    x_heart, y_heart = heart_equation(t, radius)
    return y_heart

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
        t = i * np.pi / (len(x) - 1)
        x_heart, y_heart = heart_equation(t, radius)
        # Multiplicar por el factor de escala (1/16)
        glVertex3f(x_heart / 16, y_heart / 16, 0)
    glEnd()

    # Dibujar la interpolación
    glBegin(GL_LINE_STRIP)
    
    glColor3f(0, 0, 0)
    for i in range(len(x)):
        t = i * np.pi / (len(x) - 1)
        x_heart, y_heart = heart_equation(t, radius)
        # Multiplicar por el factor de escala (1/16)
        glVertex3f(x_heart / 16, interp(x)[i] / 16, 0)
    glEnd()

    # Dibujar puntos de muestra
    glBegin(GL_POINTS)
    glColor3f(0, 1, 0)
    for i in range(len(xk)):
        glVertex3f(xk[i], true_fn(xk, radius)[i], 0)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
