import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def simular_SIR(grafo, beta, gamma, infectados_iniciais, nos_vacinados):
    estado = {n: 'S' for n in grafo.nodes}
    for i in infectados_iniciais:
        estado[i] = 'I'

    for v in nos_vacinados:
      if v != 0:
        estado[v] = 'R' # already recovered or immunized

    historia = []  
    estados_temporais = []  

    while 'I' in estado.values():
        estados_temporais.append(estado.copy()) 

        novos_estados = estado.copy()
        for n in grafo.nodes:
            if estado[n] == 'I':
                for vizinho in grafo.neighbors(n):
                    peso = grafo[n][vizinho].get('peso', 1.0)  
                    prob_transmissao = beta * peso
                    if estado[vizinho] == 'S' and random.random() < prob_transmissao:
                        novos_estados[vizinho] = 'I'
                if random.random() < gamma:
                    novos_estados[n] = 'R'
        estado = novos_estados
        historia.append(list(estado.values()).count('I'))

    estados_temporais.append(estado.copy()) 
    return historia, estados_temporais

n = 70  
p = 0.085  

grafo = nx.erdos_renyi_graph(n, p, seed=14)
for u, v in grafo.edges():
    grafo[u][v]['peso'] = random.choice([0.1, 0.3, 0.5, 0.9])

beta = 0.7   
gamma = 0.4  
nos_vacinados = random.sample(list(grafo.nodes()), k=30) 
infectados_iniciais = [0]  
resultado, estados_temporais = simular_SIR(grafo, beta, gamma, infectados_iniciais, nos_vacinados)

plt.plot(resultado, label='Infectados ao longo do tempo')
plt.xlabel('Tempo')
plt.ylabel('Número de Infectados')
plt.title('Simulação do Modelo SIR em um Grafo Aleatório')
plt.legend()
plt.grid(True)
plt.show()

pos = nx.spring_layout(grafo, seed=25) 
pesos = [grafo[u][v]['peso'] for u, v in grafo.edges()]
cores_arestas = [plt.cm.viridis(p) for p in pesos] 

nx.draw(
    grafo, pos,
    edge_color=cores_arestas,
    width=1.5,
    node_color='skyblue',
    with_labels=True,
    node_size=800
)
plt.title("Grafo com Pesos Representados por Cores")
plt.show()

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