# Run your MATLAB function parallelly

> Constrained by MATLAB's `parfor` function, I wrote my own script to call MATLAB functions in parallel using python.

This is a very simple and handy tool that allows to **call your MATLAB scripts in parallel** to maximize the use of computational resources.

## How to run the python script

- Simply run `python starter.py`, and you can customize your input parameters.
- You can see an example in the `demo.py`.

## How to fit it in your project

1. Customize your python script;

2. Place it in the same level directory as the script you need to call in your MATLAB project;

3. Configure the python environment in which to run the script:

   - Notice that the python version must compatible with your MATLAB, you can check it [here](https://ww2.mathworks.cn/support/requirements/python-compatibility.html).

   -  Usually, you just need to install the `matlab` engine module. To install this module, please follow the steps:

     1. You can find the `setup.py` in the path `{matlab_root}\extern\engines\python` where `{matlab_root}`  is the path MATLAB installed.

     2. Activate your python environment, and run `python setup.py install`.

     3. To verify that the installation was successful, you can start a python cmd, and run the following code:

        ```python
        import matlab.engine
        eng = matlab.engine.start_matlab()
        ```

## Weaknesses

- Since it's a very simple parallel script, I don't have a memory limit on it, so please **allocate the number of threads wisely**!

