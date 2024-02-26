import csv
from sklearn.preprocessing import MinMaxScaler

def read_csv_as_list(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            numeric_row = []
            for item in row:
                try:
                    numeric_row.append(float(item))  # Convert each item to float
                except ValueError:
                    numeric_row.append(item)  # If conversion fails, keep it as it is
            data.append(numeric_row)
    scaler = MinMaxScaler(feature_range=(0, 4))  # Scale to range from 0 to 4
    scaled_data = scaler.fit_transform(data)

    return scaled_data

# Writing to CSV
def write_list_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)
    print(f'CSV file "{filename}" has been created successfully.')
