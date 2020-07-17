from parsl.config import Config
from parsl.providers import SlurmProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_interface
from parsl.launchers import SimpleLauncher

config = Config(
    executors=[
        HighThroughputExecutor(
            label='Cori_HTEX_multinode',
            # This is the network interface on the login node to
            # which compute nodes can communicate
            address=address_by_interface('bond0.144'),
            max_workers=2, # Limit the number of tasks that can be run concurrently
            provider=SlurmProvider(
                'debug',  # Partition / QOS
                nodes_per_block=4,
                init_blocks=1,
                # string to prepend to #SBATCH blocks in the submit
                # script to the scheduler eg: '#SBATCH --constraint=knl,quad,cache'
                # scheduler_options='#SBATCH --constraint=knl,quad,cache\n#SBATCH --tasks-per-node=12',
                scheduler_options='#SBATCH --constraint=knl,quad,cache',

                # Command to be run before starting a worker, such as:
                # 'module load Anaconda; source activate parsl_env'.            
                worker_init='module load openmpi; source ~/setup_parsl_env.sh',
                # We request all hyperthreads on a node.
                # No launcher is requested, meaning our workers on the mom node
                # launcher=SrunLauncher(overrides='-c 272'),
                walltime='00:10:00',
                # Slurm scheduler on Cori can be slow at times,
                # increase the command timeouts
                cmd_timeout=120,
                launcher=SimpleLauncher(),
            ),
        )
    ]
)
