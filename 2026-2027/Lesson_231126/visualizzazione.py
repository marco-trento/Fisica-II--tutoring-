"""
visualizzazione.py  --  parte grafica

Funzioni da usare:

    mostra_campo(campo_elettrico, L, D)
        disegna le piastre e il campo elettrico

    anima_traiettoria(campo_elettrico, L, D, t, x, y, z)
        come sopra, e in più anima l'elettrone lungo la traiettoria
        x(t), y(t), z(t) già calcolata

    anima_cariche(storia, cariche, L, D)
        anima le cariche che si spostano sulle piastre
        (storia = lista di array di posizioni, uno per fotogramma)

A mostra_campo e anima_traiettoria si possono passare anche le cariche usate
per calcolare il campo:  ..., posizioni=posizioni, cariche=cariche)
e vengono disegnate come puntini (rossi +, blu -).

campo_elettrico è una funzione scritta da voi:  E = campo_elettrico(r)
con r = [x, y, z] in metri e E = [Ex, Ey, Ez] in V/m.

Le piastre sono quadrate (lato L), orizzontali, centrate sull'asse z:
la positiva in z = +D/2, la negativa in z = -D/2.
"""
import numpy as np
import pyvista as pv

# freccia di lunghezza 1 CENTRATA nell'origine (quella standard di pyvista parte
# dall'origine: la coda sarebbe nel punto e la freccia sembrerebbe spostata)
FRECCIA_CENTRATA = pv.Arrow(start=(-0.5, 0, 0), direction=(1, 0, 0))


# ---------------------------------------------------------------------------
# Pezzi della scena
# ---------------------------------------------------------------------------
def nuova_finestra(L, D):
    """Finestra con sfondo bianco, le due piastre e gli assi."""
    plotter = pv.Plotter(window_size=(1200, 800))
    plotter.set_background("white")
    spessore = 0.001
    piastra_pos = pv.Box(bounds=(-L/2, L/2, -L/2, L/2, D/2 - spessore, D/2 + spessore))
    piastra_neg = pv.Box(bounds=(-L/2, L/2, -L/2, L/2, -D/2 - spessore, -D/2 + spessore))
    plotter.add_mesh(piastra_pos, color="red", opacity=0.3)     # piastra +
    plotter.add_mesh(piastra_neg, color="blue", opacity=0.3)    # piastra -
    plotter.add_axes()
    plotter.camera_position = [(3*L, -2.8*L, 1.4*L), (0, 0, 0), (0, 0, 1)]
    return plotter


def disegna_frecce(plotter, campo_elettrico, L, D):
    """Una freccia in ogni punto di una griglia: la direzione e' quella di E,
    il colore indica il modulo |E|."""
    # questi valori sono arbitrari, potete giocare con la visualizzazione
    xy_max = 0.6      # in x e y le frecce vanno da -xy_max*L a +xy_max*L
    n_xy = 7          # numero di frecce lungo x e lungo y
    z_max = 0.7       # in z le frecce vanno da -z_max*D a +z_max*D (piastre a +-0.5 D)
    n_z = 4           # numero di livelli lungo z

    punti = []
    for x in np.linspace(-xy_max * L, xy_max * L, n_xy):
        for y in np.linspace(-xy_max * L, xy_max * L, n_xy):
            for z in np.linspace(-z_max * D, z_max * D, n_z):
                punti.append([x, y, z])
    punti = np.array(punti)

    E = np.array([campo_elettrico(p) for p in punti])
    modulo = np.linalg.norm(E, axis=1)

    # teniamo solo i punti dove il campo non è nullo
    punti, E, modulo = punti[modulo > 0], E[modulo > 0], modulo[modulo > 0]
    if len(punti) == 0:
        return

    nuvola = pv.PolyData(punti)
    nuvola["direzione"] = E / modulo[:, None]     # vettore unitario
    nuvola["|E| [V/m]"] = modulo
    frecce = nuvola.glyph(orient="direzione", scale=False, geom=FRECCIA_CENTRATA,
                          factor=0.14 * L)
    plotter.add_mesh(frecce, scalars="|E| [V/m]", cmap="viridis", clim=[0, modulo.max()],
                     scalar_bar_args={"vertical": True})


