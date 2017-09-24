import sys
import genetic.genetic
from genetic.survivor_strategy import SurvivorStrategy

if __name__ == '__main__':
    num_cities = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    results = genetic.genetic.run_three_variants(num_cities, SurvivorStrategy.HYBRID_HILL_LAMARCKIAN)
    print('Pop 50')
    print(results['50'])
    print('\nPop 100')
    print(results['100'])
    print('\nPop 200')
    print(results['200'])
    print('\nAvg')
    print(results['avg'])
