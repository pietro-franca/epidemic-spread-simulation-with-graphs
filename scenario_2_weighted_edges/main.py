import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def simulate_SIR(graph, beta, gamma, initial_infected):
    state = {node: 'S' for node in graph.nodes}
    for i in initial_infected:
        state[i] = 'I'

    infected_history = []
    state_over_time = []

    while 'I' in state.values():
        state_over_time.append(state.copy())

        new_state = state.copy()
        for node in graph.nodes:
            if state[node] == 'I':
                for neighbor in graph.neighbors(node):
                    weight = graph[node][neighbor].get('weight', 1.0)  # Edge weights affect transmission probability
                    transmission_prob = beta * weight
                    if state[neighbor] == 'S' and random.random() < transmission_prob:
                        new_state[neighbor] = 'I'
                if random.random() < gamma:
                    new_state[node] = 'R'
        state = new_state
        infected_history.append(list(state.values()).count('I'))

    state_over_time.append(state.copy())
    return infected_history, state_over_time

# Parameters
n_nodes = 50
connection_prob = 0.08
graph = nx.erdos_renyi_graph(n_nodes, connection_prob, seed=25)

for u, v in graph.edges():
    graph[u][v]['weight'] = random.choice([0.1, 0.3, 0.5, 0.9])

# No Social Distancing: (0.2, 0.4, 0.6 0.8)
# Social Distancing: (0.1, 0.3, 0.5, 0.9)

# Weights and probabilities example:
# live together: 0.8 -> 0.9
# work together: 0.6 -> 0.5
# same community: 0.4 -> 0.3
# casual contact: 0.2 -> 0.1

# increases the likelihood of infection among people 
# living together and decreases other probabilities

beta = 0.5
gamma = 0.35
initial_infected = [0]

infected_result, state_over_time = simulate_SIR(graph, beta, gamma, initial_infected)

# Plot infection curve
plt.plot(infected_result, label='Infected over time')
plt.xlabel('Time')
plt.ylabel('Number of Infected')
plt.title('SIR Model Simulation on a Random Graph')
plt.legend()
plt.grid(True)
plt.show()

# Plot weighted graph
pos = nx.spring_layout(graph, seed=25)
weights = [graph[u][v]['weight'] for u, v in graph.edges()]
edge_colors = [plt.cm.viridis(w) for w in weights]

nx.draw(
    graph, pos,
    edge_color=edge_colors,
    width=1.5,
    node_color='skyblue',
    with_labels=True,
    node_size=800
)
plt.title("Graph with Edge Weights Represented by Color")
plt.show()

# Create animation
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
