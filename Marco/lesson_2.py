import numpy as np

#Step 1:
#One charge and calculate the potential at 1 point

k_e = 8.99e9
Q = 1e-9 #1nC

source = np.array([0, 0, 0])
point = np.array([1, 0, 0])

R_vec = point - source
R_mag = np.linalg.norm(R_vec)

V = k_e * Q / R_mag
print("R_vec:", R_vec)
print("R_mag:", R_mag)
print("Potential at point:", V)

#Step 2:
#We can reuse the discretization from lesson 1 to evaluate the potential on a whole 3D grid

L = 2.0
n = 21

x = np.linspace(-L, L, n)
X, Y, Z = np.meshgrid(x,x,x, indexing='ij')
points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

#Again you can show the shape of these variables
print("X shape:", X.shape)
print("points shape:", points.shape)

R_vec = points - source
R_mag = np.linalg.norm(R_vec, axis=1)
#In order to calculate the potential, we need to avoid division by zero, therefore...

cutoff = 0.18
mask = R_mag>cutoff
V = np.zeros_like(R_mag)
V[mask] = k_e * Q / R_mag[mask]

print(V.shape) #V[i] is the potential at point i

# At this point in the lesson I would put the lines above in a function to make the code reusable. 

#def electric_potential(source, Q, points, cutoff):
#    ...
#    return V, mask

#Now we can take two charges (dipole)

a = 0.6
source1 = np.array([-a, 0, 0])
source2 = np.array([a, 0, 0])
V1, mask1 = electric_potential(source1, Q, points, cutoff)
V2, mask2 = electric_potential(source2, -Q, points, cutoff)
V = V1+V2
mask = mask1 & mask2

#Now the potential must be reshaped to the 3D grid shape for visualization

V_grid = V.reshape(X.shape)     #V_grid[i,j,k] is the potential at (X[i,j,k], Y[i,j,k], Z[i,j,k])
print("V shape:", V.shape)
print("V_grid shape:", V_grid.shape)

#E = -grad(V)
dx = x[1]-x[0] # for L = 2 and n = 21 dx = 0.2
dV_dx, dV_dy, dV_dz = np.gradient(V_grid, dx, dx,dx)

#Maybe it could be useful to explain the students what np.gradient does.
#We can explicit verify that dV_dx = V_grid[i-1,j,k] - V_grid[i+1,j,k] / 2dx, etc.
Ex_grid = -dV_dx
Ey_grid = -dV_dy
Ez_grid = -dV_dz

E_numerical = np.column_stack((Ex_grid.ravel(), Ey_grid.ravel(), Ez_grid.ravel())) #it has dimension (n**3, 3)


#Now we can bring PyVista in

import pyvista as pv

grid = pv.ImageData(dimensions=(n,n,n), spacing = (dx,dx,dx), origin=(-L,-L,-L))
grid.point_data['V'] = V_grid.flatten(order='F') #PyVista uses Fortran order for the data

slice_xy = grid.slice(normal='z', origin=(0,0,0))

plotter = pv.Plotter()
plotter.add_mesh(slice_xy, scalars='V', show_scalar_bar=True)
plotter.add_axes()
plotter.show_grid()
plotter.show()

