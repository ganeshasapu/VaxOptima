"""File for the representation of the world graph"""


class Country:
    """Class that represents a Country. Equivalent to Vertex in Graph

    Instance Attributes:
    - name:
        name of country
    - vaccine_rate:
        vaccine rate of country

    """
    name: str
    vaccine_rate: float

    def __init__(self, name: str, vaccine_rate: float):
        self.name = name
        self.vaccine_rate = vaccine_rate


class ExportingCountry(Country):
    """Class that represents a country exporting vaccines."""
    export_rate: float
    vaccine_supply: int

class Edge:
    """A class that represents an edge between an exporter and importer.
    Equivalent to a directed and weighted edge."""
    exporter: ExportingCountry
    importer: Country
    shipment_time: int

class World:
    """A class representing the world. Equivalent to Graph."""
    countries: set[Country | ExportingCountry]
    edges: set[Edge]

    def __init__(self, countries: set, edges: set):
        self.countries = countries
        self.edges = edges
