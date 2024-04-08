from data_opti import GetData
from minette_opti import FinalStrategy
from evaluate_opti import evaluate_strategy
import numpy as np
from itertools import product
from tqdm import tqdm
from strategies_opti import *
import random
from copy import deepcopy
import MetaTrader5 as mt

'''Optimize over range of parameters and combinaisons of strategies for each timeframe and each market'''

def generate_param_combinations(param_dict):
    keys = param_dict.keys()
    values = param_dict.values()
    for param_combo in product(*values):
        yield dict(zip(keys, param_combo))

def initialize_population(pop_size, init_complexity=0.5):
    population = []
    for _ in range(pop_size):
        individual = {}
        
        for tf in timeframes:
            available_strategies = list(strategies.keys())
            
            if tf == 'M5':
                available_strategies.remove('DI')
            
            if random.random() < init_complexity:
                strategy_combo = random.sample(available_strategies, len(available_strategies))
            else:
                strategy_combo = random.sample(available_strategies, random.randint(1, len(available_strategies) // 2))
            
            param_dict = {strat: random.choice(list(generate_param_combinations(strategies[strat]))) for strat in strategy_combo}
            
            individual[tf] = (strategy_combo, param_dict)
        
        population.append(individual)
        
    return population

def extract_parameters(individual):
    extracted_params = {}
    strategies_by_timeframe = {'M5': None, 'M15': None, 'M30': None}

    for timeframe, (strategy_combo, param_dict) in individual.items():
        strategies_by_timeframe[timeframe] = strategy_combo

        for strategy, params in param_dict.items():
            time_suffix = f'_{timeframe.lower()}'
            if strategy == 'DI':
                extracted_params[f'n_rsi{time_suffix}'] = params.get('n_rsi')
                extracted_params[f'tol{time_suffix}'] = params.get('tol')

            elif strategy == 'ST':
                extracted_params[f'ema{time_suffix}'] = params.get('ema')

            elif strategy == 'CE':
                extracted_params[f'zlsma{time_suffix}'] = params.get('zlsma')
                extracted_params[f'ce_mult{time_suffix}'] = params.get('ce_mult')

    return strategies_by_timeframe, extracted_params

def select_parents(population, fitness_values, num_elites=1):
    sorted_indices = np.argsort(fitness_values)[::-1]  # Sort indices by fitness_values in descending order
    elite_parents = [population[i] for i in sorted_indices[:num_elites]]
    
    num_parents = len(population) // 2
    selected_parents = elite_parents[:]  # Start with elite parents
    
    for _ in range(num_parents - num_elites): 
        # Tournament selection
        tournament = random.sample(list(zip(population, fitness_values)), 7)
        tournament.sort(key=lambda x: x[1], reverse=True)
        selected_parents.append(tournament[0][0])
        elite_parents = [population[i] for i in sorted_indices[:num_elites]]
        
    return selected_parents, elite_parents

def crossover_par(parent1, parent2):
    crossover_point = random.randint(1, len(timeframes) - 1)
    child = {}
    for i, tf in enumerate(timeframes):
        if i < crossover_point:
            child[tf] = parent1[tf]
        else:
            child[tf] = parent2[tf]
    return child

'''def crossover_par(parent1, parent2):
    child = {}
    for tf in timeframes:  # Make sure 'timeframes' is initialized and contains the expected keys
        if tf not in parent1 or tf not in parent2:
            print(f"Timeframe {tf} not in both parents!")
            continue

        if len(parent1[tf]) != 2 or len(parent2[tf]) != 2:
            print(f"Invalid data for timeframe {tf} in one of the parents!")
            continue
        
        strategies1, params1 = parent1[tf]
        strategies2, params2 = parent2[tf]
        
        print(f"Length of strategies1: {len(strategies1)}, Length of strategies2: {len(strategies2)}")

        # Now it's safe to check the types
        if not isinstance(strategies1, list) or not isinstance(strategies2, list):
            print(f"Unexpected data types for strategies: {type(strategies1)}, {type(strategies2)}")
            continue  # Skip to the next iteration of the loop

        # Uniformly mix strategies
        child_strategies = random.choice([strategies1, strategies2])
        
        # Uniformly mix parameters
        child_params = {}
        for strat in child_strategies:
            child_params[strat] = {}
            for key in strategies[strat].keys():  # Assuming 'strategies' is globally defined and contains default keys
                param1 = params1.get(strat, {}).get(key)
                param2 = params2.get(strat, {}).get(key)

                if param1 is None or param2 is None:
                    print(f"None value encountered for {strat}, {key}")
                    child_params[strat][key] = param1 if param1 is not None else param2
                else:
                    child_params[strat][key] = random.choice([param1, param2])

        child[tf] = (child_strategies, child_params)

    return child'''

def mutate(individual):
    mutation_prob = random.uniform(0, 1)
    if mutation_prob < base_mutation_rate:
        tf = random.choice(timeframes)
        strategy_combo, param_dict = individual[tf]
        if len(strategy_combo) == 0:
            return  # No mutation possible
        strategy = random.choice(strategy_combo)
        param_to_change = random.choice(list(param_dict[strategy].keys()))
        possible_values = strategies[strategy][param_to_change]
        individual[tf][1][strategy][param_to_change] = random.choice(possible_values)

# Dynamic Mutation Rate
base_mutation_rate = 0.1
last_avg_fitness = 0
increase_rate = 0.05

def dynamic_mutation_rate_adjustment(fitness_values):
    global base_mutation_rate, last_avg_fitness, increase_rate

    avg_fitness = np.mean(fitness_values)
    diversity = np.std(fitness_values)

    if avg_fitness <= last_avg_fitness or diversity < 0.1:
        base_mutation_rate += increase_rate
    else:
        base_mutation_rate = max(base_mutation_rate - increase_rate, 0.01)
    
    last_avg_fitness = avg_fitness
    return base_mutation_rate

def dominates(row1, row2):
    return all(r >= s for r, s in zip(row1, row2)) and any(r > s for r, s in zip(row1, row2))

def adaptive_selection(population, fitness_values, diversity_threshold=0.1):
    diversity = np.std(fitness_values)
    print(f'Diversity : {diversity}')

    if diversity < diversity_threshold:
        print('Low diversity : Using rank based selection.')
        return rank_based_selection(population, fitness_values)
    else:
        print('High diversity : Using pareto selection.')
        return pareto_selection(population, fitness_values, num_parents=10)

def rank_based_selection(population, fitness_values):
    sorted_indices = np.argsort(fitness_values)
    sorted_population = [population[i] for i in sorted_indices]
    selected_parents = []
    
    n = len(sorted_population)
    
    # Assign a probability proportional to rank
    probabilities = [(2 * (i+1)) / (n * (n + 1)) for i in range(n)]
    
    selected_indices = np.random.choice(range(n), size=n//2, p=probabilities)
    
    return [sorted_population[i] for i in selected_indices]

# Multi-Objective (Pareto) Selection
def pareto_selection(population, fitness_values, num_parents):
    dominated_by = {i: set() for i in range(len(population))}
    dominates_count = {i: 0 for i in range(len(population))}
    
    for i in range(len(fitness_values)):
        for j in range(i + 1, len(fitness_values)):
            if dominates(fitness_values[i], fitness_values[j]):
                dominated_by[j].add(i)
                dominates_count[i] += 1
            elif dominates(fitness_values[j], fitness_values[i]):
                dominated_by[i].add(j)
                dominates_count[j] += 1

    # Create Pareto fronts
    fronts = []
    current_front = [i for i, count in dominates_count.items() if count == 0]
    while current_front:
        next_front = []
        for i in current_front:
            for j in dominated_by[i]:
                dominates_count[j] -= 1
                if dominates_count[j] == 0:
                    next_front.append(j)
        fronts.append(current_front)
        current_front = next_front
    
    # Select parents from fronts
    selected_parents = []
    for front in fronts:
        if len(selected_parents) + len(front) <= num_parents:
            selected_parents.extend(front)
        else:
            remaining = num_parents - len(selected_parents)
            selected_parents.extend(front[:remaining])
            break
    
    return [population[i] for i in selected_parents]

if mt.initialize():
    print('Connected')

# Strategies and their possible parameters
strategies = {
    'DI': {'n_rsi': list(range(8, 27)), 'tol': list(range(1, 8))},
    'ST': {'ema': list(range(50, 300, 10)),
           'per_m5': list(range(10, 15)),
           'per_m15': list(range(12, 17)),
           'per_m30': list(range(14, 19)),
           'atr_mul_m5': list(range(1, 5)),
           'atr_mul_m15': list(range(2, 6)),
           'atr_mul_m30': list(range(3, 7))},
    'CE': {'zlsma': list(range(10, 40, 5)), 'ce_mult': list(range(1, 5, 1))}
}

# The timeframes
timeframes = ['M5', 'M15', 'M30']

# Initialize population
pop_size = 100
population = initialize_population(pop_size)

# Number of generations
n_gen = 25

df_M30, df_M15, df_M5 = GetData('EURUSD')

# Best individual ever seen, initialized to None
best_individual_ever = None
best_profit_ever = -float('inf')
best_perc_ever = 0
best_trades_ever = 0
best_profit = -float('inf') 
list_parents_children = []

for gen in tqdm(range(n_gen)):
    # Evaluate fitness

    # Initialize an empty list for multi-objective fitness values
    multi_objective_fitness_values = []
    perc_values = []
    individuals = []
    num_trade = []
    profits_val = []

    for individual in tqdm(population):
        strategies_by_timeframe, extracted_params = extract_parameters(individual)
        df = FinalStrategy(df_M30, df_M15, df_M5, strategies_by_timeframe, extracted_params)
        df = evaluate_strategy(df)

        trade_mask = (df['final_signal_M5'] != 0) | (df['final_signal_M15'] != 0) | (df['final_signal_M30'] != 0)
        num_trades = trade_mask.sum()
        profits = round(df['profit'].sum(), 2)
        pct = (round(len(df[df['profit']>0])/len(df[df['profit']!=0]), 2))*100

        # Append these as a list to multi_objective_fitness_values
        multi_objective_fitness_values.append([1*profits, 20*pct])
    
        perc_values.append(pct)
        individuals.append(individual)
        num_trade.append(num_trades)
        profits_val.append(profits)

     # Convert the list to a NumPy array for easier manipulation later
    multi_objective_fitness_values = np.array(multi_objective_fitness_values)

    # Find the best in this generation according to multi-objective function
    multi_objective_function_values = np.array([1 * x[0] + 20 * x[1] for x in multi_objective_fitness_values])
    max_function_value_index = np.argmax(multi_objective_function_values)

    best_individual_gen = deepcopy(individuals[max_function_value_index])
    best_profit_gen = profits_val[max_function_value_index]
    best_perc_gen = perc_values[max_function_value_index]
    best_trades_gen = num_trade[max_function_value_index]

    print(f"Generation {gen+1}, Best profit: {best_profit_gen}, Best individual: {best_individual_gen} with Percentage: {best_perc_gen}, Number of trades: {best_trades_gen}")

    # Update the best individual ever seen, if the new one is better
    if best_profit_gen > best_profit_ever and best_perc_gen > best_perc_ever:
        best_individual_ever = best_individual_gen
        best_profit_ever = best_profit_gen
        best_perc_ever = best_perc_gen
        best_trades_ever = best_trades_gen

    # Dynamic Mutation Rate Adjustment
    dynamic_mutation_rate_adjustment(multi_objective_fitness_values)

    parents, elites = adaptive_selection(population, multi_objective_fitness_values, num_elites = 10)
    
    # Crossover and Mutation
    children = []
    while len(children) < pop_size - len(elites):  # reserve spots for elites
        parent1, parent2 = random.sample(parents, 2)
        child = crossover_par(parent1, parent2)
        mutate(child)
        children.append(child)

    children.extend(elites)

    list_parents_children.append([{
        'Generation' : gen + 1,
        'Parents' : parents,
        'Children' : children
    }])

    # Replace the old population
    population = children

# Print the best individual ever at the end
print(f"Overall best individual : {best_individual_ever}, with profits : {best_profit_ever} and percentage : {best_perc_ever} and number of trades : {best_trades_ever}.")

mt.shutdown()