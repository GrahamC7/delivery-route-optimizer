import datetime

from .helpers import get_address_index, get_distance


def deliver_packages(truck, package_table, address_data, distance_data):
    undelivered = [package_table.search(pid) for pid in truck.packages]
    truck.packages.clear()

    while undelivered:
        closest_package = None
        shortest_distance = float("inf")

        for package in undelivered:
            current_index = get_address_index(truck.current_location, address_data)
            package_index = get_address_index(package.address, address_data)
            if current_index is None or package_index is None:
                continue

            distance = get_distance(current_index, package_index, distance_data)

            if distance < shortest_distance:
                closest_package = package
                shortest_distance = distance

        if closest_package:
            truck.packages.append(closest_package.package_id)
            undelivered.remove(closest_package)
            truck.miles += shortest_distance
            truck.current_location = closest_package.address
            truck.time += datetime.timedelta(hours=shortest_distance / truck.speed)

            closest_package.departure_time = truck.departure_time
            closest_package.delivery_time = truck.time
