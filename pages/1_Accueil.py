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
    caption="RMS Titanic au départ de Southampton le 10 avril 1912.",
)


st.write("")


# Texte à lire
text = """Le naufrage du Titanic est l’une des catastrophes maritimes les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme “insubmersible”, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  

Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres. L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? », en s’appuyant sur les données disponibles de 891 passagers (nom, âge, sexe, classe socio-économique, etc...)

Votre capitaine Flamm Didier et la compagnie DIDS (Dive into Data Science), vous souhaitent la bienvenue à bord du projet Titanic.  

Bon voyage !  
⚓ 🚢 ⚠️ 🧊 🚨 💥 🆘 🛟 🚣 
"""


# Fonction de stream
def stream_data():
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.1)


# 👇 Lancement au clic
#if st.button("🚢 Accélérer l'embarquement"): #or "go_next_1" in st.session_state:
    #st.session_state.go_next_1 = False
    # 🔊 Synthèse vocale avec interaction utilisateur (voix française)
components.html(
        f"""
        <button onclick="speak()">🔊 Audioguide</button>
        <script>
            function speak() {{
                var msg = new SpeechSynthesisUtterance({text!r});
                msg.lang = 'fr-FR';
                window.speechSynthesis.cancel(); // Arrêter toute lecture en cours
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """,
        height=40,
    )

if "go_next_1" not in st.session_state:
        st.write_stream(stream_data)
else:
        st.write(text)

st.divider()

st.write("Ensemble de données (891 passagers) :")

df = load_csv()
st.dataframe(df)
st.caption("Les valeurs 'None' grises indiquent des données manquantes")

with st.expander("Afficher les données manquantes"):
        # Compter les valeurs manquantes et formater proprement
        missing = df.isna().sum().to_frame(name="Valeurs manquantes")
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

st.write("Note concernant les variables :")
df = pd.DataFrame(
        {
            "Variable": [
                "    Survived",
                "    Pclass",
                "    SibSp",
                "    Parch",
                "    Fare",
                "    Cabin",
                "    Embarked",
            ],
            "Définition": [
                "Survie du passager",
                "Classe du billet (indicateur du statut socio-économique)",
                "Nombre de frères, Sœurs, époux ou épouse à bord du Titanic",
                "Nombre de parents et enfants à bord du Titanic",
                "Tarif de la cabine (pour l'ensemble des occupants)",
                "Numéro de la cabine",
                "Port d'embarquement",
            ],
            "Valeurs": [
                "0 = Non, 1 = Oui",
                "1 = 1ère (classe aisée), 2 = 2ème (classe moyenne), 3 = 3ème (classe populaire))",
                "",
                "",
                "",
                "",
                "C = Cherbourg, Q = Queenstown, S = Southampton",
            ],
        }
    )

st.table(df.set_index("Variable"))

st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/TitanicRoute.svg")

    # ajout d'une variable d'état go_next pour éviter que l’appel à st.switch_page() soit ignoré
    # parce que le bouton a déclenché un rerun qui reset des variables.

st.session_state.go_next_1 = True

st.button("Passer à l'étape suivante")

    #st.switch_page(st.session_state.pages[1])

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
