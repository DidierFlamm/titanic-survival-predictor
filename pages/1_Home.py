# -*- coding: utf-8 -*-
import streamlit as st
import time
from utils import load_csv
import pandas as pd
import streamlit.components.v1 as components


# add next page at top of script to skip it if wished
if len(st.session_state.pages) == 1:
    st.session_state.pages.append(
        st.Page(
            "pages/2_Visualisation.py",
            title="Visualisation",
            icon="📊",
        )
    )
    st.navigation(st.session_state.pages, position="top")

st.title("🚢 Titanic Survival Predictor")


st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Titanic_in_color.png/960px-Titanic_in_color.png",
    caption=(
        "RMS Titanic au départ de Southampton le 10 avril 1912"
        if st.session_state.lang == "fr"
        else "RMS Titanic departing from Southampton on April 10, 1912"
    ),
)


st.header("Introduction")


# Textes à lire

text_FR = """
Le naufrage du Titanic est l’une des catastrophes maritimes les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme insubmersible, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  

Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres. L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? » en s’appuyant sur certaines données de 891 passagers, telles que leur nom, âge, sexe, famille, classe, etc...

Votre capitaine, Flamm Didier, et vos matelots Charlize et James vous souhaitent la bienvenue à bord du projet Titanic.  

Embarquez pour un voyage serein et passionnant à travers le vaste océan des données avec DIDS  
"""

text_DIDS = """Dive Into Data Science !"""

text_INTRO = text_FR

text = text_INTRO + text_DIDS


# Fonction de stream
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.1)


script = f"""
<script>
    var msgINTRO = new SpeechSynthesisUtterance({text_FR!r});
    msgINTRO.lang = {st.session_state.lang!r};
    msgINTRO.rate = 1.1;

    var msgDIDS = new SpeechSynthesisUtterance({text_DIDS!r});
    msgDIDS.lang = 'en-US';
    msgDIDS.rate = 1.1;

    function speak() {{
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msgINTRO);
        window.speechSynthesis.speak(msgDIDS);
    }}

    function stop() {{
        window.speechSynthesis.cancel();
    }}
</script>
"""

col1, col2 = st.columns(2)

with col1:
    components.html(
        script
        + f"""<button onclick="speak()">🎧 Audio Guide {st.session_state.flag}</button>""",
        height=40,
    )

with col2:
    components.html(
        script + """<button onclick="stop()">🔇 Stop Audio Guide</button>""",
        height=40,
    )


if "skip_stream" not in st.session_state:
    st.session_state.skip_stream = True
    st.write_stream(stream_data(text))
else:
    st.write(text)


st.write("🤿 📊 🌊")

st.divider()

st.header("Données" if st.session_state.lang == "fr" else "Data")

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
st.caption(
    "Les valeurs 'None' grises indiquent des valeurs manquantes"
    if st.session_state.lang == "fr"
    else "The gray 'None' values indicate missing data"
)

with st.expander(
    "Afficher les valeurs manquantes"
    if st.session_state.lang == "fr"
    else "Display missing values"
):
    # Compter les valeurs manquantes et formater proprement
    missing = df_display.isna().sum().to_frame(name="Nombre")
    missing.index.name = "Valeurs manquantes"
    missing["%"] = missing["Nombre"] / len(df)
    missing["%"] = missing["%"].map(lambda x: f"{x:.1%}")
    # filtre et trie des valeurs manquantes
    missing = missing[missing["Nombre"] > 0]
    missing = missing.sort_values("Nombre", ascending=False)
    st.dataframe(missing, width=300, use_container_width=False)


st.markdown(
    ("Source des données" if st.session_state.lang == "fr" else "Data source")
    + ' : <a href="https://github.com/datasciencedojo/datasets/blob/master/titanic.csv" target="_blank">Data Science Dojo</a>',
    unsafe_allow_html=True,
)

st.divider()

st.write(
    "Précisions concernant les variables:"
    if st.session_state.lang == "fr"
    else "Details about the variables:"
)
df = pd.DataFrame(
    {
        "Variable": [
            "Survie",
            "Sexe",
            "Classe",
            """Fratrie  
            & Époux(se)""",
            """Parents  
            & Enfants""",
            "Tarif",
            "Cabine",
            """Embarquement""",
        ],
        "Définition": [
            "Est-ce que le passager a survécu ?",
            "Sexe du passager",
            """Classe du billet  
            (indicateur du statut socio-économique)""",
            """Nombre de frères, sœurs, époux(se)  
            à bord du Titanic""",
            """Nombre de parents et enfants  
            à bord du Titanic""",
            """Tarif de la cabine en livre sterling (£)  
            pour l'ensemble de ses occupants""",
            "Numéro de la cabine",
            "Port d'embarquement",
        ],
        "Valeurs": [
            """🟢 = Oui  
            🔴 = Non""",
            """F = Femme  
            H = Homme""",
            """1 = 1ère (classe aisée)  
            2 = 2ème (classe moyenne)  
            3 = 3ème (classe populaire)""",
            "",
            "",
            "",
            "",
            """C = Cherbourg 🇫🇷  
            Q = Queenstown 🇮🇪  
            S = Southampton 🇬🇧""",
        ],
    }
)

st.table(df.set_index("Variable"))

st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/TitanicRoute.svg")

st.divider()


st.page_link(
    st.Page(
        "pages/2_Visualisation.py",
        title=(
            "Passer à l'étape suivante"
            if st.session_state.lang == "fr"
            else "Go to the next step"
        ),
        icon="➡️",
    )
)

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
