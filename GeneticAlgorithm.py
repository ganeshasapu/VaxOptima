"""
File that performs the genetic algorithm
"""

from WorldGraph import World, ExportingCountry, Country, Edge
import random
timestamps_vaccine_amount = [100, 200, 300]
exporters = ["exporter1", "exporter2"]
countries = ["country1", "country2"]
world = World()

class Gene:
    termination_timestamp: int | None
    vaccine_distribution: dict[str: list[list[tuple[str, int]]]]
    # Exporter -> Timestamp -> List of (Country, Vaccine Amount)
    # Example vaccine distribution (2 exporters, 2 countries, 3 timestamps): 
    # {
    # 'exporter1': [[('country1', 48), ('country2', 52)], [('country2', 63), ('country1', 137)], [('country2', 105), ('country1', 195)]], 
    # 'exporter2': [[('country2', 39), ('country1', 61)], [('country2', 81), ('country1', 119)], [('country2', 139), ('country1', 161)]]
    # }


    def __init__(self, termination_timestamp: int | None, vaccine_distribution: dict):
        self.termination_timestamp = termination_timestamp
        self.vaccine_distribution = vaccine_distribution

    def __str__(self):
        return f"Termination Timestamp: {self.termination_timestamp}, Vaccine Distribution: {self.vaccine_distribution}"

    def fitness(self, world: World):
        """Runs simulation and gives a fitness score to the gene"""
        for i in range(len(timestamps_vaccine_amount)):
            for exporter in exporters:
                for country, vaccine_amount in self.vaccine_distribution[exporter][i]:
                    world.export_vaccine(exporter, country, vaccine_amount, i)
            if world.check_termination():
                self.termination_timestamp = i
                break




class Chromosome:
    """A chromosome is a list of genes"""
    genes: list[Gene]

    def __init__(self, genes: list[Gene]):
        self.genes = genes

    def fitness(self, world: World):
        """Runs simulation and gives a fitness score to the each of the genes in the chromosome"""
        for gene in self.genes:
            gene.fitness(world=world.copy())

        

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

    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosome_size = chromosome_size
        self.num_chromosomes = num_chromosomes

    def run(self) -> Chromosome:
        """Runs the genetic algorithm and returns the final chromosome"""
        pass

    def create_initial_chromosome(self) -> Chromosome:
        """Creates the initial chromosome
        """
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

        return Chromosome(genes)

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
