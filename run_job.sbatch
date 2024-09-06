#!/bin/bash
# define SBATCH

module load python/anaconda-22.05
# activate environment

diffusion=1
vertices="starting_conditions/s2/vertices_big.csv"
cells="starting_conditions/s2/cell_indices_big.csv"
save_dir="output"
step_size=0.001
propulsion=1.0
total_time=1
shape_index=2
save_name="output_test3.hdf5"

python main.py --diffusion $diffusion \
    --vertices $vertices \
    --cells $cells \
    --save_dir $output \
    --step_size $step_size \
    --propulsion $propulsion \
    --total_time $total_time \
    --shape_index $shape_index \
    --save_name $save_name