from matplotlib import pyplot as plt
import networkx as nx
G=nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8])
G.add_edges_from([(1,2),(2,3),(3,4),(4,1),(4,5),(5,6),(6,4)])
G1=nx.Graph()
G1.add_nodes_from([1,2,3,4,5,6,7,8])
G1.add_edges_from([(1,2),(2,3),(3,4)])
#nx.draw_networkx(G)

try:
    f1 = nx.algorithms.find_cycle(G)
    print(list(f1))
    f2 = nx.algorithms.cycle_basis(G)
    print(type(f2))
    print(list(f2))
    f1 = nx.algorithms.find_cycle(G1)
    print(list(f1))
    f2 = nx.algorithms.cycle_basis(G1)
    
    print(type(f2))
    print(list(f2))
    for cycles in f2:
        print(cycles)
        for item in cycles:
            print(item)
    if f2:
        print("has loop")
    else:
        print("no loop")
except: #Exception as e:
    #print(e.args)
    pass
#plt.show()
