"""LEZIONE 1 - Campo elettrico di una singola carica puntiforme.

Librerie necessarie: numpy, pyvista
"""

import numpy as np
import pyvista as pv


# 1. Vettore di coordinate lungo ciascun asse
L = 2
n = 5
x = np.linspace(-L, L, n)
print("Coordinate x:", x)
print("Forma di x:", x.shape)

# 2. Griglia 2D 
X2, Y2 = np.meshgrid(x, x, indexing="ij")
print("Forma della griglia 2D:", X2.shape, Y2.shape)
print("X2:\n", X2)
print("Y2:\n", Y2)

# 3. Griglia 3D e conversione in nuvola di punti
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
print("Forma della griglia 3D:", X.shape)

# Ogni riga di points contiene le coordinate (x, y, z) di un punto.
points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
print("Forma di points:", points.shape)  # (125, 3)

# 4. Costanti fisiche e posizione della carica
k_e = 8.99e9                 # Costante di Coulomb, N m^2 / C^2
q = 1.6e-19                 # Carica positiva, C
source = np.array([0.0, 0.0, 0.0])

# 5. Vettore distanza tra ciascun punto e la sorgente
R = points - source
R_mag = np.linalg.norm(R, axis=1)
print("Forma di R:", R.shape)
print("Primo vettore R:", R[0])
print("Modulo del primo vettore R:", R_mag[0])

# 6. Maschera per evitare la singolarita' in prossimita' della carica
cutoff = 0.18
mask = R_mag > cutoff
print("Maschera:", mask)

# 7. Campo elettrico: E = k_e * q * R / |R|^3
E = np.zeros_like(points)
E[mask] = k_e * q * R[mask] / R_mag[mask, None]**3

# 8. Selezione dei punti validi e visualizzazione
plot_points = points[mask]
plot_E = E[mask]

cloud = pv.PolyData(plot_points)
cloud["E"] = plot_E
arrows = cloud.glyph(orient="E", scale=False, factor=0.15)

plotter = pv.Plotter()
plotter.add_mesh(arrows, color="black")

# La sfera va aggiunta PRIMA di mostrare la finestra.
sphere = pv.Sphere(radius=0.08, center=source)
plotter.add_mesh(sphere, color="red")

plotter.show()
