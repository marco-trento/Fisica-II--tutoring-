"""
Condensatore a piastre conduttrici: le cariche si muovono!

Partiamo dalle cariche del primo programma: tutte uguali, su una griglia
regolare (carica uniforme).
Ogni carica sente la forza di tutte le altre (Coulomb) e si sposta un po'
nella direzione della forza, restando sulla sua piastra. Ripetendo tante
volte, le cariche raggiungono l'equilibrio: e' quello che succede in un
conduttore, dove le cariche sono libere di muoversi.

Si vede che le cariche si addensano verso i bordi e negli angoli.
"""
import numpy as np
from scipy.integrate import solve_ivp

from visualizzazione import anima_cariche, anima_traiettoria

# ---------------------------------------------------------------------------
# Costanti fisiche (unita' SI)
# ---------------------------------------------------------------------------
eps0 = 8.854e-12          # F/m
k = 1 / (4 * np.pi * eps0)
e = 1.602e-19             # C   (l'elettrone ha carica -e)
m = 9.109e-31             # kg

# ---------------------------------------------------------------------------
# PARAMETRI
# ---------------------------------------------------------------------------
V = 2000.0                # usato solo per fissare la carica totale (vedi sotto)
L = 0.10                  # lato delle piastre [m]
D = 0.04                  # distanza tra le piastre [m]
N = 20                    # ogni piastra parte con una griglia N x N di cariche

r0 = [-0.045, 0.0, 0.0]   # posizione iniziale dell'elettrone [m]
v0 = [1.0e7, 0.0, 0.0]    # velocita' iniziale dell'elettrone [m/s]

t_max = 20e-9             # durata massima della simulazione [s]

# carica totale su ogni piastra: quella del condensatore ideale, Q = eps0 L^2 V / D
# (in un conduttore collegato a un generatore con tensione V la carica sarebbe circa il doppio:
#  qui fissiamo la carica, non la tensione)
Q = eps0 * L**2 * V / D
q = Q / N**2              # tutte le cariche sono uguali (come nel primo programma)


# ---------------------------------------------------------------------------
# 1) Posizioni iniziali: la stessa griglia regolare del primo programma
# ---------------------------------------------------------------------------
posizioni = []
cariche = []
for x in np.linspace(-L/2, L/2, N):
    for y in np.linspace(-L/2, L/2, N):
        posizioni.append([x, y, +D/2]); cariche.append(+q)
        posizioni.append([x, y, -D/2]); cariche.append(-q)
posizioni = np.array(posizioni)
cariche = np.array(cariche)


# ---------------------------------------------------------------------------
# 2) Campo elettrico: somma dei campi di Coulomb
# ---------------------------------------------------------------------------
def campo_elettrico(r):
    d = r - posizioni                           # vettori carica -> punto: (M, 3)
    dist = np.sqrt(np.sum(d**2, axis=1) + 0.001**2)
    return np.sum(k * cariche[:, None] * d / dist[:, None]**3, axis=0)
# nota: se r coincide con una carica, il suo contributo e' zero (d = 0),
# quindi campo_elettrico(posizioni[i]) e' il campo dovuto a tutte le ALTRE cariche


# ---------------------------------------------------------------------------
# 3) Rilassamento: ogni carica si sposta nella direzione della forza,
#    tanto piu' quanto piu' la forza e' grande, finche' le forze non si annullano
# ---------------------------------------------------------------------------
def calcola_forze():
    """Forza su ogni carica: F_i = q_i E(r_i), con E dovuto alle ALTRE cariche.
    Restituisce un array (M, 3): una riga [Fx, Fy, Fz] per ogni carica."""
    forze = np.array([cariche[i] * campo_elettrico(posizioni[i])
                      for i in range(len(cariche))])
    forze[:, 2] = 0.0                           # le cariche restano sulla piastra
    # una carica sul bordo spinta verso l'esterno non può uscire: quella
    # componente è bilanciata dal bordo stesso (come in un vero conduttore)
    for c in [0, 1]:                            # c = 0: asse x,  c = 1: asse y
        sul_bordo = np.abs(posizioni[:, c]) >= L/2
        verso_fuori = posizioni[:, c] * forze[:, c] > 0
        forze[sul_bordo & verso_fuori, c] = 0.0
    return forze


storia = [posizioni.copy()]                     # per l'animazione

distanza = L / (N - 1)                          # distanza iniziale tra due cariche vicine
forze = calcola_forze()
F_iniziale = np.max(np.linalg.norm(forze, axis=1))

# Ogni carica si sposta di  muovi * F  
#  Scegliamo muovi in modo che al primo passo la carica piu' spinta si sposti di distanza/10.
k_spostamento = (distanza / 10) / F_iniziale

# ci si ferma quando la forza più grande è scesa all'1% di quella iniziale
F_max = F_iniziale
passo = 0
while F_max > F_iniziale / 100 and passo < 2000:      # (2000: limite di sicurezza)
    posizioni = posizioni + k_spostamento * forze

    # le cariche non possono uscire dalla piastra
    posizioni[:, 0] = np.clip(posizioni[:, 0], -L/2, L/2)
    posizioni[:, 1] = np.clip(posizioni[:, 1], -L/2, L/2)

    forze = calcola_forze()
    F_max = np.max(np.linalg.norm(forze, axis=1))
    passo = passo + 1
    storia.append(posizioni.copy())

print("equilibrio raggiunto in " +str(passo)+ " passi "
      "(forza massima scesa al "+str(F_max / F_iniziale) + "di quella iniziale)")


# ---------------------------------------------------------------------------
# 4) Moto dell'elettrone (identico agli altri programmi)
# ---------------------------------------------------------------------------
def equazioni_moto(t, stato):
    """stato = [x, y, z, vx, vy, vz]  ->  [vx, vy, vz, ax, ay, az]"""
    r = stato[0:3]
    v = stato[3:6]
    a = -e / m * campo_elettrico(r)
    return np.concatenate([v, a])


def indice_fine(x, y, z):
    """Indice in cui fermare la traiettoria: l'elettrone attraversa una piastra
    (piano z = +-D/2 dentro il quadrato |x|, |y| < L/2) o esce dalla scena."""
    for i in range(1, len(z)):
        sopra_la_piastra = abs(x[i]) < L/2 and abs(y[i]) < L/2
        attraversa_piano = (abs(z[i-1]) - D/2) * (abs(z[i]) - D/2) <= 0
        if sopra_la_piastra and attraversa_piano:
            return i
        if np.sqrt(x[i]**2 + y[i]**2 + z[i]**2) > 1.5 * L:
            return i
    return len(z) - 1


stato_iniziale = np.concatenate([r0, v0])
tempi = np.linspace(0, t_max, 400)

sol = solve_ivp(equazioni_moto, [0, t_max], stato_iniziale, t_eval=tempi,
                max_step=1e-10, rtol=1e-8)

t = sol.t
x, y, z = sol.y[0], sol.y[1], sol.y[2]
vx, vy, vz = sol.y[3], sol.y[4], sol.y[5]

n = indice_fine(x, y, z) + 1
t, x, y, z, vx, vy, vz = t[:n], x[:n], y[:n], z[:n], vx[:n], vy[:n], vz[:n]



# ---------------------------------------------------------------------------
# 5) Visualizzazione
# ---------------------------------------------------------------------------
anima_cariche(storia, cariche, L, D)          # 1a finestra: le cariche si riorganizzano
anima_traiettoria(campo_elettrico, L, D, t, x, y, z,
                  posizioni=posizioni, cariche=cariche)   # 2a finestra: campo + elettrone
