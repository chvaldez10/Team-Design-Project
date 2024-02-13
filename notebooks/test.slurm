#! /bin/bash
# ======================================================================
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --time=0-02:00:00
# ======================================================================

# Setup scratch directory
SCRATCH="/scratch/$SLURM_JOBID"
mkdir -p $SCRATCH

# Run Python script and pass SCRATCH as an argument
python run_tools.py $SCRATCH

# Clean up by removing the scratch directory after use
rm -rf $SCRATCH
