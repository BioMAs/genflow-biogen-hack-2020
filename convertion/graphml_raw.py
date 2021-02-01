 
 
import networkx as nx

import io,sys

from pygraphml import GraphMLParser
from pygraphml import Graph


##################parameters

# for string
#inputfile = io.BytesIO(s.encode('UTF-8'))

inputfile="nextflow.gexf"
wcase="gexf"

inputfile="snakemake.dot"
wcase="dot"


outputfile="graph.xml"
##################



if wcase=="gexf":
  ig=nx.Graph(nx.read_gexf(inputfile))

elif wcase=="dot":
  ig=nx.drawing.nx_pydot.read_dot(inputfile)


def write_raw_graphml(ig,outputfile,wcase):

  g = Graph()
  directed=True


  #print(ig.graph)
  #print("============")


  ndict=dict()
  ndictobj=dict()
  edict=dict()

  #print("==================")
  for nod_id,ndata in ig.nodes(data=True):
    print(nod_id)
    print(ndata)
    node = g.add_node("%s" %(nod_id))
     
    ndict[nod_id]=ndata
    ndictobj[nod_id]=node
    for key,val in ndata.items():
       node[key]=val



  for nod,nbrsdict in ig.adjacency():
      print("%s ->  %s" %(nod,nbrsdict))
      for nod_nbr,keydict in nbrsdict.items():
        print(nod_nbr)
        edge=g.add_edge(ndictobj[nod], ndictobj[nod_nbr],directed)
          
        #edict[nod_id]=ndata
        for key,eattr in keydict.items():
            print("%s:%s" %(key,eattr)) 
            print("zz"+str(key))
            

            if wcase=="gexf":
              edge[key]=eattr

            elif wcase=="dot":
              for xkey,xeattr in eattr.items():
                   edge[xkey]=xeattr
             


  
  print("going to write %s" %(outputfile))

  parser = GraphMLParser() 
  parser.write(g, outputfile)

def read_graphml_raw(rawfile):

  parser = GraphMLParser()
  g = parser.parse(rawfile)

 
  edges = g.edges()
  for edge in edges:
     print(edge)

  nodes = g.nodes()
  for node in nodes:
     print(node)


  


write_raw_graphml(ig,outputfile,wcase)

    

read_graphml_raw(outputfile)


