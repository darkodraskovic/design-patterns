# Each class should have one responsibility, one single purpose
# Robert C. Martin: "A class should have only one reason to change".
# anti-pattern: God object (sometimes also called an Omniscient or All-knowing object) is an object that references a large number of distinct types, has too many unrelated or uncategorized methods, or some combination of both (https://en.wikipedia.org/wiki/God_object)
from typing import Any


class Journal:
    def __init__(self) -> None:
        self.entries: list[str] = []
        self.count: int = 0

    def add_entry(self, text: str) -> None:
        self.count += 1
        self.entries.append(f"{self.count}: {text}")

    def remove_entry(self, index: int) -> None:
        del self.entries[index]

    def __str__(self) -> str:
        return "\n".join(self.entries)

    # WRONG: break single responsibility principle

    # the following methods should be part of persistence handling class
    def save(self, filename: str) -> None:
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename: str) -> None:
        ...

    def load_from_web(self, url: str) -> None:
        ...


# CORRECT: use separate class responsible for persistence only
class PersistenceHandler:
    def __init__(self) -> None:
        pass

    def save(self, object: Any, filename: str) -> None:
        file = open(filename, "w")
        file.write(str(object))
        file.close()

    def load(self, filename: str) -> Any:
        ...

    def load_from_web(self, url: str) -> Any:
        ...


def test() -> None:
    journal = Journal()
    journal.add_entry("I feel fine today.")
    journal.add_entry("A friend payed me a visit.")

    print(journal)

    filename = "temp/journal.txt"
    persistenceHandler = PersistenceHandler()
    persistenceHandler.save(journal, filename)

    with open(filename) as file:
        print(file.read())


test()
