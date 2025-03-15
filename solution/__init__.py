import re
import uuid
from tabulate import tabulate


class OverfillException(Exception):
    pass


class Storage:
    def __init__(self):
        self.containers = []

    def add_container(self, capacity, height, dry_mass, depth):
        serial_number = str(uuid.uuid4())
        if serial_number in [container.serial_number for container in self.containers]:
            raise Exception(
                "Container with the following serial number already exists: "
                + serial_number
            )
        container = Container(capacity, height, dry_mass, depth, serial_number)
        self.containers.append(container)
        print(
            "Successfully added container: with the following serial number: "
            + serial_number
        )
        return container

    def empty_warehouse(self):
        self.containers = []
        print("Storage has been emptied.")

    def replace_container(self, serial_number, new_container):
        for container in self.containers:
            if container.serial_number == serial_number:
                container = new_container
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
    def __init__(self, capacity, height, dry_mass, depth, serial_number):
        self.capacity = capacity
        self.loaded_mass = 0
        self.height = height
        self.dry_mass = dry_mass
        self.depth = depth
        self.serial_number = serial_number
        self.cargo = []
        self.hazard_notifier = HazardNotifier()

    def load_container(self, cargo):
        if self.loaded_mass + cargo.load_mass > self.capacity:
            self.hazard_notifier.warn_hazard(self, OverfillException)
        else:
            self.cargo.append(cargo)
            self.loaded_mass += cargo.load_mass
            print(f"Container has been loaded with {cargo.load_mass}kg of cargo.")

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
    def __init__(self, capacity, height, dry_mass, depth, serial_number):
        super().__init__(capacity, height, dry_mass, depth, serial_number)

    def load_container(self, cargo):
        max_capacity = self.capacity * 0.9 if cargo.safe else self.capacity * 0.5

        if self.loaded_mass + cargo.load_mass > max_capacity:
            self.hazard_notifier.warn_hazard(self, OverfillException)
        else:
            self.cargo.append(cargo)
            self.loaded_mass += cargo.load_mass
            print(f"Container has been loaded with {cargo.load_mass}kg of cargo.")


class GasContainer(Container):
    def __init__(self, capacity, height, dry_mass, depth, serial_number):
        super().__init__(capacity, height, dry_mass, depth, serial_number)

    def empty_container(self):
        self.loaded_mass = self.loaded_mass * 0.05
        self.cargo = []
        print(
            "Container emptied with 5% of the load mass remaining due to the cargo being a gas"
        )


class ChilledContainer(Container):
    def __init__(
        self,
        capacity,
        height,
        dry_mass,
        depth,
        serial_number,
        type_of_cargo,
        temperature,
    ):
        super().__init__(capacity, height, dry_mass, depth, serial_number)
        self.type_of_cargo = type_of_cargo
        self.temperature = temperature

    def load_container(self, cargo, type_of_cargo, required_temperature):
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
        self.storage = Storage()
        self.max_speed = max_speed
        self.capacity = capacity  # in number of containers
        self.max_tonnage = max_tonnage
        self.current_tonnage = 0

    def load_container(self, container):
        self.storage.containers.append(container)

    def load_container_group(self, container_group: list[Container]):
        for container in container_group:
            self.load_container(container)

    def unload_container(self, container):
        self.storage.remove_container(container)

    def unload_ship(self):
        self.storage.empty_warehouse()

    def replace_container(self, serial_number, new_container):
        self.storage.replace_container(serial_number, new_container)

    def transport_container(self, container, destination_ship):
        self.unload_container(container)
        destination_ship.load_container(container)
