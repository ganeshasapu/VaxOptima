"""File for the representation of the world graph"""
import DataManipulation as dm


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


def initialize_all_countries() -> dict:
    """Helper method to initialize all exporting countries"""
    countries = dm.get_all_countries()
    country_populations = dm.get_country_pop()
    country_vax_hesitancy = dm.get_all_countries_vaxhesitancy()  # TODO do we need this
    country_vax_rate = dm.get_all_country_vaxrate()

    exporters = dm.VACCINE_EXPORTERS
    export_rate = dm.get_export_rate()

    all_countries = {"Exporters": {}, "Countries": {}}
    for c in countries:
        if c not in exporters:
            all_countries["Countries"][c] = Country(name=c,
                                                    population=country_populations[c],
                                                    vaccine_rate=country_vax_rate[c])
        else:
            edges = _get_edges(c, countries, country_populations, country_vax_rate)
            all_countries["Exporters"][c] = ExportingCountry(name=c,
                                                             population=country_populations[c],
                                                             vaccine_rate=country_vax_rate[c],
                                                             export_rate=export_rate[c],
                                                             edges=edges)
    return all_countries


def _get_edges(exporter: str, countries: set, populations: dict, vax_rates: dict) -> dict:
    """Gets all edges to all other countries other than exporters"""
    shipment_times = dm.get_all_countries_shipment_time()

    edges = {}
    for c in countries:
        if c != exporter:
            edges[c] = Edge(importer=Country(name=c,
                                             population=populations[c],
                                             vaccine_rate=vax_rates[c]),
                            shipment_time=shipment_times[c])

    return edges
