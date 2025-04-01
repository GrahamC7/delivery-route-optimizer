import csv
import os.path

from jupyter_server.transutils import base_dir

from models.package import Package


def load_packages(filename, package_table):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            package = Package(
                package_id=int(row[0]),
                address=row[1],
                city=row[2],
                state=row[3],
                zip_code=row[4],
                delivery_deadline=row[5],
                weight_kg=row[6]
            )
            package_table.insert(package.package_id, package)


def load_csv_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")

    address_path = os.path.join(data_dir, "address.csv")
    distance_path = os.path.join(data_dir, "distance.csv")

    with open("data/address.csv") as address_file:
        address_data = list(csv.reader(address_file))
    with open("data/distance.csv") as distance_file:
        distance_data = list(csv.reader(distance_file))

    return address_data, distance_data
