import argparse
import copy
import multiprocessing
import os
from multiprocessing import Pool

import matlab.engine


def get_left_params(dataset, kernel):
    all_params = []
    ratios = [0.2, 0.5, 0.8]
    for i in range(-3, 4):
        for j in range(-3, 4):
            for r in ratios:
                all_params.append([10 ** i, 10 ** j, r])

    path = 'outputs/rimar/{}/{}/'.format(dataset, kernel)

    masks = os.listdir(path)

    folders = []
    for file in masks:
        if os.path.isdir(os.path.join(path, file)):
            folders.append(file)

    num = 0
    dic = {}
    for foler in folders:
        folder_path = path + foler

        files = os.listdir(folder_path)

        elements = [file.strip('.mat').split('_') for file in files]

        params = copy.deepcopy(all_params)

        # store all finished params
        for element in elements:
            if element[0] == 'evaluation':
                param = [float(element[1]), float(element[2]), float(element[3])]

                idx = params.index(param)
                params.pop(idx)

        dic[foler] = params
        num += len(params)

    print('There are {} combinations needed to run!'.format(num))

    return dic


def start_matlab_to_train(params):
    # Set a matlab engine
    print('start a matlab engine')
    engine = matlab.engine.start_matlab()
    future = engine.run_alg(params[0], params[1], params[2], params[3], float(params[7]), float(params[8]),
                            float(params[9]), float(params[4]), float(params[5]), float(params[6]))
    return future


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.description = 'Please specify the dataset and kernel to be trained first.'
    parser.add_argument('--dataset', type=str, default='corel5k')
    parser.add_argument('--kernel', type=str, default='gaussian')
    parser.add_argument('--process', type=int, default=multiprocessing.cpu_count())

    args = parser.parse_args()

    dataset = args.dataset
    kernel = args.kernel

    left_params = get_left_params(dataset, kernel)

    keys = left_params.keys()

    num_cores = multiprocessing.cpu_count()

    print('The number of cores: {}'.format(num_cores))

    matlabs = []
    pool = Pool(processes=args.process)

    params = []
    for key in keys:
        masks = key.split('-')
        fm, lm = float(masks[1]), float(masks[3])

        for param in left_params[key]:
            params.append(['rimar', kernel, dataset, False, 1, fm, lm, param[0], param[1], param[2]])

    pool.map(start_matlab_to_train, params)
