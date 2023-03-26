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
    population: int
    vaccinated_population: int
    vaccines_held: int
    vaccine_rate: float

    def __init__(self, name: str, vaccine_rate: float):
        self.name = name
        self.vaccine_rate = vaccine_rate
    
    def vaccinate(self):
        """Vaccinates the country"""
        amount_vaxinated = self.vaccine_rate * self.vaccines_held
        if amount_vaxinated > self.population - self.vaccinated_population:
            self.vaccinated_population = self.population
        else:
            self.vaccinated_population += amount_vaxinated


class Edge:
    """A class that represents an edge between an exporter and importer.
    Equivalent to a directed and weighted edge."""
    importer: Country
    shipment_time: int
    buffer_vaccine_shipments: list[tuple(int, int)]

    def __init__(self, importer: Country, shipment_time: int, buffer_vaccines: int):
        self.importer = importer
        self.shipment_time = shipment_time
        self.buffer_vaccines = buffer_vaccines


class ExportingCountry(Country):
    """Class that represents a country exporting vaccines."""
    export_rate: float
    vaccine_supply: int
    edges: dict[str: Edge]

    def __init__(self, name: str, vaccine_rate: float, export_rate: float, vaccine_supply: int):
        super().__init__(name, vaccine_rate)
        self.export_rate = export_rate
        self.vaccine_supply = vaccine_supply
        self.edges = {}



class World:
    """A class representing the world. Equivalent to Graph."""
    exporting_countries: dict[str: ExportingCountry]
    countries: dict[str: Country]

    def __init__(self, countries: dict):
        self.countries = countries
    
    def export_vaccine(self, exporter:ExportingCountry, importer: Country, vaccine_amount: int):
        exporter.vaccine_supply -= vaccine_amount
        importer.vaccines_held += vaccine_amount

    def check_termination(self) -> bool:
        """Checks if the 70% population has been vaccinated"""
        tot_vaccinated = 0
        tot_pop = 0
        for country in self.countries.values():
            tot_vaccinated += country.vaccinated_population
            tot_pop += country.population
        return tot_pop / tot_vaccinated >= 0.7
