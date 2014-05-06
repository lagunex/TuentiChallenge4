'''
Extracted from Wikipedia

http://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

The method find_path in Wikipedia uses DFS. I replaced it by BFS using

http://semanticweb.org/wiki/Python_implementation_of_Edmonds-Karp_algorithm
'''
class Edge(object):
    def __init__(self, name, u, v, w):
        self.name = name
        self.source = u
        self.sink = v  
        self.capacity = w
        self.redge = None
    def __repr__(self):
        return "%s:%s->%s:%s" % (self.name, self.source, self.sink, self.capacity)

class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
 
    def get_vertex(self):
        return self.adj.keys()

    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, name, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(name,u,v,w)
        redge = Edge(name,v,u,0)
        edge.redge = redge  
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink):
        queue = [source]                 
        paths = {source: []}
        while queue:
            vertex = queue.pop(0)
            for edge in self.get_edges(vertex):
                if edge.capacity - self.flow[edge] > 0 and edge.sink not in paths:
                    paths[edge.sink] = paths[edge.source] + [edge]
                    if edge.sink == sink:
                        return paths[edge.sink]
                    queue.append(edge.sink)
        return None
   
    def max_flow(self, source, sink):
        path = self.find_path(source, sink)
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink)
        return sum(self.flow[edge] for edge in self.get_edges(source))
