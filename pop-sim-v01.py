import random
import matplotlib.pyplot as plt

# parâmetros
p_death = 0.1
timesteps = 1000

# estado inicial
N = 0
pop_history = []

for t in range(timesteps):
    # 1. nascimento
    N += 1
    
    # 2. mortes (cada entidade tem 10% de chance de morrer)
    survivors = sum(random.random() > p_death for _ in range(N))
    
    N = survivors
    pop_history.append(N)

# plot
plt.plot(pop_history)
plt.xlabel("Tempo (step)")
plt.ylabel("Número de entidades vivas")
plt.title("Simulação da população com morte aleatória e nascimento fixo")
plt.show()