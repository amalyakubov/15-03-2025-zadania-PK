from solution import (
    Storage,
    Container,
    ContainerForLiquids,
    GasContainer,
    ChilledContainer,
    Cargo,
    Ship,
)


def main():
    print("\n=== TESTING CONTAINER MANAGEMENT SYSTEM ===\n")

    # 1. Create containers of different types
    print("\n--- Creating Containers ---\n")
    storage = Storage()

    # Regular container
    regular_container = storage.add_container(1000, 250, 300, 600)

    # Container for liquids
    liquid_container = ContainerForLiquids(800, 200, 250, 500, "KON-LIQ-001")

    # Gas container
    gas_container = GasContainer(500, 180, 200, 450, "KON-GAS-001")

    # Chilled container
    chilled_container = ChilledContainer(
        1200, 280, 350, 650, "KON-CHL-001", "Frozen Food", -18
    )

    # 2. Load cargo into containers
    print("\n--- Loading Cargo into Containers ---\n")

    # Load regular container
    safe_cargo = Cargo(True, 500)
    regular_container.load_container(safe_cargo)

    # Load liquid container
    liquid_cargo = Cargo(True, 400)
    liquid_container.load_container(liquid_cargo)

    # Load gas container
    gas_cargo = Cargo(True, 300)
    gas_container.load_container(gas_cargo)

    # Load chilled container
    try:
        chilled_cargo = Cargo(True, 600)
        chilled_container.load_container(chilled_cargo, "Frozen Food", -20)
    except Exception as e:
        print(f"Error: {e}")

    # 3 & 4. Create ships and load containers
    print("\n--- Creating Ships and Loading Containers ---\n")

    # Create ships
    ship1 = Ship(30, 10, 10000)
    ship2 = Ship(25, 8, 8000)

    # 3. Load a single container onto ship1
    ship1.load_container(regular_container)

    # 4. Load a list of containers onto ship1
    container_group = [liquid_container, gas_container]
    ship1.load_container_group(container_group)

    # 5. Remove a container from ship1
    print("\n--- Removing Container from Ship ---\n")
    ship1.unload_container(liquid_container)

    # 6. Empty a container
    print("\n--- Emptying Containers ---\n")
    regular_container.empty_container()
    gas_container.empty_container()  # Special behavior for gas containers

    # 7. Replace a container on the ship
    print("\n--- Replacing Container on Ship ---\n")
    ship1.replace_container(gas_container.serial_number, chilled_container)

    # 8. Transfer container between ships
    print("\n--- Transferring Container Between Ships ---\n")
    ship1.transport_container(regular_container, ship2)

    # 9. Display container information
    print("\n--- Container Information ---\n")
    regular_container.print_info()
    chilled_container.print_info()

    # 10. Display ship information
    print("\n--- Ship Information ---\n")
    print(
        f"Ship 1 - Max Speed: {ship1.max_speed} knots, Capacity: {ship1.capacity} containers, Max Tonnage: {ship1.max_tonnage} tons"
    )
    print("Containers on Ship 1:")
    for i, container in enumerate(ship1.storage.containers, 1):
        print(
            f"  {i}. Container {container.serial_number} - {container.dry_mass + container.loaded_mass} kg"
        )

    print(
        f"\nShip 2 - Max Speed: {ship2.max_speed} knots, Capacity: {ship2.capacity} containers, Max Tonnage: {ship2.max_tonnage} tons"
    )
    print("Containers on Ship 2:")
    for i, container in enumerate(ship2.storage.containers, 1):
        print(
            f"  {i}. Container {container.serial_number} - {container.dry_mass + container.loaded_mass} kg"
        )


if __name__ == "__main__":
    main()
