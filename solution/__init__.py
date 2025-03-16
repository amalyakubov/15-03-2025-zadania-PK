import re
import uuid
from tabulate import tabulate


class OverfillException(Exception):
    pass


def generate_serial_number():
    return str(uuid.uuid4())


class Storage:
    def __init__(self):
        self.containers = []

    def add_container(self, container):
        if container is None:
            raise Exception("Container cannot be None")
        self.containers.append(container)
        print(
            f"Container with the serial number {container.serial_number} has been added to storage"
        )

    def empty_warehouse(self):
        self.containers = []
        print("Storage has been emptied.")

    def replace_container(self, serial_number, new_container):
        if serial_number is None or new_container is None:
            raise Exception("Serial number or new container is None")
        for container in self.containers:
            if container.serial_number == serial_number:
                self.containers[self.containers.index(container)] = new_container
                print(
                    "Container with the following serial number: "
                    + serial_number
                    + " has been replaced with a new container."
                )

    def remove_container(self, container):
        self.containers.remove(container)
        print(
            f"Container with the following serial number: {container.serial_number} has been removed from the storage."
        )

    def remove_container_by_serial_number(self, serial_number):
        for container in self.containers:
            if container.serial_number == serial_number:
                self.containers.remove(container)
                print(
                    f"Container with the following serial number: {container.serial_number} has been removed from the storage."
                )


class HazardNotifier:
    def warn_hazard(self, container, exception):
        if issubclass(exception, OverfillException):
            print(
                f"Warning! Container with the following serial number: {container.serial_number} has suffered a hazard: {exception.__name__}"
            )


class SerialNumber:
    def __init__(self, serial_number: str):
        pattern = r"KON-\w*-\d*"
        if re.match(pattern, serial_number):
            self.serial_number = serial_number
        else:
            raise Exception("Invalid serial number. Received: " + serial_number)


class Cargo:
    def __init__(self, safe: bool, load_mass):
        self.safe = safe
        self.load_mass = load_mass


class Container:
    def __init__(self, capacity, height, dry_mass, depth):
        if capacity <= 0 or height <= 0 or dry_mass <= 0 or depth <= 0:
            raise Exception(
                "Invalid capacity, height, dry mass or depth cannot be lower than 0"
            )
        if capacity is None or height is None or dry_mass is None or depth is None:
            raise Exception("Capacity, height, dry mass or depth cannot be None")
        self.capacity = capacity
        self.loaded_mass = 0
        self.height = height
        self.dry_mass = dry_mass
        self.depth = depth
        self.serial_number = generate_serial_number()
        self.cargo = []
        self.hazard_notifier = HazardNotifier()

    def load_container(self, cargo):
        if cargo is None:
            raise Exception("Cargo is None")
        if self.loaded_mass + cargo.load_mass > self.capacity:
            self.hazard_notifier.warn_hazard(self, OverfillException)
        else:
            self.cargo.append(cargo)
            self.loaded_mass += cargo.load_mass
            print(
                f"Container {self.serial_number} has been loaded with {cargo.load_mass}kg of cargo."
            )

    def empty_container(self):
        self.cargo = []
        self.loaded_mass = 0
        print(
            f"Container with the following serial number: {self.serial_number} has been emptied."
        )

    def print_info(self):
        container_info = [
            ["Serial Number", self.serial_number],
            ["Type", "Container"],
            ["Capacity", f"{self.capacity} kg"],
            [
                "Loaded Mass",
                f"{self.loaded_mass} kg ({self.loaded_mass/self.capacity*100}%)",
            ],
            ["Height", f"{self.height} cm"],
            ["Depth", f"{self.depth} cm"],
            ["Dry Mass", f"{self.dry_mass} kg"],
            ["Total Mass", f"{self.dry_mass + self.loaded_mass} kg"],
        ]

        if hasattr(self, "temperature") and hasattr(self, "type_of_cargo"):
            container_info.extend(
                [
                    ["Cargo Type", self.type_of_cargo],
                    ["Temperature", f"{self.temperature}°C"],
                ]
            )

        print(tabulate(container_info, headers=["Property", "Value"], tablefmt="grid"))

        if self.cargo:
            cargo_table = []
            for i, item in enumerate(self.cargo, 1):
                cargo_table.append(
                    [i, item.load_mass, "Safe" if item.safe else "Hazardous"]
                )
            print("\nCargo Contents:")
            print(
                tabulate(
                    cargo_table,
                    headers=["Item #", "Mass (kg)", "Safety Status"],
                    tablefmt="grid",
                )
            )


class ContainerForLiquids(Container):
    def __init__(self, capacity, height, dry_mass, depth):
        super().__init__(capacity, height, dry_mass, depth)

    def load_container(self, cargo):
        max_capacity = self.capacity * 0.9 if cargo.safe else self.capacity * 0.5

        if self.loaded_mass + cargo.load_mass > max_capacity:
            self.hazard_notifier.warn_hazard(self, OverfillException)
        else:
            self.cargo.append(cargo)
            self.loaded_mass += cargo.load_mass
            print(
                f"Container {self.serial_number} has been loaded with {cargo.load_mass}kg of cargo."
            )


