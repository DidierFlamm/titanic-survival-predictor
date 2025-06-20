# -*- coding: utf-8 -*-
import streamlit as st
from utils import load_csv
import pandas as pd

st.set_page_config(page_title="Titanic")
st.title("Bienvenue à bord du projet Titanic")


st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Titanic_in_color.png/960px-Titanic_in_color.png",
    caption="RMS Titanic au départ de Southampton le 10 avril 1912.",
)


st.write("")
st.markdown(
    """Le naufrage du [Titanic](https://fr.wikipedia.org/wiki/Titanic) est l’un des naufrages les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme “insubmersible”, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  
Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres ("les femmes et les enfants d'abord" ?).  

L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? », en s’appuyant sur les [données](https://github.com/datasciencedojo/datasets/blob/master/titanic.csv) disponibles de 891 passagers (nom, âge, sexe, classe socio-économique, etc...) reprises ci-dessous."""
)


df = load_csv()
st.dataframe(df)
st.caption("Les valeurs grises indiquent des données manquantes.")

with st.expander("Afficher les valeurs manquantes"):
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

st.markdown("---")
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

if st.button("Passer à l'étape suivante"):
    if len(st.session_state.pages) == 1:
        st.session_state.pages.append(
            st.Page(
                "pages/2_Visualisation.py",
                title="Visualisation",
                icon="📊",
            )
        )
    st.switch_page(st.session_state.pages[1])

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
