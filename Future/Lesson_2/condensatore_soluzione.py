"""
Condensatore a piastre piane  --  SOLUZIONE

In questo file c'è la parte di  Fisica. La grafica è in visualizzazione.py ed è già scritta.
Il moto si integra con solve_ivp di scipy (Runge-Kutta già pronto).
"""
import numpy as np
from scipy.integrate import solve_ivp # se fallisce usate pip install scipy
# importo le funzioni già scritte di visualizzazione, così si possono usare
from visualizzazione import mostra_campo, anima_traiettoria 

# ---------------------------------------------------------------------------
# Costanti fisiche (unita' SI)
# ---------------------------------------------------------------------------
eps0 = 8.854e-12          # F/m
k = 1 / (4 * np.pi * eps0)
e = 1.602e-19             # C   
m = 9.109e-31             # kg

# ---------------------------------------------------------------------------
# PARAMETRI
# Questi parametri sono arbitrari, potete modificarli e giocarci
# ---------------------------------------------------------------------------
V = 2000.0                # differenza di potenziale [V]
L = 0.10                  # lato delle piastre [m]
D = 0.04                  # distanza tra le piastre [m]

r0 = [-0.045, 0.0, 0.0]   # posizione iniziale dell'elettrone [m]
v0 = [1.0e7, 0.0, 0.0]    # velocità iniziale dell'elettrone [m/s]

t_max = 20e-9             # durata massima della simulazione [s]


# ---------------------------------------------------------------------------
# 1) Campo elettrico: modello ideale
# ---------------------------------------------------------------------------
def campo_uniforme(r):
    x, y, z = r
    dentro = abs(x) < L/2 and abs(y) < L/2 and abs(z) < D/2
    if dentro:
        return np.array([0.0, 0.0, -V / D])   # da + (alto) verso - (basso)
    else:
        return np.array([0.0, 0.0, 0.0]) # fuori dal condensatore pongo campo a zero (fisicamente sbagliato)


# ---------------------------------------------------------------------------
# 2) Campo elettrico: piastre fatte di tante cariche puntiformi
# ---------------------------------------------------------------------------
N = 20                     # ogni piastra è una griglia N x N di cariche
sigma = eps0 * V / D              # densità superficiale di carica
q = sigma * (L / N)**2            # carica di ogni puntino

posizioni = []
cariche = []
for x in np.linspace(-L/2, L/2, N):
    for y in np.linspace(-L/2, L/2, N):
        posizioni.append([x, y, +D/2]); cariche.append(+q)
        posizioni.append([x, y, -D/2]); cariche.append(-q)
posizioni = np.array(posizioni)
cariche = np.array(cariche)


def campo_piastre_finite(r):
    """Principio di sovrapposizione: somma dei campi di Coulomb."""
    E = np.zeros(3)
    for j in range(len(cariche)):
        d = r - posizioni[j]                    # vettore dalla carica j al punto r
        dist = np.sqrt(np.dot(d, d) + 0.001**2)        # +1 mm^2: evita di dividere per 0
        E = E + k * cariche[j] * d / dist**3
    return E

campo_elettrico = campo_uniforme ## importante! devo scegliere quale modello di campo usare

# ---------------------------------------------------------------------------
# 3) Equazioni del moto
# ---------------------------------------------------------------------------
def equazioni_moto(t, stato):
    """stato = [x, y, z, vx, vy, vz].
    Restituisce la derivata dello stato: [vx, vy, vz, ax, ay, az].
    Legge di Newton:  m a = -e E"""
    r = stato[0:3]
    v = stato[3:6]
    a = -e / m * campo_elettrico(r)
    return np.concatenate([v, a])


def indice_fine(x, y, z):
    """Restituisce l'indice del punto in cui fermare la traiettoria:
    - quando l'elettrone attraversa una piastra, ocvvero il piano z = +-D/2
    - oppure quando si allontana troppo e uscirebbe dalla scena.
    Se non succede nessuna delle due cose restituisce l'ultimo indice."""
    for i in range(1, len(z)):
        sopra_la_piastra = abs(x[i]) < L/2 and abs(y[i]) < L/2
        attraversa_piano = (abs(z[i-1]) - D/2) * (abs(z[i]) - D/2) <= 0
        if sopra_la_piastra and attraversa_piano:
            return i
        if np.sqrt(x[i]**2 + y[i]**2 + z[i]**2) > 1.5 * L:
            return i
    return len(z) - 1


# ---------------------------------------------------------------------------
# 4) Risolvo e visualizzo
# ---------------------------------------------------------------------------
stato_iniziale = np.concatenate([r0, v0])
tempi = np.linspace(0, t_max, 400)           # istanti in cui voglio la soluzione

sol = solve_ivp(equazioni_moto, [0, t_max], stato_iniziale, t_eval=tempi,
                max_step=1e-10, rtol=1e-8)

t = sol.t
x, y, z = sol.y[0], sol.y[1], sol.y[2]
vx, vy, vz = sol.y[3], sol.y[4], sol.y[5]

# tengo la traiettoria solo fino a quando l'elettrone colpisce una piastra (o esce dalla scena)
n = indice_fine(x, y, z) + 1
t, x, y, z, vx, vy, vz = t[:n], x[:n], y[:n], z[:n], vx[:n], vy[:n], vz[:n]

mostra_campo(campo_elettrico, L, D, posizioni=posizioni, cariche=cariche)         # solo il campo
anima_traiettoria(campo_elettrico, L, D, t, x, y, z) #campo 
#anima_traiettoria(campo_elettrico, L, D, t, x, y, z, posizioni=posizioni, cariche=cariche) #campo + cariche
