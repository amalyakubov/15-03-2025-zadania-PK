import pytest
from solution import (
    Storage,
    Container,
    ContainerForLiquids,
    GasContainer,
    ChilledContainer,
    Cargo,
    Ship,
    OverfillException,
)


def test_create_container_regular():
    storage = Storage()
    container = storage.add_container(1000, 200, 500, 100)
    assert container is not None
    assert container.capacity == 1000
    assert container in storage.containers


def test_load_cargo_regular(capsys):
    container = Container(1000, 200, 500, 100, "TEST123")
    cargo1 = Cargo(safe=True, load_mass=200)
    container.load_container(cargo1)
    assert container.loaded_mass == 200
    assert len(container.cargo) == 1

    cargo2 = Cargo(safe=True, load_mass=900)  # This should trigger an overfill warning
    container.load_container(cargo2)
    captured = capsys.readouterr().out
    # Verify that the danger warning was printed and cargo was not added
    assert container.loaded_mass == 200
    assert "Warning" in captured or "suffered a hazard" in captured.lower()


def test_load_container_on_ship():
    ship = Ship(30, 10, 10000)
    container = Container(1000, 200, 500, 100, "SHIPCONT1")
    ship.load_container(container)
    assert container in ship.storage.containers


def test_load_list_of_containers_on_ship():
    ship = Ship(30, 10, 10000)
    container1 = Container(1000, 200, 500, 100, "CONT1")
    container2 = Container(1500, 250, 600, 120, "CONT2")
    ship.load_container_group([container1, container2])
    assert container1 in ship.storage.containers
    assert container2 in ship.storage.containers


def test_remove_container_from_ship():
    ship = Ship(30, 10, 10000)
    container = Container(1000, 200, 500, 100, "REMOVE1")
    ship.load_container(container)
    ship.unload_container(container)
    assert container not in ship.storage.containers


def test_empty_container_regular():
    container = Container(1000, 200, 500, 100, "EMPTY1")
    cargo = Cargo(safe=True, load_mass=500)
    container.load_container(cargo)
    assert container.loaded_mass == 500
    container.empty_container()
    assert container.loaded_mass == 0
    assert len(container.cargo) == 0


def test_empty_container_gas():
    gas_container = GasContainer(1000, 200, 500, 100, "GAS1")
    cargo = Cargo(safe=True, load_mass=500)
    gas_container.load_container(cargo)
    assert gas_container.loaded_mass == 500
    gas_container.empty_container()
    # According to GasContainer.empty_container, loaded mass becomes 5% of original
    assert gas_container.loaded_mass == 25
    assert len(gas_container.cargo) == 0


def test_replace_container_on_ship():
    ship = Ship(30, 10, 10000)
    container1 = Container(1000, 200, 500, 100, "OLD1")
    ship.load_container(container1)
    container2 = Container(1500, 250, 600, 120, "NEW1")
    ship.replace_container("OLD1", container2)
    assert container1 not in ship.storage.containers
    assert container2 in ship.storage.containers


def test_transfer_container_between_ships():
    ship1 = Ship(30, 10, 10000)
    ship2 = Ship(30, 10, 10000)
    container = Container(1000, 200, 500, 100, "TRANS1")
    ship1.load_container(container)
    ship1.transport_container(container, ship2)
    assert container not in ship1.storage.containers
    assert container in ship2.storage.containers


def test_print_container_info(capsys):
    container = Container(1000, 200, 500, 100, "INFO1")
    cargo = Cargo(safe=True, load_mass=200)
    container.load_container(cargo)
    container.print_info()
    captured = capsys.readouterr().out
    assert "INFO1" in captured
    assert "200" in captured


def test_print_ship_info_and_cargo(capsys):
    ship = Ship(30, 10, 10000)
    container = Container(1000, 200, 500, 100, "SHIPINFO1")
    cargo = Cargo(safe=True, load_mass=300)
    container.load_container(cargo)
    ship.load_container(container)
    # Simulate printing ship's info by printing each container's info
    for cont in ship.storage.containers:
        cont.print_info()
    captured = capsys.readouterr().out
    assert "SHIPINFO1" in captured
    assert "300" in captured


def test_load_container_for_liquids(capsys):
    container_liquid = ContainerForLiquids(1000, 200, 500, 100, "LIQUID1")
    cargo_safe = Cargo(safe=True, load_mass=850)  # 0.9*1000 = 900, so 850 is ok
    cargo_unsafe = Cargo(
        safe=False, load_mass=600
    )  # 0.5*1000 = 500, should trigger hazard
    container_liquid.load_container(cargo_safe)
    assert container_liquid.loaded_mass == 850
    container_liquid.load_container(cargo_unsafe)
    captured = capsys.readouterr().out
    assert "Warning" in captured or "suffered a hazard" in captured.lower()
    assert container_liquid.loaded_mass == 850


def test_load_chilled_container():
    chilled = ChilledContainer(1000, 200, 500, 100, "CHILL1", "Fruits", 5)
    cargo = Cargo(safe=True, load_mass=200)
    # Valid load: matching cargo type and adequate temperature
    chilled.load_container(cargo, "Fruits", 5)
    assert chilled.loaded_mass == 200

    # Invalid cargo type
    with pytest.raises(
        Exception, match="Unable to load cargo with a different type of cargo"
    ):
        chilled.load_container(cargo, "Vegetables", 5)

    # Invalid required temperature (too high)
    with pytest.raises(
        Exception, match="Unable to load cargo with a required temperature"
    ):
        chilled.load_container(cargo, "Fruits", 6)
