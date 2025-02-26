def load_data(file_path):
    data = []
    headers = []
    filenames = []
    with open(file_path, 'r') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            values = line.strip().split(',')
            filenames.append(values[0])  # Store filename as identifier
            row = []
            for i, val in enumerate(values[1:]):  # Exclude filename from numerical data
                if headers[i + 1] == "energiaKlass":
                    row.append({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}.get(val, 0))
                else:
                    try:
                        row.append(float(val))
                    except ValueError:
                        row.append(0.0)
            data.append(row)
    return filenames, headers, data

def minmax_normalization(data, filenames, headers):
    num_features = len(data[0])
    min_vals = [min(row[i] for row in data) for i in range(num_features)]
    max_vals = [max(row[i] for row in data) for i in range(num_features)]
    
    normalized_data = []
    for i, row in enumerate(data):
        normalized_row = [filenames[i]]
        for j in range(num_features):
            if max_vals[j] - min_vals[j] == 0:
                normalized_row.append(0.0)  # Avoid division by zero
            else:
                normalized_value = (row[j] - min_vals[j]) / (max_vals[j] - min_vals[j])
                normalized_row.append(normalized_value)
        normalized_data.append(normalized_row)
    
    return [headers] + normalized_data

def calculate_euclidean_distance_matrix(data, filenames):
    num_rows = len(data)
    distance_matrix = [[0.0] * num_rows for _ in range(num_rows)]
    
    for i in range(num_rows):
        for j in range(num_rows):
            distance_matrix[i][j] = (sum((data[i][k] - data[j][k]) ** 2 for k in range(1, len(data[i])))) ** 0.5
    
    return [["filename"] + filenames] + [[filenames[i]] + distance_matrix[i] for i in range(num_rows)]

def print_matrix(matrix):
    for row in matrix:
        print(",".join(map(str, row)))

# Example usage
if __name__ == "__main__":
    file_path = "ehr_files/output.csv"  # Replace with actual file path
    filenames, headers, data = load_data(file_path)
    
    print("Min-Max Normalized Data Matrix:")
    normalized_data = minmax_normalization(data, filenames, ["filename"] + headers)
    print_matrix(normalized_data)
    
    print("\nEuclidean Distance Matrix:")
    distance_matrix = calculate_euclidean_distance_matrix(normalized_data[1:], filenames)
    print_matrix(distance_matrix)
