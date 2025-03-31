import datetime

class Package:
    """Represents a package with delivery metadata."""
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight_kg, status="At WGUPS Hub"):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight_kg = weight_kg
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def update_status(self, current_time):
        if self.delivery_time is None:
            self.status = "At WGUPS Hub"
        elif current_time < self.departure_time:
            self.status = "At WGUPS Hub"
        elif current_time < self.delivery_time:
            self.status = "On the way"
        else:
            self.status = "Delivered"

        if self.package_id == 9 and current_time >= datetime.timedelta(hours=10, minutes=20):
            self.address = "410 S State St"
            self.zip_code = "84111"
