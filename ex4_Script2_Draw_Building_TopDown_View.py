import json
import numpy as np
import os
import pandas as pd
from shapely.geometry import Polygon

# Use mapping to iterate in order and write group and address on jpegs
buildings_map = {
    "121363179": ("222", "Pärnu Rääma tn 9"),
    "121363182": ("222", "Pärnu Rääma tn 9a"),
    "121363185": ("222", "Pärnu Rääma tn 11"),
    "103014811": ("223", "Pärnu Mai 39"),
    "103015648": ("223", "Pärnu Mai 45"),
    "103015786": ("223", "Pärnu Mai 43"),
    "104018086": ("224", "Tartu Mõisavahe 35"),
    "104018376": ("224", "Tartu Mõisavahe 38"),
    "104023804": ("224", "Tartu Mõisavahe 42"),
    "104018213": ("225", "Tartu Mõisavahe 43"),
    "104019313": ("225", "Tartu Mõisavahe 47"),
    "104036004": ("225", "Tartu Mõisavahe 39")
}

# Function to load polygon coordinates from a JSON file
def load_polygon_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[0]["ehitis"]["ehitiseKujud"]["ruumikuju"][0]["geometry"]["coordinates"][0]

# Function to rotate a point around another point
def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return [qx, qy]

# Function to calculate the angle to rotate the polygon
def angle_to_rotate_polygon(coords):
    max_length = 0
    angle_of_longest_edge = 0
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        length = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        if length > max_length:
            max_length = length
            angle_of_longest_edge = np.arctan2((p2[1] - p1[1]), (p2[0] - p1[0]))
    return -angle_of_longest_edge

# Function to calculate centroid, area, perimeter
def calculate_polygon_properties(coords):
    polygon = Polygon(coords)
    centroid = polygon.centroid.coords[0]
    area = polygon.area
    perimeter = polygon.length
    return centroid, area, perimeter, len(coords)

# Function to perform Min-Max normalization
def normalize_minmax(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    return (data - min_vals) / (max_vals - min_vals)

# Function to compute Euclidean distance
def calculate_euclidean_distances(matrix):
    size = len(matrix)
    dist_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dist_matrix[i, j] = np.sqrt(np.sum((matrix[i] - matrix[j])**2))
    return dist_matrix

polygon_data = []
ehr_codes = buildings_map.keys()
for building_code in ehr_codes:
    try:
        json_file = f"ehr_files/{building_code}.ehr.json"
        if not os.path.exists(json_file):
            continue
        
        polygon_coords = load_polygon_from_json(json_file)
        code, address = buildings_map[building_code]
        print(f"Processing {json_file} for {building_code} {code} at {address}")
        
        angle = angle_to_rotate_polygon(polygon_coords)
        origin = polygon_coords[0]
        rotated_polygon_coords = [rotate_point(origin, point, angle) for point in polygon_coords]
        
        min_x_rotated = min(coord[0] for coord in rotated_polygon_coords)
        min_y_rotated = min(coord[1] for coord in rotated_polygon_coords)
        transformed_rotated_coords = [[x - min_x_rotated, y - min_y_rotated] for x, y in rotated_polygon_coords]
        
        print(f"Coordinates: {transformed_rotated_coords}")
        centroid, area, perimeter, num_vertices = calculate_polygon_properties(transformed_rotated_coords)
        print(f"Centroid: {centroid}, Area: {area}, Perimeter: {perimeter}, Nof Vertices: {num_vertices}")
        
        polygon_data.append([centroid[0], centroid[1], area, perimeter, num_vertices])
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

# Normalize data using Min-Max Scaling
normalized_data = normalize_minmax(np.array(polygon_data))

# calculate Euclidean Distance Matrix
distance_matrix = calculate_euclidean_distances(normalized_data)

# Reorder results based on buildings_map
distance_df = pd.DataFrame(distance_matrix, index=ehr_codes, columns=ehr_codes)
distance_df = distance_df.loc[ehr_codes, ehr_codes]
distance_df = distance_df.reindex(index=ehr_codes, columns=ehr_codes)

# print Euclidean Distance Matrix to console
print("\nEuclidean Distance Matrix:")
print(distance_df.to_csv(index=True))