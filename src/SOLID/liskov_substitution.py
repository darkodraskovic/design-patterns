# The Liskov Substitution Principle states that any subclass object
# should be substitutable for the superclass object from which it is derived.


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self._width: float = width
        self._height: float = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    @property
    def area(self) -> float:
        return self._width * self._height

    def __str__(self) -> str:
        return f"width: {self.width}, height: {self.height}"


class Square(Rectangle):
    def __init__(self, size: float) -> None:
        super().__init__(size, size)

    # WRONG: break Liskov substitution principle
    # The base class sets only width here
    @Rectangle.width.setter
    def width(self, value: float) -> None:
        self._width = self._height = value

    # WRONG: break Liskov substitution principle
    # The base class sets only height here
    @Rectangle.height.setter
    def height(self, value: float) -> None:
        self._width = self._height = value


# WRONG: this function only works with Rectangle and does not work
# with classes derived from Rectangle and thus breaks the LSP:
# If interface works with base class, it should work with any derived class
def use_rectangle(rectangle: Rectangle) -> None:
    width = rectangle.width
    rectangle.height = 10
    # ok if called with base class as param, error when called with Square as param
    print(f"expected an area of {width * 10}, got {rectangle.area}")


def test() -> None:
    rect = Rectangle(4, 6)
    use_rectangle(rect)

    square = Square(4)
    use_rectangle(square)
