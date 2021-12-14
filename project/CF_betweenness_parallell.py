from multiprocessing import Pool
import time
import itertools
import osmnx as ox
import numpy as np
import networkx as nx

def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def betweenness_centrality_parallel(G, processes=None, **kwargs):
    """Parallel betweenness centrality  function"""    
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)

    bt_sc = p.starmap(
        nx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            ["travel_time"] * num_chunks,
            
        ), 
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

def load_centrality_parallel(G, processes=None, **kwargs):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)

    bt_sc = p.starmap(
        nx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            ["travel_time"] * num_chunks,

        ),
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

from abc import ABC, abstractmethod
class AbstractStrategy:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    @abstractmethod
    def get_metric(self, graph: nx.Graph):
        pass

    @abstractmethod
    def __str__(self):
        pass

class BetweennessStrategy(AbstractStrategy):
    def __init__(self, k, normalized, weight):
        super(BetweennessStrategy, self).__init__(k=k, normalized=normalized, weight=weight)

    def get_metric(self, graph: nx.Graph):
        return betweenness_centrality_parallel(graph, **self.kwargs)
    
    def __str__(self):
        return f"Betweenness_k={self.kwargs['k']}_norm={int(self.kwargs['normalized'])}_weight={self.kwargs['weight']}"


class LoadCentralityStrategy(AbstractStrategy):
    def __init__(self, k, normalized, weight):
        super(LoadCentralityStrategy, self).__init__(k=k, normalized=normalized, weight=weight)

    def get_metric(self, graph: nx.Graph):
        return load_centrality_parallel(graph, **self.kwargs)

    def __str__(self):
        return f"Load_centrality_norm={int(self.kwargs['normalized'])}_weight={self.kwargs['weight']}"


class PercolationStrategy(AbstractStrategy):
    def __init__(self):
        super(PercolationStrategy,self).super()
    


    def get_metric(self, graph: nx.Graph):
        return nx.percolation_centrality(graph)

class BetweennessStrategyFast(AbstractStrategy):
    """
    Takes a sample of nodes for the betweenness metric.
    In order to stay statistically relevant the betweenness metric is executed
    iterations times and then averaged.
    """
    def __init__(self, k, normalized, weight, iterations):
        self.iterations = iterations
        super(BetweennessStrategyFast, self).__init__(k=k, normalized=normalized, weight=weight)

    def get_metric(self, graph: nx.Graph):
        betweennesses = []
        for i in range(self.iterations):
            betweennesses.append(nx.betweenness_centrality(graph, **self.kwargs))
        
        result = {}
        for node in betweennesses[0].keys():
            temp = 0
            for b in betweennesses:
                temp+=b[node]
            result[node] = temp/len(betweennesses)

        return result
    
    def __str__(self):
        return f"Betweenness_k={self.kwargs['k']}_norm={int(self.kwargs['normalized'])}_weight={self.kwargs['weight']}"
    
