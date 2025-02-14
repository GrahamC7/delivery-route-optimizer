# Author: Graham Cockerham
# Student ID: 001146093
import csv
import datetime

# loading address.csv file
with open("CSV_Files/address.csv") as addressCSV:
    AddressCSV = csv.reader(addressCSV)
    AddressCSV = list(AddressCSV)

# loading distance.csv file
with open("CSV_Files/distance.csv") as distanceCSV:
    DistanceCSV = csv.reader(distanceCSV)
    DistanceCSV = list(DistanceCSV)

# loading packages.csv file
with open("CSV_Files/packages.csv") as packagesCSV:
    PackagesCSV = csv.reader(packagesCSV)
    PackagesCSV = list(PackagesCSV)


# creation of hash table
class HashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

        # inserting new item into hash table

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # updating existing keys in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                # printing key value
                return True

        # inserting item into the end of the list if it does not already exist
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

        # searching hash table for item that matches the key

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # if item is found
        return None  # if item is not found

        # removal of item from hash table

    def hash_remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # removal of item that matches hash table key
        if key in bucket_list:
            bucket_list.remove(key)


# creation of PackageFunction class - stores information about the packages
class PackageFunction:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight_kgs, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight_kgs = weight_kgs
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip_code, self.delivery_deadline,
            self.weight_kgs,
            self.status, self.delivery_time)

    # package status updates based on time of entry
    def update_status(self, time_change):
        if self.delivery_time == None:
            self.status = "At WGUPS Hub"
        elif time_change < self.departure_time:
            self.status = "At WGUPS Hub"
        elif time_change < self.delivery_time:
            self.status = "On the way"
        else:
            self.status = "Delivered"
        if time_change > datetime.timedelta(hours=10, minutes=20):
            self.address = "410 S State St"
            self.zip_code = "84111"
        else:
            self.address = "300 State St"
            self.zip_code = "84103"


# loading packages infor from csv file to insert into hash table
def load_packages(filename, packages_hash):
    with open(filename) as packages_info:
        packages_data = csv.reader(packages_info, delimiter=',')
        next(packages_data)
        for package in packages_data:
            # print statements for specific information associated with individual packages
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip_code = package[4]
            package_delivery_deadline = package[5]
            package_weight_kgs = package[6]
            package_notes = package[7]
            package_status = "At WGUPS Hub"
            package_departure_time = None
            package_delivery_time = None

            # inserting package information into hash table
            package = PackageFunction(package_id, package_address, package_city, package_state, package_zip_code,
                                      package_delivery_deadline, package_weight_kgs, package_status)

            # printing package variable
            packages_hash.insert(package_id, package)


# creating hash table
package_hash = HashTable()


# finding the shortest distance to next delivery address
def address(address_main):
    for row in AddressCSV:
        if address_main in row[2]:
            return int(row[0])


# comparing distance between two addresses
def between_address(address1, address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)


def address_info(address_main):
    for row in AddressCSV:
        if address_main in row[2]:
            return int(row[0])


load_packages("CSV_Files/packages.csv", package_hash)


# creating class for delivery trucks
class Trucks:
    def __init__(self, speed, miles, current_location, departure_time, packages):
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.departure_time = departure_time
        self.time = departure_time
        self.packages = packages  # Correctly assign packages as a list

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.speed, self.miles, self.current_location, self.departure_time, self.time, self.packages)


# manually loading the trucks and assigning them a departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])


# nearest neighbor method implementation for package delivery
def package_delivery(truck):
    # array for packages not yet delivered
    not_delivered = []
    for package_id in truck.packages:
        package = package_hash.search(package_id)
        not_delivered.append(package)

    # clearing package list to load packages in trucks using nearest neighbor algorithm
    truck.packages.clear()

    # cycles list of packages not yet delivered until all packages are assigned
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if package.package_id in [25, 6]:
                next_package = package
                next_address = between_address(address_info(truck.current_location), address_info(package.address))
                break
            if between_address(address_info(truck.current_location), address_info(package.address)) <= next_address:
                next_address = between_address(address_info(truck.current_location), address_info(package.address))
                next_package = package
        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.miles += next_address
        truck.current_location = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time


# commencing delivery of packages via trucks
package_delivery(truck1)
package_delivery(truck2)
truck3.departure_time = min(truck1.time,
                            truck2.time)  # truck 3 will not leave WGUPS until truck1 or truck2 have returned - there are only 2 drivers
package_delivery(truck3)

# user interface
print("WGUPS - Western Governors University Parcel Service")
# showing total mileage driven by the 3 trucks
print("Total mileage driven is: ", truck1.miles + truck2.miles + truck3.miles)

while True:
    # printing combined mileage for the 3 trucks
    time_request = input("To see a time status update of each package, enter the time in HH:MM format.")

    # input format validation
    if ":" not in time_request:
        print("Invalid time format. Please use HH:MM format.")
        continue  # Prompt again

    try:
        (h, m) = time_request.split(":")
        timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    except ValueError:
        print("Invalid time format. Make sure to use numeric values in HH:MM format.")
        continue  # Prompt again

    try:
        user_entry = [int(input("Enter package ID."))]
    except ValueError:
        user_entry = range(1, 41)

    for package_id in user_entry:
        package = package_hash.search(package_id)
        if package is not None:  # only updating status if the package exists
            package.update_status(timeChange)
            print(str(package))
        else:
            print(f"Package ID {package_id} not found in the hash table.")
