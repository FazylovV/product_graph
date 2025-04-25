import networkx as nx
import pandas as pd

# Загрузка данных из CSV-файла
df = pd.read_csv('./data/pairs_of_products.csv')

# Создание направленного графа
G = nx.DiGraph()
for _, row in df.iterrows():
    source_product = row.iloc[0]
    target_product = row.iloc[1]
    G.add_edge(source_product, target_product)

# Вычисляем необходимые меры центральной значимости вершин

# In-degree centrality (количество входящих рёбер)
in_degree_centralities = dict(nx.in_degree_centrality(G))

# Eigenvector centrality (центральность собственных значений)
# eigenvector_centralities = dict(nx.eigenvector_centrality_numpy(G))

# Betweenness centrality (промежуточность)
betweenness_centralities = dict(nx.betweenness_centrality(G))

# Чтобы рассчитать фрагментированность сети (Fragmentation), сначала нам нужно удалить каждую вершину,
# оценить число компонент связности после удаления и сравнить с исходным числом компонентов.
# def calculate_fragmentation_centrality(graph):
#     # Исходное число компонент связности
#     initial_components = len(list(nx.connected_components(graph.to_undirected())))
    
#     fragmentation_centralities = {}
#     for node in graph.nodes():
#         H = graph.copy()  # Создаем копию графа
#         H.remove_node(node)  # Удаляем вершину
        
#         # Число компонент связности после удаления узла
#         components_after_removal = len(list(nx.connected_components(H.to_undirected())))
        
#         # Разница показывает степень увеличения числа компонент
#         fragmentation_centralities[node] = components_after_removal - initial_components
    
#     return fragmentation_centralities

# fragmentation_centralities = calculate_fragmentation_centrality(G)

# Собираем результаты вместе
centralities_df = pd.DataFrame({
    'InDegree': list(in_degree_centralities.values()),
    'Betweenness': list(betweenness_centralities.values()),
}, index=in_degree_centralities.keys())

print(centralities_df)