import pandas as pd
class CascadeFailure:
    def __init__(self, path: str, ox_path: str, strategy: AbstractStrategy, multiplier: float=1.5):
        self.path = path
        self.ox_path = ox_path
        self.strategy = strategy
        self.muliplier = multiplier
        self.prepare_graph()
        self.failed_nodes = []

    def __str__(self):
        return f"CF_max_multiplier={self.muliplier}_{self.strategy}"

    def prepare_graph(self):
        self.graph = nx.read_gml(self.path) 
        self.graph = self.get_largest_component(self.graph)
        #betweenness = nx.betweenness_centrality(self.graph, k=k)
        #self.graph = self.strategy.prepare_graph(self.graph)
        metric = self.strategy.get_metric(self.graph)
        for key in metric.keys():
            n = self.graph.nodes()[key]
            #n["is_active"] = True
            n["metric"] = metric[key]
            n["max_metric"] = metric[key] * self.muliplier


    def get_largest_component(self,graph)->nx.Graph:
        largest_component = list(sorted(nx.strongly_connected_components(graph), key=len, reverse=True))[0]
        return graph.subgraph(largest_component).copy()

    def create_images(self, save, filepath, show):
        max_iterations = len(self.failed_nodes)
        #self.create_image(self.failed_nodes[:1], save, f"{filepath}_initial.png",show,max_color=max_iterations)
        self.create_image(self.failed_nodes, save=True, filepath=filepath, max_color=max_iterations)
        #for i in range(1,len(self.failed_nodes)):
        #    self.create_image(self.failed_nodes[:i+1], save, f"{filepath}_iter#{i-1}.png",show,max_color=max_iterations )

    def create_image(self, save=False, filepath=None, show=False):
        ox_graph = ox.load_graphml(self.ox_path)
        ox_graph = self.get_largest_component(ox_graph)



        colors = ox.plot.get_colors(n=len(self.failed_nodes)+1, cmap="Paired")
        node_colors = {}

        for node in ox_graph:
            node_colors[int(node)] = colors[0]
        for i, failed in enumerate(self.failed_nodes):
            print(f"Creating image {i}")
            for node in failed:
                node_colors[int(node)] = colors[i+1]
            if i == 0:
                fp = f"{filepath}_initial.png"
            else:
                fp = f"{filepath}_iteration{i}.png"
            node_colors = pd.Series(node_colors)

            ox.plot_graph(ox_graph, node_color=node_colors, edge_color="w", figsize=(20,20), bgcolor="k", save=save, filepath=fp, show=show)

    def get_len_failed_nodes(self):
        count = 0
        for fn in self.failed_nodes:
            count+=len(fn)
        return count

    def attack_nodes(self, n=20, removal_mode="random", image_each_iteration=False, attack_number=1,filepath="imgs/cascade"):

        if removal_mode=="random":
            failed_nodes = []
            for i in range(n):
                node = np.random.choice(self.graph)
                self.graph.remove_node(node)
                failed_nodes.append(node)
            self.failed_nodes.append(failed_nodes)

        if removal_mode == "target":
            failed_nodes = []
            for i in range(n):
                node_to_remove = None
                max = -1
                for node in self.graph:
                    curr_node = self.graph.nodes()[node]
                    if curr_node["metric"]>max:
                        node_to_remove = node
                        max = curr_node["metric"]
                failed_nodes.append(node_to_remove)
                self.graph.remove_node(node_to_remove)
            self.failed_nodes.append(failed_nodes)

        print(f"Removed {n} nodes with mode {removal_mode}.")

        print("Start Cascading")
        iteration = 0

        while True:
            
            metric = self.strategy.get_metric(self.graph)
            nodes_to_remove = []
            for key in metric.keys():
                node = self.graph.nodes()[key]
                if node["max_metric"] <= metric[key]:
                    nodes_to_remove.append(key)

            print(f"Cascading iteration {iteration} overloaded {len(nodes_to_remove)}")
            if len(nodes_to_remove) == 0:
                break
            self.failed_nodes.append(nodes_to_remove)
            self.graph.remove_nodes_from(nodes_to_remove)

            print(f"Remaining nodes: {self.graph.number_of_nodes()}")

            iteration+=1

        if image_each_iteration:
            self.create_image(save=True, filepath=f"{filepath}/{self}_attack#{attack_number}_{removal_mode}_n#{n}_", show=False)


import json
if __name__ == "__main__":
    
    for i in range(100):
        start=time.perf_counter()
        print(f"iteration: {i}")
        bs = BetweennessStrategy(k=None, normalized=True, weight="travel_time")
        cf = CascadeFailure("data/cleaned_manhattan.gml", "data/uncleaned_manhattan.graphml",strategy=bs,multiplier=4)
        cf.attack_nodes(1, removal_mode="random", image_each_iteration=False)
        
        data = {
            "n_failed": cf.get_len_failed_nodes(),
            "nodes": cf.failed_nodes
        }
        
        with open(f"cf_data/{cf}.csv", "a+") as f:
            f.writelines([f"{json.dumps(data)}\n"]) 
        end = time.perf_counter()
        print(f"took: {end-start}s")
