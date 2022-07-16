# Standard library imports
from abc import ABC, abstractmethod
from collections.abc import Generator
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name: str, color: Color, size: Size) -> None:
        self.name: str = name
        self.color: Color = color
        self.size: Size = size

    def __str__(self) -> str:
        return f"{self.size.name.lower()}, \
            {self.color.name.lower()} {self.name}"


# OCP = open for extension, closed for modification principle
class ProductFilter:
    def filter_by_color(
        self, products: list[Product], color: Color
    ) -> Generator[Product, None, None]:
        for product in products:
            if product.color == color:
                yield product

    # add new functionality by extension not by modification
    def filter_by_size(
        self, products: list[Product], size: Size
    ) -> Generator[Product, None, None]:
        for product in products:
            if product.size == size:
                yield product

    # WRONG
    # As the number of state variables in the system increases,
    # the size of the system state space grows exponentially.
    # This is called the "state explosion problem"
    # In this case, 2 criteria filter yields 3 methods with connective "and"
    # Basically, it is a number of subsets per logical connective.
    def filter_by_color_and_size(
        self, products: list[Product], color: Color, size: Size
    ) -> Generator[Product, None, None]:
        for product in products:
            if product.color == color and product.size == size:
                yield product


# CORRECT Specification and Filter classes are open for extension,
# but closed for modification

# The specification pattern is a particular software design pattern,
# whereby business rules can be recombined by chaining the business
# rules together using boolean logic.
# (https://en.wikipedia.org/wiki/Specification_pattern)
class Specification(ABC):
    @abstractmethod
    def is_satisfied(self, product: Product) -> bool:
        ...


class Filter(ABC):
    @abstractmethod
    def filter(
        self, products: list[Product], specification: Specification
    ) -> Generator[Product, None, None]:
        ...


class ColorSpecification(Specification):
    def __init__(self, color: Color) -> None:
        self.color: Color = color

    def is_satisfied(self, product: Product) -> bool:
        return product.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size: Size) -> None:
        self.size: Size = size

    def is_satisfied(self, product: Product) -> bool:
        return product.size == self.size


class AndSpecification(Specification):
    def __init__(self, *args: Specification) -> None:
        self.specifications: list[Specification] = [*args]

    def is_satisfied(self, product: Product) -> bool:
        return all(
            specification.is_satisfied(product) for specification in self.specifications
        )


class BetterFilter(Filter):
    def filter(
        self, products: list[Product], specification: Specification
    ) -> Generator[Product, None, None]:
        for product in products:
            if specification.is_satisfied(product):
                yield product


def test() -> None:
    green_apple = Product("apple", Color.GREEN, Size.SMALL)
    red_apple = Product("apple", Color.RED, Size.SMALL)
    tree = Product("tree", Color.GREEN, Size.LARGE)
    house = Product("house", Color.BLUE, Size.MEDIUM)
    red_car = Product("car", Color.RED, Size.MEDIUM)
    blue_car = Product("car", Color.BLUE, Size.LARGE)
    red_table = Product("table", Color.RED, Size.MEDIUM)

    products = [green_apple, red_apple, tree, house, red_car, blue_car, red_table]

    print("\nWRONG approach\n----------------")
    product_filter = ProductFilter()
    print("\nred products:")
    for product in product_filter.filter_by_color(products, Color.RED):
        print(product)
    print("\nmedium products:")
    for product in product_filter.filter_by_size(products, Size.MEDIUM):
        print(product)

    print("\nCORRECT approach\n----------------")
    red_spec = ColorSpecification(Color.RED)
    medium_spec = SizeSpecification(Size.MEDIUM)
    better_filter = BetterFilter()
    print("\nred products:")
    for product in better_filter.filter(products, red_spec):
        print(product)
    print("\nmedium products:")
    for product in better_filter.filter(products, medium_spec):
        print(product)

    print("\nAndSpec: red and medium products\n----------------")
    and_specification = AndSpecification(red_spec, medium_spec)
    for product in better_filter.filter(products, and_specification):
        print(product)
