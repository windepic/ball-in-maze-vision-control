"""
Note: This module was NOT developed by me personally.
It is included here solely for completeness of the project.
"""

import pyvista as pv
import numpy as np

class MazeVisualizer3D:
    def __init__(self, model_path="maze.stl"):
        pv.global_theme.allow_empty_mesh = True
        self.plotter = pv.Plotter()
        self.plotter.window_size = [600, 400]
        self.model = pv.read(model_path)
        rotate_y = pv.transformations.axis_angle_rotation([0, 1, 0], 90)
        self.model.transform(rotate_y, inplace=True)

        self.maze_actor = self.plotter.add_mesh(self.model.copy(), opacity=0.3, color="#FFDB58")
        self.ball_actor = self.plotter.add_mesh(pv.Sphere(radius=4, center=(0, 0, 0)), color="silver")
        self.trail_points = []
        self.trail_actor = self.plotter.add_mesh(pv.PolyData(), color="red", line_width=2)

        center = self.model.center
        self.plotter.camera.position = (center[0]-400, center[1]+400, center[2]-300)
        self.plotter.camera.focal_point = center
        self.plotter.camera.up = (0, 0, 1)

        self.plotter.open_movie("maze_3d_animation.mp4", framerate=30)
        self.plotter.show(auto_close=False, interactive_update=True)

    def rotate_about_center(self, axis, angle_degrees):
        center = self.model.center
        t1 = np.eye(4); t1[:3, 3] = -np.array(center)
        r = pv.transformations.axis_angle_rotation(axis, np.deg2rad(angle_degrees))
        t2 = np.eye(4); t2[:3, 3] = np.array(center)
        return t2 @ r @ t1

    def update(self, angle_x, angle_y, ball_coor):
        rot_x = self.rotate_about_center([1, 0, 0], angle_x)
        rot_y = self.rotate_about_center([0, 0, 1], angle_y)
        transformed = self.model.copy()
        transformed.transform(rot_x @ rot_y)
        self.maze_actor.mapper.SetInputData(transformed)

        ball_x = ball_coor[0]*(237/640)
        ball_y = ball_coor[1]*(188/480)
        pos = (-ball_x, 0.5, 178 - ball_y)
        new_ball = pv.Sphere(radius=4.5, center=pos)
        self.ball_actor.mapper.SetInputData(new_ball)

        self.trail_points.append(pos)
        if len(self.trail_points) > 1:
            line = pv.lines_from_points(self.trail_points)
            self.trail_actor.mapper.SetInputData(line)

        self.plotter.update()
        self.plotter.render()
        self.plotter.write_frame()
