"""Main runner file"""
import random
import WorldGraph as wg
import GeneticAlgorithm as ga

if __name__ == "__main__":
    timestamps_vaccine_amount = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    exporters_names = ["exporter1", "exporter2"]
    countries_names = ["country1", "country2"]

    exporters: ga.ExportingCountry = {}
    countries: ga.Country = {}
    edges = {}
    for country in countries_names:
        countries[country] = ga.Country(name=country, vaccine_rate=0.5, population=1500)
    for country in countries:
        edges[country] = wg.Edge(importer=countries[country], shipment_time=random.randint(1, 3))
    for exporter in exporters_names:
        exporters[exporter] = ga.ExportingCountry(name=exporter, vaccine_rate=0.5, export_rate=0.5, edges=edges, population=50000)


    world = wg.World(exporting_countries=exporters, countries=countries)
    simulation = ga.GeneticAlgorithm(mutation_rate=0.5, crossover_rate=0.3, replication_rate=0.2, chromosome_size=10, num_chromosomes=10, world=world, num_timestamps=10)
    final = simulation.run()
    print(final)

