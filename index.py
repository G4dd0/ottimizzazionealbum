# ============================================================
# PROBLEMA FIGURINE PANINI - OTTIMIZZAZIONE BUSTINE / SINGOLE
# ============================================================

# Librerie principali
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 1. PARAMETRI DEL PROBLEMA
# ============================================================

# Numero totale di figurine dell'album
N_FIGURINE = 980

# Numero di figurine per bustina
FIGURINE_PER_BUSTINA = 7

# Costo di una bustina
COSTO_BUSTINA = 1.50

# Costo di una figurina singola mancante
COSTO_FIGURINA_SINGOLA = 0.50


# ============================================================
# 2. FUNZIONE PER STIMARE LE FIGURINE MANCANTI
# ============================================================

def figurine_mancanti_attese(numero_bustine):
    """
    Calcola quante figurine mancano in media dopo aver comprato
    un certo numero di bustine.

    Idea:
    Ogni bustina contiene 7 figurine.
    Dopo b bustine, abbiamo estratto 7*b figurine.

    La probabilità che una specifica figurina NON sia mai uscita
    dopo 7*b estrazioni è circa:

        (1 - 1/N)^(7*b)

    Quindi il numero atteso di figurine ancora mancanti è:

        N * (1 - 1/N)^(7*b)

    Questa è una buona approssimazione del problema.
    """

    estrazioni_totali = numero_bustine * FIGURINE_PER_BUSTINA

    mancanti = N_FIGURINE * (1 - 1 / N_FIGURINE) ** estrazioni_totali

    return mancanti


def figurine_diverse_attese(numero_bustine):
    """
    Calcola quante figurine diverse ci aspettiamo di avere
    dopo un certo numero di bustine.
    """

    mancanti = figurine_mancanti_attese(numero_bustine)

    diverse = N_FIGURINE - mancanti

    return diverse


def costo_totale_atteso(numero_bustine):
    """
    Calcola il costo totale atteso della strategia:

    1. compro un certo numero di bustine
    2. poi compro singolarmente tutte le figurine mancanti

    Costo totale =
        costo bustine +
        costo figurine mancanti singole
    """

    costo_bustine = numero_bustine * COSTO_BUSTINA

    mancanti = figurine_mancanti_attese(numero_bustine)

    costo_singole = mancanti * COSTO_FIGURINA_SINGOLA

    totale = costo_bustine + costo_singole

    return totale


# ============================================================
# 3. CREAZIONE DELLA TABELLA DATI
# ============================================================

# Decidiamo fino a quante bustine simulare/calcolare.
# 300 è più che sufficiente per vedere bene il minimo.
max_bustine = 300

# Lista dei possibili numeri di bustine
bustine = np.arange(0, max_bustine + 1)

# Creiamo una tabella con tutti i valori calcolati
df = pd.DataFrame({
    "Bustine": bustine,
    "Costo bustine": bustine * COSTO_BUSTINA,
    "Figurine diverse attese": [figurine_diverse_attese(b) for b in bustine],
    "Figurine mancanti attese": [figurine_mancanti_attese(b) for b in bustine],
    "Costo singole mancanti": [figurine_mancanti_attese(b) * COSTO_FIGURINA_SINGOLA for b in bustine],
    "Costo totale atteso": [costo_totale_atteso(b) for b in bustine]
})

# Arrotondiamo alcuni valori per renderli più leggibili
df["Figurine diverse attese"] = df["Figurine diverse attese"].round(2)
df["Figurine mancanti attese"] = df["Figurine mancanti attese"].round(2)
df["Costo bustine"] = df["Costo bustine"].round(2)
df["Costo singole mancanti"] = df["Costo singole mancanti"].round(2)
df["Costo totale atteso"] = df["Costo totale atteso"].round(2)


# ============================================================
# 4. TROVIAMO LA STRATEGIA MIGLIORE
# ============================================================

# Troviamo la riga con costo totale minimo
riga_ottima = df.loc[df["Costo totale atteso"].idxmin()]

bustine_ottime = int(riga_ottima["Bustine"])
costo_minimo = riga_ottima["Costo totale atteso"]
mancanti_al_minimo = riga_ottima["Figurine mancanti attese"]
diverse_al_minimo = riga_ottima["Figurine diverse attese"]


print("STRATEGIA OTTIMA ATTESA")
print("-----------------------")
print(f"Bustine da comprare: {bustine_ottime}")
print(f"Figurine diverse attese: {diverse_al_minimo}")
print(f"Figurine mancanti attese: {mancanti_al_minimo}")
print(f"Costo minimo atteso: {costo_minimo} €")


# Mostriamo alcune righe interessanti della tabella
df_interessante = df[df["Bustine"].isin([0, 50, 80, 100, 110, 119, 120, 130, 140, 150, 200])]

print(df_interessante)

# ============================================================
# 5. GRAFICO DEL COSTO TOTALE ATTESO
# ============================================================

fig = px.line(
    df,
    x="Bustine",
    y="Costo totale atteso",
    title="Costo totale atteso: bustine + figurine singole mancanti",
    labels={
        "Bustine": "Numero di bustine acquistate",
        "Costo totale atteso": "Costo totale atteso (€)"
    },
    markers=False
)

