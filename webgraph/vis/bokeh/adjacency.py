from __future__ import absolute_import, division, print_function

from traceback import print_exc

import bokeh.plotting as plt
import numpy as np


def find_in_array(array, val):
    for i, arr_val in enumerate(array):
        if arr_val == val:
            return i
    return -1


def build_subgraph(nodes, csr_offsets, csr_indices):
    row_offsets = np.zeros(len(nodes) + 1, dtype=int)
    col_indices = np.empty(csr_indices.shape, dtype=int)
    curr_edge = 0
    for new_id, node_id in enumerate(nodes):
        cols = csr_indices[csr_offsets[node_id]:csr_offsets[node_id+1]]
        row_offsets[new_id] = curr_edge
        for col_id in cols:
            col_new_id = find_in_array(nodes, col_id)
            if col_new_id != -1:
                col_indices[curr_edge] = col_new_id
                curr_edge += 1
    row_offsets[new_id+1] = curr_edge
    return row_offsets, col_indices


def plot_graph(nodes, csr_offsets, csr_indices):
    try:
        import sys
        sys.argv = ["adjacency.py"]
        
        rows, cols = build_subgraph(nodes[:1000], csr_offsets, csr_indices)
        adj = compute_adj(rows, cols)
        plot_adj(adj)
    except:        
        print_exc()
    return 0


def load_random_graph():
    N = 500
    M = 10
    values = np.random.random(N)
    rows = np.empty(N+1)
    idx = 0
    for i in range(N):
        idx += np.random.randint(0, M)
        rows[i] = idx
    rows[N] = rows[N-1] + M
    rows = rows.astype(np.int)
    cols = np.random.randint(0, N, rows[-1])
    return rows, cols


def compute_adj(rows, cols):
    N = len(rows) - 1
    adj = np.zeros((N, N))
    for i in range(N):
        start, end = rows[i], rows[i+1]
        for j in range(start, end):
            adj[i, cols[j]] = 100
    return adj


def plot_adj(adj):
    N, _ = adj.shape
    plt.output_file("adjacency.html", title="Adjacency")
    TOOLS="pan,wheel_zoom,box_zoom,reset,click,previewsave"
    plt.figure(plot_width=N+100, plot_height=N+100, tools=TOOLS)
    plt.image(image=[adj], x =[0], y=[0], dw=[N], dh=[N], 
      x_range=[0, N], y_range=[0, N],palette=["YlGnBu-3"])
    plt.show()


def main():
    r, c = load_random_graph()
    adj = compute_adj(r, c)
    plot_adj(adj)

if __name__ == "__main__":
    main()
