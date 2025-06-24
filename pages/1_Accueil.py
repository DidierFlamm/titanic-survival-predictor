# -*- coding: utf-8 -*-
import streamlit as st
import time
from utils import load_csv
import pandas as pd
import streamlit.components.v1 as components

# set title
st.set_page_config(page_title="Titanic")

# add next page
if len(st.session_state.pages) == 1:
    st.session_state.pages.append(
        st.Page(
            "pages/2_Visualisation.py",
            title="Visualisation",
            icon="📊",
        )
    )

# manage switch
if "go_next_1" in st.session_state:
    if st.session_state.go_next_1:
        st.session_state.go_next_1 = False
        st.switch_page(st.session_state.pages[1])


st.title("Titanic")


st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Titanic_in_color.png/960px-Titanic_in_color.png",
    caption="RMS Titanic au départ de Southampton le 10 avril 1912",
)


st.header("Introduction")


# Texte à lire


text_FR1 = """Le naufrage du Titanic est l’une des catastrophes maritimes les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme “insubmersible”, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  

Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres. L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? », en s’appuyant sur les données de 891 passagers telles que leur nom, âge, sexe, classe socio-économique, etc...

Votre capitaine Flamm Didier vous souhaite la bienvenue à bord du projet Titanic, opéré par la compagnie DIDS """

text_EN = """(Dive Into Data Science)."""

text_FR2 = """

Bon voyage ! 
"""

text = text_FR1 + text_EN + text_FR2


# Fonction de stream
def stream_data():
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.1)


# 👇 Lancement au clic
# if st.button("🚢 Accélérer l'embarquement"): #or "go_next_1" in st.session_state:
# st.session_state.go_next_1 = False
# 🔊 Synthèse vocale avec interaction utilisateur (voix française)

components.html(
    f"""
    <button onclick="speak()">🎧 Audioguide</button>
    <script>
        function speak() {{
            const msgFR1 = new SpeechSynthesisUtterance({text_FR1!r});
            msgFR1.lang = 'fr-FR';
            msgFR1.rate = 1.3;

            const msgEN = new SpeechSynthesisUtterance({text_EN!r});
            msgEN.lang = 'en-US';
            msgEN.rate = 1.0;

            const msgFR2 = new SpeechSynthesisUtterance({text_FR2!r});
            msgFR2.lang = 'fr-FR';
            msgFR2.rate = 1.3;

            window.speechSynthesis.cancel(); // Arrête toute lecture précédente
            window.speechSynthesis.speak(msgFR1);
            window.speechSynthesis.speak(msgEN);
            window.speechSynthesis.speak(msgFR2);
        }}
    </script>
    """,
    height=40,
)


if "go_next_1" not in st.session_state:
    st.write_stream(stream_data)
else:
    st.write(text)

st.write("⚓ 🚢 ⚠️ 🧊 🚨 💥 🆘 🛟 🚣")

st.divider()

st.header("Données")

df = load_csv()

df_display = df.copy()
df_display.columns = [
    "Survie",
    "Classe",
    "Nom",
    "Sexe",
    "Age",
    "Fratrie & Conjoint(e)",
    "Parents & Enfants",
    "Ticket",
    "Tarif",
    "Cabine",
    "Embarquement",
]
df_display["Survie"].replace({1: "🟢", 0: "🔴"}, inplace=True)
df_display["Sexe"].replace({"male": "H", "female": "F"}, inplace=True)

st.dataframe(df_display)
st.caption("Les valeurs 'None' grises indiquent des valeurs manquantes")

with st.expander("Afficher les valeurs manquantes"):
    # Compter les valeurs manquantes et formater proprement
    missing = df_display.isna().sum().to_frame(name="Valeurs manquantes")
    missing["%"] = missing["Valeurs manquantes"] / len(df)
    missing["%"] = missing["%"].map(lambda x: f"{x:.1%}")
    # filtre et trie des valeurs manquantes
    missing = missing[missing["Valeurs manquantes"] > 0]
    missing = missing.sort_values("Valeurs manquantes", ascending=False)
    # affiche en markdown pour avoir style center
    st.markdown(
        missing.style.set_properties(**{"text-align": "center"}).to_html(),  # type: ignore
        unsafe_allow_html=True,
    )

st.markdown('Source des données : <a href="https://github.com/datasciencedojo/datasets/blob/master/titanic.csv" target="_blank">Data Science Dojo</a>', unsafe_allow_html=True)

st.divider()

st.write("Précisions concernant les variables :")
df = pd.DataFrame(
    {
        "Variable": [
            "    Survie",
            "    Sexe",
            "    Classe",
            "    Fratrie & Conjoint(e)",
            "    Parents & Enfants",
            "    Tarif",
            "    Cabine",
            "    Embarquement",
        ],
        "Définition": [
            "Est-ce que le passager a survécu ?",
            "Sexe du passager",
            "Classe du billet (indicateur du statut socio-économique)",
            "Nombre de frères, sœurs, époux ou épouse à bord du Titanic",
            "Nombre de parents et enfants à bord du Titanic",
            "Tarif de la cabine (pour l'ensemble des occupants de la cabine)",
            "Numéro de la cabine",
            "Port d'embarquement",
        ],
        "Valeurs": [
            "🟢 = Oui, 🔴 = Non",
            "F = Femme, H = Homme",
            "1 = 1ère (classe aisée), 2 = 2ème (classe moyenne), 3 = 3ème (classe populaire))",
            "",
            "",
            "",
            "",
            "C = Cherbourg 🇫🇷, Q = Queenstown 🇮🇪, S = Southampton 🇬🇧",
        ],
    }
)

st.table(df.set_index("Variable"))

st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/TitanicRoute.svg")

# ajout d'une variable d'état go_next pour éviter que l’appel à st.switch_page() soit ignoré
# parce que le bouton a déclenché un rerun qui reset des variables.

st.divider()

st.session_state.go_next_1 = True

st.button("Passer à l'étape suivante")

# st.switch_page(st.session_state.pages[1])

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
