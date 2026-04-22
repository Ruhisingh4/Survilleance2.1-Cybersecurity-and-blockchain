import networkx as nx

def build_graph(df):
    """
    Creates node relationships between ID, User, and Device.
    Returns the networkx graph object.
    """
    G = nx.Graph()
    
    for _, row in df.iterrows():
        id_node = f"ID:{row['ID_Code']}"
        user_node = f"User:{row['User']}"
        device_node = f"Device:{row['Device']}"
        
        # Add edges representing usage
        G.add_edge(user_node, id_node, time=row['Time'], attempts=row['Attempts'])
        G.add_edge(id_node, device_node, time=row['Time'], attempts=row['Attempts'])
        
    return G

def get_suspicious_nodes(G, degree_threshold=2):
    """
    Identifies suspicious nodes (e.g. an ID used across many devices/users).
    """
    suspicious = []
    for node, degree in dict(G.degree()).items():
        if degree > degree_threshold:
            suspicious.append({"node": node, "connections": degree})
    return suspicious
