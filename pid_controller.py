"""
Note: This module was NOT developed by me personally.
It is included here solely for the completeness of the project.
"""

import time
import numpy as np

class PIDController:
    def __init__(self, kp=0.45, ki=0.015, kd=0.022, max_i=20, max_d=20, max_tilt_x=4, max_tilt_y=5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_i = max_i
        self.max_d = max_d
        self.max_tilt_x = max_tilt_x
        self.max_tilt_y = max_tilt_y
        self.integral_x = 0
        self.integral_y = 0
        self.prev_error_x = 0
        self.prev_error_y = 0
        self.prev_time = time.time()

    def reset(self):
        self.integral_x = 0
        self.integral_y = 0
        self.prev_error_x = 0
        self.prev_error_y = 0
        self.prev_time = time.time()

    def compute(self, x, y, target_x, target_y, slow_mode=False):
        now = time.time()
        dt = now - self.prev_time
        dt = max(dt, 1e-6)

        error_x = x - target_x
        error_y = y - target_y

        self.integral_x += error_x * dt
        self.integral_y += error_y * dt
        self.integral_x = np.clip(self.integral_x, -self.max_i, self.max_i)
        self.integral_y = np.clip(self.integral_y, -self.max_i, self.max_i)

        if abs(error_x) < 5 and abs(error_y) < 5:
            self.integral_x = 0
            self.integral_y = 0

        derivative_x = (error_x - self.prev_error_x) / dt
        derivative_y = (error_y - self.prev_error_y) / dt
        derivative_x = np.clip(derivative_x, -self.max_d, self.max_d)
        derivative_y = np.clip(derivative_y, -self.max_d, self.max_d)

        gains = (0.15, 0.01, 0.03) if slow_mode else (self.kp, self.ki, self.kd)
        kp, ki, kd = gains

        theta_x = kp * error_x + ki * self.integral_x + kd * derivative_x
        theta_y = kp * error_y + ki * self.integral_y + kd * derivative_y

        theta_x = max(-self.max_tilt_x, min(self.max_tilt_x, theta_x))
        theta_y = max(-self.max_tilt_y, min(self.max_tilt_y, theta_y))

        self.prev_error_x = error_x
        self.prev_error_y = error_y
        self.prev_time = now

        return theta_x, theta_y
