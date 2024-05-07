import networkx as nx

# Step 4: Read Graph from GraphML
def read_graph(file_path):
    return nx.read_graphml(file_path)


# Usage: Read the graph from the saved GraphML file
graph_file_path = "graph_data.graphml"
G = read_graph(graph_file_path)

# Now you can use the graph G as needed
print("Number of nodes:", G.number_of_nodes())
print("Number of edges / G1 recommendations:", G.number_of_edges())
print("Graph density:", nx.density(G))

# Sort edges by weight
sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)

# Get top 10 recommendations
top_recommendations = sorted_edges[:10]

# Print top 10 recommendations
print("\nTop 10 Recommendations:")
for i, (source, target, data) in enumerate(top_recommendations):
    print(f"{i + 1}. {source} -> {target}, Weight: {data['weight']}")

# a-> b -> c
def find_cascade_recommendations(G, top_n=10):
    cascade_recommendations = []

    for node in G.nodes():
        if G.out_degree(node) >= 2:
            # successors of the node
            successors = list(G.successors(node))
            filtered_successors = [successor for successor in successors if G.out_degree(successor) >= 2]
            if len(filtered_successors) >= 2:
                sorted_successors = sorted(filtered_successors, key=lambda x: sum([G[node][successor]["weight"] for successor in successors]), reverse=True)
                cascade_recommendations.append((node, sorted_successors[:2]))

    #sort base on total weight of their edges
    
    print("Number of Cascade recmmendations: " + str(len(cascade_recommendations)))

    cascade_recommendations = sorted(cascade_recommendations, key=lambda x: sum([G[x[0]][node]["weight"] for node in x[1]]), reverse=True)
    
    return cascade_recommendations[:top_n]

def find_split_recommendations(G, top_n=10):
    split_recommendations = []

    for node in G.nodes():
        successors = list(G.successors(node))

        if len(successors) >= 2:
            pairs = [(successors[i], successors[j]) for i in range(len(successors)) for j in range(i + 1, len(successors))]
            pair_weights = [(pair, G[node][pair[0]]['weight'] + G[node][pair[1]]['weight']) for pair in pairs]
            sorted_pairs = sorted(pair_weights, key=lambda x: x[1], reverse=True)
            split_recommendations.extend([(node, pair[0], pair[1], weight) for pair, weight in sorted_pairs[:2]])

    split_recommendations.sort(key=lambda x: x[3], reverse=True)

    print("Number of Split recmmendations: " + str(len(split_recommendations)))

    return split_recommendations[:top_n]

split_recommendations = find_split_recommendations(G)

print("Top 10 Split Recommendations:")
for i, (node, B, C, total_weight) in enumerate(split_recommendations[:10]):
    print(f"{i + 1}. {node} -> {B} and {node} -> {C} (Total Weight: {total_weight})")


cascade_recommendations = find_cascade_recommendations(G)

# Print the top 10 cascade recommendations
print("\nTop 10 Cascade Recommendations:")
for i, (A, (B, C)) in enumerate(cascade_recommendations[:10]):
    total_weight = sum([G[A][B]["weight"] for B in (B, C)])
    print(f"{i + 1}. {A} -> {B} -> {C} (Total Weight: {total_weight})")