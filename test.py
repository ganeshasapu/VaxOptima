from GeneticAlgorithm import GeneticAlgorithm
from WorldGraph import World

if __name__ == "__main__":
    countries = {"country1", "country2", "country3", "country4", "country5", "country6", "country7", "country8", "country9", "country10"}
    edges = set()
    world = World(countries, edges)
    ga = GeneticAlgorithm(mutation_rate=0.1, crossover_rate=0.1, replication_rate=0.1, chromosone_size=3, num_chromosones=10, world=world)
    init_chr = ga.create_initial_chromosone()
    print(init_chr)