from manim import *
import numpy as np

class Electric_Field(Scene):
    def construct(self):
        q = +1
        r0 = np.array([0, 0, 0])
        tint = RED if q > 0 else BLUE

        charge = Dot(r0, radius=0.12, color=tint)

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.5}
        )

        def E(point):
            r = point - r0
            d = np.linalg.norm(r)

            if d < 0.25:
                return np.array([0, 0, 0])

            direction = r / d
            k = 1/ (4 * np.pi * 8.85e-12)
            magnitude = k * abs(q) / d**2
            visualizeble_magnitude = 2 * np.tanh(magnitude/k)
            return np.sign(q) * visualizeble_magnitude * direction

        field = ArrowVectorField(
            E,
            x_range=[-5, 5, 0.5],
            y_range=[-5, 5, 0.5],
        )

        self.add(plane)
        self.play(FadeIn(charge))
        self.play(Create(field))
        self.wait(10)

