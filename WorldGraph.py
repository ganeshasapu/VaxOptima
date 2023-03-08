class Country: # Equivalent to Vertex
    name: str

    def __init__(self, name: str):
        self.name = name

class ExportingCountry(Country): # Exporting Countries
    # Vaccine Export Rate
    # Vaccine Stored Amount
    pass

class Edge: # Equivalent to Edge
    exporter: ExportingCountry
    importer: Country
    shipment_time: float

class World: # Equivalent to Graph
    countries: set[Country | ExportingCountry]
    edges: set[Edge]

    def __init__(self, countries: set, edges: set):
        self.countries = countries
        self.edges = edges