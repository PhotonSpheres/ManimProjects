from manim import *
from manim.opengl import *

# Scene only works with the flag --renderer=opengl
# not yet implemented for Jupyter

class SurfaceExample(Scene):
    def construct(self):
        torus1 = Torus(major_radius=1, minor_radius=1)
        torus2 = Torus(major_radius=3, minor_radius=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)

        # Change those paths accordingly
        night_texture = "/The_earth_at_night.jpg"
        day_texture = "/Whole_world_-_land_and_oceans.jpg"

        surfaces = [
            OpenGLTexturedSurface(surface, day_texture, night_texture) for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.mesh = OpenGLSurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)
        surface = surfaces[0]

        frame = self.renderer.camera
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        self.play(
            FadeIn(surface),
            Create(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)

        self.play(
            Rotate(surface, PI / 2),
            run_time=2
        )
        
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=3,
        )
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.wait(33)