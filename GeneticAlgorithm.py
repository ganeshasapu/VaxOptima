"""
File that performs the genetic algorithm
"""

from dataclasses import dataclass
from WorldGraph import World, ExportingCountry, Country, Edge
import random
from typing import Optional


class Gene:
    """
    A gene is a mapping of exporting countries to a list of importing countries while also specifying their chronological order of the exports

    Instance Attributes:
        - fitness_value: the fitness value of the gene obtained by passing the gene into the fitness function
        - vaccine_distribution: a dictionary mapping an exporter to a list of tuples of importing countries and the amount of vaccines to be exported to them
    Notes:
     - vaccine_distribution is ordered in chronological order by the concept of timestamps
    """

    fitness_value: Optional[int]
    vaccine_distribution: dict[str: list[list[tuple[str, int]]]]
    # Exporter -> Timestamp -> List of (Country, Vaccine Amount)
    # Example vaccine distribution (2 exporters, 2 countries, 3 timestamps):
    # {
    # 'exporter1': [[('country1', 48), ('country2', 52)], [('country2', 63), ('country1', 137)], [('country2', 105), ('country1', 195)]],
    # 'exporter2': [[('country2', 39), ('country1', 61)], [('country2', 81), ('country1', 119)], [('country2', 139), ('country1', 161)]]
    # }

    def __init__(self, vaccine_distribution: dict, fitness_value: Optional[int] = None) -> None:
        self.fitness_value = fitness_value
        self.vaccine_distribution = vaccine_distribution

    def __str__(self) -> str:
        return f"Termination Timestamp: {self.fitness_value}, Vaccine Distribution: {self.vaccine_distribution}"

    def fitness(self, world: World, num_timestamps: int):
        """Runs simulation and gives a fitness score to the gene"""
        vaccine_shipiments: list[VaccineShipment] = []
        exporters = list(world.exporting_countries.keys())
        for i in range(num_timestamps): 
            for exporter in exporters:
                for country, vaccine_amount in self.vaccine_distribution[exporter][i]:
                    exporter_obj = world.exporting_countries[exporter]
                    # adding shipment to stack
                    vaccine_shipiments.append(VaccineShipment(importing_country=world.countries[country], vaccine_amount=vaccine_amount, time_left=exporter_obj.edges[country].shipment_time))
            for shipment in vaccine_shipiments:
                # updating shipments
                shipment.time_left -= 1
                if shipment.time_left == 0:
                    # shipment has arrived to country
                    world.export_vaccine(importer=shipment.importing_country, vaccine_amount=shipment.vaccine_amount)
                    vaccine_shipiments.remove(shipment)
            for country in world.countries.values():
                # country distributes vaccines to its population
                country.vaccinate()
            if world.check_termination():
                # if 70% of the population is vaccinated, terminate
                self.fitness_value = i
                return
        self.fitness_value = num_timestamps


@dataclass
class VaccineShipment:
    importing_country: Country
    vaccine_amount: int
    time_left: int


class Chromosome:
    """A chromosome is a list of genes

    Instance Attributes:
        - genes: a list of genes
    """
    genes: list[Gene]

    def __init__(self, genes: list[Gene]) -> None:
        self.genes = genes

    def fitness(self, world: World, num_timestamps: int):
        """Runs simulation and gives a fitness score to the each of the genes in the chromosome"""
        for gene in self.genes:
            gene.fitness(world=world, num_timestamps=num_timestamps)
            world.reset()
        
    def __str__(self) -> str:
        string = ""
        for gene in self.genes:
            string += str(gene) + "\n"
        return string


