class World: # Equivalent to Graph
    countries: set
    edges: set

    def __init__(self, countries: set, edges: set):
        self.countries = countries
        self.edges = edges

class Country: # Equivalent to Vertex
    pass

class Edge: # Equivalent to Edge
    pass

class ExportingCountry(Country): # Exporting Countries
    pass