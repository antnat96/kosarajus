# Author: Anthony Natale
# Date: October 2022
# Assignment 3, Design and Analysis of Algorithms, ECU
# Instructions:
# 1. Enter 'python main.py' to start the program.
# 2. When prompted to input, paste your graph representation and hit enter TWICE.
# 3. If this fails due to incorrect input formatting, you may enter 'python main.py -f {file_name}' to read from a file.


# Notes: Your program runs correctly for most test cases, though it failed to produce the correct output for my "scc4"
# test case (-12).
# Also, the output contains parallel edges (-5).
# Your implementation appears to run using the correct time complexity.

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
        return self.size > 0

    def rev(self):
        self.items.reverse()


def main():
    edges = []
    n = None
    e = None
    print('Enter the graph representation. When you are finished, enter an empty line and the program will proces '
          'your input')
    while True:
        try:
            line = raw_input()
            if line is None or line == "":
                raise EOFError
            if "\n" in line:
                line = line.replace("\n", "")
            # First input line is number of vertices
            if n is None:
                n = int(line)
            # Second input line is number of edges
            elif e is None:
                e = int(line)
            else:
                stripped_line = line.strip()
                edge_1 = int(stripped_line.split(" ")[0])
                edge_2 = int(stripped_line.split(" ")[1])
                edges.append([edge_1, edge_2])
        except EOFError:
            break

    if e != len(edges):
        print('You may be missing an edge or may have entered extra edges. Please check your input.')

    # Create graph representation and initialize visited list
    adjacency_list = [[]] * n
    visited = [False] * n
    for edge in edges:
        adjacency_list[edge[0]].append(edge[1])

    # Initialize the stack to record post order traversal
    post_order_stack = Stack()
    post_order_stack.push(0)

    # Push vertices to the post_order stack as they (and their children) are done being explored
    dfs_build_post_order(post_order_stack.pop(), post_order_stack, adjacency_list, visited)

    # Reverse the graph
    for y in edges:
        y = y.reverse()

    # Create new graph representation and reinitialize visited list to all False
    reverse_adjacency_list = []
    visited = [False] * n
    for a in range(n):
        reverse_adjacency_list.append([])
    for edge in edges:
        reverse_adjacency_list[edge[0]].append(edge[1])

    # Initialize a list of SCCs
    scc = []
    # And a list describing the SCC currently being built by the DFS
    curr_scc = []

    while post_order_stack.has_elements() is True:
        v = post_order_stack.pop()
        if visited[v] is False:
            dfs_2(v, post_order_stack, reverse_adjacency_list, visited, scc, curr_scc)
            scc.append(curr_scc)
            curr_scc = []

    # Print the strongly connected components
    if len(scc) != n:
        print("There are " + str(len(scc)) + " Strongly Connected Components:")
        for x in range(len(scc)):
            print "SCC",
            print x,
            print ":",
            for y in scc[x]:
                print str(y),
            print("\n")
        print("Kernel Graph Adjacency List (SCC Connections):")
        construct_kernel(scc, edges)

    else:
        print("Each component stands alone-that is, there are no strongly connected components because no 2 components "
              "have connections to one another according to our adjacency list.")


def dfs_build_post_order(v, post_order, adj_list, visited):
    # Note that v has been visited
    visited[v] = True
    # For every adjacent node
    for u in adj_list[v]:
        # If it hasn't been visited
        if visited[u] is False:
            # Call dfs_1 on it
            dfs_build_post_order(u, post_order, adj_list, visited)
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


def construct_kernel(sccs, edges):
    outward_connections = []

    # Look through each SCC
    for scc in sccs:
        # Look through each vertex in that SCC
        for scc_vertex in scc:
            # Identify a list of that vertex's relations with another SCC
            for edge in edges:
                if scc_vertex is edge[0] and edge[1] not in scc:
                    outward_connections.append([edge[0], edge[1]])

    unique_edges = []
    # Display unique connections between SCCs
    for outward_connection in outward_connections:
        edge = []
        for y in range(len(sccs)):
            if outward_connection[1] in sccs[y]:
                edge.append(y)
            if outward_connection[0] in sccs[y]:
                edge.append(y)
            if len(edge) != 2:
                continue
            exists = any(unique_edge[0] == edge[0] and unique_edge[1] == edge[1] for unique_edge in unique_edges)
            if exists is False:
                unique_edges.append(edge)

    for unique_edge in unique_edges:
        print unique_edge[0], unique_edge[1], "\n"


if __name__ == '__main__':
    main()
