"""Main runner file"""
import DataManipulation as dm
import WorldGraph as wg
import GeneticAlgorithm as ga
import visualization as vis

if __name__ == "__main__":
    timestamps_vaccine_amount = [100, 200, 300]
    exporters_names = ["exporter1", "exporter2"]
    countries_names = ["country1", "country2"]

    exporters: ga.ExportingCountry = {}
    countries: ga.Country = {}

    for exporter in exporters_names:
        exporters[exporter] = ga.ExportingCountry(name=exporter, vaccine_rate=0.5, export_rate=0.5, vaccine_supply=1000)
    for country in countries_names:
        countries[country] = ga.Country(name=country, vaccine_rate=0.5, vaccine_supply=1000)

    world = wg.World()
    simulation = ga.GeneticAlgorithm(mutation_rate=0.4, crossover_rate=0.1, replication_rate=0.5, chromosome_size=10, num_chromosomes=10, world=world)
    final = simulation.run()
    print(final)