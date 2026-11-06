import numpy as np
import pyvista as pv
print("PyVista version:", pv.__version__)
print("NumPy version:", np.__version__)

#sphere = pv.Sphere()
#sphere.plot()


L = 2
n = 7
x = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
#distance = np.linalg.norm(points, axis=1)

def radius_from_origin(points):
    return np.linalg.norm(points, axis=1)

radius = radius_from_origin(points)

cloud = pv.PolyData(points)


cloud.point_data['radius'] = radius

plotter = pv.Plotter()
plotter.add_mesh(cloud, scalars='radius', cmap='viridis', point_size=10)
plotter.show()


