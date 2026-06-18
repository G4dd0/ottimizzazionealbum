# ============================================================
# PROBLEMA FIGURINE PANINI - OTTIMIZZAZIONE BUSTINE / SINGOLE
# ============================================================

# Librerie principali
import numpy as np                  # Useremo numpy per la gestione di alcuni dati numerici
import pandas as pd                 # Useremo pandas per la gestione del dataframe in cui inseriremo le diverse ipotesi di dato
import plotly.express as px         # Le funzioni di plotly ci serviranno per graficare i dati all'interno del nostro datagframe
import plotly.graph_objects as go


# ============================================================
# COSTANTI DEL PROBLEMA
# ============================================================

# Numero totale di figurine dell'album
N_FIGURINE = 980

# Numero di figurine per bustina
FIGURINE_PER_BUSTINA = 7

# Costo di una bustina
COSTO_BUSTINA = 1.50

# Costo di una figurina singola mancante
COSTO_FIGURINA_SINGOLA = 0.50

# Costo fisso dell'album
COSTO_ALBUM = 4.50

# ============================================================
# FUNZIONI PER CALCOLARE FIGURINE ATTESE, MANCANTI E COSTO TOTALE                
# ============================================================

# Questa funzione calcola quante figurine mancano in media dopo aver comprato un numero n di bustine (il nostro parametro "numero_bustine").
# Se ogni bustina contiene 7 figurine, dopo aver comprato n bustine avremo 7*n figurine.
# Dopo aver estratto 7*n figurine, la probabilità che una specifica figurina non sia ancora uscita è:
#                           (1 - 1/Numero totale di figurine)^(7*n)
# Quindi il numero di di figurine ancora mancanti è: 
#                           Num tot figurine * (1 - 1/Numero totale di figurine)^(7*n)   

def figurine_mancanti_attese(numero_bustine):

    # se per esempio abbiamo già 10 bustine, la nostra variabile "estrazioni_totali" sarà = a 70
    estrazioni_totali = numero_bustine * FIGURINE_PER_BUSTINA

    mancanti = N_FIGURINE * (1 - 1 / N_FIGURINE) ** estrazioni_totali

    return mancanti

# Questa funzione, sulla base del risultato della precedente, ci dice quante figurine dovremmo già avere 

def figurine_diverse_attese(numero_bustine):

    mancanti = figurine_mancanti_attese(numero_bustine)

    diverse = N_FIGURINE - mancanti

    return diverse

# Questa funzione rappresenta un po' il clou del problema: quando mi conviene fermarmi dal comprare bustine ed acquistarle quindi singolarmente?
# All'interno del mio dataframe, simulerò in ogni riga, progressivamente l'acquisto di un numero n di bustine.
# Sulla base delle n bustine che acquisto, posso quindi calcolare quanto sarà il costo della parte "bustine" e quale della parte delle singole figurine specifiche

def costo_totale_atteso(numero_bustine):

    # Qui daremo, riga per riga, il numero di bustine acquistate. Tramite la prima funzione ci dirà quante figurine otterremo da quelle bustine
    costo_bustine = numero_bustine * COSTO_BUSTINA 

    # Calcoliamo quante figurine mancano dopo l'acquisto di n bustine.
    mancanti = figurine_mancanti_attese(numero_bustine)

    costo_singole = mancanti * COSTO_FIGURINA_SINGOLA

    totale = costo_bustine + costo_singole + COSTO_ALBUM # si aggiunge infine il costo fisso dell'album

    return totale


# ============================================================
# CREAZIONE DELLA TABELLA DATI
# ============================================================

# Decidiamo fino a quante bustine simulare/calcolare.
# 300 è più che sufficiente per vedere bene il minimo.
max_bustine = 300

# Con la funzione "arange" creiamo una lista di tutti i numeri interi da 0 al max_bustine + 1 e la salviamo in "bustine"
bustine = np.arange(0, max_bustine + 1)

