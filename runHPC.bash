#!/bin/bash
#SBATCH --job-name=fastest_knot
#SBATCH --output=fastest_knot_%j.out
#SBATCH --error=fastest_knot_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --time=12:00:00
#SBATCH --mem=4G
#SBATCH --partition=general

# --- Load environment if needed (e.g., conda or module) ---
# Example if using conda:
# source /home/yourusername/miniconda3/etc/profile.d/conda.sh
# conda activate yourenv

# Or if using modules:
# module load python/3.x.x
# module load spherogram  # If available via module

# --- Navigate to directory containing fastest?.py ---
cd $SLURM_SUBMIT_DIR

# --- Run the script using 12 workers ---
python3 "fastest?.py"
