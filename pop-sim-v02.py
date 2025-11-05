import random
import plotly.graph_objects as go

# -------------------------------
# Parâmetros
# -------------------------------
p_death = 0.1          # probabilidade de morte
timesteps = 180        # número de passos
start_mean_step = 20   # a partir de qual step calcular a média acumulada

# -------------------------------
# Estado inicial
# -------------------------------
N = 0
pop_history = []
running_mean = []

# -------------------------------
# Simulação
# -------------------------------
for t in range(timesteps):
    # 1. nascimento
    N += 1
    
    # 2. mortes (cada entidade tem 10% de chance de morrer)
    survivors = sum(random.random() > p_death for _ in range(N))
    N = survivors

    # histórico
    pop_history.append(N)
    
    # média acumulada apenas após certo step
    if t + 1 >= start_mean_step:
        subset = pop_history[start_mean_step - 1:]  # fatia da lista a partir do step desejado
        running_mean.append(sum(subset) / len(subset))
    else:
        running_mean.append(None)  # ainda não começou a calcular

# criar gráfico interativo
fig = go.Figure()

fig.add_trace(go.Scatter(
    y=pop_history,
    mode='lines',
    name='População viva',
    line=dict(color='blue', width=2)
))

fig.add_trace(go.Scatter(
    y=running_mean,
    mode='lines',
    name='Média acumulada',
    line=dict(color='red', dash='dash')
))

fig.update_layout(
    title='Simulação da população com morte aleatória e nascimento fixo',
    xaxis_title='Tempo (step)',
    yaxis_title='Número de entidades vivas',
    hovermode='x unified',
    template='plotly_white'
)

fig.show()