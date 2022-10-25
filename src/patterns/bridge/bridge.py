from abc import ABC

# Implementor defines the interface for implementation classes
class Renderer(ABC):
    def render_circle(self, radius: float) -> None:
        pass

    # def render_square(self, width: float, height: float) -> None:
    #     pass


# ConcreteImplementor
class VectorRenderer(Renderer):
    def render_circle(self, radius: float) -> None:
        print(f"draw vector circle of radius {radius}")


# ConcreteImplementor
class RasterRenderer(Renderer):
    def render_circle(self, radius: float) -> None:
        print(f"draw raster circle of radius {radius}")


# Abstraction defines abstraction's interface and refers to Implementor
class Shape(ABC):
    renderer: Renderer

    def __init__(self, renderer: Renderer) -> None:
        super().__init__()

        self.renderer = renderer

    def draw(self) -> None:
        pass

    def resize(self, factor: float) -> None:
        pass


# RefinedAbastraction extends abstraction's interface
class Circle(Shape):
    radius: float = 0

    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self.radius = radius

    # use the reference as a bridge to connect to a Renderer instance
    def draw(self) -> None:
        self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        self.radius *= factor


if __name__ == "__main__":
    vector_renderer = VectorRenderer()
    raster_renderer = RasterRenderer()

    vector_circle = Circle(vector_renderer, 2)
    raster_circle = Circle(raster_renderer, 4)

    vector_circle.draw()
    vector_circle.resize(3)
    vector_circle.draw()

    raster_circle.draw()
