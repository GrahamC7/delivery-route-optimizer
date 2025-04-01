import datetime
from zipfile import error

from flask import Flask, render_template, request
from sympy.physics.units import minutes

from logic.data_loader import load_packages, load_csv_files
from logic.routing import deliver_packages
from models.hash_table import HashTable
from models.truck import Truck

app = Flask(__name__)

# load data
address_data, distance_data = load_csv_files()
package_table = HashTable()

# initialize packages

load_packages("data/packages.csv", package_table)

# trucks and delivery setup
truck1 = Truck(departure_time=datetime.timedelta(hours=8),
               packages=[1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Truck(departure_time=datetime.timedelta(hours=10, minutes=20),
               packages=[2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Truck(departure_time=datetime.timedelta(hours=9, minutes=5),
               packages=[6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])

deliver_packages(truck1, package_table, address_data, distance_data)
deliver_packages(truck2, package_table, address_data, distance_data)
truck3.departure_time = min(truck1.time, truck2.time)
truck3.time = truck3.departure_time
deliver_packages(truck3, package_table, address_data, distance_data)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            package_id = int(request.form["package_id"])
            time_input = request.form["time"]
            hours, minutes = map(int, time_input.split(":"))
            current_time = datetime.timedelta(hours=hours, minutes=minutes)

            package = package_table.search(package_id)
            if not package:
                return render_template("results.html", error="Package not found.")

            package.update_status(current_time)

            location = (
                package.address if package.status == "Delivered"
                else "On Truck" if package.status == "On the way"
                else "WGUPS hub"
            )

            delivery_time = (
                (datetime.datetime.min + package.delivery_time).time().strftime('%H:%M')
                if package.delivery_time else "Not Delivered"
            )

            return render_template("results.html", package=package, location=location, delivery_time=delivery_time,
                                   time_input=time_input)

        except Exception as e:
            return render_template("results.html", error=f"Error: {str(e)}")

    return render_template("index.html")


@app.route("/packages", methods=["GET", "POST"])
def view_all_packages():
    if request.method == "POST":
        try:
            time_input = request.form["time"]
            hours, minutes = map(int, time_input.split(":"))
            current_time = datetime.timedelta(hours=hours, minutes=minutes)

            # update status of all packages
            all_packages = []
            for package_id in range(1, 41):
                package = package_table.search(package_id)
                package.update_status(current_time)
                all_packages.append(package)

            return render_template("all_packages.html", packages=all_packages, time_input=time_input, datetime=datetime)

        except Exception as e:
            return render_template("all_packages.html", error=f"Error: {str(e)}")

    return render_template("all_packages.html")


@app.route("/trucks", methods=["GET", "POST"])
def truck_dashboard():
    if request.method == "POST":
        try:
            time_input = request.form["time"]
            hours, minutes = map(int, time_input.split(":"))
            current_time = datetime.timedelta(hours=hours, minutes=minutes)
        except Exception as e:
            return render_template("trucks.html", error=f"Invalid time input: {str(e)}")

        def get_progress(truck):
            delivered = 0
            for pid in truck.packages:
                pkg = package_table.search(pid)
                # Update package status using the provided time
                pkg.update_status(current_time)
                if pkg.status == "Delivered":
                    delivered += 1
            return delivered, len(truck.packages)

        trucks = []
        for i, truck in enumerate([truck1, truck2, truck3], start=1):
            delivered, total = get_progress(truck)
            trucks.append({
                "name": f"Truck {i}",
                "departure": (datetime.datetime.min + truck.departure_time).time().strftime('%H:%M'),
                "miles": round(truck.miles, 2),
                "packages": truck.packages,
                "delivered": delivered,
                "total": total
            })

        return render_template("trucks.html", trucks=trucks, time_input=time_input)
    else:
        return render_template("trucks.html")


if __name__ == "__main__":
    app.run(debug=True)
