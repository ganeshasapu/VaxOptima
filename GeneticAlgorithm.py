"""
File that performs the genetic algorithm
"""

from WorldGraph import World, ExportingCountry, Country, Edge
import random

"""A gene is a single unit of a chromosone that informs the fitness function """
class Gene:
    termination_timestamp: int | None
    vaccine_distribution: dict[dict[str: list[int: list[tuple[str, int]]]]]
    # Exporter -> Timestamp -> List of (Country, Vaccine Amount)
    # Example vaccine distribution (max 10 countries, 2 timestamp): {
    #    "exporter1": [1: [("country1", 5000), ("country2", 10000)], 2: [("country8", 5000)]],
    #    "exporter2": [1: [("country4", 5000), ("country5", 10000)], 2: [("country2", 5000)]],
    #    "exporter3": [1: [("country6", 5000), ("country3", 10000)], 2: [("country3", 5000)]]
    # }

    def __init__(self, termination_timestamp: int | None, vaccine_distribution: dict):
        self.termination_timestamp = termination_timestamp
        self.vaccine_distribution = vaccine_distribution

    def __str__(self):
        return f"Termination Timestamp: {self.termination_timestamp}, Vaccine Distribution: {self.vaccine_distribution}"
    
"""A chromosone is a list of genes"""
class Chromosone:
    genes: list[Gene]

    def __init__(self, genes: list[Gene]):
        self.genes = genes

    def fitness(self):
        pass

    def __str__(self):
        string = ""
        for gene in self.genes:
            string += str(gene) + "\n"
        return string




class GeneticAlgorithm:
    mutation_rate: float
    crossover_rate: float
    replication_rate: float

    chromosone_size: int
    num_chromosones: int
    world: World


    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosone_size: int, num_chromosones: int, world: World):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosone_size = chromosone_size
        self.num_chromosones = num_chromosones
        self.world = world


    def run(self) -> Chromosone:
        """Runs the genetic algorithm and returns the final chromosone"""
        pass

    def create_initial_chromosone(self) -> Chromosone:
        """Creates the initial chromosone
        """
        timestamps_vaccine_amount = [100, 200, 300]
        exporters = ["exporter1", "exporter2"]
        countries = ["country1", "country2"]

        genes = []
        for i in range(self.chromosone_size):
            vaccine_distribution = {}
            for exporter in exporters:
                vaccine_distribution[exporter] = {}
                for i in range(len(timestamps_vaccine_amount)):
                    vaccine_distribution[exporter][i] = []
                    selected_amount = random.randint(0, timestamps_vaccine_amount[i])
                    selected_country = random.choice(countries)
                    vaccine_distribution[exporter][i].append((selected_country, selected_amount))
            genes.append(Gene(None, vaccine_distribution))

        return Chromosone(genes)


    def selection(self, chromosone: Chromosone) -> Chromosone:
        """Selects the best genes from the chromosone and returns a modified chromosone"""
        pass

    def crossover(self, gene1: Gene, gene2: Gene) -> list[Gene]:
        """Performs crossover on the two genes and returns a list of the two children genes"""
        pass

    def mutation(self, gene: Gene) -> Gene:
        """Performs mutation on the gene and returns the mutated gene"""
        pass

    def replication(self, gene: Gene) -> Gene:
        """Returns the replicated gene"""
        return gene