# Aggiungiamo il punto minimo
fig.add_trace(
    go.Scatter(
        x=[bustine_ottime],
        y=[costo_minimo],
        mode="markers+text",
        text=[f"Minimo: {bustine_ottime} bustine<br>{costo_minimo:.2f} €"],
        textposition="top center",
        marker=dict(size=12),
        name="Strategia ottima"
    )
)

# Linea verticale sul punto ottimo
fig.add_vline(
    x=bustine_ottime,
    line_dash="dash",
    annotation_text=f"Ottimo: {bustine_ottime} bustine",
    annotation_position="top left"
)

fig.show()

# ============================================================
# 6. GRAFICO FIGURINE DIVERSE / MANCANTI
# ============================================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Bustine"],
        y=df["Figurine diverse attese"],
        mode="lines",
        name="Figurine diverse attese"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["Bustine"],
        y=df["Figurine mancanti attese"],
        mode="lines",
        name="Figurine mancanti attese"
    )
)

fig.add_vline(
    x=bustine_ottime,
    line_dash="dash",
    annotation_text=f"Ottimo: {bustine_ottime} bustine",
    annotation_position="top right"
)

fig.update_layout(
    title="Andamento delle figurine diverse e mancanti",
    xaxis_title="Numero di bustine acquistate",
    yaxis_title="Numero di figurine",
    hovermode="x unified"
)

fig.show()

# ============================================================
# 7. GRAFICO DELLE COMPONENTI DI COSTO
# ============================================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Bustine"],
        y=df["Costo bustine"],
        mode="lines",
        name="Costo bustine"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["Bustine"],
        y=df["Costo singole mancanti"],
        mode="lines",
        name="Costo figurine singole mancanti"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["Bustine"],
        y=df["Costo totale atteso"],
        mode="lines",
        name="Costo totale atteso",
        line=dict(width=4)
    )
)

fig.add_vline(
    x=bustine_ottime,
    line_dash="dash",
    annotation_text=f"Minimo: {bustine_ottime} bustine",
    annotation_position="top right"
)

fig.update_layout(
    title="Costo bustine, costo singole e costo totale",
    xaxis_title="Numero di bustine acquistate",
    yaxis_title="Costo (€)",
    hovermode="x unified"
)

fig.show()

# ============================================================
# 8. SIMULAZIONE MONTE CARLO
# ============================================================

import random


def simula_album(numero_bustine):
    """
    Simula l'acquisto di un certo numero di bustine.

    Ogni bustina contiene 7 figurine casuali diverse.
    Alla fine restituisce:
    - numero di figurine diverse trovate
    - numero di figurine mancanti
    - costo totale della strategia
    """

    # Insieme delle figurine trovate.
    # Usiamo un set perché elimina automaticamente i duplicati.
    figurine_trovate = set()

    # Simuliamo l'apertura delle bustine
    for _ in range(numero_bustine):

        # Estraiamo 7 figurine diverse da un album di 980
        bustina = random.sample(range(1, N_FIGURINE + 1), FIGURINE_PER_BUSTINA)

        # Aggiungiamo le figurine trovate al set
        figurine_trovate.update(bustina)

    # Calcoliamo quante diverse abbiamo trovato
    diverse = len(figurine_trovate)

    # Calcoliamo quante mancano
    mancanti = N_FIGURINE - diverse

    # Costo totale:
    # bustine comprate + acquisto singolo delle mancanti
    costo = (
        numero_bustine * COSTO_BUSTINA
        + mancanti * COSTO_FIGURINA_SINGOLA
    )

    return diverse, mancanti, costo


def monte_carlo(numero_bustine, numero_simulazioni=1000):
    """
    Ripete la simulazione tante volte per stimare:
    - media delle figurine diverse
    - media delle figurine mancanti
    - media del costo totale
    - deviazione standard del costo
    """

    risultati = []

    for _ in range(numero_simulazioni):
        diverse, mancanti, costo = simula_album(numero_bustine)

        risultati.append({
            "Bustine": numero_bustine,
            "Figurine diverse": diverse,
            "Figurine mancanti": mancanti,
            "Costo totale": costo
        })

    return pd.DataFrame(risultati)


# Proviamo la simulazione sul numero ottimale teorico
simulazioni_ottimo = monte_carlo(bustine_ottime, numero_simulazioni=5000)

print(simulazioni_ottimo.describe())

# ============================================================
# 9. ISTOGRAMMA DEI COSTI SIMULATI
# ============================================================

fig = px.histogram(
    simulazioni_ottimo,
    x="Costo totale",
    nbins=40,
    title=f"Distribuzione dei costi simulati con {bustine_ottime} bustine",
    labels={
        "Costo totale": "Costo totale (€)"
    }
)

fig.add_vline(
    x=simulazioni_ottimo["Costo totale"].mean(),
    line_dash="dash",
    annotation_text=f"Media: {simulazioni_ottimo['Costo totale'].mean():.2f} €",
    annotation_position="top right"
)

fig.show()