import os
import ast
import argparse
import networkx as nx
import plotly.graph_objects as go

class ImportVisitor(ast.NodeVisitor):
    def __init__(self, current_module):
        super().__init__()
        self.current_module = current_module
        self.imported_modules = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imported_modules.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        parts = self.current_module.split('.')
        if node.level > len(parts):
            self.generic_visit(node)
            return
        base = parts[:len(parts) - node.level] if node.level else []
        base_str = '.'.join(base)
        if node.module:
            full_module = (base_str + '.' if base_str else '') + node.module
            self.imported_modules.add(full_module)
        else:
            for alias in node.names:
                full_module = (base_str + '.' if base_str else '') + alias.name
                self.imported_modules.add(full_module)
        self.generic_visit(node)

def get_py_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)

def main():
    parser = argparse.ArgumentParser(description="CLI tool to visualize Python import relationships as a graph.")
    parser.add_argument('directory', nargs='?', default='.', help='Root directory to analyze (default: current directory)')
    parser.add_argument('--output', default=None, help='Output HTML file (if not provided, show in browser)')
    parser.add_argument('--dim', type=int, default=3, choices=[2, 3], help='Dimension of the graph (2 or 3)')
    parser.add_argument('--include-external', action='store_true', help='Include external dependencies in the graph')
    parser.add_argument('--seed', type=int, default=42, help='Seed for layout reproducibility')
    parser.add_argument('--show-shared', action='store_true', help='Print top shared modules (by degree) after visualization')
    args = parser.parse_args()

    # Collect all internal modules
    modules = {}
    for filepath in get_py_files(args.directory):
        rel_path = os.path.relpath(filepath, args.directory).replace(os.sep, '/')
        if rel_path.endswith('__init__.py'):
            module_name = rel_path[:-len('/__init__.py')].strip('/').replace('/', '.')
        else:
            module_name = rel_path[:-3].replace('/', '.')
        if module_name.startswith('.'):
            module_name = module_name.lstrip('.')
        if not module_name:
            continue  # Skip root __init__.py if no package name
        modules[module_name] = filepath

    # Build the graph
    G = nx.Graph()  # Undirected graph for relationships

    for module, filepath in modules.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                source = f.read()
                tree = ast.parse(source)
            except Exception as e:
                print(f"Warning: Could not parse {filepath}: {e}")
                continue

        visitor = ImportVisitor(module)
        visitor.visit(tree)

        for imp_mod in visitor.imported_modules:
            if imp_mod in modules or args.include_external:
                G.add_edge(module, imp_mod)

    if not G.nodes():
        print("No imports found in the provided directory.")
        return

    # Compute layout
    pos = nx.spring_layout(G, dim=args.dim, seed=args.seed)

    # Prepare node trace
    labels = list(G.nodes())
    if args.dim == 3:
        x_nodes = [pos[node][0] for node in G.nodes()]
        y_nodes = [pos[node][1] for node in G.nodes()]
        z_nodes = [pos[node][2] for node in G.nodes()]
        node_trace = go.Scatter3d(
            x=x_nodes, y=y_nodes, z=z_nodes,
            mode='markers+text',
            text=labels,
            textposition='top center',
            marker=dict(size=6, color='skyblue'),
            hoverinfo='text'
        )
        edge_traces = []
        for edge in G.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_traces.append(go.Scatter3d(
                x=[x0, x1], y=[y0, y1], z=[z0, z1],
                mode='lines',
                line=dict(color='gray', width=2),
                hoverinfo='none'
            ))
        fig = go.Figure(data=[node_trace] + edge_traces)
        fig.update_layout(
            title=f"Python Import Graph in 3D for {args.directory}",
            showlegend=False,
            margin=dict(l=0, r=0, b=0, t=40),
            scene=dict(
                xaxis=dict(showbackground=False, visible=False),
                yaxis=dict(showbackground=False, visible=False),
                zaxis=dict(showbackground=False, visible=False),
            )
        )
    else:  # dim=2
        x_nodes = [pos[node][0] for node in G.nodes()]
        y_nodes = [pos[node][1] for node in G.nodes()]
        node_trace = go.Scatter(
            x=x_nodes, y=y_nodes,
            mode='markers+text',
            text=labels,
            textposition='top center',
            marker=dict(size=10, color='skyblue'),
            hoverinfo='text'
        )
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_traces.append(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(color='gray', width=2),
                hoverinfo='none'
            ))
        fig = go.Figure(data=[node_trace] + edge_traces)
        fig.update_layout(
            title=f"Python Import Graph in 2D for {args.directory}",
            showlegend=False,
            margin=dict(l=0, r=0, b=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False)
        )

    # Display or save
    if args.output:
        fig.write_html(args.output)
        print(f"Graph saved to {args.output}")
    else:
        fig.show()

    # Optional: Show top shared modules (highest degree, indicating shared relationships)
    if args.show_shared:
        degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]  # Top 10
        print("\nTop shared modules/packages (by number of connections):")
        for node, degree in degrees:
            print(f"{node}: {degree} connections")

if __name__ == "__main__":
    main()