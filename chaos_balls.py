from manim import *
from manim.opengl import *

def get_free_fall_traj_bounded_by_circle(init_pos, init_velo, time=8, radius=1):
    traj = init_pos
    pos = init_pos
    dt = 0.0001
    t = 0
    full_t = 0
    while full_t <= time:
        while np.dot(pos, pos) < radius:
            pos = t**2 * np.array([0, -(1/2)*9.81, 0]) + t * init_velo + init_pos
            traj = np.vstack([traj, pos])
            t += dt
        
        traj = np.delete(traj, -1, axis=0)
        pos = traj[-1]

        init_pos = pos
        end_velo = 2 * t * np.array([0, -(1/2)*9.81, 0]) + init_velo
        init_velo = end_velo - (  2/(radius**2) ) * np.dot(end_velo, pos) * pos

        full_t += t
        t = 0

    return traj

pos_0 = np.array([0.001, 0.5, 0])
vel_0 = np.array([0, 0, 0])
tra_1 = get_free_fall_traj_bounded_by_circle(pos_0, vel_0)
print(len(tra_1))

pos_1 = np.array([0.0012, 0.5, 0])
vel_1 = np.array([0, 0, 0])
tra_2 = get_free_fall_traj_bounded_by_circle(pos_1, vel_1)
tra_2 = np.delete(tra_2, np.arange(len(tra_1), len(tra_2), 1), axis=0)
print(len(tra_2))

diff =  tra_2 - tra_1
distance = np.linalg.norm(diff, axis=1)
print(len(distance))

time_arr = np.linspace(0,12,len(distance))
aux_0 = np.zeros(len(distance))
graph_points = np.stack((time_arr, distance, aux_0),axis=1)



class TwoObjectsFalling(Scene):
    def construct(self):
        ball_1 = OpenGLCircle(radius=0.1).move_to(np.array([0.001, 0.5, 0]))
        ball_2 = Circle(radius=0.1)

        boundary = OpenGLCircle(radius=1).set_color(WHITE)

        path_1 = OpenGLVMobject()
        path_1.set_points_as_corners(tra_1)
        path_1.set_stroke(color=ORANGE, width=2, opacity=0.8)

        path_2 = OpenGLVMobject()
        path_2.set_points_as_corners(tra_2)
        path_2.set_stroke(color=BLUE, width=2, opacity=0.8)

        graph = OpenGLVMobject()
        graph.set_points_as_corners(graph_points)
        graph.set_stroke(color=GREEN, width=3, opacity=0.8)
        graph.to_edge(DOWN).shift(LEFT*6)

        group = OpenGLVGroup(path_1, path_2, boundary).scale(3)
        boundary.scale(1.01)
        group.to_edge(UP)

        line = OpenGLLine(ORIGIN, 2*UP).to_edge(DOWN).shift(LEFT*6).set_color(GREEN)
        label_0 = Text("2").scale(0.7).next_to(line.get_end(), LEFT).set_color(GREEN)
        label_1 = Text("0").scale(0.7).next_to(line.get_start(), LEFT).set_color(GREEN)
        text_0 = Text("Distance").scale(0.7).next_to(line, RIGHT).set_color(GREEN)
        text_1 = Text("Radius = 1").scale(0.7).to_edge(LEFT)

        twit_blue = "#1DA1F2"
        name = Text("@Photon_Sphere").scale(0.54).to_edge(UR, buff=0.3)
        twit = SVGMobject("/Users/O.Schoen/Desktop/Stuff/Manim/community/project/images/Logos/SVG/photon_sphere-01.svg",fill_opacity=0,stroke_width=2).set_color(twit_blue).scale(0.2).next_to(name, LEFT, buff=0.3)


        self.play(
            Create(boundary),
            Create(line),
            Write(label_0),
            Write(label_1),
            Write(text_0),
            Write(text_1),
            Create(twit),
            Write(name)
        )
        self.wait()

        self.play(
            Create(path_1),
            Create(path_2),
            Create(graph),
            rate_func = linear,
            run_time = 15,
        )
        self.wait()


