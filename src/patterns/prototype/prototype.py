import copy


class Address:
    street: str
    city: str
    country: str

    def __init__(self, street: str, city: str, country: str) -> None:
        self.street = street
        self.city = city
        self.country = country

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.country}"


class Person:
    name: str
    address: Address

    def __init__(self, name: str, address: Address) -> None:
        self.name = name
        self.address = address

    def __str__(self) -> str:
        return f"{self.name} lives at {self.address}"

    def clone(self) -> "Person":
        return copy.deepcopy(self)


if __name__ == "__main__":
    john = Person("John Smith", Address("123 George Berkeley", "London", "England"))
    print(john)
    jane = john.clone()
    jane.name = "Jane"
    jane.address.street = "256 George Berkeley"
    print(jane)
