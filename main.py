import argparse
import os

import simulate

if __name__ == '__main__':

    ap = argparse.ArgumentParser()

    ap.add_argument("--diffusion", type=float, required=True, 
                    help="Rotational diffusion of cells, how fast cells turn")
    ap.add_argument("--propulsion", type=float, required=True, 
                    help="Self propulsion force, how fast cells move forward")
    ap.add_argument("--shape_index", type=float, required=True, 
                    help="Shape index of cells, increasing makes more elliptical")
    ap.add_argument("--step_size", type=float, required=True, 
                    help="how large each step")
    ap.add_argument("--total_time", type=float, required=True, 
                    help="total number of steps")
    # in save directory location, if there is no folder with the same name, 
    # a new directory will be created. Otherwise, the directory with the correct
    # name will be used
    ap.add_argument("--save_dir", type=str, required=True, 
                    help="where file will be saved")
    # the name of the actual output hdf5 file
    # if running a batch you would probably change this parameter but keep the
    # save director file the same
    ap.add_argument("--save_name", type=str, required=True, 
                    help="name of output file")
    ap.add_argument("--vertices", type=str, required=True, 
                    help="initial vertices")
    ap.add_argument("--cells", type=str, required=True, 
                    help="initial cell connections")
    
args = ap.parse_args()

if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)

simulate.run_active_vertex_model(
    args.vertices,
    args.cells,
    os.path.join(args.save_dir, args.save_name),
    KA=1,
    KP=1,
    dt=args.step_size,
    D=args.diffusion,
    v0=args.propulsion,
    max_time=args.total_time,
    p0=args.shape_index,
)