def disegna_cariche(plotter, posizioni, cariche, dimensione=6):
    """Disegna le cariche come puntini: rossi i positivi, blu i negativi.
    Restituisce la nuvola di punti (serve per animarla)."""
    nuvola = pv.PolyData(np.array(posizioni, dtype=float))
    nuvola["segno"] = np.sign(cariche)            # +1 o -1
    plotter.add_mesh(nuvola, scalars="segno", cmap=["darkblue", "darkred"], clim=[-1, 1],
                     point_size=dimensione, render_points_as_spheres=True,
                     show_scalar_bar=False)
    return nuvola


def crea_scena(campo_elettrico, L, D, posizioni=None, cariche=None):
    """Piastre e frecce del campo (più le cariche, se passate)."""
    plotter = nuova_finestra(L, D)
    disegna_frecce(plotter, campo_elettrico, L, D)
    if posizioni is not None:
        disegna_cariche(plotter, posizioni, cariche)
    return plotter


def aspetta_barra_spaziatrice(plotter):
    """Lascia la finestra ferma finché non si preme la barra spaziatrice
    (così c'è il tempo di portarla in primo piano prima dell'animazione)."""
    premuto = [False]

    def via():
        premuto[0] = True

    plotter.add_key_event("space", via)
    plotter.add_text("Premi la barra spaziatrice per iniziare", name="avvio",
                     position="lower_edge", font_size=14, color="black")
    while not premuto[0] and not plotter._closed:
        plotter.update()
    plotter.remove_actor("avvio")


# ---------------------------------------------------------------------------
# Funzioni da usare
# ---------------------------------------------------------------------------
def mostra_campo(campo_elettrico, L, D, posizioni=None, cariche=None):
    plotter = crea_scena(campo_elettrico, L, D, posizioni, cariche)
    plotter.show()


def anima_traiettoria(campo_elettrico, L, D, t, x, y, z, posizioni=None, cariche=None):
    """Anima l'elettrone lungo i punti (x[i], y[i], z[i]) agli istanti t[i]."""
    plotter = crea_scena(campo_elettrico, L, D, posizioni, cariche)

    # l'elettrone: una sferetta nera (raggio arbitrario, per visualizzazione)
    elettrone = pv.Sphere(radius=0.04 * L)       # centrata nell'origine
    punti_sfera = elettrone.points.copy()
    elettrone.points = punti_sfera + [x[0], y[0], z[0]]
    plotter.add_mesh(elettrone, color="black")

    plotter.show(interactive_update=True)       # apre la finestra senza bloccare
    aspetta_barra_spaziatrice(plotter)
    for i in range(len(t)):
        if plotter._closed:                     # finestra chiusa dall'utente
            break
        elettrone.points = punti_sfera + [x[i], y[i], z[i]]     # sposto la sfera
        if i > 0:                                                # scia percorsa finora
            scia = np.column_stack([x[:i+1], y[:i+1], z[:i+1]])
            plotter.add_mesh(pv.lines_from_points(scia), color="black",
                             line_width=3, name="scia", reset_camera=False)
        plotter.add_text(f"t = {t[i]*1e9:.2f} ns", name="tempo", color="black")
        plotter.update()

    if not plotter._closed:
        plotter.show()                           # a fine animazione la finestra resta aperta


def anima_cariche(storia, cariche, L, D):
    """Anima le cariche che si spostano sulle piastre."""
    plotter = nuova_finestra(L, D)
    plotter.camera_position = [(0.6*L, -3.0*L, 2.2*L), (0, 0, 0), (0, 0, 1)]   
    nuvola = disegna_cariche(plotter, storia[0], cariche, dimensione=10)

    plotter.show(interactive_update=True)       # apre la finestra senza bloccare
    aspetta_barra_spaziatrice(plotter)
    for i in range(len(storia)):
        if plotter._closed:
            break
        nuvola.points = storia[i]                # nuove posizioni delle cariche
        plotter.add_text(f"fotogramma {i + 1} / {len(storia)}", name="passo", color="black")
        plotter.update()

    if not plotter._closed:
        plotter.show()                           # alla fine la finestra resta aperta
