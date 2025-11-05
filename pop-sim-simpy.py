import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------
# Parâmetros do modelo
# -------------------------------------
p_birth = 1.0        # probabilidade de nascimento por step
p_death = 0.1        # probabilidade de morte por step
move_scale = 0.02    # amplitude de movimento
timesteps = 180      # número de steps
max_entities = 20    # limite de entidades simultâneas

# -------------------------------------
# Estado global
# -------------------------------------
entities = []  # lista de dicionários com x, y, alive
pop_history = []

# -------------------------------------
# Função: ciclo de vida de uma entidade
# -------------------------------------
def entity_life(env, entity_id, population):
    entity = {"id": entity_id, "x": random.random(), "y": random.random(), "alive": True}
    population.append(entity)

    while entity["alive"]:
        # chance de morte
        if random.random() < p_death:
            entity["alive"] = False
        else:
            # movimento aleatório
            entity["x"] = np.clip(entity["x"] + random.uniform(-move_scale, move_scale), 0, 1)
            entity["y"] = np.clip(entity["y"] + random.uniform(-move_scale, move_scale), 0, 1)
        yield env.timeout(1)

# -------------------------------------
# Função: processo global de nascimento
# -------------------------------------
def birth_process(env, population):
    entity_id = 0
    while True:
        if random.random() < p_birth and len(population) < max_entities:
            env.process(entity_life(env, entity_id, population))
            entity_id += 1
        yield env.timeout(1)

# -------------------------------------
# Função: coleta de dados da população
# -------------------------------------
def data_collector(env, population):
    while True:
        vivos = sum(e["alive"] for e in population)
        pop_history.append(vivos)
        yield env.timeout(1)

# -------------------------------------
# Execução da simulação
# -------------------------------------
env = simpy.Environment()
env.process(birth_process(env, entities))
env.process(data_collector(env, entities))
env.run(until=timesteps)

# -------------------------------------
# Visualização
# -------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(pop_history, color="tab:red", label="População viva")
plt.axhline(np.mean(pop_history), color="gray", linestyle="--", label="Média")
plt.xlabel("Tempo (step)")
plt.ylabel("Número de entidades vivas")
plt.title("Simulação Populacional (SimPy)")
plt.legend()
plt.grid(True)
plt.show()