import random
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Parâmetros comuns
# -------------------------------
p_death = 0.1
timesteps = 180
random.seed(42)  # mesma semente para comparação

# -------------------------------
# Modelo 1: population-dynamics-simulation-v02
# -------------------------------
N = 0
pop_history_1 = []
for t in range(timesteps):
    N += 1  # nascimento fixo
    survivors = sum(random.random() > p_death for _ in range(N))
    N = survivors
    pop_history_1.append(N)
mean_1 = np.cumsum(pop_history_1) / np.arange(1, len(pop_history_1) + 1)

# -------------------------------
# Modelo 2: animation-v02 simplificado (sem fade nem movimento visual)
# -------------------------------
p_birth = 1.0
max_entities = 20

entities = []
pop_history_2 = []

random.seed(42)  # mesma semente

for t in range(timesteps):
    # nascimento probabilístico
    if random.random() < p_birth and len(entities) < max_entities:
        entities.append({"alive": True})

    new_entities = []
    for e in entities:
        if e["alive"]:
            if random.random() < p_death:
                e["alive"] = False
        if e["alive"]:
            new_entities.append(e)
    entities = new_entities
    pop_history_2.append(len(entities))

mean_2 = np.cumsum(pop_history_2) / np.arange(1, len(pop_history_2) + 1)

# -------------------------------
# Plot comparativo
# -------------------------------
plt.figure(figsize=(10, 6))
plt.plot(pop_history_1, label="Modelo 1 - Crescimento fixo", alpha=0.8)
plt.plot(pop_history_2, label="Modelo 2 - Nascimento probabilístico", alpha=0.8)
plt.plot(mean_1, "--", color="tab:red", label="Média Modelo 1")
plt.plot(mean_2, "--", color="tab:gray", label="Média Modelo 2")
plt.xlabel("Tempo (step)")
plt.ylabel("População viva")
plt.title("Comparação entre modelos de simulação populacional")
plt.legend()
plt.grid(True)
plt.show()
