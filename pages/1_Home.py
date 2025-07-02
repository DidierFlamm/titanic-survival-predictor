# -*- coding: utf-8 -*-
import streamlit as st
from utils import load_csv, to_display, translate_text
import pandas as pd
import streamlit.components.v1 as components

st.markdown(
    "<h1 style='text-align: center; color: #0366d6;'>🚢 Titanic Survival Predictor</h1>",
    unsafe_allow_html=True,
)

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Titanic_in_color.png/960px-Titanic_in_color.png",
    caption=(
        """RMS Titanic au départ de Southampton le 10 avril 1912  
        Francis G. O. Stuart (1843–1923), colorisée (domaine public)"""
        if st.session_state.lang.startswith("fr")
        else """RMS Titanic departing from Southampton on April 10, 1912  – Francis G. O. Stuart (1843–1923), colorized (public domain)"""
    ),
)


st.header(":blue[Introduction]", divider=True)


# Textes à lire

intro_FR = """
Le naufrage du Titanic est l’une des catastrophes maritimes les plus célèbres de l’histoire. Le 15 avril 1912, lors de son voyage inaugural, le RMS Titanic, pourtant considéré comme insubmersible, a coulé après une collision avec un iceberg. Malheureusement, il n’y avait pas assez de canots de sauvetage pour toutes les personnes à bord, ce qui a entraîné la mort de 1502 des 2224 passagers et membres d’équipage.  

Bien que le hasard ait joué un rôle dans les chances de survie, certains groupes de personnes semblaient avoir plus de chances de survivre que d’autres. L'objectif de ce projet est de construire un modèle prédictif pour répondre à la question « Quels types de personnes avaient le plus de chances de survivre ? » en s’appuyant sur certaines données de 891 passagers, telles que leur nom, âge, sexe, famille, classe, etc...

Votre capitaine, Flamm Didier, et vos matelots Charlize et James vous souhaitent la bienvenue à bord du projet Titanic. Embarquez pour un voyage serein et passionnant à travers le vaste océan des données !
"""

intro_translated = translate_text(intro_FR, st.session_state.lang.split("-")[0])

text_DIDS = """DIDS — Dive Into Data Science"""


script = f"""
<script>
    var msgINTRO = new SpeechSynthesisUtterance({intro_translated!r});
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


# if "skip_stream" not in st.session_state:
#    st.session_state.skip_stream = True
#    st.write_stream(stream_data(intro_translated))
#    st.write_stream(stream_data(text_DIDS))
# else:
st.write(intro_translated)
st.write(text_DIDS)

st.header(
    ":blue[Données]" if st.session_state.lang.startswith("fr") else ":blue[Data]",
    divider=True,
)

df = load_csv(drop_outliers=False)
df_display = to_display(df)

st.dataframe(df_display.style.format({"Tarif": "£{:.2f}"}))
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
            """Fratrie & Époux(se)""",
            """Parents & Enfants""",
            "Tarif",
            "Cabine",
            "Embarquement",
        ],
        "Définition": [
            "Est-ce que le passager a survécu ?",
            "Sexe du passager",
            """Classe du billet *(indicateur du statut socio-économique)*:  
            • 1ère : classe aisée  
            • 2ème : classe moyenne  
            • 3ème : classe populaire""",
            """Nombre de frères, sœurs, époux(se) à bord du Titanic""",
            """Nombre de parents et enfants à bord du Titanic""",
            """Tarif de la cabine en livre sterling (£) pour l'ensemble de ses occupants""",
            "Numéro de la cabine",
            "Port d'embarquement (voir carte ci-dessous)",
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
