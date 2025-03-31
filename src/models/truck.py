class Truck:
    """Represents a delivery truck with routing and timing information."""
    def __init__(self, speed=18, current_location="4001 South 700 East", departure_time=None, packages=None):
        self.speed = speed
        self.miles = 0.0
        self.current_location = current_location
        self.departure_time = departure_time
        self.time = departure_time
        self.packages = packages if packages is not None else []

    def __str__(self):
        return (f"Speed: {self.speed} mph | Miles: {self.miles:.2f} | "
                f"Location: {self.current_location} | Time: {self.time} | "
                f"Packages: {self.packages}")
