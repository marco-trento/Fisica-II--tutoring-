"""LEZIONE 1 - Dipolo elettrico, VERSIONE INIZIALE da completare in aula.

Librerie necessarie: numpy, pyvista

Il programma di partenza e' eseguibile: mostra le due cariche.
Durante la lezione si completano i TODO per mostrare anche il campo elettrico.
"""

import numpy as np
import pyvista as pv


# PARTE GIA' PRONTA: griglia 3D e costante di Coulomb
L = 2
n = 5
x = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

k_e = 8.99e9  # N m^2 / C^2


# TODO 1 - Completare la funzione del campo elettrico di UNA carica.
def electric_field(points, source, q, cutoff=0.18):
    # a) Calcolare il vettore R = points - source.
    # b) Calcolare il modulo R_mag con np.linalg.norm(..., axis=1).
    # c) Creare la maschera: R_mag > cutoff.
    # d) Inizializzare E con np.zeros_like(points).
    # e) Calcolare E solo dove la maschera e' True.
    # f) Restituire E e mask.
    raise NotImplementedError("TODO 1: completare electric_field")


# PARTE GIA' PRONTA: valori e posizioni delle due cariche
q1 = 1.6e-19
q2 = -1.6e-19
source1 = np.array([-0.5, 0.0, 0.0])
source2 = np.array([0.5, 0.0, 0.0])


# TODO 2 - Calcolare separatamente il campo delle due cariche.
# E1, mask1 = electric_field(...)
# E2, mask2 = electric_field(...)

# TODO 3 - Applicare il principio di sovrapposizione.
# E = ...
# mask = ...  # Usare l'operatore logico & sulle due maschere.

# TODO 4 - Preparare la visualizzazione del campo.
# plot_points = ...
# plot_E = ...
# E_mag = ...
# cloud = pv.PolyData(...)
# cloud["E"] = ...
# arrows = cloud.glyph(orient="E", scale=False, factor=0.15)


# VISUALIZZAZIONE INIZIALE: si vedono le due cariche, non ancora le frecce.
plotter = pv.Plotter()

# TODO 5 - Dopo avere creato arrows, aggiungerle alla scena.
# plotter.add_mesh(arrows, color="black")

sphere1 = pv.Sphere(radius=0.08, center=source1)
sphere2 = pv.Sphere(radius=0.08, center=source2)
plotter.add_mesh(sphere1, color="red")   # Carica positiva
plotter.add_mesh(sphere2, color="blue")  # Carica negativa

plotter.show()
