# High level modules should not depend on low level modules; both should depend
# on abstractions.
# Abstractions should not depend on details. Details should depend upon abstractions.

from abc import ABC, abstractmethod
from collections.abc import Generator
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


# interface (abstraction)
class RelationshipBrowser(ABC):
    @abstractmethod
    def find_all_children(self, parent: Person) -> Generator[Person, None, None]:
        pass


# low level module
class Relationships(RelationshipBrowser):
    relations: list[tuple[Person, Relationship, Person]]

    def __init__(self) -> None:
        self.relations = []

    def add_parrent_and_child(self, parent: Person, child: Person) -> None:
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.CHILD, child))

    # if internal storage (self.relations) change, rewrite this method
    # and client code will still work
    def find_all_children(self, parent: Person) -> Generator[Person, None, None]:
        for r in self.relations:
            if r[0] == parent and r[1] == Relationship.PARENT:
                yield r[2]


# high level modules
class Research:
    def __init__(self, relationships: Relationships, parent: Person) -> None:

        # # WRONG: high level module accesses internal storage mechanism of
        # # low level module
        # relations = relationships.relations
        # for r in relations:
        #     if r[0] == parent and r[1] == Relationship.PARENT:
        #         print(f"{parent.name} has a child called {r[2].name}")

        # RIGHT: high level module depends on abstract interface
        for c in relationships.find_all_children(parent):
            print(f"{parent.name} has a child called {c.name}")


john = Person("John")
chris = Person("Chris")
matt = Person("Matt")
relationships = Relationships()
relationships.add_parrent_and_child(john, chris)
relationships.add_parrent_and_child(john, matt)
research = Research(relationships, john)
