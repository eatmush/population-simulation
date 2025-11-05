import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML


# -------------------------------
# Parâmetros do modelo
# -------------------------------
p_death = 0.1        # probabilidade de morte a cada passo
p_birth = 1.0        # probabilidade de nascimento por frame
timesteps = 180      # número de steps
move_scale = 0.02    # amplitude de movimento por frame
max_entities = 20   # limite máximo de entidades vivas
fade_speed = 0.1    # velocidade do fade-out (quanto mais alto, mais rápido somem)

# -------------------------------
# Estado inicial
# -------------------------------
entities = []     # lista de dicionários: {x, y, alive, alpha}
pop_history = []  # histórico de população viva

# -------------------------------
# Setup do gráfico de animação
# -------------------------------
fig, (ax_anim, ax_plot) = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Simulação da População (Visual + Curva)")

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
ax_plot.set_ylim(0, max_entities)
ax_plot.set_xlabel("Tempo (step)")
ax_plot.set_ylabel("Número de entidades vivas")
line, = ax_plot.plot([], [], color="tab:red")
ax_plot.grid(True)

# -------------------------------
# Função de atualização da animação
# -------------------------------
def update(frame):
    global entities

    # nascimento
    if random.random() < p_birth and len(entities) < max_entities:
        entities.append({
            "x": random.random(),
            "y": random.random(),
            "alive": True,
            "alpha": 1.0
        })

    # movimento + morte + fade
    new_entities = []
    for e in entities:
        if e["alive"]:
            if random.random() < p_death:
                e["alive"] = False
            else:
                # movimento aleatório
                e["x"] = np.clip(e["x"] + random.uniform(-move_scale, move_scale), 0, 1)
                e["y"] = np.clip(e["y"] + random.uniform(-move_scale, move_scale), 0, 1)
        else:
            # fade-out gradual
            e["alpha"] -= fade_speed

        # manter só entidades visíveis
        if e["alpha"] > 0:
            new_entities.append(e)

    entities = new_entities

    # atualizar gráfico da animação
    xs = [e["x"] for e in entities]
    ys = [e["y"] for e in entities]
    alphas = [e["alpha"] for e in entities]
    scat.set_offsets(np.column_stack((xs, ys)) if xs else [])
    scat.set_facecolors([[0.1, 0.3, 0.8, a] for a in alphas])
    ax_anim.set_title(f"t = {frame} | vivos = {sum(e['alive'] for e in entities)}")

    # atualizar histórico da população
    pop_history.append(sum(e["alive"] for e in entities))

    # atualizar linha do gráfico
    line.set_data(range(len(pop_history)), pop_history)

    return scat, line

# -------------------------------
# Criar animação
# -------------------------------
anim = FuncAnimation(
    fig, update,
    frames=timesteps,
    interval=timesteps*10,
    blit=True
)

plt.tight_layout()
plt.show()

# -------------------------------
# Para salvar como MP4 (opcional)
# -------------------------------
anim.save("simulacao_populacao_v01.mp4", writer="ffmpeg", fps=16)

# HTML(anim.to_jshtml())