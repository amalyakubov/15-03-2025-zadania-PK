from solution import *


def console_add_container(storage):
    print("Wybierz typ kontenera:")
    print("1. Kontener multimodalny")
    print("2. Kontener do cieczy")
    print("3. Kontener do gazów")
    print("4. Kontener chłodniczy")

    type = input("Wybierz typ kontenera: ")
    container_type = None
    match type:
        case "1":
            container_type = Container
        case "2":
            container_type = ContainerForLiquids
        case "3":
            container_type = GasContainer
        case "4":
            container_type = ChilledContainer
        case _:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            return

    try:
        capacity = float(input("Podaj pojemność kontenera: "))
        height = float(input("Podaj wysokość kontenera: "))
        dry_mass = float(input("Podaj wagę surową kontenera: "))
        depth = float(input("Podaj głębokość kontenera: "))

        container = container_type(capacity, height, dry_mass, depth)
        storage.add_container(container)
    except ValueError:
        print("Wprowadzono nieprawidłowe dane. Spróbuj ponownie.")


def console_refresh_view(storage):
    print("\nLista kontenerów:")
    if not storage.containers:
        print("Brak kontenerów w magazynie.")
    else:
        for container in storage.containers:
            print(f"Numer seryjny: {container.serial_number}")
            print(f"Pojemność: {container.capacity} kg")
            print(f"Waga: {container.loaded_mass} kg")
            print("-" * 30)
    print("=" * 50 + "\n")


def console_remove_container(storage):
    if not storage.containers:
        print("Brak kontenerów do usunięcia.")
        return

    print("Dostępne kontenery:")
    for index, container in enumerate(storage.containers):
        print(f"{index}. Numer seryjny: {container.serial_number}")
        print(f"   Pojemność: {container.capacity} kg")
        print(f"   Waga: {container.loaded_mass} kg")

    try:
        selected = int(input("Wybierz numer kontenera do usunięcia: "))
        if 0 <= selected < len(storage.containers):
            print(f"Wybrano numer: {selected} ")
            serial_number = storage.containers[selected].serial_number
            storage.remove_container_by_serial_number(serial_number)
            print(f"Usunięto kontener o numerze seryjnym: {serial_number}")
        else:
            print("Nieprawidłowy numer kontenera.")
    except ValueError:
        print("Wprowadź poprawny numer.")


def console_modify_container(storage):
    if not storage.containers:
        print("Brak kontenerów do modyfikacji.")
        return

    print("Dostępne kontenery:")
    for index, container in enumerate(storage.containers):
        print(f"{index}. Numer seryjny: {container.serial_number}")
        print(f"   Pojemność: {container.capacity} kg")
        print(f"   Waga: {container.loaded_mass} kg")
        print(f"   Typ: {container.__class__.__name__}")

    try:
        selected = int(input("Wybierz numer kontenera do modyfikacji: "))
        if 0 <= selected < len(storage.containers):
            container = storage.containers[selected]
            print(f"Modyfikujesz kontener: {container.serial_number}")

            print("Co chcesz zrobić?")
            print("1. Załaduj towar")
            print("2. Rozładuj towar")

            action = input("Wybierz akcję: ")

            try:
                if action == "1":
                    mass = float(input("Podaj masę towaru do załadowania: "))
                    container.load(mass)
                    print(
                        f"Załadowano {mass} kg. Aktualna masa: {container.loaded_mass} kg"
                    )
                elif action == "2":
                    mass = float(input("Podaj masę towaru do rozładowania: "))
                    container.unload(mass)
                    print(
                        f"Rozładowano {mass} kg. Aktualna masa: {container.loaded_mass} kg"
                    )
                else:
                    print("Nieprawidłowa akcja.")
            except Exception as e:
                print(f"Błąd: {e}")
        else:
            print("Nieprawidłowy numer kontenera.")
    except ValueError:
        print("Wprowadź poprawny numer.")


def console_ship_overview(ships):
    if not ships:
        print("Brak dostępnych statków.")
        return

    print("Dostępne statki:")
    for index, ship in enumerate(ships):
        print(f"{index}. Maksymalna prędkość: {ship.max_speed} węzłów")
        print(f"   Maksymalna waga: {ship.max_tonnage} kg")
        print(f"   Aktualna waga: {ship.current_tonnage} kg")
        print(f"   Aktualna prędkość: {ship.current_speed} węzłów")

        print("   Kontenery na statku:")
        if not ship.containers:
            print("   Brak kontenerów na statku.")
        else:
            for container in ship.containers:
                print(f"   - Numer seryjny: {container.serial_number}")
                print(f"     Pojemność: {container.capacity} kg")
                print(f"     Waga: {container.loaded_mass} kg")


def console_app():
    storage = Storage()
    ships = []  # Tu można dodać inicjalizację statków

    while True:
        print("\n=== SYSTEM ZARZĄDZANIA KONTENERAMI ===")

        print("\nLista kontenerów w magazynie:")
        if not storage.containers:
            print("Brak kontenerów w magazynie.")
        else:
            for container in storage.containers:
                print(f"- Numer seryjny: {container.serial_number}")
                print(f"  Pojemność: {container.capacity} kg")
                print(f"  Waga: {container.loaded_mass} kg")

        print("\nMożliwe akcje:")
        print("1. Dodaj kontener")
        print("2. Usuń kontener")
        print("3. Modyfikuj kontener")
        print("4. Przegląd statków")
        print("5. Wyjście")

        action = input("\nWybierz akcję: ")
        match action:
            case "1":
                console_add_container(storage)
            case "2":
                console_remove_container(storage)
            case "3":
                console_modify_container(storage)
            case "4":
                console_ship_overview(ships)
            case "5":
                print("Dziękujemy za skorzystanie z systemu. Do widzenia!")
                break
            case "q":
                break
            case _:
                print("Nieprawidłowa akcja. Spróbuj ponownie.")


if __name__ == "__main__":
    console_app()
