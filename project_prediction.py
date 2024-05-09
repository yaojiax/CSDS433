import pandas as pd
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

graph = nx.read_graphml('graph_data.graphml')

edges = graph.edges(data=False)
df = pd.DataFrame(edges, columns=['source', 'target'])

#remove float
df['source'] = pd.to_numeric(df['source'], errors='coerce')
df['target'] = pd.to_numeric(df['target'], errors='coerce')
df = df.dropna()

X = df[['source']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")