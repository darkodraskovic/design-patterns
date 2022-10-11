import copy


class Address:
    street: str
    suite: int
    country: str

    def __init__(self, street: str, suite: int, country: str) -> None:
        self.street = street
        self.suite = suite
        self.country = country

    def __str__(self) -> str:
        return f"{self.street}, suite #{self.suite}, {self.country}"


class Employee:
    name: str
    address: Address

    def __init__(self, name: str, address: Address) -> None:
        self.name = name
        self.address = address

    def __str__(self) -> str:
        return f"{self.name} works at {self.address}"

    def clone(self) -> "Employee":
        return copy.deepcopy(self)


class EmployeeFactory:
    main_office_employee = Employee(
        "",
        Address("123 West Road", 0, "New York"),
    )
    aux_office_employee = Employee(
        "",
        Address("123 South Road", 0, "New York"),
    )

    @staticmethod
    def __new_employee(proto: Employee, name: str, suite: int) -> Employee:
        result = copy.deepcopy(proto)
        result.name = name
        result.address.suite = suite
        return result

    @staticmethod
    def new_main_office_employee(name: str, suite: int) -> Employee:
        return EmployeeFactory.__new_employee(EmployeeFactory.main_office_employee, name, suite)

    @staticmethod
    def new_aux_office_employee(name: str, suite: int) -> Employee:
        return EmployeeFactory.__new_employee(EmployeeFactory.aux_office_employee, name, suite)


if __name__ == "__main__":
    john = EmployeeFactory.new_main_office_employee("John", 101)
    print(john)
    jack = EmployeeFactory.new_aux_office_employee("Jack", 102)
    print(jack)
