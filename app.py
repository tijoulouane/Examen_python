# %% [markdown]
# 1) Import des packages nécessaires

# %%
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px 


# %% [markdown]
# 2) Initialisation de l'application Dash 

# %%
# Importation des données
df = pd.read_csv("supermarket_sales.csv")

# Conversion de la colonne "Date" en format datetime
df["Date"] = pd.to_datetime(df["Date"])
# Création d'une colonne "Week" pour regrouper les données par semaine
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)

# Nettoyage des noms de colonnes (suppression des espaces)
df.columns = df.columns.str.strip()

# Listes pour les filtres
cities = sorted(df["City"].dropna().unique())
genders = sorted(df["Gender"].dropna().unique())


# %% [markdown]
# 3) Création de l'application

# %%
# Initialisation de l'application Dash
application = Dash(__name__)
application.title = "Tableau de bord - Ventes supermarché"

# Couleurs et styles
COULEUR_FOND = "#f6f8f7"
COULEUR_CARTE = "#ffffff"
COULEUR_TITRE = "#1f2d3d"
COULEUR_TEXTE = "#4f5b66"
VERT = "#2e7d32"
VERT_CLAIR = "#e8f5e9"
ORANGE = "#ffb300"
ORANGE_CLAIR = "#fff8e1"
BORDURE = "#dfe6e9"
OMBRE = "0 6px 18px rgba(0,0,0,0.08)"

application.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "margin": "0",
        "backgroundColor": COULEUR_FOND,
        "padding": "12px",
    },
    children=[
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "gap": "20px",
                "marginBottom": "18px",
                "padding": "10px 20px",
                "width": "96%",
                "marginLeft": "auto",
                "marginRight": "auto",
                "flexWrap": "nowrap",
                "backgroundColor": "#f0f4f3",
                "borderRadius": "18px",
                "boxShadow": OMBRE,
                "border": f"1px solid {BORDURE}",
            },
            children=[
                html.Div(
                    [
                        html.H1(
                            " Ventes supermarché",
                            style={
                                "color": COULEUR_TITRE,
                                "margin": "0",
                                "fontSize": "42px",
                                "fontWeight": "800",
                                "whiteSpace": "nowrap",
                                "lineHeight": "1.1",
                            },
                        ),
                        html.P(
                            "Analyse interactive des ventes par sexe et par ville",
                            style={
                                "margin": "6px 0 0 0",
                                "color": COULEUR_TEXTE,
                                "fontSize": "15px",
                            },
                        ),
                    ],
                    style={"flexShrink": "0"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "14px",
                        "alignItems": "center",
                        "justifyContent": "flex-end",
                        "flex": "1",
                    },
                    children=[
                        dcc.Dropdown(
                            id="filtre-sexe",
                            options=[{"label": s, "value": s} for s in genders],
                            value=[],
                            multi=True,
                            placeholder="Sélectionner un sexe",
                            style={"width": "300px"},
                        ),
                        dcc.Dropdown(
                            id="filtre-ville",
                            options=[{"label": v, "value": v} for v in cities],
                            value=[],
                            multi=True,
                            placeholder="Sélectionner une ville",
                            style={"width": "300px"},
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "18px",
                "marginBottom": "18px",
                "width": "96%",
                "marginLeft": "auto",
                "marginRight": "auto",
            },
            children=[
                html.Div(
                    id="indicateur-total",
                    style={
                        "background": f"linear-gradient(135deg, {VERT_CLAIR} 0%, #ffffff 100%)",
                        "padding": "28px",
                        "borderRadius": "20px",
                        "boxShadow": OMBRE,
                        "textAlign": "center",
                        "border": f"1px solid #d9eadb",
                    },
                ),
                html.Div(
                    id="indicateur-nombre",
                    style={
                        "background": f"linear-gradient(135deg, {ORANGE_CLAIR} 0%, #ffffff 100%)",
                        "padding": "28px",
                        "borderRadius": "20px",
                        "boxShadow": OMBRE,
                        "textAlign": "center",
                        "border": f"1px solid #f3e2b3",
                    },
                ),
            ],
        ),

        html.Div(
            style={
                "width": "96%",
                "marginLeft": "auto",
                "marginRight": "auto",
                "marginBottom": "18px",
            },
            children=[
                html.Div(
                    dcc.Graph(id="courbe-ventes-hebdo", style={"height": "500px"}),
                    style={
                        "backgroundColor": COULEUR_CARTE,
                        "padding": "12px",
                        "borderRadius": "20px",
                        "boxShadow": OMBRE,
                        "border": f"1px solid {BORDURE}",
                    },
                )
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "18px",
                "width": "96%",
                "marginLeft": "auto",
                "marginRight": "auto",
            },
            children=[
                html.Div(
                    dcc.Graph(id="barres-achats", style={"height": "430px"}),
                    style={
                        "backgroundColor": COULEUR_CARTE,
                        "padding": "12px",
                        "borderRadius": "20px",
                        "boxShadow": OMBRE,
                        "border": f"1px solid {BORDURE}",
                    },
                ),
                html.Div(
                    dcc.Graph(id="camembert-categories", style={"height": "430px"}),
                    style={
                        "backgroundColor": COULEUR_CARTE,
                        "padding": "12px",
                        "borderRadius": "20px",
                        "boxShadow": OMBRE,
                        "border": f"1px solid {BORDURE}",
                    },
                ),
            ],
        ),
    ],
)

