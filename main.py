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
    adjacency_list = []
    visited = [False] * n
    for a in range(n):
        adjacency_list.append([])
    for x in edges:
        adjacency_list[x[0]].append(x[1])

    # Initialize the stack to record post order traversal
    post_order_stack = Stack()
    post_order_stack.push(0)

    # First DFS - Pushes vertices to the post_order stack as they (and their children) are done being explored
    dfs_build_post_order(post_order_stack.pop(), post_order_stack, adjacency_list, visited)

    # TODO: Change the following to work without explicitly constructing the reverse graph
    # Reverse the graph
    for y in edges:
        y = y.reverse()

    # Create new graph representation and reinitialize visited list to all False
    adjacency_list = []
    visited = [False] * n
    for a in range(n):
        adjacency_list.append([])
    for x in edges:
        adjacency_list[x[0]].append(x[1])

    # Initialize a list of SCCs
    scc = []
    # And a list describing the SCC currently being built by the DFS
    curr_scc = []

    # Second DFS - Uses the reversed graph to identify the strongly connected components
    # dfs_2(post_order.pop(), post_order, adj_list, visited, scc, curr_scc)

    while post_order_stack.has_elements() is True:
        v = post_order_stack.pop()
        if visited[v] is False:
            dfs_2(v, post_order_stack, adjacency_list, visited, scc, curr_scc)
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