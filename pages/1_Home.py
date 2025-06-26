# -*- coding: utf-8 -*-
import streamlit as st
import time
from utils import load_csv
import pandas as pd
import streamlit.components.v1 as components


st.markdown(
    "<h1 style='text-align: center; color: #0366d6;'>🚢 Titanic Survival Predictor</h1>",
    unsafe_allow_html=True,
)

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Titanic_in_color.png/960px-Titanic_in_color.png",
    caption=(
        "RMS Titanic au départ de Southampton le 10 avril 1912"
        if st.session_state.lang.startswith("fr")
        else "RMS Titanic departing from Southampton on April 10, 1912"
    ),
)


st.header(":blue[Introduction]", divider=True)


# Textes à lire

text_FR = """
Le naufrage du Titanic est l’une des catastrophes maritimes les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme insubmersible, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  

Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres. L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? » en s’appuyant sur certaines données de 891 passagers, telles que leur nom, âge, sexe, famille, classe, etc...

Votre capitaine, Flamm Didier, et vos matelots Charlize et James vous souhaitent la bienvenue à bord du projet Titanic. Embarquez pour un voyage serein et passionnant à travers le vaste océan des données !
"""

text_EN = """
The sinking of the Titanic is one of the most famous maritime disasters in history. On April 15, 1912, during its maiden voyage, the RMS Titanic—considered “unsinkable”—sank after colliding with an iceberg. Unfortunately, there were not enough lifeboats for everyone on board, resulting in the deaths of 1,502 out of 2,224 passengers and crew members.  

Although chance played a role in survival odds, some groups of people seemed more likely to survive than others. The goal of this project is to build a predictive model to answer the question: “What types of people were most likely to survive?” based on data from 891 passengers, such as their name, age, sex, family, class, and more.  

Your captain, Flamm Didier, and your crewmates Charlize and James welcome you aboard the Titanic project. Embark on a safe and exciting journey through the vast ocean of data !
"""

text_DIDS = """DIDS — Dive Into Data Science"""

text_INTRO = text_FR if st.session_state.lang.startswith("fr") else text_EN

text = text_INTRO + text_DIDS


# Fonction de stream
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.1)


script = f"""
<script>
    var msgINTRO = new SpeechSynthesisUtterance({text_INTRO!r});
    msgINTRO.lang = {st.session_state.lang!r};
    msgINTRO.rate = 1.1;

    var msgDIDS = new SpeechSynthesisUtterance({text_DIDS!r});
    msgDIDS.lang = 'en-GB';
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

(col1, col2, *_) = st.columns(4, vertical_alignment="center")

with col1:
    components.html(
        script
        + f"""<button onclick="speak()">🎧 {st.session_state.flag}<br>Audio Guide</button>""",
        height=45,
    )

with col2:
    components.html(
        script + """<button onclick="stop()">🔇<br>Stop</button>""",
        height=45,
    )


if "skip_stream" not in st.session_state:
    st.session_state.skip_stream = True
    st.write_stream(stream_data(text_INTRO))
    st.write_stream(stream_data(text_DIDS))
else:
    st.write(text_INTRO)
    st.write(text_DIDS)


st.write("🤿 📊 🌊")


st.header(
    ":blue[Données]" if st.session_state.lang.startswith("fr") else ":blue[Data]",
    divider=True,
)

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
    if st.session_state.lang.startswith("fr")
    else "The gray 'None' values indicate missing data"
)

with st.expander(
    "Afficher les valeurs manquantes"
    if st.session_state.lang.startswith("fr")
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
    ("Source des données" if st.session_state.lang.startswith("fr") else "Data source")
    + ' : <a href="https://github.com/datasciencedojo/datasets/blob/master/titanic.csv" target="_blank">Data Science Dojo</a>',
    unsafe_allow_html=True,
)


st.subheader(
    (
        ":blue[Précisions]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Details]"
    ),
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
            """1 = 1ère classe (aisée)  
            2 = 2ème classe (moyenne)  
            3 = 3ème classe (populaire)""",
            "",
            "",
            "",
            "",
            """C = 🇫🇷 Cherbourg  
            Q = 🇮🇪 Queenstown  
            S = 🇬🇧 Southampton""",
        ],
    }
)

st.table(df.set_index("Variable"))

st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/TitanicRoute.svg")


_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/2_Visualisation.py",
            title=(
                "Passer à l'étape suivante"
                if st.session_state.lang.startswith("fr")
                else "Go to the next step"
            ),
            icon="➡️",
        )
    )

st.divider()

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
