"""
Condensatore a piastre piane 

La grafica è già pronta in visualizzazione.py.
Voi scrivete la fisica: le parti segnate con  TODO.

  1. campo_uniforme       -> provate con mostra_campo (in fondo al file)
  2. equazioni_moto       -> provate con anima_traiettoria
  3. campo_piastre_finite -> confrontate le traiettorie nei due modelli
"""
import numpy as np
from scipy.integrate import solve_ivp

from visualizzazione import mostra_campo, anima_traiettoria

# ---------------------------------------------------------------------------
# Costanti fisiche (unità SI)
# ---------------------------------------------------------------------------
eps0 = 8.854e-12          # F/m
k = 1 / (4 * np.pi * eps0)
e = 1.602e-19             # C   (l'elettrone ha carica -e)
m = 9.109e-31             # kg


# ---------------------------------------------------------------------------
# PARAMETRI
# Questi parametri sono arbitrari, potete modificarli e giocarci
# ---------------------------------------------------------------------------
V = 200.0                 # differenza di potenziale [V]
L = 0.10                  # lato delle piastre [m]
D = 0.04                  # distanza tra le piastre [m]

r0 = [-0.045, 0.0, 0.0]   # posizione iniziale dell'elettrone [m]
v0 = [1.0e7, 0.0, 0.0]    # velocità iniziale dell'elettrone [m/s]

t_max = 20e-9             # durata massima della simulazione [s]


# ---------------------------------------------------------------------------
# 1) Campo elettrico: modello ideale
# ---------------------------------------------------------------------------
def campo_uniforme(r):
    """r = [x, y, z]. Restituisce np.array([Ex, Ey, Ez]).
    Tra le piastre (|x| < L/2, |y| < L/2, |z| < D/2) il campo è uniforme,
    di modulo V/D, diretto dalla piastra + (in alto) alla piastra - (in basso).
    Fuori E = 0. """
    x, y, z = r
    # TODO
    return np.array([0.0, 0.0, 0.0])


# ---------------------------------------------------------------------------
# 2) Campo elettrico: piastre fatte di tante cariche puntiformi
# ---------------------------------------------------------------------------
N = 20                            # ogni piastra è una griglia N x N di cariche
sigma = eps0 * V / D              # densità superficiale di carica
q = sigma * (L / N)**2            # carica di ogni puntino

posizioni = []
cariche = []
# TODO riempire la griglia NxN sulle due piastr

posizioni = np.array(posizioni)   # posizioni[j] = [xj, yj, zj] della carica j
cariche = np.array(cariche)       # cariche[j]   = valore della carica j


def campo_piastre_finite(r):
    """Principio di sovrapposizione:
        E(r) = somma su j di  k * q_j * (r - r_j) / |r - r_j|^3
    Suggerimento: per non dividere per zero, usate
        |r - r_j| = sqrt( (r - r_j)·(r - r_j) + 0.001**2 )"""
    E = np.zeros(3)
    # TODO: ciclo for sulle cariche
    return E

## IMPORTANTE
# da qui in poi scegliete quale modello di campo usare, possiamo farlo dando un nome ad una
# nuova funzione e assegnandogli uno dei due modelli:
campo_elettrico = campo_uniforme  # ora campo elettrico punta a campo_uniforme
# se voglio l'altro modello 
# campo_elettrico = campo_piastre_finite 

# ---------------------------------------------------------------------------
# 3) Equazioni del moto
# ---------------------------------------------------------------------------
def equazioni_moto(t, stato):
    """stato = [x, y, z, vx, vy, vz].
    Deve restituire la derivata dello stato: [vx, vy, vz, ax, ay, az],
    con l'accelerazione data dalla legge di Newton per un elettrone nel campo E.
    Legge di Newton:  m a = -e E"""
    # qui dentro posso chiamare la funzione campo_elettrico(r)
    r = stato[0:3]
    v = stato[3:6]
    a = np.zeros(3)   # TODO
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
        if np.sqrt(x[i]**2 + y[i]**2 + z[i]**2) > 1.5 * L: #troppo lontano
            return i
    return len(z) - 1


# ---------------------------------------------------------------------------
# 4) Risolvo e visualizzo
# ---------------------------------------------------------------------------
stato_iniziale = np.concatenate([r0, v0])
tempi = np.linspace(0, t_max, 400)           # istanti in cui voglio la soluzione

# solve_ivp integra  d(stato)/dt = equazioni_moto(t, stato)  con Runge-Kutta
sol = solve_ivp(equazioni_moto, [0, t_max], stato_iniziale, t_eval=tempi,
                max_step=1e-10, rtol=1e-8)

t = sol.t
x, y, z = sol.y[0], sol.y[1], sol.y[2]
vx, vy, vz = sol.y[3], sol.y[4], sol.y[5]

# tengo la traiettoria solo fino a quando l'elettrone colpisce una piastra (o esce dalla scena)
n = indice_fine(x, y, z) + 1
t, x, y, z, vx, vy, vz = t[:n], x[:n], y[:n], z[:n], vx[:n], vy[:n], vz[:n]
# volendo potrei stampare valori di energia cinetica, tempo della simulazione etc 
# TODO se volete

# iniziamo dal caso con campo uniforme
mostra_campo(campo_uniforme, L, D)           # passo 1: solo il campo
# anima_traiettoria(campo_uniforme, L, D, t, x, y, z)   # passo 2: l'elettrone

# caso con piastre finite
# mostra_campo(campo_piastre_finite, L, D, posizioni=posizioni, cariche=cariche) 
# anima_traiettoria(campo_piastre_finite, L, D, t, x, y, z, posizioni=posizioni, cariche=cariche)   # passo 2: l'elettrone
