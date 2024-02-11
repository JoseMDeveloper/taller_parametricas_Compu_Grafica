import numpy as np
from OpenGL.GL import *


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

def generate_botella_klein(
        alpha_samples=30,
        beta_samples=30,
        escala=2
):
    point_matrix = []
    for alpha in np.linspace(0, 2 * np.pi, alpha_samples):
        point_array = []
        for beta in np.linspace(0, 2 * np.pi, beta_samples):
            point_array.append(
                (
                    (6/escala * np.cos(alpha) * (1/escala + np.sin(alpha)) + 4/escala * (1/escala - np.cos(alpha) / 2/escala) * np.cos(beta) * np.cos(((np.sign(np.pi - alpha) + 1/escala) / 2/escala) * alpha) * np.sign(np.pi - alpha)),
                    (16/escala * np.sin(alpha) + 4/escala * (1/escala - np.cos(alpha) / 2/escala) * np.cos(beta) * np.sin(((np.sign(np.pi - alpha) + 1/escala) / 2/escala) * alpha)),
                    (4/escala * (1/escala - np.cos(alpha) / 2/escala) * np.sin(beta))
                )
            )
        point_matrix.append(point_array)
    return point_matrix
