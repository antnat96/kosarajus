# Author: Anthony Natale
# Date: October 2022
# Assignment 3, Design and Analysis of Algorithms, ECU
# TODO: Remove!
# Notes: Your program runs correctly for most test cases, though it failed to produce the correct output for my "scc4"
# test case (-12).
# Also, the output contains parallel edges (-5).
# Your implementation appears to run using the correct time complexity.
import sys


class Stack:
    def __init__(self):
        self.items = []
        self.size = 0

    def push(self, item=None):
        self.items.append(item)
        self.size = self.size + 1

    def pop(self):
        self.size = self.size - 1
        return self.items.pop()

    def has_elements(self):
        if self.size > 0:
            return True
        else:
            return False

    def rev(self):
        self.items.reverse()

    def get_items(self):
        return self.items

    def clear(self):
        self.items = []
        self.size = 0


def main():

    fname = sys.argv[1]
    if ".txt" not in fname:
        fname = fname + ".txt"
    while True:
        try:
            inp = open(fname, "r")
            break
        except IOError as e:
            print("Please ensure that you are entering the file name properly")
            fname = raw_input("Try entering the file name again now:")
            if ".txt" not in fname:
                fname = fname + ".txt"
    line = inp.readline()
    # Build graph information list
    graph_info = []
    while line:
        if "\n" in line:
            line = line.replace("\n", "")
        graph_info.append(line.strip())
        line = inp.readline()
    n = int(graph_info.pop(0))
    e = int(graph_info.pop(0))
    edges = []
    for x in graph_info:
        edges.append([int(x.split(" ")[0]), int(x.split(" ")[1])])

    # My test cases
    # Test_1
    # n = 8
    # e = 9
    # edges = [[0,1],[1,2],[2,3],[3,0],[2,4],[4,5],[5,6],[6,4],[6,7]]
    # Test_2
    # n = 8
    # e = 11
    # edges = [[0,1],[1,5],[0,2],[1,2],[3,1],[2,3],[3,6],[2,4],[3,4],[7,3],[4,7]]
    # Test_3
    # n = 5
    # e = 5
    # edges = [[1,0],[0,2],[2,1],[0,3],[1,4]]
    # Test_4
    # n = 6
    # e = 6
    # edges = [[0,1],[0,2],[1,3],[1,4],[4,5],[2,5]]

    # Create graph representation and initialize visited list
    adj_list = []
    visited = [False] * n
    for a in range(n):
        adj_list.append([])
    for x in edges:
        adj_list[x[0]].append(x[1])
    orig_adj_list = adj_list

    # Initialize the stack to record post order traversal
    post_order = Stack()
    post_order.push(0)

    # First DFS - Pushes vertices to the post_order stack as they (and their children) are done being explored
    dfs_1(post_order.pop(), post_order, adj_list, visited)

    # TODO: Change the following to work without explicitly constructing the reverse graph
    # Reverse the graph
    for y in edges:
        y = y.reverse()

    # Create new graph representation and reinitialize visited list to all False
    adj_list = []
    visited = [False] * n
    for a in range(n):
        adj_list.append([])
    for x in edges:
        adj_list[x[0]].append(x[1])

    # Initialize a list of SCCs
    scc = []
    # And a list describing the SCC currently being built by the DFS
    curr_scc = []

    # Second DFS - Uses the reversed graph to identify the strongly connected components
    # dfs_2(post_order.pop(), post_order, adj_list, visited, scc, curr_scc)

    while post_order.has_elements() is True:
        v = post_order.pop()
        if visited[v] is False:
            dfs_2(v, post_order, adj_list, visited, scc, curr_scc)
            scc.append(curr_scc)
            curr_scc = []

    # Print the strongly connected components
    if len(scc) != n:
        print("There are " + str(len(scc)) + " Strongly Connected Components:")
        for x in range(len(scc)):
            print x,
            print ":",
            for y in scc[x]:
                print str(y),
            print("\n")
        print("Kernel Graph Adjacency List:")
        construct_kernel(scc, edges)

    else:
        print("Each component stands alone-that is, there are no strongly connected components because no 2 components "
              "have connections to one another according to our adjacency list.")


def dfs_1(v, post_order, adj_list, visited):
    # Note that v has been visited
    visited[v] = True
    # For every adjacent node
    for u in adj_list[v]:
        # If it hasn't been visited
        if visited[u] is False:
            # Call dfs_1 on it
            dfs_1(u, post_order, adj_list, visited)
    # If there is nowhere else to visit after v, add it to the processed nodes
    post_order.push(v)


def dfs_2(v, post_order, adj_list, visited, scc, curr_scc):
    # Note that v has been visited
    visited[v] = True
    # Add it to the current SCC
    curr_scc.append(v)
    # For every adjacent node
    for u in adj_list[v]:
        # If it hasn't been visited
        if visited[u] is False:
            # Call dfs_2 on it
            dfs_2(u, post_order, adj_list, visited, scc, curr_scc)


def construct_kernel(scc, edges):
    outward_conn = []
    outward_conn_scc = []
    # Look through each SCC
    for x in scc:
        # Look through each vertex in that SCC
        for y in x:
            # Identify a list of that vertex's relations with another SC
            for z in edges:
                if y is z[0] and z[1] not in x:
                    outward_conn.append([z[0], z[1]])
    for x in outward_conn:
        for y in range(len(scc)):
            if x[0] in scc[y]:
                print "SCC " + str(y) + " has an outbound edge to SCC",
        for y in range(len(scc)):
            if x[1] in scc[y]:
                print str(y) + "\n by the connection from " + str(x[0]) + " to " + str(x[1]),
        print("\n")
    return


if __name__ == '__main__':
    main()