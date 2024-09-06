# vertex-model-official

## General
- Codes for an active vertex model. It simulates movement in simple multicellular system. No cell death or cell replication is accounted for.
- Calculations based on the paper [cellGPU: massively parallel simulations of dynamic vertex models](https://arxiv.org/abs/1702.02939)

## Files
### Running Simulations
- `data_holder.py`
- `cell.py`
- `vertices.py`
- `simulate.py`
- `movement.py`
- `geometry.py`

### Plotting Animations 
- `plotting.py` no relation to running simulations, only visualizations. used exclusively in run_sims.ipynb.

### Other
- `main.py` call to run simulations
- `starting conditions/` contains 2 different starting conditions for sample simulations
- `run_sims.ipynb` jupyter notebook to run simulations and create/save animations
- `run_job.sbatch` demonstrates how the simulations are run and attempt at creating sbatch file
- `requirements.txt` environment setup

## Assumptions
- vertices of cells listed in counterclockwise order
- each vertex is always part of exactly 3 cells

## Using Simulations
- the simulation can be run from the command line using `python main.py ...` where `...` can be replaced by the required arguments
- a full example of how to run can be see in `run_job.sbatch`
- example run: `python main.py --diffusion=1 --vertices=starting_conditions/s2/vertices_big.csv --cells=starting_conditions/s2/cell_indices_big.csv --save_dir=output --step_size=0.001 --propulsion=1.0 --total_time=1 --shape_index=2 --save_name output_test3.hdf5`

## Notes
- the simulation is inconsitent when shape index (p0) > 3.9

## Contact Information
- Tyler Chang (developed while working with Vincenzo Vitelli)
- trchang@wisc.edu