# Creiamo il nostro dataframe, ovvero la tabella con tutti i valori calcolati, ognuno in base al numero di bustine di quella riga
# Il dataframe sarà strutturato così:
# Bustine   |   Costo bustine   |   Figurine diverse attese    | Figurine mancanti attese | Costo singole mancanti | Costo totale atteso
df = pd.DataFrame({
    "Bustine": bustine,
    "Costo bustine": bustine * COSTO_BUSTINA,
    "Figurine diverse attese": [figurine_diverse_attese(b) for b in bustine],   # per esempio qui scorriamo ogni valore della lista "bustine" per calcolare quante figurine diverse abbiamo trovato con n bustine
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
# TROVIAMO LA STRATEGIA MIGLIORE
# ============================================================

# Troviamo la riga con costo totale minimo
# NB: la funzione "loc[]" di pandas serve per estrarre una colonna/riga in base alla sua label
riga_ottima = df.loc[df["Costo totale atteso"].idxmin()] # idxmin va a prendere la riga con valore minore

# In base alla riga ottima che abbiamo ottenuto estraiamo anche i dati delle altre colonne di quella riga (n bustine, costo, ecc.)
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
# GRAFICO DEL COSTO TOTALE ATTESO
# ============================================================

# La funzione .line di Plotly Express serve per creare grafici a linee interattivi.
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

# Aggiungiamo il punto minimo usando go (Graph Objects) di Plotly
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

# La funzione show() ci mostra il grafico. La libreria di Plotly fa il render del grafico automaticamente attraverso il browser.
fig.show()

# ============================================================
# GRAFICO FIGURINE DIVERSE / MANCANTI
# In maniera simile a prima creiamo un'altro grafico.
# Questa volta però il grafico rappresenta il costo delle bustine e quello delle figurine singole all'aumentare del numero n di bustine acquistate.
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
# GRAFICO DELLE COMPONENTI DI COSTO
# Grafico riassuntivo di costi bustine, figurine singole e strategia ottima.
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
# SIMULAZIONE MONTE CARLO
# ============================================================

import random

# Con il metodo Monte Carlo andiamo a simulare l'acquisto di n bustine --> Ogni bustina contiene 7 figurine casuali diverse.
# Questa funzione alla fine restituisce quante figurine diverse abbiamo trovato aprendo n bustine, quante ne mancano e qual'è il costo totale della strategia.

def simula_album(numero_bustine):
   
    # Insieme delle figurine trovate.
    # NB: Usiamo un set per raccogliere le figurine perché elimina automaticamente i duplicati.
    figurine_trovate = set()

    # Simuliamo l'apertura delle bustine
    for _ in range(numero_bustine):

        # Estraiamo 7 figurine diverse da un album di 980 assegnando ad ogni figurina un numero intero invece che il nome/squadra/altro
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

# Questa funzione invece simula il metodo Monte Carlo per un numero di volte pari a quello riportato nel parametro "numero_simulazioni"
# Calcoliamo poi la media di figurine diverse trovate, media delle figurine mancanti e media del costo totale oltre che la deviazione standard del costo.
def monte_carlo(numero_bustine, numero_simulazioni=1000):

    risultati = []

    for _ in range(numero_simulazioni):
        diverse, mancanti, costo = simula_album(numero_bustine)

        risultati.append({
            "Bustine": numero_bustine,
            "Figurine diverse": diverse,
            "Figurine mancanti": mancanti,
            "Costo totale": costo
        })

    # Infine restituisce il Dataframe con le simulazioni per il numero di bustine passato come parametro (noi proveremo il numero ottimale di prima)
    return pd.DataFrame(risultati)


# Proviamo la simulazione sul numero ottimale teorico ottenuto prima
simulazioni_ottimo = monte_carlo(bustine_ottime, numero_simulazioni=5000)

print(simulazioni_ottimo.describe())

# ============================================================
# ISTOGRAMMA DEI COSTI SIMULATI
# ============================================================

# Istogramma dei costi simulati attraverso il metodo Monte Carlo
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