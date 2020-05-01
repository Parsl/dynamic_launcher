#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mpi.h>

#define error(format, ...) fprintf(stderr, format , __VA_ARGS__)
#define debug(format, ...) if (debug == 1) fprintf(stdout, format , __VA_ARGS__)

int main(int argc, char *argv[])
{
    int  repeat = 1;
    char ch;
    int myrank;
    int nprocs;
    int ticks;
    int type = 1;
    char processor_name[200];
    int namelen;
    int bs = 4; // Default block size
    int stat;
    MPI_Init(&argc, &argv);
    stat = MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    if ( stat != 0 ) error ("MPI_Comm_size returned an error code : %d", stat);

    stat = MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    if ( stat != 0 ) error ("MPI_Comm_rank returned an error code : %d", stat);

    MPI_Get_processor_name(processor_name, &namelen);

    fprintf(stdout, "[Rank:%d] Processor : %s\n", myrank, processor_name);
    fprintf(stdout, "[Rank:%d] %s %s\n", myrank, argv[1], argv[2]);
    MPI_Finalize();

    return 0;
}
