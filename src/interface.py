import datetime

class DeliveryInterface:
    """Command-line interface for interacting with the delivery system."""

    def __init__(self, package_table, truck1, truck2, truck3):
        self.package_table = package_table
        self.trucks = {"1": truck1, "2": truck2, "3": truck3}
        self.menu()

    def menu(self):
        while True:
            print("\n📦 WGUPS Delivery System")
            print("1. View total mileage traveled by all trucks")
            print("2. Check status of a specific package at a given time")
            print("3. Check status of all packages at a given time")
            print("4. Check truck packages at a given time")
            print("5. View assigned packages for each truck")
            print("6. Exit")
            choice = input("Choose an option (1–6): ")

            match choice:
                case "1": self.view_total_mileage()
                case "2": self.check_single_package()
                case "3": self.check_all_packages()
                case "4": self.check_truck_packages()
                case "5": self.show_truck_assignments()
                case "6":
                    print("Exiting. Thank you for using WGUPS!")
                    break
                case _: print("Invalid selection. Please enter a number from 1 to 6.")

    def view_total_mileage(self):
        print("\n🚛 Total Mileage Report")
        total = 0
        for i, truck in self.trucks.items():
            print(f"Truck {i}: {truck.miles:.2f} miles")
            total += truck.miles
        print(f"Total Mileage: {total:.2f} miles")

    def check_single_package(self):
        try:
            package_id = int(input("Enter package ID (1–40): "))
            package = self.package_table.search(package_id)
            if not package:
                print(f"❌ Package {package_id} not found.")
                return
            current_time = self.get_time_input()
            package.update_status(current_time)

            location = (
                package.address if package.status == "Delivered"
                else "On Truck" if package.status == "On the way"
                else "WGUPS Hub"
            )
            delivery_time = (
                (datetime.datetime.min + package.delivery_time).time().strftime('%H:%M')
                if package.delivery_time else "Not Delivered"
            )

            print("\n📦 Package Status")
            print("-" * 30)
            print(f"Package ID   : {package.package_id}")
            print(f"Status       : {package.status}")
            print(f"Location     : {location}")
            print(f"Delivery Time: {delivery_time}")
            print(f"Deadline     : {package.delivery_deadline}")

        except ValueError:
            print("⚠️ Invalid input. Please enter a valid package ID and time (HH:MM).")

    def check_all_packages(self):
        try:
            current_time = self.get_time_input()
            print(f"\n📦 Package Statuses at {str(current_time)}")
            print("=" * 60)

            for package_id in range(1, 41):
                package = self.package_table.search(package_id)
                package.update_status(current_time)

                location = (
                    package.address if package.status == "Delivered"
                    else "On Truck" if package.status == "On the way"
                    else "WGUPS Hub"
                )
                delivery_time = (
                    (datetime.datetime.min + package.delivery_time).time().strftime('%H:%M')
                    if package.delivery_time else "Not Delivered"
                )
                print(
                    f"Package {package_id:02}: {package.status} | Location: {location} | "
                    f"Delivery Time: {delivery_time} | Deadline: {package.delivery_deadline}"
                )

        except ValueError:
            print("⚠️ Invalid time format. Please enter as HH:MM.")

    def check_truck_packages(self):
        try:
            truck_choice = input("Enter truck number (1, 2, or 3): ").strip()
            truck = self.trucks.get(truck_choice)

            if not truck:
                print("⚠️ Invalid truck number. Please enter 1, 2, or 3.")
                return

            current_time = self.get_time_input()

            print(f"\n🚚 Truck {truck_choice} Package Status at {str(current_time)}")
            print("=" * 60)
            print(f"Truck {truck_choice} Mileage: {truck.miles:.2f} miles\n")

            for package_id in truck.packages:
                package = self.package_table.search(package_id)
                package.update_status(current_time)

                location = (
                    package.address if package.status == "Delivered"
                    else "On Truck" if package.status == "On the way"
                    else "WGUPS Hub"
                )
                delivery_time = (
                    (datetime.datetime.min + package.delivery_time).time().strftime('%H:%M')
                    if package.delivery_time else "Not Delivered"
                )
                print(
                    f"Package {package_id:02}: {package.status} | Location: {location} | "
                    f"Delivery Time: {delivery_time} | Deadline: {package.delivery_deadline}"
                )

        except ValueError:
            print("⚠️ Invalid input. Please enter values in correct format (e.g., HH:MM).")

    def show_truck_assignments(self):
        print("\n🚚 Package Assignments by Truck")
        print("-" * 40)
        for i, truck in self.trucks.items():
            print(f"Truck {i}: {', '.join(map(str, truck.packages))}")

    def get_time_input(self):
        time_input = input("Enter a time (HH:MM): ")
        hours, minutes = map(int, time_input.split(":"))
        return datetime.timedelta(hours=hours, minutes=minutes)
