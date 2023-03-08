class GeneticAlgorithm:
    mutation_rate: float
    crossover_rate: float
    replication_rate: float

    chromosone_size: int
    num_chromosones: int


    def __init__(self, mutation_rate: float, crossover_rate: float, replication_rate: float, chromosone_size: int, num_chromosones: int):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.replication_rate = replication_rate
        self.chromosone_size = chromosone_size
        self.num_chromosones = num_chromosones
    


    def run(self):
        pass

    def initial_chromosone(self):
        pass

    def fitness(self):
        pass

    def selection(self):
        pass

    def crossover(self):
        pass

