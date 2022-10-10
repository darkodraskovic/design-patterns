from math import sin, cos, pi
from enum import Enum


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


# class that does not use factory method
class Point_0:
    x: float
    y: float

    def __init__(
        self, a: float, b: float, system: CoordinateSystem = CoordinateSystem.CARTESIAN
    ) -> None:
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            self.x = a * cos(b)
            self.y = a * sin(b)


# class that uses factory method
class Point:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    # factory is a method that creates an object; it is an aleternative to constructors and
    # initalizers with multiple, special case parameters
    @staticmethod
    def new_cartesian(x: float, y: float) -> "Point":
        return Point(x, y)

    @staticmethod
    def new_polar(rho: float, theta: float) -> "Point":
        return Point(rho * cos(theta), rho * sin(theta))

    # factory can be an inner class (no point doing this in Python, though, becasause
    # everything is public)
    class PointFactory:
        def new_cartesian(self, x: float, y: float) -> "Point":
            # use no params constructor to semantically decouple class factory from object class
            p: Point = Point()
            p.x = x
            p.y = y
            return p

        def new_polar(self, rho: float, theta: float) -> "Point":
            return Point(rho * cos(theta), rho * sin(theta))

    # singleton factory instance
    factory = PointFactory()


# Alternative is to create a factory with factory methods
# factory class is coupled to an object class/definition
class PointFactory:
    @staticmethod
    def new_cartesian(x: float, y: float) -> "Point":
        # use no params constructor to semantically decouple class factory from object class
        p: Point = Point()
        p.x = x
        p.y = y
        return p

    @staticmethod
    def new_polar(rho: float, theta: float) -> "Point":
        return Point(rho * cos(theta), rho * sin(theta))


if __name__ == "__main__":
    # use constructor
    p1 = Point(10, 15)

    # use factory methods
    p2 = Point.new_cartesian(12, 24.5)

    p3 = Point.new_polar(1, pi / 4)

    p4 = Point.factory.new_cartesian(1, 1)
    print(p4)

    print()
