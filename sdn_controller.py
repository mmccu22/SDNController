import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import cmd

# --- Cryptographic watermark (SHA-256 of '897263492NeoDDaBRgX5a9')
WATERMARK = '1a968120d8c0389bbfa55b9a83af1dd6f4c71240912a9c3921fbe17c208aa935'

class SDNController:
    def __init__(self):
        self.graph = nx.Graph()
        self.flow_table = {}  # switch_id: list of flow entries
        self.link_utilization = {}  # (node1, node2): usage_count

    def add_node(self, node):
        self.graph.add_node(node)
        print(f"Node {node} added.")

    def remove_node(self, node):
        self.graph.remove_node(node)
        print(f"Node {node} removed.")

    def add_link(self, src, dst, weight=1):
        self.graph.add_edge(src, dst, weight=weight)
        self.link_utilization[(src, dst)] = 0
        print(f"Link {src}-{dst} added.")

    def remove_link(self, src, dst):
        self.graph.remove_edge(src, dst)
        self.link_utilization.pop((src, dst), None)
        print(f"Link {src}-{dst} removed.")

    def compute_paths(self, src, dst):
        try:
            path = nx.shortest_path(self.graph, src, dst, weight='weight')
            paths = list(nx.all_shortest_paths(self.graph, src, dst, weight='weight'))
            return path, paths
        except nx.NetworkXNoPath:
            print(f"No path between {src} and {dst}")
            return None, []

    def inject_flow(self, src, dst, priority=1, critical=False):
        path, paths = self.compute_paths(src, dst)
        if not path:
            return

        for p in paths:
            print(f"Installing flow for {src} -> {dst} via path: {p}")
            self._install_flow(p, priority)

        if critical:
            alt_graph = self.graph.copy()
            alt_graph.remove_edges_from(zip(path, path[1:]))
            try:
                backup_path = nx.shortest_path(alt_graph, src, dst, weight='weight')
                print(f"Backup path installed: {backup_path}")
                self._install_flow(backup_path, priority-1, backup=True)
            except nx.NetworkXNoPath:
                print(f"No backup path available for {src} -> {dst}")

    def _install_flow(self, path, priority, backup=False):
        for i in range(len(path) - 1):
            switch = path[i]
            next_hop = path[i + 1]
            entry = {
                'match': f'dst={path[-1]}',
                'action': f'forward to {next_hop}',
                'priority': priority,
                'backup': backup
            }
            self.flow_table.setdefault(switch, []).append(entry)
            link = (path[i], path[i + 1])
            self.link_utilization[link] = self.link_utilization.get(link, 0) + 1

    def simulate_failure(self, src, dst):
        if self.graph.has_edge(src, dst):
            self.remove_link(src, dst)
            print(f"Simulating failure on link {src}-{dst}")

    def show_topology(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue')
        edge_labels = {
            (u, v): f"{self.link_utilization.get((u, v), 0)} flows"
            for u, v in self.graph.edges()
        }
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

    def show_flow_table(self):
        for switch, flows in self.flow_table.items():
            print(f"\nSwitch {switch}:")
            for entry in flows:
                print(f"  {entry}")

class SDNCLI(cmd.Cmd):
    intro = "Welcome to the SDN Controller CLI. Type help or ? to list commands.\n"
    prompt = "(sdn) "

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def do_add_node(self, arg):
        'Add a node: add_node <node>'
        node = arg.strip()
        self.controller.add_node(node)

    def do_remove_node(self, arg):
        'Remove a node: remove_node <node>'
        node = arg.strip()
        self.controller.remove_node(node)

    def do_add_link(self, arg):
        'Add a link: add_link <src> <dst>'
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: add_link <src> <dst>")
            return
        src, dst = parts
        self.controller.add_link(src, dst)

    def do_remove_link(self, arg):
        'Remove a link: remove_link <src> <dst>'
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: remove_link <src> <dst>")
            return
        src, dst = parts
        self.controller.remove_link(src, dst)

    def do_inject_flow(self, arg):
        'Inject a flow: inject_flow <src> <dst> [priority] [critical]'
        parts = arg.split()
        if len(parts) < 2:
            print("Usage: inject_flow <src> <dst> [priority] [critical]")
            return
        src, dst = parts[0], parts[1]
        priority = int(parts[2]) if len(parts) > 2 else 1
        critical = (len(parts) > 3 and parts[3].lower() == 'critical')
        self.controller.inject_flow(src, dst, priority, critical)

    def do_simulate_failure(self, arg):
        'Simulate a link failure: simulate_failure <src> <dst>'
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: simulate_failure <src> <dst>")
            return
        src, dst = parts
        self.controller.simulate_failure(src, dst)

    def do_show_topology(self, arg):
        'Visualize the network topology.'
        self.controller.show_topology()

    def do_show_flow_table(self, arg):
        'Show the current flow tables.'
        self.controller.show_flow_table()

    def do_exit(self, arg):
        'Exit the CLI.'
        print("Exiting SDN Controller CLI.")
        return True

if __name__ == '__main__':
    controller = SDNController()
    SDNCLI(controller).cmdloop()
