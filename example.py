import argparse
import time
import os
import parsl
from parsl.app.app import python_app, bash_app


@bash_app
def mpi_hello(nodes, ranks, msg, stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME, mock=False):
    if mock:
        cmd = f"echo {msg} on Nodes:{nodes} X Ranks:{ranks}"
    else:
        cmd = f"srun -n {ranks} -N {nodes} /global/homes/y/yadunand/dakota_collab/mpi_hello hello {msg}"
    return cmd


@python_app
def platform(sleep=10, stdout=None):
    import platform
    import time
    time.sleep(sleep)
    return platform.uname()


@bash_app
def srun_test(nodes, ranks, command, stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    return f'srun -n {ranks} -N {nodes} {command}'


def print_file(filename):
    with open(filename) as f:
        print(f.read())

def launch_tasks(n=10):
    """ Launch N arbitrary tasks onto an active job
    
    We will launch half the tasks with ranks on a single node, and the rest
    will be spread over 2 nodes.
    """
    dfk = parsl.dfk()
    name = list(dfk.executors.keys())[0]

    # Get 
    nodes_requested = dfk.executors[name].provider.nodes_per_block
    slots = dfk.executors[name].max_workers

    x = platform(sleep=0).result()
    print(f"Nodes requested : {nodes_requested}")
    print(f"Slots per job : {slots}")
    print(f"Platform info : {x}")
    print("Slots available   : {}".format(dfk.executors[name].connected_workers))

    futures = []
    # Launch a mix of single node and 2 node tasks
    for i in range(n):
        if i%2 == 0:
            x = mpi_hello(1, 4, i, mock=False)
        else:
            x = mpi_hello(2, 4, i, mock=False)
        futures.append(x)

    # wait for everything
    for i in futures:
        print(i.result())
        print(i.stdout, print_file(i.stdout))
        

def launch_batches(n=4, batches=2):
    """ Launch batches of  N arbitrary tasks onto an active job after the previous one is complete
    
    """

    print("Launching batch 1")
    launch_tasks(n=4)
    print("Launching batch 2")
    launch_tasks(n=4)


def async_launch(n=10, throttle=4):
    """ Launch N arbitrary tasks onto an active job
    
    We will launch half the tasks with ranks on a single node, and the rest
    will be spread over 2 nodes.
    """
    x = platform(sleep=0).result()
    print(f"Platform info : {x}")

    futures = []

    while n > 0 or len(futures) > 0:

        print(f"Tasks Pending: {n}, Tasks Active: {len(futures)}")
        
        if len(futures) < throttle and n > 0:
            # Launch a mix of single node and 2 node tasks
            print("Launching task")
            if n%2 == 0:
                x = mpi_hello(1, 4, n, mock=False)
            else:
                x = mpi_hello(2, 4, n, mock=False)
            futures.append(x)
            n -= 1

        done = [f for f in futures if f.done()]
        for i in done:
            print("Completed : ", i.result())
            print(i.stdout, print_file(i.stdout))
            futures.remove(i)

        time.sleep(1)
            

    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default="10",
                        help="Count of apps to launch")

    parser.add_argument("-d", "--debug", action='store_true',
                        help="Count of apps to launch")

    parser.add_argument("-f", "--fileconfig", required=True,
                        help="Specify config to load, eg cori / local")

    parser.add_argument("-e", "--example", default="tasks",
                        help="Options = tasks / batches / async")
    
    args = parser.parse_args()

    if args.debug:
        parsl.set_stream_logger()

    config = None
    exec("from {} import config".format(args.fileconfig))
    parsl.load(config)
    if args.example == "tasks":
        launch_tasks(n=int(args.count))
    elif args.example == "batches":
        launch_batches(n=int(args.count))
    elif args.example == "async":
        async_launch(n=int(args.count))
    else:
        print("Unknown example type requested")
