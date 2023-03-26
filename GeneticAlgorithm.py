"""
File that performs the genetic algorithm
"""

from WorldGraph import World, ExportingCountry, Country, Edge
import random

class Gene:
    termination_timestamp: int | None
    vaccine_distribution: dict[dict[str: list[list[tuple[str, int]]]]]
    # Exporter -> Timestamp -> List of (Country, Vaccine Amount)
    # Example vaccine distribution (max 10 countries, 2 timestamp): {
    #    "exporter1": [[("country1", 5000), ("country2", 10000)], [("country8", 5000)]],
    #    "exporter2": [[("country4", 5000), ("country5", 10000)], [("country2", 5000)]],
    #    "exporter3": [[("country6", 5000), ("country3", 10000)], [("country3", 5000)]]
    # }


    def __init__(self, termination_timestamp: int | None, vaccine_distribution: dict):
        self.termination_timestamp = termination_timestamp
        self.vaccine_distribution = vaccine_distribution

    def __str__(self):
        return f"Termination Timestamp: {self.termination_timestamp}, Vaccine Distribution: {self.vaccine_distribution}"


class Chromosome:
    """A chromosome is a list of genes"""
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

    chromosome_size: int
    num_chromosomes: int
    world: World

    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int, world: World):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosome_size = chromosome_size
        self.num_chromosomes = num_chromosomes
        self.world = world

    def run(self) -> Chromosome:
        """Runs the genetic algorithm and returns the final chromosome"""
        pass

    def create_initial_chromosome(self) -> Chromosome:
        """Creates the initial chromosome
        """
        timestamps_vaccine_amount = [100, 200, 300]
        exporters = ["exporter1", "exporter2"]
        countries = ["country1", "country2"]

        genes = []
        for i in range(self.chromosome_size):
            vaccine_distribution = {}
            for exporter in exporters:
                vaccine_distribution[exporter] = []
                for i in range(len(timestamps_vaccine_amount)):
                    chosen_countries = [] # list of countries that have already been chosen
                    vaccine_distribution[exporter].append([])  
                    total_vaccine_amount = timestamps_vaccine_amount[i] # total amount of vaccines at timestamp i (decreases as we pick countries)
                    while True:
                        # picks between 1/4 and 1/2 of the total amount of vaccines at timestamp i
                        selected_amount = random.randint(timestamps_vaccine_amount[i] // 4, timestamps_vaccine_amount[i] // 2)
                        countries_left  = list(set(countries).difference(set(chosen_countries)))
                        selected_country = random.choice(countries_left)
                        # 1 country left or chosen amount is greater than the amount of vaccines left
                        if len(chosen_countries) == len(countries) - 1 or total_vaccine_amount <= selected_amount:
                            print(total_vaccine_amount)
                            vaccine_distribution[exporter][i].append((selected_country, total_vaccine_amount))
                            break
                        vaccine_distribution[exporter][i].append((selected_country, selected_amount)) 
                        total_vaccine_amount -= selected_amount
                        chosen_countries.append(selected_country)
            genes.append(Gene(None, vaccine_distribution))

        return chromosome(genes)

    def selection(self, chromosome: Chromosome) -> Chromosome:
        """Select the best genes from the chromosome and perform crossover, mutation, and replication on the best genes and returns a chromosome including these genes"""
        most_fit_genes_so_far = []
        minimum_fitness_value = min([gene.fitness_value for gene in chromosome.genes])
        for gene in chromosome.genes:
            if len(most_fit_genes_so_far) == 2:
                return most_fit_genes_so_far
            if gene.fitness_value == minimum_fitness_value:
                most_fit_genes_so_far.append(gene)

    def crossover(self, gene1: Gene, gene2: Gene) -> list[Gene]:
        """Performs crossover on the two genes and returns a list of the two children genes"""
        pass

    def mutation(self, gene: Gene) -> Gene:
        """Performs mutation on the gene and returns the mutated gene"""
        pass

    def replication(self, gene: Gene) -> Gene:
        """Returns the replicated gene"""
        return gene
