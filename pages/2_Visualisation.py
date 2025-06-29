import streamlit as st
from utils import load_csv
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>📊 Visualisation</h2>",
    unsafe_allow_html=True,
)

df = load_csv(drop_outliers=False)

df_display = df.copy()

df_display["Sex"] = df_display["Sex"].map({"female": "Femme", "male": "Homme"})
df_display["Survived"] = df_display["Survived"].map({0: "Non", 1: "Oui"})

palette = sns.color_palette("RdYlGn", n_colors=3)  # rouge - jaune - vert
palette = [palette[2], palette[0]]  # vert et rouge

st.subheader(":blue[Analyse univariée]", divider=True)

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
        "Survie (cible)",
        "Sexe",
        "Age",
        "Classe",
        "Tarif",
        "Fratrie & conjoint(e)",
        "Parents & enfants",
        "Embarquement",
    ]
)

with tab_survived:
    fig = px.pie(
        df_display,
        names="Survived",
        category_orders={"Survived": ["Oui", "Non"]},
        title="Répartition des survivants",
    )
    st.plotly_chart(fig)

with tab_sex:
    fig = px.pie(
        df_display,
        names="Sex",
        category_orders={"Sex": ["Femme", "Homme"]},
        title="Répartition des genres",
    )
    st.plotly_chart(fig)

with tab_age:
    fig = px.histogram(
        df_display,
        x="Age",
        title="Distribution des âges",
    )
    st.plotly_chart(fig)

with tab_class:
    fig = px.pie(
        df_display,
        names="Pclass",
        category_orders={"Pclass": [1, 2, 3]},
        title="Répartition des classes",
    )
    st.plotly_chart(fig)

with tab_fare:
    fig = px.histogram(
        df_display,
        x="Fare",
        title="Distribution des tarifs",
    )
    st.plotly_chart(fig)
    st.write(
        "Trois passagers présentent un tarif de £512.33, nettement supérieur à la distribution générale. Bien que ces valeurs extrêmes ne soient pas nécessairement aberrantes, elles sont considérées comme des outliers et seront exclues du jeu de données afin d'éviter qu’elles ne biaisent les résultats ultérieurs."
    )

with tab_sibsp:
    fig = px.pie(
        df_display,
        names="SibSp",
        category_orders={"SibSp": sorted(df_display.SibSp.unique())},
        title="Répartition du nombre de frères, sœurs et conjoint(e)",
    )
    st.plotly_chart(fig)

with tab_parch:
    fig = px.pie(
        df_display,
        names="Parch",
        category_orders={"Parch": sorted(df_display.Parch.unique())},
        title="Répartition du nombre de parents et enfants",
    )
    st.plotly_chart(fig)

with tab_embark:
    fig = px.pie(
        df_display,
        names="Embarked",
        # category_orders={"Parch": sorted(df_display.Parch.unique())},
        title="Répartition des ports d'embarquement",
    )
    st.plotly_chart(fig)


fig, axs = plt.subplots(1, 3, figsize=(12, 4))
sns.countplot(
    x="Survived", data=df_display, order=["Oui", "Non"], palette=palette, ax=axs[0]
)


axs[0].set_xlabel("Survie")
for ax in axs:
    ax.set_ylabel("Nombre de passagers")
axs[0].set_title("Survie des passagers (cible de l'étude)")

sns.histplot(
    data=df_display,
    x="Age",
    # rug=True,
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 81],
    ax=axs[1],
)
axs[1].set_title("Distribution de l'âge des passagers")

sns.histplot(
    data=df_display,
    x="Fare",
    # bins=[0, 100, 200, 30, 40, 50, 60, 70, 80],
    ax=axs[2],
)
axs[2].set_xlabel("Tarif")
axs[2].set_title("Distribution des tarifs")

plt.tight_layout()

st.pyplot(fig)
####################################################

st.write(
    "Trois passagers présentent un tarif de 512.33, nettement supérieur à la distribution générale. Bien que ces valeurs extrêmes ne soient pas nécessairement aberrantes, elles sont considérées comme des outliers et seront exclues du jeu de données afin d'éviter qu’elles ne biaisent les résultats ultérieurs. L’analyse est ainsi restreinte aux 888 passagers ayant un tarif compris entre 0 et 263."
    if st.session_state.lang.startswith("fr")
    else "Three passengers have a fare of 512.33, which is significantly higher than the overall distribution. While these extreme values are not necessarily erroneous, they are considered outliers and will be excluded from the dataset to prevent them from skewing subsequent results. The analysis is thus limited to the 888 passengers whose fares range between 0 and 263."
)


st.subheader(":blue[Analyse multivariée]", divider=True)

df_display = df_display[df_display["Fare"] < 500]

fig, axs = plt.subplots(3, 2, figsize=(12, 12))  # 3 lignes, 2 colonnes

sns.kdeplot(
    data=df_display,
    x="Age",
    hue="Survived",
    hue_order=["Oui", "Non"],
    palette=palette,
    cut=0,
    fill=True,
    alpha=0.6,
    ax=axs[0, 0],
)
axs[0, 0].set_xlabel("Âge")
axs[0, 0].set_ylabel("Densité")
axs[0, 0].set_title("Survie en fonction de l'âge")

sns.histplot(
    data=df_display,
    x="Age",
    bins=17,
    hue="Survived",
    hue_order=["Non", "Oui"],
    multiple="fill",
    cumulative=False,
    palette=palette[::-1],
    fill=True,
    alpha=0.6,
    ax=axs[1, 0],
)
axs[1, 0].set_xlabel("Âge")
axs[1, 0].set_ylabel("Densité")
axs[1, 0].set_title("Survie en fonction de l'âge")

sns.histplot(
    data=df_display,
    x="Fare",
    bins=20,
    hue="Survived",
    hue_order=["Oui", "Non"],
    multiple="fill",
    cumulative=False,
    palette=palette,
    fill=True,
    alpha=0.6,
    ax=axs[1, 1],
)
# axs[1, 0].set_xlim(0, 300)
# axs[1, 1].set_ylim(0, 150)

###################################################

sns.kdeplot(
    data=df_display,
    x="Fare",
    hue="Survived",
    hue_order=["Oui", "Non"],
    palette=palette,
    cut=0,
    fill=True,
    alpha=0.6,
    ax=axs[0, 1],
)
# axs[0, 1].set_xlim(0, 150)
axs[0, 1].set_xlabel("Tarif")
axs[0, 1].set_ylabel("Densité")
axs[0, 1].set_title("Survie en fonction du tarif")

sns.countplot(
    x="Sex",
    data=df_display,
    hue="Survived",
    order=["Femme", "Homme"],
    hue_order=["Oui", "Non"],
    palette=palette,
    # stat="count",
    # saturation=0.75,
)

sns.countplot(
    x="Pclass",
    data=df_display,
    hue="Survived",
    hue_order=["Oui", "Non"],
    palette=palette,
)

sns.countplot(
    x="SibSp",
    data=df_display,
    hue="Survived",
    hue_order=["Oui", "Non"],
    palette=palette,
)

sns.countplot(
    x="Parch",
    data=df_display,
    hue="Survived",
    hue_order=["Oui", "Non"],
    palette=palette,
)
plt.title("Survie en fonction du nombre de parents")
plt.tight_layout()
st.pyplot(fig)


st.subheader(":blue[Analyse interactive]", divider=True)

hist = px.histogram(df, x="Survived", color="Sex", barmode="group")
st.plotly_chart(hist)

hist_bis = px.sunburst(df, path=["Sex", "Pclass"])
st.plotly_chart(hist_bis)


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
