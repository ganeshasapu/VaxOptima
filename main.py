"""Main runner file"""
import random
import WorldGraph as wg
import GeneticAlgorithm as ga
import DataManipulation as dm


def algorithm_runner_fixed(exporters_names: list, countries_names: list, num_timestamps: int, num_best_genes: int, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int, population: int, max_shipment_time: int):
    """Runs the algorithm"""

    exporters: ga.ExportingCountry = {}
    countries: ga.Country = {}
    edges = {}
    for country in countries_names:
        countries[country] = ga.Country(name=country, vaccine_rate=0.5, population=population)
    for country in countries:
        edges[country] = wg.Edge(importer=countries[country], shipment_time=random.randint(1, max_shipment_time))
    for exporter in exporters_names:
        exporters[exporter] = ga.ExportingCountry(name=exporter, vaccine_rate=random.random(), export_rate=random.random(), edges=edges, population=population)


    world = wg.World(exporting_countries=exporters, countries=countries)
    simulation = ga.GeneticAlgorithm(mutation_rate=mutation_rate, crossover_rate=crossover_rate, replication_rate=replication_rate, chromosome_size=chromosome_size, num_chromosomes=num_chromosomes, world=world, num_timestamps=num_timestamps, num_best_genes=num_best_genes)
    final = simulation.run()
    # print(final)

if __name__ == "__main__":
    # algorithm_runner_fixed(exporters_names=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], countries_names=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], num_timestamps=3, num_best_genes=2, mutation_rate=0.79, crossover_rate=0.2, replication_rate=0.01, chromosome_size=10, num_chromosomes=5, population=500, max_shipment_time=3)
    algorithm_runner_fixed(exporters_names=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], countries_names=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], num_timestamps=30, num_best_genes=10, mutation_rate=0.6, crossover_rate=0.2, replication_rate=0.2, chromosome_size=100, num_chromosomes=100, population=1000000, max_shipment_time=3)
