import json
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# Mapping of codes to addresses and corresponding numeric codes
address_mapping = {
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
    # Extracting the first polygon's coordinates
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

# Get all .ehr.json files in the ehr_files directory
json_files = glob.glob(os.path.join("ehr_files", "*.ehr.json"))

for json_file in json_files:
    try:
        # Load polygon coordinates from JSON file
        polygon_coords = load_polygon_from_json(json_file)



        # Extract building code from filename
        building_code = os.path.basename(json_file).replace('.ehr.json', '')
        code, address = address_mapping.get(building_code, ("000", "Unknown Address"))

        print(f"Processing {json_file} for {building_code} {code} at {address}")
        #print(f"Loaded polygon coordinates: {polygon_coords}", len(polygon_coords))
        # Calculate the angle needed to rotate the polygon
        angle = angle_to_rotate_polygon(polygon_coords)

        # Choose the first vertex of the longest edge as the origin for rotation
        origin = polygon_coords[0]

        # Rotate the polygon
        rotated_polygon_coords = [rotate_point(origin, point, angle) for point in polygon_coords]

        # Transform the rotated polygon so the minimums for both axes are 0
        min_x_rotated = min(coord[0] for coord in rotated_polygon_coords)
        min_y_rotated = min(coord[1] for coord in rotated_polygon_coords)
        transformed_rotated_coords = [[x - min_x_rotated, y - min_y_rotated] for x, y in rotated_polygon_coords]


        # Plotting the transformed and rotated polygon
        x_transformed_rotated, y_transformed_rotated = zip(*transformed_rotated_coords)


        print(f"Rotated polygon by transformed_rotated_coords {x_transformed_rotated} {y_transformed_rotated}")

        plt.figure()
        plt.fill(x_transformed_rotated, y_transformed_rotated, 'b', alpha=0.5)
        plt.plot(x_transformed_rotated, y_transformed_rotated, 'r-')
        plt.title(f"Top-down view of EHR: {building_code} Grp: {code} Address: {address}")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True)
        plt.axis('equal')
        
        # Save plot as JPEG with address annotation
        output_filename = f"{building_code}_{code}.jpg"
        
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Error processing {json_file}: {e}")
