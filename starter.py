import argparse
import copy
import multiprocessing
import os
from multiprocessing import Pool

import matlab.engine


def get_params(dataset, kernel):
    '''set your own parameter list here'''

    # it should be a 2-D list array, 
    # each row is a combination of your parameters
    all_params = []

    return all_params


def start_matlab_to_train(params):
    """Set a matlab engine"""

    print('start a matlab engine')
    
    # firstly start a matlab engine
    engine = matlab.engine.start_matlab()
    
    # pass your params to the matlab function, and call it
    future = engine.run_alg(params)
    
    return future


if __name__ == '__main__':

    # Customize your parser here
    parser = argparse.ArgumentParser()
    parser.description = 'Please specify the dataset and kernel to be trained first.'
    parser.add_argument('--dataset', type=str, default='corel5k')
    parser.add_argument('--kernel', type=str, default='gaussian')
    parser.add_argument('--process', type=int, default=multiprocessing.cpu_count())

    args = parser.parse_args()

    # Set your own parameter list here
    dataset = args.dataset
    kernel = args.kernel
    left_params = get_params(dataset, kernel)

    # The following two line would show the number of cpu cores on your PC.
    # Normally, you should not exceed it in the number of threads.
    num_cores = multiprocessing.cpu_count()
    print('The number of cores: {}'.format(num_cores))

    # Start a parallel pool
    pool = Pool(processes=args.process)

    # Get the list of the parameters you want to run
    params = get_params(dataset, kernel)

    # Finally map the parameters into the function
    pool.map(start_matlab_to_train, params)
