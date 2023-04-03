"""Main runner file"""
import python_ta
import world_graph as wg
import genetic_algorithm as ga
import visualization as vis


def algorithm_runner(num_timestamps: int, num_best_genes: int, mutation_rate: float, crossover_rate: float,
                     replication_rate: float, chromosome_size: int, num_chromosomes: int) -> None:
    """Runs the algorithm"""
    world = wg.create_world()
    simulation = ga.GeneticAlgorithm(mutation_rate=mutation_rate, crossover_rate=crossover_rate,
                                     replication_rate=replication_rate, chromosome_size=chromosome_size,
                                     num_chromosomes=num_chromosomes, world=world,
                                     num_timestamps=num_timestamps, num_best_genes=num_best_genes)
    simulation.run()
    vis.visualize_data(simulation.final_chromosome_data)
    vis.visualize_fitness(simulation.fitness_values)


if __name__ == "__main__":
    algorithm_runner(num_timestamps=500, num_best_genes=10, mutation_rate=0.5,
                     crossover_rate=0.4, replication_rate=0.1, chromosome_size=100, num_chromosomes=100)

    python_ta.check_all(config={
        'extra-imports': ["genetic_algorithm", "visualization", "world_graph"],
        'allowed-io': [],
        'max-line-length': 120
    })
