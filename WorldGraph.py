"""
File for the representation of the world graph
"""

class Country:
    """Class that represents a Country. Equivalent to Vertex in Graph
    
    Instance Attributes:
    - 
    """
    name: str
    population: int
    vaccinated_population: int

    def __init__(self, name: str):
        self.name = name

class Edge:
    """A class that represents an edge between an exporter and importer. 
    Equivalent to a directed and weighted edge."""
    importer: Country
    shipment_time: int
    buffer_vaccines: int

class ExportingCountry(Country):
    """Class that represents a country exporting vaccines."""
    export_rate: float
    vaccine_supply: int
    edges: set[Edge]

class World:
    """A class representing the world. Equivalent to Graph."""
    exporting_countries: dict[str: ExportingCountry]
    countries: set[Country]

    def __init__(self, countries: set, edges: set):
        self.countries = countries
    
    def export_vaccine(self, exporter:ExportingCountry, importer: Country, vaccine_amount: int):
        self.exporting_countries[exporter].edges[importer].vaccinated_population += vaccine_amount

    def check_termination(self) -> bool:
        """Checks if the 70% population has been vaccinated"""
        vaccinated_population = 0
        total_population = 0
        for country in self.countries:
            vaccinated_population += country.vaccinated_population
            total_population += country.population
        return vaccinated_population / total_population >= 0.7