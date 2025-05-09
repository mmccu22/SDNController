This project implements a **Software-Defined Networking (SDN) controller** in Python, simulating the behavior of OpenFlow switches. 
The controller maintains a dynamic network topology, computes routing paths, handles link failures, and visualizes the network in real-time.

## Features

- **Network Topology Management:**
  - Add/remove nodes and links dynamically.
  - Visual representation of the network graph.

- **Path Computation:**
  - Computes shortest paths between nodes.
  - Load-balances traffic across multiple equal-cost paths.

- **Traffic Engineering:**
  - Supports flow prioritization based on source/destination.
  - Automatically installs backup paths for critical flows.

- **Failure Handling:**
  - Simulates link failures and updates routes accordingly.

- **Visualization:**
  - Shows the network topology.
  - Displays active flows and link utilization (flow counts on edges).

- **CLI Interface:**
  - Interactive commands for managing the SDN controller.

## Requirements

- Python 3.x
- `networkx`
- `matplotlib`

### Install dependencies:
pip install networkx matplotlib
How to Run
Save the main Python file as:

sdn_controller.py
Run the controller using:
python sdn_controller.py

Below are sample commands you can use to test the controller:

# Add nodes
add_node A
add_node B
add_node C
add_node D

# Add links
add_link A B
add_link B C
add_link C D
add_link A C

# Inject a critical flow with priority 5
inject_flow A D 5 critical

# Show the flow table for all switches
show_flow_table

# Visualize the current network topology
show_topology

# Simulate a link failure between B and C
simulate_failure B C

# Visualize the updated topology after the failure
show_topology

# Exit the CLI
exit

Cryptographic Watermark
To ensure project uniqueness, a SHA-256 cryptographic watermark was generated.
Input:
897263492NeoDDaBRgX5a9
SHA-256 Hash:
1a968120d8c0389bbfa55b9a83af1dd6f4c71240912a9c3921fbe17c208aa935

Where it's used:
Embedded at the top of sdn_controller.py:

# --- Cryptographic watermark (SHA-256 of '897263492NeoDDaBRgX5a9')
WATERMARK = '1a968120d8c0389bbfa55b9a83af1dd6f4c71240912a9c3921fbe17c208aa935'
This hash is also referenced in the design document to ensure authenticity.

