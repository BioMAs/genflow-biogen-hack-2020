
#graphml manipulation in python

import graph_tool.all as gt

graph = gt.Graph(directed=True) 

graph.ep.weight=graph.new_edge_property("double",val=0.0)
graph.vp.command=graph.new_vertex_property("string",val="undef");
 

 
n1=graph.add_vertex()
n2=graph.add_vertex()
e1=graph.add_edge(n1, n2)

graph.ep["weight"][e1]="12"

graph.vp["command"][n1]="blastall"
graph.vp["command"][n2]="hitmerge"

for v in  graph.vertices():
           cval=graph.vp["command"][v]
           print(cval)
for e in  graph.edges():
           cval=graph.ep["weight"][e]
           print(cval)
print("==write====")
            
graphml_file="graph.xml"
g=gt.Graph(graph, prune=True)
g.save(graphml_file)

print("===load===")

g2=gt.load_graph(graphml_file)
g2.set_directed(True)
g2=gt.Graph(g2, prune=True)

print("======")
for v in  g2.vertices():
           cval=g2.vp["command"][v]
           print(cval)
