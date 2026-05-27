from manim import *
import numpy as np

class Electric_Field(Scene):
    def construct(self):
        q1 = +1
        q2 = -1
        r0_1 = np.array([-1, 0, 0])
        r0_2 = np.array([1,0,0])
        tint_1 = RED if q1 > 0 else BLUE
        tint_2 = RED if q2 >0 else BLUE
        charge_1 = Dot(r0_1, radius=0.12, color = tint_1)
        charge_2 = Dot(r0_2, radius = 0.12, color = tint_2)
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.5}
        )

        def E(point):
            r1 = point - r0_1
            r2 = point - r0_2
            d1 = np.linalg.norm(r1)
            d2 = np.linalg.norm(r2)

            #Condizipne grafica solo per non far entrare i vettori nelle cariche
            if d1 < 0.25 or d2 < 0.55:
                return np.array([0, 0, 0])

            
            k = 1/ (4 * np.pi * 8.85e-12)
            E1 = k*q1 * r1/ d1**3
            E2 = k*q2 * r2/ d2**3
            E_tot = E1 + E2

            #Graficamente per visualizzare meglio i vettori: 
            visualize_E_tot = E_tot/k
            
            return visualize_E_tot 

        field = ArrowVectorField(
            E,
            x_range=[-5, 5, 0.25],
            y_range=[-5, 5, 0.25],
        )

        self.add(plane)
        self.play(FadeIn(charge_1), FadeIn(charge_2))
        self.play(Create(field))
        self.wait(10)

