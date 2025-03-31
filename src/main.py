import datetime
from models.hash_table import HashTable
from models.truck import Truck
from logic.data_loader import load_packages, load_csv_files
from logic.routing import deliver_packages
from interface import DeliveryInterface

# Load CSV data
address_data, distance_data = load_csv_files()

# Initialize hash table and load packages
package_table = HashTable()
load_packages("data/packages.csv", package_table)

# Define trucks with departure times and package IDs
truck1 = Truck(departure_time=datetime.timedelta(hours=8), packages=[1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Truck(departure_time=datetime.timedelta(hours=10, minutes=20), packages=[2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Truck(departure_time=datetime.timedelta(hours=9, minutes=5), packages=[6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])

# Run deliveries
deliver_packages(truck1, package_table, address_data, distance_data)
deliver_packages(truck2, package_table, address_data, distance_data)
truck3.departure_time = min(truck1.time, truck2.time)
truck3.time = truck3.departure_time
deliver_packages(truck3, package_table, address_data, distance_data)

# Start CLI
if __name__ == "__main__":
    DeliveryInterface(package_table, truck1, truck2, truck3)
