import numpy as np
import cv2

def reorder_contour(contour, start_idx, finish_idx):
    if start_idx < finish_idx:
        return contour[start_idx:finish_idx + 1]
    else:
        return np.concatenate((contour[start_idx:], contour[:finish_idx + 1]))

def calculate_arc_lengths(contour):
    distances = [0.0]
    for i in range(len(contour) - 1):
        p1 = contour[i][0]
        p2 = contour[i + 1][0]
        dist = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        distances.append(distances[-1] + dist)
    return np.array(distances)

def sample_contour_by_arc_length(contour, num_samples):
    if len(contour) < 2 or num_samples <= 1:
        return [tuple(map(int, p[0])) for p in contour]
    arc_lengths = calculate_arc_lengths(contour)
    total_length = arc_lengths[-1]
    target_distances = np.linspace(0, total_length, num_samples)
    sampled_points = []
    current_length = 0.0
    contour_index = 0
    for target_dist in target_distances:
        if target_dist == 0:
            sampled_points.append(tuple(map(int, contour[0][0])))
            continue
        while contour_index < len(contour) - 1:
            p1 = contour[contour_index][0]
            p2 = contour[contour_index + 1][0]
            segment_length = np.linalg.norm(np.array(p2) - np.array(p1))
            if current_length + segment_length >= target_dist:
                alpha = (target_dist - current_length) / segment_length
                interp_x = int(p1[0] + alpha * (p2[0] - p1[0]))
                interp_y = int(p1[1] + alpha * (p2[1] - p1[1]))
                sampled_points.append((interp_x, interp_y))
                break
            else:
                current_length += segment_length
                contour_index += 1
        else:
            sampled_points.append(tuple(map(int, contour[-1][0])))
    return sampled_points
