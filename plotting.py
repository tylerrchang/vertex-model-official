from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import h5py

def graph_frame(ax, vertices, edges, lx, ly, color = "black"):
    graph_lines(ax, edges, lx, ly, color)
    # graph_points(ax, vertices)

def graph_lines(ax, edges, lx, ly, color="black"):
    """
    Graphs lines associated with one frame
    Cells = 3D array with each row being an individual cell, each column being
    one vertex, and the third dimension being either the x or y coord
    ax = is a matplotlib axis
    lx, ly = bounds of the image
    """
    # graph lines
    for edge in edges:
        for i in range(1):
            x1 = edge[i][0]
            y1 = edge[i][1]
            x2 = edge[(i + 1) % len(edge)][0]
            y2 = edge[(i + 1) % len(edge)][1]
            # if any boundaries broken, must check which boundaries
            # then draw 2 segments connecting to the edge of the border
            if abs(x1 - x2) > lx / 2 or abs(y1 - y2) > ly / 2:
                # segment 1
                if abs(x1 - x2) > lx / 2:
                    if x1 > x2:
                        x2 += lx
                    else:
                        x1 += lx
                if abs(y1 - y2) > ly / 2:
                    if y1 > y2:
                        y2 += ly
                    else:
                        y1 += ly
                ax.plot([x1, x2], [y1, y2], color=color)
                # segment 2
                x1 = edge[i][0]
                y1 = edge[i][1]
                x2 = edge[(i + 1) % len(edge)][0]
                y2 = edge[(i + 1) % len(edge)][1]
                if abs(x1 - x2) > lx / 2:
                    if x1 > x2:
                        x1 -= lx
                    else:
                        x2 -= lx
                if abs(y1 - y2) > ly / 2:
                    if y1 > y2:
                        y1 -= ly
                    else:
                        y2 -= ly
                ax.plot([x1, x2], [y1, y2], color=color)
            # no boundaries broken
            # when no periodic boundaries broken, just draw one segment
            else:
                ax.plot([x1, x2], [y1, y2], color=color)

def graph_points(ax, vertices):
    """
    Graphs the scatter plot of vertices
    vertices = list of lists with each row being a vertex and each column
    being an x or y coordinate
    """
    ax.scatter(vertices[:, 0], vertices[:, 1], color = "r")

def plot_data(path, stepsize=10):
    try:
        with h5py.File(path, "r") as f:
            totalframes = len(f.keys())
            lx = f["step_00000/vertices"].attrs["lx"]
            ly = f["step_00000/vertices"].attrs["ly"]
    except FileNotFoundError:
        print("No File Found")
        return

    fig, ax = plt.subplots(figsize = (6,6))

    # Set limits for x and y axis
    ax.set_xlim(0.1, lx)
    ax.set_ylim(0.1, ly)
    ax.set_xticks([])
    ax.set_yticks([])

    scat = ax.scatter([], [], c="red")

    def init():
        with h5py.File(path, "r") as f:
            dset = f["step_00000/edges"]
            j = f["step_00000/vertices"]
            lx = f["step_00000/vertices"].attrs["lx"]
            ly = f["step_00000/vertices"].attrs["ly"]
            graph_frame(ax, j, dset, lx, ly)
        return (scat,)

    def animate(i):
        ax.clear()
        with h5py.File(path, "r") as f:
            dset = f[f"step_{i:05d}/edges"]
            j = f[f"step_{i:05d}/vertices"]
            lx = f[f"step_{i:05d}/vertices"].attrs["lx"]
            ly = f[f"step_{i:05d}/vertices"].attrs["ly"]
            ax.set_xlim(0.1, lx)
            ax.set_ylim(0.1, ly)
            ax.set_xticks([])
            ax.set_yticks([])
            graph_frame(ax, j, dset, lx, ly)
        return (scat,)

    plt.close()
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=np.arange(0, totalframes, stepsize),
        interval=100,
        blit=True,
    )
    return anim
# def graph_lines_beta(ax, cells, lx, ly, color="black"):
#     """
#     Graphs lines associated with one frame
#     Cells = 3D array with each row being an individual cell, each column being
#     one vertex, and the third dimension being either the x or y coord
#     ax = is a matplotlib axis
#     lx, ly = bounds of the image
#     """
#     # graph lines
#     for cell in cells:
#         for i in range(len(cell)):
#             x1 = cell[i][0]
#             y1 = cell[i][1]
#             x2 = cell[(i + 1) % len(cell)][0]
#             y2 = cell[(i + 1) % len(cell)][1]
#             # if any boundaries broken, must check which boundaries
#             # then draw 2 segments connecting to the edge of the border
#             if abs(x1 - x2) > lx / 2 or abs(y1 - y2) > ly / 2:
#                 # segment 1
#                 if abs(x1 - x2) > lx / 2:
#                     if x1 > x2:
#                         x2 += lx
#                     else:
#                         x1 += lx
#                 if abs(y1 - y2) > ly / 2:
#                     if y1 > y2:
#                         y2 += ly
#                     else:
#                         y1 += ly
#                 ax.plot([x1, x2], [y1, y2], color=color)
#                 # segment 2
#                 x1 = cell[i][0]
#                 y1 = cell[i][1]
#                 x2 = cell[(i + 1) % len(cell)][0]
#                 y2 = cell[(i + 1) % len(cell)][1]
#                 if abs(x1 - x2) > lx / 2:
#                     if x1 > x2:
#                         x1 -= lx
#                     else:
#                         x2 -= lx
#                 if abs(y1 - y2) > ly / 2:
#                     if y1 > y2:
#                         y1 -= ly
#                     else:
#                         y2 -= ly
#                 ax.plot([x1, x2], [y1, y2], color=color)
#             # no boundaries broken
#             # when no periodic boundaries broken, just draw one segment
#             else:
#                 ax.plot([x1, x2], [y1, y2], color=color)