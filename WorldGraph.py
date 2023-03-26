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

    def __init__(self, name: str, vaccine_rate: float, population: int):
        self.name = name
        self.vaccine_rate = vaccine_rate
        self.population = population
        self.vaccinated_population = 0
        self.vaccines_held = 0

    def vaccinate(self):
        """Vaccinates the country"""
        amount_vaxinated = self.vaccine_rate * self.vaccines_held
        if amount_vaxinated > self.population - self.vaccinated_population:
            self.vaccinated_population = self.population
        else:
            self.vaccinated_population += amount_vaxinated

    def __str__(self):
        return f"{self.name}: {self.vaccinated_population} / {self.population}"


class Edge:
    """A class that represents an edge between an exporter and importer.
    Equivalent to a directed and weighted edge."""
    importer: Country
    shipment_time: int
    buffer_vaccine_shipments: list[tuple[int, int]] = []

    def __init__(self, importer: Country, shipment_time: int):
        self.importer = importer
        self.shipment_time = shipment_time
        self.buffer_vaccine_shipments = []


class ExportingCountry(Country):
    """Class that represents a country exporting vaccines."""
    export_rate: float
    edges: dict[str: Edge]

    def __init__(self, name: str, vaccine_rate: float, export_rate: float, edges: dict[str: Edge], population: int):
        super().__init__(name=name, vaccine_rate=vaccine_rate, population=population)
        self.export_rate = export_rate
        self.edges = edges


class World:
    """A class representing the world. Equivalent to Graph."""
    exporting_countries: dict[str: ExportingCountry]
    countries: dict[str: Country]

    def __init__(self, countries: dict, exporting_countries: dict):
        self.countries = countries
        self.exporting_countries = exporting_countries

    def create_countries(self) -> dict[str | Country]:
        """Function that helps initialize World, returns a dict of all countries in the world"""
        pass

    def create_exporting_countries(self) -> dict[str | ExportingCountry]:
        """Function that helps initialzie World, returns a list of all exporting countries in the world"""
        pass

    def reset(self):
        """Resets the world to the initial state"""
        for country in self.countries.values():
            country.vaccinated_population = 0
            country.vaccines_held = 0
        for exporter in self.exporting_countries.values():
            exporter.vaccines_held = 0
            exporter.vaccinated_population = 0
            for edge in exporter.edges.values():
                edge.buffer_vaccine_shipments = []

        # for country in self.countries.values():
        #     print("Vaccinaed pop ", country.vaccinated_population)
        #     print("Vaccinaed Held ", country.vaccines_held)
        # for exporter in self.exporting_countries.values():
        #     print("Vaccines Held", exporter.vaccines_held)
        #     print("Vaccinaed pop ", exporter.vaccinated_population)
        #     for edge in exporter.edges.values():
        #         print("vax ship", edge.buffer_vaccine_shipments)

    def export_vaccine(self, importer: Country, vaccine_amount: int):
        """Export vaccine"""
        importer.vaccines_held += vaccine_amount

    def check_termination(self) -> bool:
        """Checks if the 70% population has been vaccinated"""
        tot_vaccinated = 0
        tot_pop = 0
        for country in self.countries.values():
            tot_vaccinated += country.vaccinated_population
            tot_pop += country.population
        return tot_vaccinated / tot_pop >= 0.7
