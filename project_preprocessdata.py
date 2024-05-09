import networkx as nx


def preprocess_data(file_path):
    products = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Process each line
        current_product = {}
        for line in lines:
            line = line.strip() 
            
            if line.startswith("Id:"):
                if current_product:  #exising product being processed
                    products.append(current_product)
                current_product = {"Id": int(line.split()[1])}  
            elif line.startswith("ASIN:"):
                current_product["ASIN"] = line.split()[1]
            elif line.startswith("title:"):
                title = line.split(": ", 1)[1]
                current_product["title"] = line.split(": ", 1)[1]
            elif line.startswith("group:"):
                current_product["group"] = line.split()[1]
            elif line.startswith("salesrank:"):
                current_product["salesrank"] = int(line.split()[1])
            elif line.startswith("similar:"):
                similar_asins = line.split()[2:]
                if similar_asins:
                    current_product["similar"] = similar_asins
            elif line.startswith("categories:"):
                categories = line.split("|")[1:]
                current_product["categories"] = [category.strip() for category in categories]
            elif line.startswith("reviews:"):
                review_info = line.split(": ")
                review_data = {
                    "total": int(review_info[2].split(" ")[0]),
                    "downloaded": int(review_info[3].split(" ")[0]),
                    "avg_rating": float(review_info[4]),
                    "reviews": []
                }
                current_product["reviews"] = review_data
            elif line.startswith(" "): 
                review_data = line.split()
                review = {
                    "date": review_data[0],
                    "customer": review_data[2],
                    "rating": int(review_data[4]),
                    "votes": int(review_data[6]),
                    "helpful": int(review_data[8])
                }
                current_product["reviews"]["reviews"].append(review)

        if current_product: #last product being processed
            products.append(current_product)
    
    return products

def create_graph(data):
    G = nx.DiGraph()  #dirgraph
    for product in data:
        G.add_node(product["ASIN"])

    for product in data:
        if "similar" in product:
            for similar_asin in product["similar"]:
                G.add_edge(product["ASIN"], similar_asin, weight=product["reviews"]["total"])

    return G

def save_graph(graph, file_path):
    nx.write_graphml(graph, file_path)

file_path = "amazon-meta.txt"
data = preprocess_data(file_path)

def get_title_from_asin(data, asin):
    for product in data:
        if product["ASIN"] == asin:
            return product.get("title", "Title not found")
    return "ASIN not found"


# asin_to_find = "0807281956"  
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)

# asin_to_find = "0807286001"  
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)


# asin_to_find = "0786222727"  
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)


# asin_to_find = "0590353403"
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)


# asin_to_find = "0807281751" 
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)


# asin_to_find = "043936213X"  
# title = get_title_from_asin(data, asin_to_find)
# print("Title:", title)


G = create_graph(data)

graph_file_path = "graph_data.graphml"
save_graph(G, graph_file_path)