class GeneticAlgorithm:
    """
    A GeneticAlgorithm is a class that performs the genetic algorithm on a world graph

    Instance Attributes:
        - replication_rate: the rate at which the best genes are replicated
        - mutation_rate: the rate at which the best genes are mutated
        - crossover_rate: the rate at which the best genes are crossed over
        - gene_count: the number of genes in a chromosome
        - num_chromosomes: the number of chromosomes in a population
        - world: the world graph

    """
    replication_rate: float
    mutation_rate: float
    crossover_rate: float
    chromosome_size: int
    num_chromosomes: int

    world_graph: World
    num_timestamps: int

    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int, world: World, num_timestamps: int):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosome_size = chromosome_size
        self.num_chromosomes = num_chromosomes
        self.world_graph = world
        self.num_timestamps = num_timestamps

    def run(self) -> Chromosome:
        """Runs the genetic algorithm and returns the final chromosome"""
        chromosome = self.create_initial_chromosome()
        chromosome.fitness(
            num_timestamps=self.num_timestamps, world=self.world_graph)
        for i in range(self.num_chromosomes):
            print(i)
            chromosome = self.selection(chromosome=chromosome)
            chromosome.fitness(world=self.world_graph,
                                num_timestamps=self.num_timestamps)
        return chromosome

    def create_initial_chromosome(self) -> Chromosome:
        """Creates the initial chromosome
        """
        genes: list[Gene] = []
        timestamps_vaccine_amount = generate_timestamp_vaccine_amount(
            num_timestamps=self.num_timestamps)
        countries = list(self.world_graph.countries.keys())
        exporting_countries = list(self.world_graph.exporting_countries.keys())

        for i in range(self.chromosome_size):
            vaccine_distribution = {}  # Building up gene
            for exporter in exporting_countries:
                # each exporter has a list of shipments
                vaccine_distribution[exporter] = []
                for i in range(len(timestamps_vaccine_amount)):
                    chosen_countries = []  # list of countries that have already been chosen
                    # each timestamp has a list of shipments
                    vaccine_distribution[exporter].append([])
                    # total amount of vaccines at timestamp i (decreases as we pick countries)
                    total_vaccine_amount = timestamps_vaccine_amount[i]
                    while True:
                        # picks between 1/4 and 1/2 of the total amount of vaccines at timestamp i
                        selected_amount = random.randint(
                            timestamps_vaccine_amount[i] // 4, timestamps_vaccine_amount[i] // 2)
                        countries_left = list(
                            set(countries).difference(set(chosen_countries)))
                        # 1 country left or chosen amount is greater than the amount of vaccines left
                        selected_country = random.choice(countries_left)
                        if len(chosen_countries) == len(countries) - 1 or total_vaccine_amount <= selected_amount:
                            vaccine_distribution[exporter][i].append(
                                (selected_country, total_vaccine_amount))
                            break
                        vaccine_distribution[exporter][i].append(
                            (selected_country, selected_amount))
                        total_vaccine_amount -= selected_amount
                        chosen_countries.append(selected_country)
            genes.append(
                Gene(vaccine_distribution=vaccine_distribution, fitness_value=None))

        return Chromosome(genes)

    def selection(self, chromosome: Chromosome) -> Chromosome:
        """Select the best genes from the chromosome and perform crossover, mutation, and replication on the best genes and returns a chromosome including these genes"""
        most_fit_genes_so_far = []
        minimum_fitness_value = min(
            [gene.fitness_value for gene in chromosome.genes])
        genes_for_chromosome = []
        print([gene.fitness_value for gene in chromosome.genes])
        for gene in chromosome.genes:
            if len(most_fit_genes_so_far) == 2:
                break
            if gene.fitness_value == minimum_fitness_value:
                most_fit_genes_so_far.append(gene)
                new_lst = [gene.fitness_value for gene in chromosome.genes]
                new_lst.remove(minimum_fitness_value)
                minimum_fitness_value = min(new_lst)

        while len(genes_for_chromosome) != 10:
            index_so_far = 0
            if len(genes_for_chromosome) == 9:
                current_option = random.choice(
                    [self.replication, self.mutation])
                weighted_randint = random.uniform(
                    0, self.replication_rate + self.mutation_rate)
                if weighted_randint <= self.replication_rate:
                    current_option = 'replication'
                else:
                    current_option = 'mutation'
            else:
                weighted_randint = random.random()
                if weighted_randint <= self.replication_rate:
                    current_option = 'replication'
                elif self.replication_rate < weighted_randint <= self.mutation_rate:
                    current_option = 'mutation'
                else:
                    current_option = 'crossover'

            if current_option == 'replication':
                genes_for_chromosome.append(self.replication(
                    most_fit_genes_so_far[index_so_far]))
            elif current_option == 'mutation':
                genes_for_chromosome.append(self.mutation(
                    most_fit_genes_so_far[index_so_far]))
            else:
                crossover_index = random.randint(
                    0, len(most_fit_genes_so_far) - 1)
                while crossover_index == index_so_far:
                    crossover_index = random.randint(
                        0, len(most_fit_genes_so_far) - 1)
                genes_for_chromosome.extend(self.crossover(
                    most_fit_genes_so_far[index_so_far], most_fit_genes_so_far[crossover_index]))
            index_so_far += 1
        return Chromosome(genes_for_chromosome)

    def crossover(self, gene1: Gene, gene2: Gene) -> list[Gene]:
        """Performs crossover on the two genes and returns a list of the two children genes"""
        for exporter in gene1.vaccine_distribution:
            for i in range(len(gene1.vaccine_distribution[exporter])):
                truth_value = random.choice([True, False])
                if truth_value:
                    gene1.vaccine_distribution[exporter][i] = gene2.vaccine_distribution[exporter][i]
        return [gene1, gene2]

    def mutation(self, gene: Gene) -> Gene:
        """Performs mutation on the gene and returns the mutated gene"""
        new_vaccine_distribution = {}
        for exporter in gene.vaccine_distribution:
            list_of_timestamps = []
            for timestamp in gene.vaccine_distribution[exporter]:
                timestamp_copy = timestamp.copy()
                newest_timestamp = []
                num = random.randint(0, len(timestamp))
                while num != 0:
                    mutated_tuple = timestamp_copy.pop()
                    mutated_tuple = (mutated_tuple[0], random.randint(
                        int(mutated_tuple[1] * 0.8), int(mutated_tuple[1] * 1.2)))
                    newest_timestamp.append(mutated_tuple)
                    num -= 1
                for tuple in newest_timestamp:
                    if tuple[0] not in [tup[0] for tup in newest_timestamp]:
                        newest_timestamp.append(tuple)
                list_of_timestamps.append(newest_timestamp)
                new_vaccine_distribution[exporter] = list_of_timestamps
        return Gene(vaccine_distribution=new_vaccine_distribution)

    def replication(self, gene: Gene) -> Gene:
        """Returns the replicated gene"""
        return gene


def generate_timestamp_vaccine_amount(num_timestamps) -> list[int]:
    """Generates a list of the amount of vaccines at each timestamp"""
    timestamps_vaccine_amount = []
    for i in range(num_timestamps):
        timestamps_vaccine_amount.append(i * 100)
    return timestamps_vaccine_amount
