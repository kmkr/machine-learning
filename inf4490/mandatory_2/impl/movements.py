#!/usr/bin/env Python3
'''
    This file will read in data and start your mlp network.
    You can leave this file mostly untouched and do your
    mlp implementation in mlp.py.
'''
# Feel free to use numpy in your MLP if you like to.
import numpy as np
import mlp
import os
import sys
import math

dirPath = os.path.dirname(os.path.abspath(__file__))

filename = '/data/movements_day1-3.dat'

movements = np.loadtxt(dirPath + filename,delimiter='\t')

# Subtract arithmetic mean for each sensor. We only care about how it varies:
movements[:,:40] = movements[:,:40] - movements[:,:40].mean(axis=0)

# Find maximum absolute value:
imax = np.concatenate(  ( movements.max(axis=0) * np.ones((1,41)) ,
                          np.abs( movements.min(axis=0) * np.ones((1,41)) ) ),
                          axis=0 ).max(axis=0)

# Divide by imax, values should now be between -1,1
movements[:,:40] = movements[:,:40]/imax[:40]

# Generate target vectors for all inputs 2 -> [0,1,0,0,0,0,0,0]
target = np.zeros((np.shape(movements)[0],8));
for x in range(1,9):
    indices = np.where(movements[:,40]==x)
    target[indices,x-1] = 1

# Randomly order the data
order = list(range(np.shape(movements)[0]))
np.random.shuffle(order)
movements = movements[order,:]
target = target[order,:]

# Split data into 3 sets
def split_movements(movements, targets):
    # Training updates the weights of the network and thus improves the network
    train = movements[::2,0:40]
    train_targets = targets[::2]

    # Validation checks how well the network is performing and when to stop
    valid = movements[1::4,0:40]
    valid_targets = targets[1::4]

    # Test data is used to evaluate how good the completely trained network is.
    test = movements[3::4,0:40]
    test_targets = targets[3::4]

    return { 'train': train, 'train_targets': train_targets, 'valid': valid, 'valid_targets': valid_targets, 'test': test, 'test_targets': test_targets }

def run(num_hidden, datasets):
    train = datasets['train']
    train_targets = datasets['train_targets']
    valid = datasets['valid']
    valid_targets = datasets['valid_targets']
    test = datasets['test']
    test_targets = datasets['test_targets']

    net = mlp.Mlp(train, train_targets, num_hidden)
    net.earlystopping(train, train_targets, valid, valid_targets)
    return net.confusion(test,test_targets)

def run_multiple_times_and_calculate_mean_percentage_error():
    cur_hidden = 5
    max_hidden = 30
    num_runs = 50
    print('number_of_hidden_nodes,mean_percentage_correct')
    datasets = split_movements(movements, target)
    while cur_hidden <= max_hidden:
        cur_run = 0
        percentage_corrects = np.zeros(num_runs)
        while cur_run < num_runs:
            result = run(cur_hidden, datasets)
            percentage_corrects[cur_run] = result[1]
            cur_run += 1

        print(str(cur_hidden) + ',' + str(np.mean(percentage_corrects)))
        cur_hidden += 1

def run_one_time_and_print_confusion_matrix(datasets):
    hidden = 14
    result = run(hidden, datasets)
    confusion_matrix = result[0]
    percentage_correct = result[1]

    print('Confusion matrix:')
    print(confusion_matrix)
    print('Percentage correct:')
    print(percentage_correct)
    return percentage_correct

def run_k_fold(num_folds):
    cur_fold = 0
    num_data = movements.shape[0]
    bucket_size = math.floor(num_data / num_folds)

    indices = list(range(num_data))
    np.random.shuffle(indices)

    results = []
    while cur_fold < num_folds:
        print('\nFold', cur_fold)
        train = []
        train_targets = []
        valid = []
        valid_targets = []
        test = []
        test_targets = []
        fold_index = cur_fold * bucket_size

        for index in indices:
            folded_index = (fold_index + index) % num_data
            if folded_index % 2 == 0:
                train.append(movements[folded_index,0:40])
                train_targets.append(target[folded_index])
            elif (folded_index + 1) % 4 == 0:
                valid.append(movements[folded_index,0:40])
                valid_targets.append(target[folded_index])
            elif (folded_index + 3) % 4 == 0:
                test.append(movements[folded_index,0:40])
                test_targets.append(target[folded_index])

        datasets =  { 'train': np.array(train), 'train_targets': np.array(train_targets), 'valid': np.array(valid), 'valid_targets': np.array(valid_targets), 'test': np.array(test), 'test_targets': np.array(test_targets) }

        result = run_one_time_and_print_confusion_matrix(datasets)
        results.append(result)

        cur_fold += 1

    print('\n')
    print('max', np.max(results))
    print('std', np.std(results))
    print('avg', np.average(results))

arg = sys.argv[1] if len(sys.argv) > 1 else ''

if arg == 'mean':
    run_multiple_times_and_calculate_mean_percentage_error()
elif arg == 'kfold':
    num_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    run_k_fold(num_k)
else:
    run_one_time_and_print_confusion_matrix(split_movements(movements, target))
