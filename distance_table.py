import csv
from pathlib import Path

# Helper class for containing data for a neighbor
class Neighbor:
    def __init__(self, name: str, address: str, distance: float):
        self.name = name
        self.address = address
        self.distance = distance

# Helper class for containing data for a hub
class Hub:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.address2 = None
        self.neighbors = []

# Class for organizing distance table data
class DistanceTable:
    def __init__(self, csv_file="task_files/wgups_distance_table.csv"):
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        self.hubs = []
        self.build_table()

    # Parse data from table and return 2D list
    def parse_distance_table(self):
        with open(self.csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            start_loading_data = False
            parsed_table = []

            for row in reader:
                if "DISTANCE BETWEEN HUBS IN MILES" in row:
                    start_loading_data = True

                if start_loading_data:
                    parsed_table.append(row)       
        return parsed_table

    # Restructure data (list of hubs each containing a list of neighbors)
    def build_table(self):
        # Table 28x29, 1-27 = 2-28
        parsed_table = self.parse_distance_table()

        top_row = parsed_table[0]
        for h, row in enumerate(parsed_table):
            if h == 0:
                continue
            split_field = row[0].split("\n")
            hub_name = split_field[0]
            hub_address = split_field[1]
            current_hub = Hub(hub_name, hub_address)
            current_hub.address2 = row[1]
            #print(f"Hub: {hub_name}\nHub Address: {hub_address}\n---")
            for i, column in enumerate(row):
                if i < 2:
                    continue
                else:
                    neighbor_split = top_row[i].split("\n")
                    neighbor_name = neighbor_split[0]
                    neighbor_address = neighbor_split[1]
                    if column:
                        neighbor_distance = column
                    else:
                        neighbor_distance = float(parsed_table[i - 1][h + 1])          
                    #print(f"Neighbor: {neighbor_name}\nAddress: {neighbor_address}\nDistance: {neighbor_distance}mi\n---")
                    neighbor = Neighbor(neighbor_name, neighbor_address, neighbor_distance)
                    current_hub.neighbors.append(neighbor)
            self.hubs.append(current_hub)
                    
distance_table = DistanceTable()
print(len(distance_table.hubs))