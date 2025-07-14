import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def simular_SIR(grafo, beta, gamma, infectados_iniciais):
    estado = {n: 'S' for n in grafo.nodes}
    for i in infectados_iniciais:
        estado[i] = 'I'

    historia = []  # list with the number of infected people over time
    estados_temporais = []  # list with the state of each node at each step

    while 'I' in estado.values():
        estados_temporais.append(estado.copy())  # saves current state

        novos_estados = estado.copy()
        for n in grafo.nodes:
            if estado[n] == 'I':
                for vizinho in grafo.neighbors(n):
                    if estado[vizinho] == 'S' and random.random() < beta:
                        novos_estados[vizinho] = 'I'
                if random.random() < gamma:
                    novos_estados[n] = 'R'
        estado = novos_estados
        historia.append(list(estado.values()).count('I'))

    estados_temporais.append(estado.copy())  # last state
    return historia, estados_temporais

# Parameters
n = 100  # nodes number
p = 0.1  # connection probability (random graph)
grafo = nx.erdos_renyi_graph(n, p, seed=42)

beta = 0.5   # probability of infection
gamma = 0.2  # probability of recovery
infectados_iniciais = [0]  # starts with one infected node (index: 0)

resultado, estados_temporais = simular_SIR(grafo, beta, gamma, infectados_iniciais)

# Plot results
plt.plot(resultado, label='Infectados ao longo do tempo')
plt.xlabel('Tempo')
plt.ylabel('Número de Infectados')
plt.title('Simulação do Modelo SIR em um Grafo Aleatório')
plt.legend()
plt.grid(True)
plt.show()

# Plot graph
pos = nx.spring_layout(grafo, seed=42)
nx.draw(grafo, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=800)
plt.title("Grafo Aleatório (Erdős–Rényi)")
plt.show()

# Simulate infection
cores = {'S': 'blue', 'I': 'red', 'R': 'green'}

fig, ax = plt.subplots(figsize=(8, 6))

def atualizar(frame):
    ax.clear()
    estado_atual = estados_temporais[frame]
    cor_nos = [cores[estado_atual[n]] for n in grafo.nodes()]
    nx.draw(grafo, pos, node_color=cor_nos, with_labels=False, ax=ax, node_size=300)
    ax.set_title(f'Tempo: {frame}')

ani = animation.FuncAnimation(fig, atualizar, frames=len(estados_temporais), interval=500, repeat=False)
ani.save("animacao_epidemia.gif", writer='pillow')
plt.show()