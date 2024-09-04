"""
Imports
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import parsing
import copy
import vertex
import time
import movement
import cell
import geometry
import data_holder
import math
import h5py
import csv

"""
Initial Setup
"""

def run_active_vertex_model(
    vert_filepath,
    cell_filepath,
    output_filepath,
    KA=1,
    KP=1,
    dt=0.01,
    D=2,
    v0=0.01,
    max_time=2,
    p0=1,
):
    """
    Runs the entire model and save output in output file
    """
    # initialize/read in data
    try:
        with open(vert_filepath, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        print("No file found: vertices")
        return None

    vertex_array = np.array(data, dtype = float)

    try:
        with open(cell_filepath, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        print("No file found: cell_indices")
        return None

    # cell_array = np.array(data, dtype = int)
    # using list so can use jagged array for starting conditions
    # ie cells can start with different number of vertices
    cell_list = []
    for row in data:
        to_add = []
        for num in row:
            to_add.append(int(num))
        cell_list.append(to_add)

    data = data_holder.Data_Holder(vertex_array, cell_list, \
                                    KA = KA, \
                                    KP = KP, dt = dt, D = D, \
                                    v0 = v0, max_time = max_time, p0 = p0)

    curr_time = 0
    step = 0

    # define parameters to save in addition to vertices
    attrs = ["cell_list", "vert_adjcent_cells", "vert_list"]
    attrs_to_save = [attr for attr in dir(data) \
                     if not attr.startswith("_") and attr not in attrs]

    # save step 0
    positions = np.array([[v[0], v[1]] for v in data.vert_list])
    with h5py.File(output_filepath, "w") as f:
        # save vertices and original cell indices
        path = os.path.join(f"step_{step:05d}", "vertices")
        verts = f.create_dataset(path, data=positions)
        # save edges
        all_edges = []
        for single_cell in data.cell_list:
            for i in range(len(single_cell.vert_obj_list)):
                v1 = single_cell.vert_obj_list[i]
                v2 = single_cell.vert_obj_list[(i + 1) % len(single_cell.vert_obj_list)]
                all_edges.append([[v1[0], v1[1]], [v2[0], v2[1]]])
        path = os.path.join(f"step_{step:05d}", "edges")
        f.create_dataset(path, data = all_edges)
        # save other attributes
        for attr in attrs_to_save:
            verts.attrs[attr] = data.__getattribute__(attr)
        verts.attrs["energy"] = movement.calc_energy(data)
        verts.attrs["step"] = step
        verts.attrs["curr_time"] = curr_time
        # save original cell centers
        path = os.path.join(f"step_{step:05d}", "cell_centers")
        cell_center_list = []
        for cell in data.cell_list:
            center = cell.total_movement
            cell_center_list.append([center[0], center[1]])
        f.create_dataset(path, data=cell_center_list)

    # move vertices and save other steps
    # movement.t1_transition_check_beta(data)
    movement.t1_transition_check(data, set())
    while curr_time < data.max_time:
        if curr_time % 0.1 < 0.001:
            print(curr_time)
        step += 1
        curr_time += data.dt
        movement.move_vertices(data.vert_list, data)
        # movement.t1_transition_check_beta(data)
        movement.t1_transition_check(data, set())
        positions = np.array([[v[0], v[1]] for v in data.vert_list]) #
        with h5py.File(output_filepath, "a") as f:
            # save vertices
            path = os.path.join(f"step_{step:05d}", "vertices")
            if path in f:
                del f[path]
            verts = f.create_dataset(path, data = positions)
            # save edges
            all_edges = []
            for single_cell in data.cell_list:
                for i in range(len(single_cell.vert_obj_list)):
                    v1 = single_cell.vert_obj_list[i]
                    v2 = single_cell.vert_obj_list[(i + 1) % len(single_cell.vert_obj_list)]
                    all_edges.append([[v1[0], v1[1]], [v2[0], v2[1]]])
            path = os.path.join(f"step_{step:05d}", "edges")
            f.create_dataset(path, data = all_edges)
            # save other attributes
            for attr in attrs_to_save:
                verts.attrs[attr] = data.__getattribute__(attr)
            verts.attrs["energy"] = movement.calc_energy(data)
            verts.attrs["step"] = step
            verts.attrs["curr_time"] = curr_time
            # save original cell centers
            path = os.path.join(f"step_{step:05d}", "cell_centers")
            cell_center_list = []
            for cell in data.cell_list:
                center = cell.total_movement
                cell_center_list.append([center[0], center[1]])
            f.create_dataset(path, data=cell_center_list)