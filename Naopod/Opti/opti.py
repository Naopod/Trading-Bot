from data_opti import GetData
from minette_opti import FinalStrategy
from evaluate_opti import evaluate_strategy
from strategies_opti import *
import MetaTrader5 as mt
import numpy as np
from itertools import product
from tqdm import tqdm
import random
from copy import deepcopy

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
                extracted_params[f'per_1{time_suffix}'] = params.get('per_1')
                extracted_params[f'per_2{time_suffix}'] = params.get('per_2')
                extracted_params[f'per_3{time_suffix}'] = params.get('per_3')
                extracted_params[f'atr_mul_1{time_suffix}'] = params.get('atr_mul_1')
                extracted_params[f'atr_mul_2{time_suffix}'] = params.get('atr_mul_2')
                extracted_params[f'atr_mul_3{time_suffix}'] = params.get('atr_mul_3')

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

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(timeframes) - 1)
    child = {}
    for i, tf in enumerate(timeframes):
        if i < crossover_point:
            child[tf] = parent1[tf]
        else:
            child[tf] = parent2[tf]
    return child

# Dynamic Mutation Rate
base_mutation_rate = 0.1
last_avg_fitness = 0
increase_rate = 0.05

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
        
        new_param_dict = deepcopy(param_dict)
        new_param_dict[strategy][param_to_change] = random.choice(possible_values)
        
        individual[tf] = (strategy_combo, new_param_dict)

def dynamic_mutation_rate_adjustment(fitness_values):
    global base_mutation_rate, last_avg_fitness, increase_rate

    avg_fitness = np.mean(fitness_values)
    diversity = np.std(fitness_values)

    if avg_fitness <= last_avg_fitness or diversity < 10:
        base_mutation_rate += increase_rate
    else:
        base_mutation_rate = max(base_mutation_rate - increase_rate, 0.01)
    
    last_avg_fitness = avg_fitness
    return base_mutation_rate

if mt.initialize():
    print('Succesfully connected')

# Strategies and their possible parameters
strategies = {
    'DI': {'n_rsi': list(range(8, 27)), 'tol': list(range(1, 8))},
    'ST': {'ema': list(range(50, 300, 10)),
           'per_1': list(range(10, 15)),
           'per_2': list(range(12, 17)),
           'per_3': list(range(14, 19)),
           'atr_mul_1': list(range(1, 5)),
           'atr_mul_2': list(range(2, 6)),
           'atr_mul_3': list(range(3, 7))},
    'CE': {'zlsma': list(range(10, 40, 5)), 'ce_mult': list(range(1, 5, 1))}
}

# The timeframes
timeframes = ['M5', 'M15', 'M30']

# Initialize population
pop_size = 100
population = initialize_population(pop_size)

# Number of generations
n_gen = 5

symbol = str(input('Choose a symbol : '))
df_M30, df_M15, df_M5 = GetData(symbol)

# Best profit
best_profit = -float('inf')
list_parents_children = []

max_trades = 200

for gen in tqdm(range(n_gen)):

    # Evaluate fitness
    fitness_values = []
    perc_values = []
    individuals = []
    num_trade = []

    for individual in tqdm(population):
        strategies_by_timeframe, extracted_params = extract_parameters(individual)
        df = FinalStrategy(df_M30, df_M15, df_M5, strategies_by_timeframe, extracted_params)
        df = evaluate_strategy(df, symbol)
        pct = round(len(df[df['profit']>0])/len(df[df['profit']!=0]), 2)
        trade_mask = (df['final_signal_M5'] != 0) | (df['final_signal_M15'] != 0) | (df['final_signal_M30'] != 0)
        num_trades = trade_mask.sum()
        if num_trades < max_trades:
            fitness_value = round(df['profit'].sum(), 2) 
        else:
            fitness_value = -float('inf')

        fitness_values.append(fitness_value)
        perc_values.append(pct)
        individuals.append(individual)
        num_trade.append(num_trades)

    # Find the best in this generation according to the objective function
    max_fitness = max(fitness_values)
    if max_fitness > best_profit:
        best_profit = max_fitness
        best_individual = deepcopy(individuals[fitness_values.index(max_fitness)])
        best_perc = perc_values[fitness_values.index(max_fitness)]
        best_number_trades = num_trade[fitness_values.index(max_fitness)]

    print(f"Generation {gen+1}, Best profit: {best_profit}, Best individual: {best_individual} with Percentage: {best_perc} and number of trades : {best_number_trades}.")

    # Select parents
    parents, elites = select_parents(population, fitness_values, num_elites=7)

    # Crossover and Mutation
    children = []
    while len(children) < pop_size - len(elites):
        parent1, parent2 = random.sample(parents, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        children.append(child)

    children.extend(elites)

    # Replace the old population
    population = children

    dynamic_mutation_rate_adjustment(fitness_values)
    
    list_parents_children.append([{
        'Generation' : gen + 1,
        'Parents' : parents,
        'Children' : children
    }])

print(f'Overall best individual : {best_individual}, with profits : {best_profit}, percentage : {best_perc}, and number of trades : {best_number_trades}')

mt.shutdown()
