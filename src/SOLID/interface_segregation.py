# no code should be forced to depend on methods it does not use

# Standard library imports
# WRONG
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class Document:
    pass


class Device:
    def print(self, document: Document) -> None:
        raise NotImplementedError

    def fax(self, document: Document) -> None:
        raise NotImplementedError

    def scan(self, document: Document) -> None:
        raise NotImplementedError


class MultiFunctionPrinter(Device):
    def print(self, document: Document) -> None:
        # code goes here
        pass

    def fax(self, document: Document) -> None:
        # code goes here
        pass

    def scan(self, document: Document) -> None:
        # code goes here
        pass


class SingleFunctionPrinter(Device):
    def print(self, document: Document) -> None:
        # code goes here
        pass

    def fax(self, document: Document) -> None:
        """Not supported!"""
        # 1. do nothing
        # problem: induces false client expectations
        pass

    def scan(self, document: Document) -> None:
        """Not supported!"""
        # 2. raise error
        # problem: application crash
        raise NotImplementedError("Printer cannot fax")


# RIGHT
# Split large interface into the smallest possible interfaces
# so the client code does not have to implement methods it does not need
class Printer(metaclass=ABCMeta):
    @abstractmethod
    def print(self, document: Document) -> None:
        pass


class Telecopier(metaclass=ABCMeta):
    @abstractmethod
    def fax(self, document: Document) -> None:
        pass


class Scanner(metaclass=ABCMeta):
    @abstractmethod
    def scan(self, document: Document) -> None:
        pass


class Photocopier(Printer, Scanner):
    def print(self, document: Document) -> None:
        pass

    def scan(self, document: Document) -> None:
        pass


class MultiFunctionDevice(Printer, Telecopier, Scanner):
    @abstractmethod
    def print(self, document: Document) -> None:
        pass

    @abstractmethod
    def fax(self, document: Document) -> None:
        pass

    @abstractmethod
    def scan(self, document: Document) -> None:
        pass


class HomePrinter(MultiFunctionDevice):
    printer: Printer
    telecopier: Telecopier
    scanner: Scanner

    def __init__(
        self, printer: Printer, telecopier: Telecopier, scanner: Scanner
    ) -> None:
        super().__init__()
        self.printer = printer
        self.telecopier = telecopier
        self.scanner = scanner

    def print(self, document: Document) -> None:
        self.printer.print(document)

    def fax(self, document: Document) -> None:
        self.telecopier.fax(document)

    def scan(self, document: Document) -> None:
        self.scanner.scan(document)
