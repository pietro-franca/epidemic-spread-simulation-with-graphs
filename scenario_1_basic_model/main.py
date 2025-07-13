import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def simulate_SIR(graph, beta, gamma, initial_infected):
    state = {node: 'S' for node in graph.nodes}
    for i in initial_infected:
        state[i] = 'I'

    infected_history = [] # list with the number of infected individuals over time
    state_over_time = [] # list with the state of each node at each step

    while 'I' in state.values():
        state_over_time.append(state.copy())  # save current state

        new_state = state.copy()
        for node in graph.nodes:
            if state[node] == 'I':
                for neighbor in graph.neighbors(node):
                    if state[neighbor] == 'S' and random.random() < beta:
                        new_state[neighbor] = 'I'
                if random.random() < gamma:
                    new_state[node] = 'R'
        state = new_state
        infected_history.append(list(state.values()).count('I'))

    state_over_time.append(state.copy())  # save final state
    return infected_history, state_over_time

# Parameters
n_nodes = 100 # number of nodes
connection_prob = 0.1 # connection probability (random graph)
graph = nx.erdos_renyi_graph(n_nodes, connection_prob, seed=42)

beta = 0.5   # probability of infection
gamma = 0.2  # probability of recovery
initial_infected = [0]  # starts with one infected node (index: 0)

infected_result, state_over_time = simulate_SIR(graph, beta, gamma, initial_infected)

# Plot infection curve
plt.plot(infected_result, label='Infected over time')
plt.xlabel('Time')
plt.ylabel('Number of Infected')
plt.title('SIR Model Simulation on a Random Graph')
plt.legend()
plt.grid(True)
plt.show()

# Plot initial graph structure
pos = nx.spring_layout(graph, seed=42)  # Layout for better visualization
nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=800)
plt.title("Random Graph (Erdős–Rényi)")
plt.show()

# Create infection animation
colors = {'S': 'blue', 'I': 'red', 'R': 'green'}

fig, ax = plt.subplots(figsize=(8, 6))

def update(frame):
    ax.clear()
    current_state = state_over_time[frame]
    node_colors = [colors[current_state[node]] for node in graph.nodes()]
    nx.draw(graph, pos, node_color=node_colors, with_labels=False, ax=ax, node_size=300)
    ax.set_title(f'Time: {frame}')

ani = animation.FuncAnimation(fig, update, frames=len(state_over_time), interval=500, repeat=False)
ani.save("epidemic_simulation.gif", writer='pillow')
plt.show()
