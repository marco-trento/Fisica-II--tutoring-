import numpy as np
import pyvista as pv

q = 1.6e-19  # Charge of a proton in Coulombs
m = 1.67e-27  # Mass of a proton in kg


#Capacitor
E0 = 2.0e3 #Electric field in N/C
d = 0.020 #distance between plates in m
plate_lenght = 0.04 #plate lenght along x


#Electric field considering positive plate above
E = np.array([0.0, -E0, 0.0])

r0=np.array([0.0, 0.0, 0.0]) #Initial position of the proton

v0=np.array([2e5,0.0,0.0]) #Initial velocity of the proton



#Calculate the acceleration of the proton
a = (q/m)*E

print("L'accelerazione del protone è:", a)
#The trajectory is a parabola!

t_end = plate_lenght/v0[0]
print("Tempo di volo del protone:", t_end)

times = np.linspace(0, t_end, 201)

r_exact = r0[None,:]+ times[:,None]*v0[None,:] + 0.5*times[:,None]**2*a[None,:]

plate_width = 0.018
plate_thickness = 0.0001

plate_center_x = plate_lenght/2

top_plate = pv.Cube(center=(plate_center_x, d/2, 0), x_length=plate_lenght, y_length=plate_thickness, z_length=plate_width)
bottom_plate = pv.Cube(center=(plate_center_x, -d/2, 0), x_length=plate_lenght, y_length=plate_thickness, z_length=plate_width)

xf = np.linspace(0.003, plate_lenght-0.003, 7)
yf = np.linspace(-0.006,0.006, 3)
XF, YF = np.meshgrid(xf, yf,indexing='ij')

field_points = np.column_stack((XF.ravel(), YF.ravel(), np.zeros(XF.size)))
E_direction = E/np.linalg.norm(E)
field_vectors = np.tile(E_direction, (field_points.shape[0], 1))
field_cloud = pv.PolyData(field_points)
field_cloud["E_dir"]= field_vectors
field_arrows = field_cloud.glyph(orient="E_dir", scale=False, factor=0.0025)

trajectory_exact = pv.MultipleLines(r_exact)

plotter = pv.Plotter()

plotter.add_mesh(
    top_plate,
    color="red"
)

plotter.add_mesh(
    bottom_plate,
    color="blue"
)

plotter.add_mesh(
    field_arrows,
    color="black"
)

plotter.add_mesh(
    trajectory_exact,
    color="orange",
    line_width=4
)

particle = pv.Sphere(
    radius=0.0006
)

particle_actor = plotter.add_mesh(
    particle,
    color="black"
)

particle_actor.position = r_exact[0]


def callback(step):

    i = min(
        step,
        len(r_exact) - 1
    )

    particle_actor.position = (
        r_exact[i]
    )

    plotter.render()


plotter.add_timer_event(
    max_steps=len(r_exact),
    duration=25,
    callback=callback
)

plotter.add_axes()
plotter.view_xy()

plotter.show()
