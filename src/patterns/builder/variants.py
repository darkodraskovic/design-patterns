class Person:
    # private
    address: str = ""
    postal_code: str = ""
    city: str = ""
    # employment
    company: str = ""
    position: str = ""
    income: str = ""

    def __str__(self) -> str:
        return (
            f"Address: {self.address}, {self.postal_code}, {self.city}\n"
            + f"Employed at {self.company} as a {self.position} earning {self.income}"
        )


class PersonBuilder:
    person: Person

    # Person is mutable, so on every __init__() call new Person instance is constructed
    def __init__(self, person: Person = Person()) -> None:
        self.person = person

    # properties construct builders, but they reuse the preconstructed Person instance
    # NB: this breaks the open close principle
    # NB: this makes superclass depend on subclasses
    @property
    def lives(self) -> "PersonPrivateBuilder":
        return PersonPrivateBuilder(self.person)

    @property
    def works(self) -> "PersonEmploymentBuilder":
        return PersonEmploymentBuilder(self.person)


class PersonPrivateBuilder(PersonBuilder):
    # reuse the preconstructed Person instance
    # i.e. builder doesn't constructs the built object instance
    def __init__(self, person: Person) -> None:
        super().__init__(person)

    def at_address(self, address: str) -> "PersonPrivateBuilder":
        self.person.address = address
        return self

    def with_postal_code(self, postal_code: str) -> "PersonPrivateBuilder":
        self.person.postal_code = postal_code
        return self

    def in_city(self, city: str) -> "PersonPrivateBuilder":
        self.person.city = city
        return self


class PersonEmploymentBuilder(PersonBuilder):
    def __init__(self, person: Person) -> None:
        super().__init__(person)

    def in_company(self, company: str) -> "PersonEmploymentBuilder":
        self.person.company = company
        return self

    def at_position(self, position: str) -> "PersonEmploymentBuilder":
        self.person.position = position
        return self

    def with_income(self, income: str) -> "PersonEmploymentBuilder":
        self.person.income = income
        return self


person_builder_1 = PersonBuilder()
person_builder_1.lives.at_address("Studentska 27").with_postal_code("11070").in_city(
    "Belgrade"
).works.in_company("Meteor").at_position("accountant").with_income("24k")
print(person_builder_1.person)

person_builder_2 = PersonBuilder()
person_builder_2.lives.at_address("Cvetni trg 3").with_postal_code("21000").in_city(
    "Novi Sad"
).works.in_company("Startas").at_position("sales manager").with_income("34k")
print(person_builder_1.person)
