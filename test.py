from notion.client import NotionClient
from notion.collection import CollectionRowBlock
from graph_tool.all import Graph, graph_draw

client = NotionClient(token_v2='[token]')

#page = client.get_block('https://www.notion.so/Knowledge-a078d9ed592c459e93e8f7a1e433bcd2')

data = client.get_collection_view('[database page link]')

graph = Graph(directed=False)

# Dictionary from entry id to vertex id to keep track of vertices that have been added
entries = {}

vertex_names = graph.new_vertex_property('string')

# For every table entry
for row in data.collection.get_rows():

    # If this entry is not in the graph, add it
    if row.id not in entries:
        entries[row.id] = graph.add_vertex()
        vertex_names[entries[row.id]] = row.title

    # Add the links of the current entry to the graph
    for child in row.children:
        if isinstance(child, CollectionRowBlock):

            if child.id not in entries:
                entries[child.id] = graph.add_vertex()
                vertex_names[entries[child.id]] = child.title

            graph.add_edge(entries[row.id], entries[child.id])

graph_draw(graph, vertex_text=vertex_names, vertex_font_size=8, vertex_size=50, output='test.pdf')
