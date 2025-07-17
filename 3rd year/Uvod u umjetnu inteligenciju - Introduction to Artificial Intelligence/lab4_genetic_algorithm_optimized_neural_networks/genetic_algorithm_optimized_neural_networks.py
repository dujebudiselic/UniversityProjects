import random
import sys
import numpy as np

def evaluate(weights, biases, hidden_layers, feature_names, features, feature_results, population_size):

    err_population = {}
    y = None
    rez_individual = {}

    for p in range(0, population_size):
        rez = []
        for f in features:
            t = weights[p]
            b = biases[p]
            w = t[0].T  
            w0 = b[0].reshape(-1, 1)
            x = np.array(f).reshape(-1, 1) 
            y_nof = w @ x + w0  
            y = 1 / (1 + np.exp(-y_nof))
            
            if len(hidden_layers) > 1:
                for i in range(1, len(hidden_layers)):
                    t = weights[p]
                    b = biases[p]
                    w = t[i].T
                    w0 = b[i].reshape(-1, 1)
                    y_nof = w @ y + w0
                    y = 1 / (1 + np.exp(-y_nof))
            
            t = weights[p]
            b = biases[p]
            w = t[len(hidden_layers)].T
            w0 = b[len(hidden_layers)].reshape(-1, 1)
            y = w @ y + w0
            
            rez.append(y)
            

        rez_individual[p] = rez
        
    for p in range(0, population_size):
        err = 0
        results = rez_individual[p]
        sum = 0
        for i, y in enumerate(feature_results):
            sum += ((y - results[i])**2)
            
        err = sum / len(feature_results)
        err_population[p] = err

    err_population_sorted = dict(sorted(err_population.items(), key=lambda x: x[1]))
    return err_population_sorted

def select_parent(err_population_sort):
    sum_fit = 0
    epsilon = 1e-10
    for err in err_population_sort:
        sum_fit += (1 / epsilon + err_population_sort[err])
    spin_wheel = random.uniform(0, sum_fit)
    len_ = 0
    for err in err_population_sort:
        len_ += (1 / epsilon + err_population_sort[err])
        if len_ >= spin_wheel:
            return err

def get_features(path):
    is_header = True
    with open(path, 'r', encoding='utf-8') as f:
        features = []
        feature_results = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if is_header:
                    feature_names = line.split(',')
                    is_header = False
                else:
                    parts = line.split(',')
                    feature_values = []
                    for value in parts[:-1]:
                        feature_values.append(float(value))
                    features.append(feature_values)
                    feature_results.append(float(parts[-1]))

    return feature_names, features, feature_results

def get_test_features(test_path):
    is_header = True
    with open(test_path, 'r', encoding='utf-8') as f:
        test_features = []
        test_feature_results = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if is_header:
                    test_feature_names = line.split(',')
                    is_header = False
                else:
                    parts = line.split(',')
                    feature_values = []
                    for value in parts[:-1]:
                        feature_values.append(float(value))
                    test_features.append(feature_values)
                    test_feature_results.append(float(parts[-1]))

    return test_feature_names, test_features, test_feature_results


entry = sys.argv
index_train = entry.index('--train')
train_path = entry[index_train + 1]
index_test = entry.index('--test')
test_path = entry[index_test + 1]

index_nn_architecture = entry.index('--nn')
nn_architecture = entry[index_nn_architecture + 1]

index_population_size = entry.index('--popsize')
population_size = entry[index_population_size + 1]
index_elitism = entry.index('--elitism')
elitism = entry[index_elitism + 1]

index_mutation_prob = entry.index('--p')
mutation_prob = entry[index_mutation_prob + 1]
index_mutation_stddev = entry.index('--K')
mutation_stddev = entry[index_mutation_stddev + 1]
index_num_iterations = entry.index('--iter')
num_iterations = entry[index_num_iterations + 1]

feature_names, features, feature_results = get_features(train_path)
test_feature_names, test_features, test_feature_results = get_test_features(test_path)


hidden_layers = []
nn_architecture = nn_architecture.split('s')
for c in nn_architecture:
    if c.isdigit():
        hidden_layers.append(c)

input_size = len(feature_names) - 1
output_size = 1
weights = {}
biases = {}

for p in range(0 , int(population_size)):

    W = []
    W0 = []
    Wx = np.random.normal(loc=0.0, scale=0.01, size=(input_size, int(hidden_layers[0])))
    W0x = np.random.normal(loc=0.0, scale=0.01, size=(int(hidden_layers[0])))
    W.append(Wx)
    W0.append(W0x)

    if len(hidden_layers) > 1:
        for i in range(0, len(hidden_layers) - 1):
            Wx = np.random.normal(loc=0.0, scale=0.01, size=(int(hidden_layers[i]), int(hidden_layers[i + 1])))
            W0x = np.random.normal(loc=0.0, scale=0.01, size=(int(hidden_layers[i + 1])))
            W.append(Wx)
            W0.append(W0x)

    Wx = np.random.normal(loc=0.0, scale=0.01, size=(int(hidden_layers[len(hidden_layers) - 1]), output_size))
    W0x = np.random.normal(loc=0.0, scale=0.01, size=(output_size))
    W.append(Wx)
    W0.append(W0x)

    weights[p] = W
    biases[p] = W0

err_population_sort = evaluate(weights, biases, hidden_layers, feature_names, features, feature_results, int(population_size))

for i in range(1, int(num_iterations) + 1):
    e = 0
    new_weights = {}
    new_biases = {}
    
    for err in err_population_sort:
        if e == int(elitism):
            break
        new_weights[e] = weights[err]
        new_biases[e] = biases[err]
        
        e += 1

    while e < int(population_size):
        
        while True:
            index_parent1 = select_parent(err_population_sort)
            index_parent2 = select_parent(err_population_sort)
            if index_parent1 != index_parent2:
                break
        
        parent1 = weights[index_parent1]
        parent2 = weights[index_parent2]
        parent1_biases = biases[index_parent1]
        parent2_biases = biases[index_parent2]
        
        new_w = []
        new_W0 = []
        for r in range(len(parent1)):
            r1 = parent1[r]
            r2 = parent2[r]
            r1_biases = parent1_biases[r]
            r2_biases = parent2_biases[r]
            n_wx = (r1 + r2) / 2
            n_w0x = (r1_biases + r2_biases) / 2
            new_w.append(n_wx)
            new_W0.append(n_w0x)

        
        for t in range(len(new_w)):
            for index, x in np.ndenumerate(new_w[t]):
                if np.random.rand() < float(mutation_prob):
                    new_w[t][index] += np.random.normal(0.0, float(mutation_stddev))
        for b in range(len(new_W0)):
            for index, x in np.ndenumerate(new_W0[b]):
                if np.random.rand() < float(mutation_prob):
                    new_W0[b][index] += np.random.normal(0.0, float(mutation_stddev))
        
        
        new_weights[e] = new_w
        new_biases[e] = new_W0
        e += 1
       
    weights = new_weights
    biases = new_biases
    err_population_sort = evaluate(weights, biases, hidden_layers, feature_names, features, feature_results, int(population_size))
   
    if i % 2000 == 0:
        best_individual_mse = next(iter(err_population_sort.values()))
        print(f"[train error @{i}]: {best_individual_mse.item()}")

err_population_sort = evaluate(weights, biases, hidden_layers, feature_names, features, feature_results, int(population_size)) 
best_individual_mse = next(iter(err_population_sort.values()))     
print(f"[test error]: {best_individual_mse.item()}")

