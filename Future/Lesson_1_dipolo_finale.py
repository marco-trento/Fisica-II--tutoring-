"""LEZIONE 1 - Campo elettrico di un dipolo, VERSIONE FINALE.

Librerie necessarie: numpy, pyvista

"""

import numpy as np
import pyvista as pv


# 1. Griglia tridimensionale
L = 2
n = 5
x = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

k_e = 8.99e9  # Costante di Coulomb, N m^2 / C^2


# 2. Campo elettrico generato da una singola carica puntiforme
def electric_field(points, source, q, cutoff=0.18):
    R = points - source
    R_mag = np.linalg.norm(R, axis=1)
    mask = R_mag > cutoff

    E = np.zeros_like(points)
    E[mask] = k_e * q * R[mask] / R_mag[mask, None]**3

    return E, mask


# 3. Due cariche di segno opposto (dipolo)
q1 = 1.6e-19
q2 = -1.6e-19
source1 = np.array([-0.5, 0.0, 0.0])
source2 = np.array([0.5, 0.0, 0.0])

# 4. Campi elettrici prodotti separatamente dalle due cariche
E1, mask1 = electric_field(points, source1, q1)
E2, mask2 = electric_field(points, source2, q2)

# 5. Principio di sovrapposizione e maschera comune
E = E1 + E2
mask = mask1 & mask2

# 6. Preparazione dei dati da rappresentare
plot_points = points[mask]
plot_E = E[mask]
E_mag = np.linalg.norm(plot_E, axis=1)

cloud = pv.PolyData(plot_points)
cloud["E"] = plot_E
arrows = cloud.glyph(orient="E", scale=False, factor=0.15)

# 7. Visualizzazione 3D del campo e delle due cariche
plotter = pv.Plotter()
plotter.add_mesh(arrows, color="black")

sphere1 = pv.Sphere(radius=0.08, center=source1)
sphere2 = pv.Sphere(radius=0.08, center=source2)
plotter.add_mesh(sphere1, color="red")   # Carica positiva
plotter.add_mesh(sphere2, color="blue")  # Carica negativa

plotter.show()
