# IMPORTANTE: NÃO nomeie este arquivo como "mesa.py"!
# Use nomes como: population_sim.py, simulacao_mesa.py, etc.

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mesa import Agent, Model
from mesa.datacollection import DataCollector

# -------------------------------
# Definição do Agente
# -------------------------------
class Entity(Agent):
    """Uma entidade que se move, pode morrer e fazer fade-out"""
    
    def __init__(self, model, pos):
        # Mesa 3.0 não usa unique_id no construtor
        super().__init__(model)
        self.pos = pos
        self.alive = True
        self.alpha = 1.0
        
    def step(self):
        """Atualização do agente a cada passo"""
        if self.alive:
            # Verifica morte
            if random.random() < self.model.p_death:
                self.alive = False
            else:
                # Movimento aleatório
                x, y = self.pos
                dx = random.uniform(-self.model.move_scale, self.model.move_scale)
                dy = random.uniform(-self.model.move_scale, self.model.move_scale)
                new_x = np.clip(x + dx, 0, 1)
                new_y = np.clip(y + dy, 0, 1)
                self.pos = (new_x, new_y)
        else:
            # Fade-out gradual
            self.alpha -= self.model.fade_speed

# -------------------------------
# Definição do Modelo
# -------------------------------
class PopulationModel(Model):
    """Modelo de população com nascimento, morte e movimento"""
    
    def __init__(self, p_death=0.1, p_birth=1.0, move_scale=0.02, 
                 max_entities=20, fade_speed=0.1):
        super().__init__()
        self.p_death = p_death
        self.p_birth = p_birth
        self.move_scale = move_scale
        self.max_entities = max_entities
        self.fade_speed = fade_speed
        
        # Lista de entidades (evitando conflito com Mesa 3.0)
        self.entities = []
        
        # Coletor de dados
        self.datacollector = DataCollector(
            model_reporters={
                "Alive": lambda m: sum(1 for a in m.entities if a.alive),
                "Total": lambda m: len(m.entities)
            }
        )
        
    def step(self):
        """Executa um passo da simulação"""
        # Tentativa de nascimento
        alive_count = sum(1 for a in self.entities if a.alive)
        if random.random() < self.p_birth and alive_count < self.max_entities:
            pos = (random.random(), random.random())
            entity = Entity(self, pos)
            self.entities.append(entity)
        
        # Atualiza todos os agentes (em ordem aleatória)
        entities_shuffled = self.entities.copy()
        random.shuffle(entities_shuffled)
        for entity in entities_shuffled:
            entity.step()
        
        # Remove agentes invisíveis
        self.entities = [a for a in self.entities if a.alpha > 0]
        
        # Coleta dados
        self.datacollector.collect(self)

# -------------------------------
# Configuração da visualização
# -------------------------------
timesteps = 180
model = PopulationModel(
    p_death=0.1,
    p_birth=1.0,
    move_scale=0.02,
    max_entities=20,
    fade_speed=0.1
)

# Setup do gráfico
fig, (ax_anim, ax_plot) = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Simulação da População com Mesa (Visual + Curva)")

# --- lado esquerdo: animação ---
ax_anim.set_xlim(0, 1)
ax_anim.set_ylim(0, 1)
ax_anim.set_xticks([])
ax_anim.set_yticks([])
ax_anim.set_facecolor("white")
ax_anim.set_title("Entidades (nascem, se movem, morrem)")

scat = ax_anim.scatter([], [], s=60, color="tab:blue", edgecolors="black")

# --- lado direito: gráfico da população ---
ax_plot.set_xlim(0, timesteps)
ax_plot.set_ylim(0, model.max_entities)
ax_plot.set_yticks(np.arange(0, model.max_entities + 1, 2))
ax_plot.set_xlabel("Tempo (step)")
ax_plot.set_ylabel("Número de entidades vivas")
line, = ax_plot.plot([], [], color="tab:red", label="População viva")
mean_line, = ax_plot.plot([], [], color="tab:gray", linestyle="--", label="Média")
ax_plot.legend(loc="upper right")
ax_plot.grid(True)

# -------------------------------
# Função de atualização da animação
# -------------------------------
def update(frame):
    # Executa um passo do modelo
    model.step()
    
    # Obtém dados dos agentes para visualização
    entities = model.entities
    if entities:
        xs = [a.pos[0] for a in entities]
        ys = [a.pos[1] for a in entities]
        alphas = [a.alpha for a in entities]
        scat.set_offsets(np.column_stack((xs, ys)))
        scat.set_facecolors([[0.1, 0.3, 0.8, a] for a in alphas])
    else:
        scat.set_offsets([])
        scat.set_facecolors([])
    
    # Atualiza título
    alive_count = sum(1 for a in entities if a.alive)
    ax_anim.set_title(f"t = {frame} | vivos = {alive_count}")
    
    # Atualiza gráfico da população
    df = model.datacollector.get_model_vars_dataframe()
    pop_history = df["Alive"].tolist()
    
    x_vals = range(len(pop_history))
    line.set_data(x_vals, pop_history)
    
    # Calcula e plota média (a partir do step 20)
    start_mean = 20
    if len(pop_history) > start_mean:
        sub_pop = np.array(pop_history[start_mean:])
        mean_values = np.concatenate([
            [np.nan] * start_mean,
            np.cumsum(sub_pop) / np.arange(1, len(sub_pop) + 1)
        ])
    else:
        mean_values = [np.nan] * len(pop_history)
    
    mean_line.set_data(x_vals, mean_values)
    
    return scat, line, mean_line

# -------------------------------
# Criar animação
# -------------------------------
anim = FuncAnimation(
    fig, update,
    frames=timesteps,
    interval=100,
    blit=True
)

plt.tight_layout()
plt.show()

# -------------------------------
# Para salvar como MP4 (opcional)
# -------------------------------
anim.save("simulacao_populacao_mesa.mp4", writer="ffmpeg", fps=16)

# Para notebooks Jupyter:
# from IPython.display import HTML
# HTML(anim.to_jshtml())