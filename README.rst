Dynamical launcher examples
===========================

Example code that launches multiple OpenMPI tasks (both single node and multiple nodes)
within a queue (scheduler) job, running on Cori, by May 1, with three use cases:

1 - program launches a set of tasks
2 - program launches a set of tasks, when they finish, launches another set
3 - program asynchronously launches tasks as they are ready

Installing
----------

Instructions for setting up on Cori::

  module load python/3.6-anaconda-5.2;
  conda create --name parsl_0.7.0_testing_py3.6 python=3.6
  source activate parsl_0.7.0_testing_py3.6

  # Install Parsl into the conda env
  git clone https://github.com/Parsl/parsl.git
  cd parsl
  pip install .

Use script to activate the env::

  # source setup_parsl_env.sh
  
Setup mpi program::

  module load openmpi
  make

Running
-------

Full set of options::

  python3 example.py -h
  usage: example.py [-h] [-c COUNT] [-d] -f FILECONFIG [-e EXAMPLE]

  optional arguments:
   -h, --help            show this help message and exit
   -c COUNT, --count COUNT
   Count of apps to launch
   -d, --debug           Count of apps to launch
   -f FILECONFIG, --fileconfig FILECONFIG
   Specify config to load, eg cori / local
   -e EXAMPLE, --example EXAMPLE
   Options = tasks / batches / async
  
  
Example::

  python3 example.py --fileconfig=cori --count=10 --example=tasks
