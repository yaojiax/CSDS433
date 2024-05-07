<strong>Code for co-purchasing analysis with Amazon purchasing data</strong>

Dataset: https://snap.stanford.edu/data/amazon-meta.html

Inspiration on finding subgraphs: https://www.cs.cornell.edu/home/kleinber/pakdd06-cascade.pdf

Brief overview: 
Represented the Amazon co-purchasing network as a graph with Python

Directed graph 

Vertices: The various Amazon ASINs of the product

Edge: A has an edge to B if B is one of the similar products of A 

Weight: Reviews of A

project_preprocessdata.py - does the processing of the .txt file into the graph using NX

project_check_data_graph.py - the data mining is done here

Done as final project for CSDS 433 at Case Western Reserve University: Database Systems.

