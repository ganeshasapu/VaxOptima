class Country:
    """Class that represents a Country. Equivalent to Vertex in Graph"""
    name: str

    def __init__(self, name: str):
        self.name = name

class ExportingCountry(Country):
    """Class that represents a country exporting vaccines."""
    # Vaccine Export Rate
    # Vaccine Stored Amount
    pass

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