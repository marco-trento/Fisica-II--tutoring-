import numpy as np
import pyvista as pv

k_e = 8.9875517873681764e9
q1 = 1.6e-19
q2 = -1.6e-19

L = 2
n = 7

x = np.linspace(-L, L, n)
#print(x.shape)

X, Y, Z = np.meshgrid(x, x, x,indexing="ij") #xy-cartesian coordinates, ij-matrix indexing
#print(X.shape)


points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))#ravel() flattens the array, column_stack stacks 1D arrays as columns into a 2D array
#print(points.shape)


###––––––––––––––––––––––––––––––––––###
#This section is for a single charge in space, (comment it out if you want to see the field of two charges)
###––––––––––––––––––––––––––––––––––###
source = np.array([0.0, 0.0, 0.0])
R = points - source
R_mag = np.linalg.norm(R, axis=1)
cutoff = 0.18
mask = R_mag > cutoff #points too close to the charge are not considered to avoid singularities 
E = np.zeros_like(points)
E[mask] = (k_e * q1 * R[mask] / R_mag[mask, None]**3) #None is used to add a new axis to the array, allowing for broadcasting in the division operation. This ensures that the division is performed element-wise for each component of the electric field vector.
E_dir = np.zeros_like(E)
nonzero = np.linalg.norm(E, axis=1) > 0


E_dir[nonzero] = E[nonzero] / np.linalg.norm(E[nonzero], axis=1)[:, None]
plot_points = points[mask]
plot_E = E[mask]
plot_E_dir = E_dir[mask]
# PyVista dataset
cloud = pv.PolyData(plot_points)
cloud["E"] = plot_E
cloud["E_dir"] = plot_E_dir
#glyph arrows
arrows = cloud.glyph(
    orient="E_dir",
    scale=False,
    factor=0.12,
)
# Visualization
plotter = pv.Plotter()
plotter.add_mesh(
    arrows,
    color="black"
)   
sphere = pv.Sphere(
    radius=0.08,
    center=source
)
plotter.add_mesh(
    sphere,
    color="red"
)
plotter.add_axes()
plotter.show_grid()
plotter.show()
####––––––––––––––––––––––––––––––––––###


#This section is for two charges in space, (comment it out if you want to see the field of a single charge)
###––––––––––––––––––––––––––––––––––###


"""
source1 = np.array([-1.0, 0.0, 0.0])
source2 = np.array([1.0, 0.0, 0.0])


def electric_field(source, points,q):

    R_vec = points - source

    R = np.linalg.norm(
        R_vec,
        axis=1
    )

    cutoff = 0.18

    mask = R > cutoff

    E = np.zeros_like(points)

    E[mask] = (
        k_e
        * q
        * R_vec[mask]
        / R[mask, None]**3
    )

    return E, mask


# Field produced by each charge
E1, mask1 = electric_field(source1, points,q1)
E2, mask2 = electric_field(source2, points,q2)


# Keep points that are away from BOTH charges
mask = mask1 & mask2


# Superposition
E = E1 + E2


# Magnitude
E_mag = np.linalg.norm(E, axis=1)


# Direction
E_dir = np.zeros_like(E)

nonzero = E_mag > 0

E_dir[nonzero] = (
    E[nonzero]
    / E_mag[nonzero, None]
)


# Apply the mask only here
plot_points = points[mask]
plot_E = E[mask]
plot_E_mag = E_mag[mask]
plot_E_dir = E_dir[mask]


# PyVista dataset
cloud = pv.PolyData(plot_points)

cloud["E"] = plot_E
cloud["E_mag"] = plot_E_mag
cloud["E_dir"] = plot_E_dir


# Glyph arrows
arrows = cloud.glyph(
    orient="E_dir",
    scale=False,
    factor=0.12,
)


# Visualization
plotter = pv.Plotter()

plotter.add_mesh(
    arrows,
    color="black"
)


# First charge
sphere1 = pv.Sphere(
    radius=0.08,
    center=source1
)

plotter.add_mesh(
    sphere1,
    color="red"
)


# Second charge
sphere2 = pv.Sphere(
    radius=0.08,
    center=source2
)

plotter.add_mesh(
    sphere2,
    color="blue"
)


plotter.add_axes()
plotter.show_grid()
plotter.show()
"""