class GasContainer(Container):
    def __init__(self, capacity, height, dry_mass, depth):
        if capacity <= 0 or height <= 0 or dry_mass <= 0 or depth <= 0:
            raise Exception(
                "Invalid capacity, height, dry mass or depth cannot be lower than 0"
            )
        if capacity is None or height is None or dry_mass is None or depth is None:
            raise Exception("Capacity, height, dry mass or depth cannot be None")
        super().__init__(capacity, height, dry_mass, depth)

    def empty_container(self):
        self.loaded_mass = self.loaded_mass * 0.05
        self.cargo = []
        print(
            f"Container {self.serial_number} has been emptied with 5% of the load mass remaining due to the cargo being a gas"
        )


class ChilledContainer(Container):
    def __init__(
        self,
        capacity,
        height,
        dry_mass,
        depth,
        type_of_cargo,
        temperature,
    ):
        if capacity <= 0 or height <= 0 or dry_mass <= 0 or depth <= 0:
            raise Exception(
                "Invalid capacity, height, dry mass or depth cannot be lower than 0"
            )
        if capacity is None or height is None or dry_mass is None or depth is None:
            raise Exception("Capacity, height, dry mass or depth cannot be None")
        super().__init__(capacity, height, dry_mass, depth)
        self.type_of_cargo = type_of_cargo
        self.temperature = temperature

    def load_container(self, cargo, type_of_cargo, required_temperature):
        if cargo is None:
            raise Exception("Cargo cannot be None")
        if type_of_cargo is None:
            raise Exception("Type of cargo cannot be None")
        if required_temperature is None:
            raise Exception("Required temperature cannot be None")
        if self.temperature < required_temperature:
            raise Exception(
                f"Unable to load cargo with a required temperature higher than the container's temperature. Received: {required_temperature}, expected: {self.temperature} or lower"
            )

        if type_of_cargo != self.type_of_cargo:
            raise Exception(
                f"Unable to load cargo with a different type of cargo. Received: {type_of_cargo}, expected: {self.type_of_cargo}"
            )

        super().load_container(cargo)


class Ship:
    def __init__(self, max_speed, capacity, max_tonnage):
        if max_speed <= 0 or capacity <= 0 or max_tonnage <= 0:
            raise Exception(
                "Invalid max speed, capacity or max tonnage cannot be lower than 0"
            )
        if max_speed is None or capacity is None or max_tonnage is None:
            raise Exception("Max speed, capacity or max tonnage cannot be None")
        self.storage = Storage()
        self.max_speed = max_speed
        self.capacity = capacity  # in number of containers
        self.max_tonnage = max_tonnage
        self.current_tonnage = 0

    def load_container(self, container):
        if container is None:
            raise Exception("Container cannot be None")
        self.storage.containers.append(container)

    def load_container_group(self, container_group: list[Container]):
        if container_group is None:
            raise Exception("Container group cannot be None")
        for container in container_group:
            self.load_container(container)

    def unload_container(self, container):
        if container is None:
            raise Exception("Container cannot be None")
        self.storage.remove_container(container)

    def unload_ship(self):
        if self.storage is None:
            raise Exception("Storage cannot be None")
        self.storage.empty_warehouse()

    def replace_container(self, serial_number, new_container):
        if serial_number is None or new_container is None:
            raise Exception("Serial number or new container cannot be None")
        self.storage.replace_container(serial_number, new_container)

    def transport_container(self, container, destination_ship):
        if container is None:
            raise Exception("Container cannot be None")
        if destination_ship is None:
            raise Exception("Destination ship cannot be None")
        self.unload_container(container)
        destination_ship.load_container(container)

    def print_info(self):
        print("Ship Data:")
        data = [
            ["Max Speed", f"{self.max_speed} knots"],
            ["Capacity", f"{self.capacity} containers"],
            ["Max Tonnage", f"{self.max_tonnage} kg"],
            ["Current Tonnage", f"{self.current_tonnage} kg"],
        ]

        print(tabulate(data, tablefmt="grid"))

        cargo_manifest = []
        for container in self.storage.containers:
            cargo_manifest.append(
                [
                    container.serial_number,
                    container.capacity,
                    container.loaded_mass,
                    container.cargo,
                ]
            )
        print(
            tabulate(
                cargo_manifest,
                headers=["Serial Number", "Capacity", "Loaded Mass", "Cargo"],
                tablefmt="grid",
            )
        )


def main():
    # Create a storage and add containers to it
    storage = Storage()
    storage.add_container(ContainerForLiquids(1000, 100, 100, 100))
    storage.add_container(GasContainer(1000, 100, 100, 100))
    storage.add_container(ChilledContainer(1000, 100, 100, 100, 10, -12))
    # Load containers with cargo
    storage.containers[0].load_container(Cargo(True, 950))
    storage.containers[1].load_container(Cargo(True, 950))
    storage.containers[1].empty_container()

    # Create a ship
    maersk = Ship(100, 1000, 10000)
    # Load one container
    maersk.load_container(storage.containers[0])
    # Load a group of containers
    maersk.load_container_group(storage.containers)

    # Unload one containre from the ship
    maersk.unload_container(maersk.storage.containers[0])

    # Empty one container
    maersk.storage.containers[0].empty_container()

    # Replace one container
    maersk.replace_container(
        maersk.storage.containers[0].serial_number, storage.containers[1]
    )

    # Transport one container to another ship
    maersk.transport_container(maersk.storage.containers[0], maersk)

    # Print info about one container
    maersk.storage.containers[0].print_info()

    container2 = ContainerForLiquids(1000, 100, 100, 100)
    container2.load_container(Cargo(True, 300))
    maersk.load_container(container2)

    maersk.print_info()
    print(maersk.storage.containers[3].cargo[0].__dict__)


main()
