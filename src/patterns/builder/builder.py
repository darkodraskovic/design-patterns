# clumsy way of building HTML elements
def build_html_clumsy() -> None:
    text = "hello"
    parts = ["<p>", text, "</p>"]
    print("".join(parts))

    words = ["hello", "world"]
    parts = ["<ul>"]
    for w in words:
        parts.append(f"  <li>{w}</li>")
    parts.append("</ul>")
    print("\n".join(parts))


# builder pattern: "Separate the construction of a complex
# object from its representation so that the same construction process
# can create different representations." (Design Patterns)


class HtmlElement:
    indent_size: int = 2
    name: str
    text: str
    elements: list["HtmlElement"]

    def __init__(self, name: str = "", text: str = "") -> None:
        self.name = name
        self.text = text
        self.elements = []

    def __str(self, indent: int) -> str:
        lines = []

        # opening tag
        tag_indent = " " * (indent * self.indent_size)
        lines.append(f"{tag_indent}<{self.name}>")

        # content
        if self.text:
            text_indent = " " * ((indent + 1) * self.indent_size)
            lines.append(f"{text_indent}<{self.text}>")

        # children
        for e in self.elements:
            lines.append(e.__str(indent + 1))

        # closing tag
        lines.append(f"{tag_indent}</{self.name}>")

        return "\n".join(lines)

    def __str__(self) -> str:
        return self.__str(0)

    @staticmethod
    def create_builder(name: str) -> "HtmlBuilder":
        return HtmlBuilder(name)


class HtmlBuilder:
    __root: HtmlElement

    # NB: builder constructs the built object instance
    def __init__(self, name: str, text: str = "") -> None:
        self.__root = HtmlElement(name=name, text=text)

    def add_child(self, child_name: str, child_text: str) -> "HtmlBuilder":
        self.__root.elements.append(HtmlElement(name=child_name, text=child_text))
        return self

    def __str__(self) -> str:
        return str(self.__root)


def build_html_builder() -> None:
    builder = HtmlBuilder("ul")
    builder.add_child("li", "hello")
    builder.add_child("li", "world")
    print(builder)

    builder = HtmlBuilder("ul")
    builder.add_child("li", "hello").add_child("li", "world")
    print(builder)

    builder = HtmlElement.create_builder("ul")
    builder.add_child("li", "hello").add_child("li", "world")
    print(builder)


# build_html_clumsy()
build_html_builder()
