"""
File that performs the genetic algorithm
"""

from dataclasses import dataclass
from WorldGraph import World, ExportingCountry, Country, Edge
import random
from typing import Optional
import pandas

CROSSOVER_AGGRESSION_RATE = 0.45


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

    def fitness(self, world: World, num_timestamps: int) -> None:
        """Runs simulation and gives a fitness score to the gene"""
        vaccine_shipments: list[VaccineShipment] = []
        exporters = list(world.exporting_countries.keys())
        for i in range(num_timestamps):
            for shipment in vaccine_shipments:
                # updating shipments
                shipment.time_left -= 1
                if shipment.time_left == 0:
                    # shipment has arrived to country
                    world.export_vaccine(
                        importer=shipment.importing_country, vaccine_amount=shipment.vaccine_amount)
                    vaccine_shipments.remove(shipment)
            for exporter in exporters:
                for country, vaccine_amount in self.vaccine_distribution[exporter][i]:
                    exporter_obj = world.exporting_countries[exporter]
                    # adding shipment to stack
                    vaccine_shipments.append(VaccineShipment(
                        importing_country=world.countries[country], vaccine_amount=vaccine_amount, time_left=exporter_obj.edges[country].shipment_time))
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
    gene_data: pandas.DataFrame

    def __init__(self, genes: list[Gene]) -> None:
        self.genes = genes
        self.gene_data = pandas.DataFrame(
            columns=["Country", "Average Vaccinated"])

    def fitness(self, world: World, num_timestamps: int):
        """Runs simulation and gives a fitness score to the each of the genes in the chromosome"""
        for gene in self.genes:
            gene.fitness(world=world, num_timestamps=num_timestamps)
            world.reset()

    def calculate_average_fitness(self) -> float:
        """Calculates the average fitness of the genes in the chromosome"""
        return sum([gene.fitness_value for gene in self.genes]) / len(self.genes)

    def calculate_mode_fitness(self) -> float:
        """Calculates the mode fitness of the genes in the chromosome"""
        fitness_values = [gene.fitness_value for gene in self.genes]
        return max(set(fitness_values), key=fitness_values.count)

    def calculate_median_fitness(self) -> float:
        """Calculates the median fitness of the genes in the chromosome"""
        fitness_values = [gene.fitness_value for gene in self.genes]
        fitness_values.sort()
        return fitness_values[len(fitness_values) // 2]

    def calculate_maximum_fitness(self) -> float:
        """Calculates the maximum of all genes in the chromosome"""
        fitness_values = [gene.fitness_value for gene in self.genes]
        return max(fitness_values)

    def calculate_minimum_fitness(self) -> float:
        """Calculates the worst gene in the chromosome"""
        fitness_values = [gene.fitness_value for gene in self.genes]
        return min(fitness_values)

    def __str__(self) -> str:
        string = ""
        for i in range(len(self.genes)):
            string += f"Gene {i + 1}: {self.genes[i]}\n\n"
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
    num_best_genes: int
    chromosome_dict: dict[int, dict[str, float]] = {}
    chromosome_dataframe: pandas.DataFrame

    world_graph: World
    num_timestamps: int
    data_record: pandas.DataFrame

    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int, world: World, num_timestamps: int, num_best_genes: int) -> None:
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosome_size = chromosome_size
        self.num_chromosomes = num_chromosomes
        self.world_graph = world
        self.num_timestamps = num_timestamps
        self.num_best_genes = num_best_genes

    def run(self) -> Chromosome:
        """Runs the genetic algorithm and returns the final chromosome"""
        # print("Generation 0: Initial Chromosome")
        index_so_far = 0
        chromosome = self.create_initial_chromosome()
        self.chromosome_dict[index_so_far] = self.average_percentage_vaccinated(
            self.world_graph, chromosome)
        chromosome.fitness(
            num_timestamps=self.num_timestamps, world=self.world_graph)
        for i in range(self.num_chromosomes):
            # print(f"Generation {i + 1}: {chromosome}")
            chromosome = self.selection(chromosome=chromosome)
            chromosome.fitness(world=self.world_graph,
                               num_timestamps=self.num_timestamps)
            self.chromosome_dict[index_so_far + 1] = self.average_percentage_vaccinated(
                self.world_graph, chromosome)
            index_so_far += 1
            print(
                f"Generation {i + 1} mean : {chromosome.calculate_average_fitness()} min: {min([gene.fitness_value for gene in chromosome.genes])} max: {max([gene.fitness_value for gene in chromosome.genes])}")
        # self.data_record.to_csv("data.csv", index=False)
            self.chromosome_dataframe = pandas.DataFrame.from_dict(
                self.chromosome_dict, orient='index')
        return chromosome

    def record_data(self, generation: int):
        """Records the data from the current generation"""
        for country in self.world_graph.countries.values():
            list_row = [generation, country.name,
                        country.vaccinated_population / country.population]
            df = self.data_record
            df.loc[len(df)] = list_row

    def create_initial_chromosome(self) -> Chromosome:
        """Creates the initial chromosome
        """
        genes: list[Gene] = []
        timestamps_vaccine_amount = generate_timestamp_vaccine_amount(
            num_timestamps=self.num_timestamps, world=self.world_graph)
        countries = list(self.world_graph.countries.keys())
        exporting_countries = list(self.world_graph.exporting_countries.keys())

        for i in range(self.chromosome_size):
            vaccine_distribution = {}  # Building up gene
            for exporter in exporting_countries:
                exporter_vaccine_amounts = timestamps_vaccine_amount[exporter.name]
                # each exporter has a list of shipments
                vaccine_distribution[exporter] = []
                for i in range(len(exporter_vaccine_amounts)):
                    chosen_countries = []  # list of countries that have already been chosen
                    # each timestamp has a list of shipments
                    vaccine_distribution[exporter].append([])
                    # total amount of vaccines at timestamp i (decreases as we pick countries)
                    total_vaccine_amount = exporter_vaccine_amounts[i]
                    while True:
                        # picks between 1/4 and 1/2 of the total amount of vaccines at timestamp i
                        selected_amount = random.randint(
                            exporter_vaccine_amounts[i] // 4, exporter_vaccine_amounts[i] // 2)
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

    def pick_best_genes(self, num_genes: int, genes: list[Gene]) -> list[Gene]:
        """Returns the best genes from the list of genes"""
        genes.sort(key=lambda x: x.fitness_value)
        return genes[:num_genes]

    def pick_random_option(self, remove_crossover: bool) -> str:
        """Returns a random option from the options of replication, mutation, and crossover"""
        if remove_crossover:
            weighted_randint = random.uniform(
                0, self.replication_rate + self.mutation_rate)
            if weighted_randint <= self.replication_rate:
                return 'replication'
            else:
                return 'mutation'
        weighted_randint = random.uniform(
            0, self.replication_rate + self.mutation_rate + self.crossover_rate)
        if weighted_randint <= self.replication_rate:
            return 'replication'
        elif weighted_randint <= self.replication_rate + self.mutation_rate:
            return 'mutation'
        else:
            return 'crossover'

    def selection(self, chromosome: Chromosome) -> Chromosome:
        """Select the best genes from the chromosome and perform crossover, mutation, and replication on the best genes and returns a chromosome including these genes"""
        # ("fitnesses: ", [gene.fitness_value for gene in chromosome.genes])
        # print("Average fitness: ", chromosome.calculate_average_fitness())

        best_genes = self.pick_best_genes(
            genes=chromosome.genes, num_genes=self.num_best_genes)
        next_chromosome_genes = []

        current_gene_index = 0

        while len(next_chromosome_genes) != self.chromosome_size:
            # randomly choosing which type of change to make
            if len(next_chromosome_genes) == self.chromosome_size - 1:  # Removing crossover option
                change_option = self.pick_random_option(remove_crossover=True)
            else:
                change_option = self.pick_random_option(remove_crossover=False)

            if change_option == 'replication':
                next_chromosome_genes.append(
                    self.replication(best_genes[current_gene_index]))
            elif change_option == 'mutation':
                next_chromosome_genes.append(
                    self.mutation_aggressive(best_genes[current_gene_index]))
            else:
                # picking a random secondary gene to crossover with
                crossover_index = random.randint(0, len(best_genes) - 2)
                if crossover_index >= current_gene_index:
                    crossover_index += 1
                next_chromosome_genes.extend(self.crossover_aggressive(
                    best_genes[current_gene_index], best_genes[crossover_index]))
            current_gene_index = (current_gene_index + 1) % len(best_genes)
        return Chromosome(next_chromosome_genes)

    def crossover(self, gene1: Gene, gene2: Gene) -> list[Gene]:
        """Performs crossover on the two genes and returns a list of the two children genes"""
        # print(Chromosome([gene1, gene2]))
        gene1_copy = Gene(vaccine_distribution=gene1.vaccine_distribution)
        gene2_copy = Gene(vaccine_distribution=gene2.vaccine_distribution)
        for exporter in gene1_copy.vaccine_distribution:
            for i in range(len(gene1_copy.vaccine_distribution[exporter])):
                truth_value = random.choice([True, False])
                if truth_value:
                    gene1_copy.vaccine_distribution[exporter][i], gene2_copy.vaccine_distribution[exporter][
                        i] = gene2_copy.vaccine_distribution[exporter][i], gene1_copy.vaccine_distribution[exporter][i]
        return [gene1_copy, gene2_copy]

    def crossover_aggressive(self, gene1: Gene, gene2: Gene) -> list[Gene]:
        """Performs crossover on the two genes and returns a list of the two children genes aggressively"""
        gene1_copy = Gene(vaccine_distribution=gene1.vaccine_distribution)
        gene2_copy = Gene(vaccine_distribution=gene2.vaccine_distribution)
        for exporter in gene1_copy.vaccine_distribution:
            for i in range(len(gene1_copy.vaccine_distribution[exporter])):
                occurrence_percentage = CROSSOVER_AGGRESSION_RATE
                crossover_probability = random.uniform(0, 1)
                if crossover_probability > occurrence_percentage:
                    gene1_copy.vaccine_distribution[exporter][i], gene2_copy.vaccine_distribution[exporter][
                        i] = gene2_copy.vaccine_distribution[exporter][i], gene1_copy.vaccine_distribution[exporter][i]
        return [gene1_copy, gene2_copy]

    def mutation_aggressive(self, gene: Gene) -> Gene:
        """Performs mutation on the gene and returns the mutated gene aggressively"""
        new_vaccine_distribution = {}
        # traversing through the vaccine distribution of the gene
        for exporter in gene.vaccine_distribution:
            list_of_timestamps = []
            for timestamp in gene.vaccine_distribution[exporter]:
                # pass each timestamp to the mutation helper to mutate it
                list_of_timestamps.append(
                    self.mutation_helper_aggressive(timestamp))
                # reassign the mutated timestamp to the mutation helper
                new_vaccine_distribution[exporter] = list_of_timestamps
        return Gene(vaccine_distribution=new_vaccine_distribution)

    def mutation_helper_aggressive(self, timestamp: list[tuple]) -> list[tuple]:
        timestamp_copy = timestamp.copy()
        newest_timestamp = []
        for _ in range(len(timestamp_copy)):
            mutated_tuple = timestamp_copy.pop()
            mutated_tuple = (mutated_tuple[0], random.randint(
                int(mutated_tuple[1] * 0.5), int(mutated_tuple[1] * 1.5)))
            newest_timestamp.append(mutated_tuple)
        for tuple in timestamp_copy:
            if tuple[0] not in [tup[0] for tup in newest_timestamp]:
                newest_timestamp.append(tuple)
        return newest_timestamp

    def mutation(self, gene: Gene) -> Gene:
        """Performs mutation on the gene and returns the mutated gene"""
        new_vaccine_distribution = {}
        # traversing through the vaccine distribution of the gene
        for exporter in gene.vaccine_distribution:
            list_of_timestamps = []
            for timestamp in gene.vaccine_distribution[exporter]:
                # pass each timestamp to the mutation helper to mutate it
                list_of_timestamps.append(self.mutation_helper(timestamp))
                # reassign the mutated timestamp to the mutation helper
                new_vaccine_distribution[exporter] = list_of_timestamps
        return Gene(vaccine_distribution=new_vaccine_distribution)

    def mutation_helper(self, timestamp: list[tuple]) -> list[tuple]:
        timestamp_copy = timestamp.copy()
        newest_timestamp = []
        num = random.randint(0, len(timestamp))
        while num != 0:
            mutated_tuple = timestamp_copy.pop()
            mutated_tuple = (mutated_tuple[0], random.randint(
                int(mutated_tuple[1] * 0.8), int(mutated_tuple[1] * 1.2)))
            newest_timestamp.append(mutated_tuple)
            num -= 1
        for tuple in timestamp_copy:
            if tuple[0] not in [tup[0] for tup in newest_timestamp]:
                newest_timestamp.append(tuple)
        return newest_timestamp

    def replication(self, gene: Gene) -> Gene:
        """Returns the replicated gene"""
        return Gene(vaccine_distribution=gene.vaccine_distribution)

    def average_percentage_vaccinated(self, world: World, chromosome: Chromosome) -> dict[str, float]:
        """Calculates the average percentage of vaccinated people in each country in a gene in a chromosome"""
        countries2 = {}
        countries_with_genes = {}
        for gene in chromosome.genes:
            for exporter in gene.vaccine_distribution:
                for timestamp in gene.vaccine_distribution[exporter]:
                    for tpl in timestamp:
                        if tpl[0] not in countries2:
                            countries2[tpl[0]] = tpl[1]
                        else:
                            countries2[tpl[0]] += tpl[1]
            countries_with_genes[gene] = countries2
            countries2 = {}
        for gene in countries_with_genes:
            for country in countries_with_genes[gene]:
                countries_with_genes[gene][country] = countries_with_genes[gene][country] / \
                    self.world_graph.countries[country].population

        countries_with_weighted_avg = {}
        for gene in countries_with_genes:
            for country in countries_with_genes[gene]:
                if country not in countries_with_weighted_avg:
                    countries_with_weighted_avg[country] = countries_with_genes[gene][country]
                else:
                    countries_with_weighted_avg[country] += countries_with_genes[gene][country]
        for country in countries_with_weighted_avg:
            countries_with_weighted_avg[country] = countries_with_weighted_avg[country] / len(
                chromosome.genes)
        return countries_with_weighted_avg


def generate_timestamp_vaccine_amount(num_timestamps, world) -> list[int]:
    """Generates a list of the amount of vaccines at each timestamp"""
    timestamps_vaccine_amount = {}
    for exporter in world.exporting_countries.values():
        timestamps_vaccine_amount[exporter.name] = []
        for i in range(num_timestamps):
            timestamps_vaccine_amount[exporter.name].append(
                (i+1) * exporter.export_rate * 10_000_000)
    return timestamps_vaccine_amount