@application.callback(
    Output("indicateur-total", "children"),
    Output("indicateur-nombre", "children"),
    Output("courbe-ventes-hebdo", "figure"),
    Output("barres-achats", "figure"),
    Output("camembert-categories", "figure"),
    Input("filtre-sexe", "value"),
    Input("filtre-ville", "value"),
)
def mettre_a_jour_tableau_de_bord(sexes_selectionnes, villes_selectionnees):
    donnees_filtrees = df.copy()

    if sexes_selectionnes:
        donnees_filtrees = donnees_filtrees[donnees_filtrees["Gender"].isin(sexes_selectionnes)]
    if villes_selectionnees:
        donnees_filtrees = donnees_filtrees[donnees_filtrees["City"].isin(villes_selectionnees)]

    if donnees_filtrees.empty:
        indicateur_total = [
            html.Div("Montant total des achats", style={"color": COULEUR_TEXTE, "fontSize": "20px", "fontWeight": "600"}),
            html.Div("0,00", style={"color": VERT, "fontSize": "48px", "fontWeight": "800", "marginTop": "12px"}),
        ]
        indicateur_nombre = [
            html.Div("Nombre total d'achats", style={"color": COULEUR_TEXTE, "fontSize": "20px", "fontWeight": "600"}),
            html.Div("0", style={"color": ORANGE, "fontSize": "48px", "fontWeight": "800", "marginTop": "12px"}),
        ]

        figure_vide = px.scatter(title="Aucune donnée disponible")
        figure_vide.update_layout(template="plotly_white")
        figure_vide.update_xaxes(visible=False)
        figure_vide.update_yaxes(visible=False)

        return indicateur_total, indicateur_nombre, figure_vide, figure_vide, figure_vide

    montant_total = donnees_filtrees["Total"].sum()
    nombre_factures = donnees_filtrees["Invoice ID"].nunique()

    indicateur_total = [
        html.Div(
            "Montant total des achats",
            style={"color": COULEUR_TEXTE, "fontSize": "21px", "fontWeight": "700", "letterSpacing": "0.2px"},
        ),
        html.Div(
            f"{montant_total:,.2f}".replace(",", " "),
            style={"color": VERT, "fontSize": "54px", "fontWeight": "900", "marginTop": "12px", "lineHeight": "1"},
        ),
        html.Div(
            "Somme de tous les montants filtrés",
            style={"color": "#7b8a8b", "fontSize": "14px", "marginTop": "10px"},
        ),
    ]

    indicateur_nombre = [
        html.Div(
            "Nombre total d'achats",
            style={"color": COULEUR_TEXTE, "fontSize": "21px", "fontWeight": "700", "letterSpacing": "0.2px"},
        ),
        html.Div(
            f"{nombre_factures}",
            style={"color": ORANGE, "fontSize": "54px", "fontWeight": "900", "marginTop": "12px", "lineHeight": "1"},
        ),
        html.Div(
            "Nombre de factures uniques",
            style={"color": "#7b8a8b", "fontSize": "14px", "marginTop": "10px"},
        ),
    ]

    ventes_hebdomadaires = (
        donnees_filtrees.groupby(["Week", "City"])["Total"]
        .sum()
        .reset_index()
        .sort_values("Week")
    )

    figure_ligne = px.line(
        ventes_hebdomadaires,
        x="Week",
        y="Total",
        color="City",
        markers=True,
        title="Évolution du montant total des achats par semaine et par ville",
        color_discrete_sequence=["#2e7d32", "#ffb300", "#1565c0"],
    )
    figure_ligne.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=20, t=65, b=40),
        xaxis_title="Semaine",
        yaxis_title="Montant total des achats",
        title_x=0.5,
        legend_title="Ville",
        font=dict(color=COULEUR_TITRE, size=14),
    )
    figure_ligne.update_traces(line=dict(width=4), marker=dict(size=9))
    figure_ligne.update_xaxes(tickformat="%d %b\n%Y", showgrid=True, gridcolor="#e8ecef")
    figure_ligne.update_yaxes(showgrid=True, gridcolor="#e8ecef")

    donnees_achats = (
        donnees_filtrees.groupby(["City", "Gender"])["Invoice ID"]
        .nunique()
        .reset_index(name="Nombre d'achats")
    )

    figure_barres = px.bar(
        donnees_achats,
        x="City",
        y="Nombre d'achats",
        color="Gender",
        barmode="group",
        text_auto=True,
        title="Nombre total d'achats par sexe et par ville",
        color_discrete_map={
            "Female": "#ec4899",
            "Male": "#3b82f6",
        },
    )
    figure_barres.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=30, r=20, t=65, b=30),
        title_x=0.5,
        legend_title="Sexe",
        font=dict(color=COULEUR_TITRE, size=14),
    )
    figure_barres.update_xaxes(showgrid=False)
    figure_barres.update_yaxes(showgrid=True, gridcolor="#e8ecef")

    donnees_categories = (
        donnees_filtrees.groupby("Product line")["Invoice ID"]
        .nunique()
        .reset_index(name="Nombre d'achats")
    )

    figure_camembert = px.pie(
        donnees_categories,
        names="Product line",
        values="Nombre d'achats",
        title="Répartition des catégories de produits",
        hole=0.4,
        color_discrete_sequence=[
            "#ef4444",
            "#f59e0b",
            "#10b981",
            "#3b82f6",
            "#8b5cf6",
            "#ec4899",
        ],
    )
    figure_camembert.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=65, b=20),
        title_x=0.5,
        legend_title="Catégorie",
        font=dict(color=COULEUR_TITRE, size=14),
    )

    return indicateur_total, indicateur_nombre, figure_ligne, figure_barres, figure_camembert

application = Dash(__name__)
server = application.server


