import streamlit as st
from utils import load_csv, to_display
import plotly.express as px


st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>📊 Visualisation</h2>",
    unsafe_allow_html=True,
)

df = load_csv(drop_outliers=False)
df_display = to_display(df)


st.subheader(":blue[Analyse univariée]", divider=True)

st.write(
    """
    L’analyse univariée consiste à examiner **chaque variable séparément**, sans tenir compte des autres. 
    Elle permet de comprendre la **répartition** des données, de détecter d’éventuels **déséquilibres**, 
    ou encore d’identifier des **outliers**, c'est à dire des valeurs extrêmes (statistiquement éloignées) ou aberrantes (souvent erronées).

    👉 Chaque onglet onglet ci-dessous présente une **visualisation unique** de la répartition de la **variable cible** (survie),
    ainsi que des **différentes caractéristiques** (âge, sexe, classe, tarif, etc.).

    Cette étape est essentielle pour avoir une première idée de la **structure des données** avant de passer 
    à des analyses plus complexes (bivariées ou multivariées) et enfin à la modélisation prédictive.
    """
)

(
    tab_survived,
    tab_sex,
    tab_age,
    tab_class,
    tab_fare,
    tab_sibsp,
    tab_parch,
    tab_embark,
) = st.tabs(
    [
        "🛟 Survie",
        "♀️♂️ Sexe",
        "👶🧓 Age",
        "🎟️ Classe",
        "💰 Tarif",
        """🧑‍🤝‍🧑 Fratrie  
        & conjoint(e)""",
        """👨‍👩‍👦‍👦 Parents  
        & enfants""",
        "⚓ Embarquement",
    ]
)

with tab_survived:
    fig = px.pie(
        df_display,
        names="Survie",
        category_orders={"Survie": ["🟢 Oui", "🔴 Non"]},
        title="Répartition des survivants",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)

    st.write(
        """La variable cible indique si un passager a survécu (`Oui`) ou pas (`Non`).   
        On observe que moins de 39% des passages ont survécu."""
    )

with tab_sex:
    fig = px.pie(
        df_display,
        names="Sexe",
        category_orders={"Sexe": ["♀️ Femme", "♂️ Homme"]},
        title="Répartition des genres",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write("Il y avait presque 2 fois plus d'hommes que de femmes à bord du Titanic")

with tab_age:
    fig = px.histogram(
        df_display, x="Age", title="Distribution des âges", marginal="box"
    )

    # Ajout du trait vertical pour la médiane
    median_age = df_display["Age"].median()
    fig.add_vline(
        x=median_age,
        line_dash="dash",
        line_color="red",
        annotation_text=f"{int(median_age)} ans",
        annotation_position="right",
    )
    st.plotly_chart(fig)
    st.write(
        """Les passagers du Titanic étaient âgés de 5 mois à 80 ans, avec une forte représentation d'adultes entre 18 et 50 ans. 
        Comme vu sur la page précédente, l'âge de 177 passagers (soit 19.9%) n'est pas renseigné dans le jeu de données. 
        La valeur médiane de la distribution (28 ans) leur sera arbitrairement attribuée."""
    )

with tab_class:
    fig = px.pie(
        df_display,
        names="Classe",
        category_orders={"Classe": ["1ère", "2ème", "3ème"]},
        title="Répartition des classes",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write("La 3ème classe (populaire) est la plus représentée")

with tab_fare:
    fig = px.histogram(
        df_display, x="Tarif", title="Distribution des tarifs", marginal="box"
    )
    st.plotly_chart(fig)
    st.write(
        "Trois passagers présentent un tarif de £512.33, nettement supérieur à la distribution générale. Bien que ces valeurs extrêmes ne soient pas nécessairement aberrantes, elles sont considérées comme des outliers et seront exclues du jeu de données afin d'éviter qu’elles ne biaisent les résultats ultérieurs."
    )

with tab_sibsp:
    fig = px.pie(
        df_display,
        names="Fratrie & Conjoint(e)",
        category_orders={
            "Fratrie & Conjoint(e)": sorted(
                df_display["Fratrie & Conjoint(e)"].unique()
            )
        },
        title="""Répartition du nombre de frères, sœurs et conjoint(e)""",
    )
    fig.update_traces(
        textposition="inside",
        textinfo="value+percent+label",
        insidetextorientation="radial",
    )

    st.plotly_chart(fig)
    st.write("Plus de 2/3 des passagers voyagent sans frère ni sœur ni conjoint(e).")

with tab_parch:
    fig = px.pie(
        df_display,
        names="Parents & Enfants",
        category_orders={
            "Parents & Enfants": sorted(df_display["Parents & Enfants"].unique())
        },
        title="Répartition du nombre de parents et enfants",
    )
    fig.update_traces(
        textposition="inside",
        textinfo="value+percent+label",
        insidetextorientation="radial",
    )
    st.plotly_chart(fig)
    st.write("Plus de 3/4 des passagers voyagent sans parent ni enfant.")

with tab_embark:
    fig = px.pie(
        df_display,
        names="Embarquement",
        title="Répartition des ports d'embarquement",
    )
    fig.update_traces(textposition="auto", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write(
        """Près de 3/4 des passagers ont embarqués à Southampton (Angleterre).  
             Comme vu sur la page précédente, le port d'embarquement de 2 passagers n'est pas renseigné dans le jeu de données. 
             La valeur majoritaire ('Southampton') leur sera arbitrairement attribuée."""
    )


st.subheader(":blue[Analyse bivariée]", divider=True)

df_display = df_display[df_display["Tarif"] < 500]
median_age = df_display["Age"].median()
embarked_mode = df_display["Embarquement"].mode()[0]
df_display["Age"] = df_display["Age"].fillna(median_age)
df_display["Embarquement"] = df_display["Embarquement"].fillna(embarked_mode)

hist = px.histogram(df_display, x="Survie", color="Sexe", barmode="group")
st.plotly_chart(hist)

st.subheader(":blue[Analyse multivariée]", divider=True)


fig = px.sunburst(df_display, path=["Sexe", "Survie", "Classe"])
st.plotly_chart(fig)

st.write(
    """Ce graphique met en évidence 2 tendances:  
        • Les femmes n'ayant pas survécu voyageaient très majoritairement en 3ème classe (parmi les 81 femmes n'ayant pas survécu, 72 voyageaient en 3ème classe).  
        • Les hommes n'ayant pas survécu sont répartis sur les 3 classes mais un déséquilibre important est observée sur la classe 3 (parmi les 347 hommes voyageant en 3ème classe, 300 n'ont pas survécu)"""
)


_, col, _ = st.columns(3)
with col:
    st.page_link(
        st.Page(
            "pages/3_Evaluation.py",
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
