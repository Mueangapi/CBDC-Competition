import streamlit as st
import pyodbc
import networkx as nx
from pyvis.network import Network
import community as community_louvain
from streamlit.components.v1 import html

st.set_page_config(
    page_title="visualize network",
    page_icon="🍁",
)

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:cbdctest.database.windows.net,1433;Database=Transactions;Uid=CloudSA4ab3329e;Pwd=$sremmaH123456;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Fetch data from the table
cursor.execute('SELECT  TOP 500 * FROM Transactions.Events')
data = cursor.fetchall()

# Create a directed graph using NetworkX
G = nx.Graph()

# Parse data and add nodes/edges to the graph
for row in data:
    sender_id, receiver_id, sender_name, receiver_name, value, _ = row
    
    # Convert value to float
    value = float(value)
    
    # Add nodes and edges to the graph
    G.add_node(sender_name, id=sender_id)
    G.add_node(receiver_name, id=receiver_id)
    G.add_edge(sender_name, receiver_name, value=value)

degree_dict = nx.degree_centrality(G)
betweenness_dict = nx.betweenness_centrality(G)
closeness_dict = nx.closeness_centrality(G)
node_degrees = dict(G.degree())

# Find nodes with the highest degrees
top10 = sorted(node_degrees, key=node_degrees.get, reverse=True)[:10]
communities = community_louvain.best_partition(G)
nx.set_node_attributes(G, communities, 'group')
com_net = Network(width="1400px", height="1400px", bgcolor='#222222', font_color='white')
com_net.from_nx(G)
com_net.save_graph('transaction.html')

# Read the saved HTML content
with open("transaction.html", "r") as file:
    html_code = file.read()

# Streamlit UI
st.title("Network Visualization")
st.subheader("Transaction Network")
st.subheader("Who has the top 10 most interaction with others:")
top10
st.components.v1.html(html_code, width=1600, height=1600)
