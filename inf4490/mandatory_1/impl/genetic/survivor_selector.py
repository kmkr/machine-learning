import genetic.population_evaluator as population_evaluator
from genetic.survivor_strategy import SurvivorStrategy
from hill_climber.hill_climb import hill_climb

MAX_ITERATIONS = 10

def _improve_with_hill_climb(distance_dataset, evaluated_offspring):
    return list(map(lambda evaluated: hill_climb(distance_dataset, evaluated['route'], MAX_ITERATIONS), evaluated_offspring))

def _sort_by_distance(evaluated_offspring):
    return sorted(evaluated_offspring, key=lambda offspring: offspring['route_distance'])

def select_survivors(distance_dataset, parents, offspring, population_size, survivor_selector_strategy):
    evaluated_offspring = population_evaluator.evaluate_population(distance_dataset, offspring)

    if survivor_selector_strategy == SurvivorStrategy.HYBRID_HILL_LAMARCKIAN:
        ##  hill climb and change offspring
        hill_climbed_offspring = _improve_with_hill_climb(distance_dataset, evaluated_offspring)

        evaluated_offspring = hill_climbed_offspring
    elif survivor_selector_strategy == SurvivorStrategy.HYBRID_HILL_BALDWINIAN:
        ## hill climb, bruk resultatet for selection, men unngå å endre offspring
        hill_climbed_offspring = _improve_with_hill_climb(distance_dataset, evaluated_offspring)
        sorted_hill_climbed_offspring = _sort_by_distance(hill_climbed_offspring)
        # ????
        print(2)

    # Discard parents ((μ,λ) selection) and select best-fit offspring
    sorted_offspring = _sort_by_distance(evaluated_offspring)
    survivors = list(map((lambda x: x['route']), sorted_offspring[0:population_size]))

    return survivors, sorted_offspring[0]
