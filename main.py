"""Main runner file"""
import world_graph as wg
import genetic_algorithm as ga
import visualization as vis
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def algorithm_runner_fixed(num_timestamps: int, num_best_genes: int, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosome_size: int, num_chromosomes: int):
    """Runs the algorithm"""
    world = wg.create_world()
    simulation = ga.GeneticAlgorithm(mutation_rate=mutation_rate, crossover_rate=crossover_rate, replication_rate=replication_rate,
                                     chromosome_size=chromosome_size, num_chromosomes=num_chromosomes, world=world, num_timestamps=num_timestamps, num_best_genes=num_best_genes)
    simulation.run()
    vis.visualize_data(simulation.final_chromosome_data)
    vis.visualize_fitness(simulation.fitness_values)


if __name__ == "__main__":
    # algorithm_runner_fixed(exporters_names=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], countries_names=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], num_timestamps=3, num_best_genes=2, mutation_rate=0.79, crossover_rate=0.2, replication_rate=0.01, chromosome_size=10, num_chromosomes=5, population=500, max_shipment_time=3)
    # algorithm_runner_fixed(exporters_names=["A", "B", "C", "D", "E", "F", "G", "H", "I"], countries_names=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100"], num_timestamps=20, num_best_genes=4, mutation_rate=0.6, crossover_rate=0.2, replication_rate=0.2, chromosome_size=100, num_chromosomes=100, population=20000, max_shipment_time=3)
    algorithm_runner_fixed(num_timestamps=500, num_best_genes=3, mutation_rate=0.5,
                           crossover_rate=0.4, replication_rate=0.1, chromosome_size=25, num_chromosomes=10)
