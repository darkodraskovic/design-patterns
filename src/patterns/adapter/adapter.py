from typing import Iterator


# we are given this API, let's call it Xy
class XyPoint:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def draw_xy_point(p: XyPoint) -> None:
    # dummy point rendering method
    print(".", end="")


# we use this API
class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    start: Point
    end: Point

    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end


class Rectangle(list[Line]):
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__()

        # self.x = x
        # self.y = y
        # self.width = width
        # self.height = height

        # top
        self.append(Line(Point(x, y), Point(x + width, y)))
        # right
        self.append(Line(Point(x + width, y), Point(x + width, y + height)))
        # left
        self.append(Line(Point(x, y), Point(x, y + height)))
        # bottom
        self.append(Line(Point(x, y + height), Point(x + width, y + height)))


# we need to build in-between component, i.e. adapter
# here we need to represent Line as list of XyPoints
# because we can only draw XyPoints and not Points, Lines or Rectangles
class LineToXyPoint(list[XyPoint]):
    def __init__(self, line: Line) -> None:
        super().__init__()

        # compute l,r,t,b coordinates of line
        # we assume that lines are either horizontal or vertical
        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = min(line.start.y, line.end.y)
        bottom = max(line.start.y, line.end.y)

        # if line is vertical
        if right - left == 0:
            for y in range(top, bottom):
                self.append(XyPoint(left, y))
        # if line is horizontal
        if bottom - top == 0:
            for x in range(left, right):
                self.append(XyPoint(x, top))


# memoization optimization: cache adapters for encountered lines
class LineToXyPointCache:
    cache: dict[int, list[XyPoint]] = {}

    def __init__(self, line: Line) -> None:
        super().__init__()

        self.hash = hash(line)
        if self.hash in self.cache:
            print("Line adapter found in cache")
            return

        print("Creating line adapter")
        # compute l,r,t,b coordinates of line
        # we assume that lines are either horizontal or vertical
        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = min(line.start.y, line.end.y)
        bottom = max(line.start.y, line.end.y)

        points: list[XyPoint] = []
        # if line is vertical
        if right - left == 0:
            for y in range(top, bottom):
                points.append(XyPoint(left, y))
        # if line is horizontal
        if bottom - top == 0:
            for x in range(left, right):
                points.append(XyPoint(x, top))

        self.cache[self.hash] = points

    def __iter__(self) -> Iterator[XyPoint]:
        return iter(self.cache[self.hash])


def draw_line(line: Line) -> None:
    # LineToXyPoint adapter adapts line drawing interface to point drawing interface
    # adapter = LineToXyPoint(line)
    adapter = LineToXyPointCache(line)
    for point in adapter:
        draw_xy_point(point)
    print()


def draw_rectangle(rectangle: Rectangle) -> None:
    for line in rectangle:
        draw_line(line)


if __name__ == "__main__":
    rectangles = [
        Rectangle(1, 1, 10, 10),
        Rectangle(3, 3, 6, 8),
    ]
    draw_rectangle(rectangles[0])
    draw_rectangle(rectangles[0])
