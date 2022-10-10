from abc import ABC
from enum import Enum, auto


# object hierarchy

# abstract object
class HotDrink(ABC):
    quantity: int

    def consume(self) -> None:
        pass


class Tea(HotDrink):
    def consume(self) -> None:
        print(f"You consume {self.quantity}ml of tea!")


class Coffee(HotDrink):
    def consume(self) -> None:
        print(f"You consume {self.quantity}ml of coffee!")


# factory hierarchy

# abstract factory; used to mandate interface
# essential in strongly typed languages, optional in Python
class HotDrinkFactory(ABC):
    def prepare(self, quantity: int) -> HotDrink:
        pass


class TeaFactory(ABC):
    def prepare(self, quantity: int) -> HotDrink:
        tea = Tea()
        tea.quantity = quantity
        return tea


class CoffeeFactory(ABC):
    def prepare(self, quantity: int) -> HotDrink:
        coffee = Coffee()
        coffee.quantity = quantity
        return coffee


def make_drink(type: str) -> HotDrink | None:
    if type == "tea":
        return TeaFactory().prepare(200)
    elif type == "coffee":
        return CoffeeFactory().prepare(50)
    else:
        return None


class HotDrinkMachine:
    factories: list[tuple[str, HotDrinkFactory]] = []
    _initialized: bool = False

    class AvailableDrink(Enum):
        TEA = auto()
        COFFEE = auto()

    def __init__(self) -> None:
        if not self._initialized:
            for d in self.AvailableDrink:
                name = d.name[0] + d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))
            self._initialized = True
        pass

    def make_drink(self) -> HotDrink:
        print("Available drinks: ")
        for i in range(len(self.factories)):
            print(str(i) + f": {self.factories[i][0]}")

        s = input(f"Pick a drink (0-{len(self.factories)-1}): ")
        idx = int(s)
        s = input("Specify quantity: ")
        quantity = int(s)
        return self.factories[idx][1].prepare(quantity)


if __name__ == "__main__":
    # entry = input("Please choose a drink: ")
    # drink = make_drink(entry)
    # if drink:
    #     drink.consume()

    hdm = HotDrinkMachine()
    drink = hdm.make_drink()
    drink.consume()
