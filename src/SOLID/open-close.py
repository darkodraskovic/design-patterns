from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generator


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    Small = 1
    Medium = 2
    Large = 3


class Product:
    def __init__(self, name: str, color: Color, size: Size) -> None:
        self.name: str = name
        self.color: Color = color
        self.size: Size = size


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


class BetterFilter(Filter):
    def filter(
        self, products: list[Product], specification: Specification
    ) -> Generator[Product, None, None]:
        for product in products:
            if specification.is_satisfied(product):
                yield product
