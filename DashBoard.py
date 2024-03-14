# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3 as sql
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Read data into pandas dataframe
c = sql.connect("db.db")
df = pd.read_sql_query("SELECT * FROM df", c)
last_df = pd.read_sql_query("SELECT * FROM last_df", c)
first_df = pd.read_sql_query("SELECT * FROM first_df", c)
left_df = pd.read_sql_query("SELECT * FROM left_df", c)
late_df = pd.read_sql_query("SELECT * FROM late_df", c)
allTrajetory_df = pd.read_sql_query("SELECT * FROM allTrajetory_df", c)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "Pesquisa Evasão e Retensão",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        html.P(
            "Selecione uma base de dados:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 15},
        ),
        dcc.Dropdown(
            id="df_name",
            options=[
                {"label": "Total", "value": "df"},
                {"label": "Primeira Situação", "value": "first_df"},
                {"label": "Última Situação", "value": "last_df"},
                {"label": "Evadidos", "value": "left_df"},
                {"label": "Atrasados", "value": "late_df"},
                {"label": "Trajetória Completa", "value": "allTrajetory_df"},
            ],
            value="df",
            placeholder="Selecione uma base de dados",
            searchable=True,
        ),
        html.P(
            "Selecione uma estatística alvo:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 15},
        ),
        dcc.Dropdown(
            id="y",
            options=[
                {"label": "Coeficiente de rendimento", "value": "CR"},
                {"label": "Atraso", "value": "Atraso"},
                {"label": "Evadiu", "value": "Evadiu"},
                {"label": "Evadiu nesse semestre", "value": "Evadiu nesse semestre"},
                {"label": "Disciplinas aprov/matr", "value": "Disciplinas aprov/matr"},
                {
                    "label": "Disciplinas aprov/matr acumuladas",
                    "value": "Disciplinas aprov/matr acumuladas",
                },
            ],
            value="CR",
            placeholder="Selecione uma estatística alvo",
            searchable=True,
        ),
        html.P(
            "Selecione uma estátistica de comparação:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 15},
        ),
        dcc.Dropdown(
            id="x",
            options=[
                {"label": "Ano de ingresso", "value": "Ano de ingresso"},
                {"label": "Ano de nascimento", "value": "Ano de nascimento"},
                {"label": "Atraso", "value": "Atraso"},
                {"label": "Branco", "value": "Branco"},
                {"label": "Brasileiro", "value": "Brasileiro"},
                {"label": "Cotista", "value": "Cotista"},
                {"label": "Curitiba", "value": "Curitiba"},
                {"label": "Data", "value": "Data"},
                {
                    "label": "Disciplinas matriculadas",
                    "value": "Disciplinas matriculadas",
                },
                {
                    "label": "Disciplinas matriculadas acumuladas",
                    "value": "Disciplinas matriculadas acumuladas",
                },
                {"label": "Disciplinas aprovadas", "value": "Disciplinas aprovadas"},
                {
                    "label": "Disciplinas aprovadas acumuladas",
                    "value": "Disciplinas aprovadas acumuladas",
                },
                {"label": "Disciplinas aprov/matr", "value": "Disciplinas aprov/matr"},
                {
                    "label": "Disciplinas aprov/matr acumuladas",
                    "value": "Disciplinas aprov/matr acumuladas",
                },
                {"label": "Disciplinas reprovadas", "value": "Disciplinas reprovadas"},
                {
                    "label": "Disciplinas reprovadas acumuladas",
                    "value": "Disciplinas reprovadas acumuladas",
                },
                {
                    "label": "Disciplinas reprovadas por nota",
                    "value": "Disciplinas reprovadas por nota",
                },
                {
                    "label": "Disciplinas reprovadas por nota acumuladas",
                    "value": "Disciplinas reprovadas por nota acumuladas",
                },
                {
                    "label": "Disciplinas reprovadas por frequência",
                    "value": "Disciplinas reprovadas por frequência",
                },
                {
                    "label": "Disciplinas reprovadas por frequência acumuladas",
                    "value": "Disciplinas reprovadas por frequência acumuladas",
                },
                {
                    "label": "Disciplinas consignadas",
                    "value": "Disciplinas consignadas",
                },
                {
                    "label": "Disciplinas consignadas acumuladas",
                    "value": "Disciplinas consignadas acumuladas",
                },
                {"label": "Evadiu", "value": "Evadiu"},
                {"label": "Evadiu nesse semestre", "value": "Evadiu nesse semestre"},
                {"label": "Forma de ingresso", "value": "Forma de ingresso"},
                {"label": "Formou", "value": "Formou"},
                {"label": "Formou nesse semestre", "value": "Formou nesse semestre"},
                {"label": "Mulher", "value": "Mulher"},
                {"label": "Idade", "value": "Idade"},
                {"label": "Ingresso", "value": "Ingresso"},
                {"label": "Mudou de curso", "value": "Mudou de curso"},
                {"label": "Paraná", "value": "Paraná"},
                {"label": "Período", "value": "Período"},
                {"label": "Semestre de ingresso", "value": "Semestre de ingresso"},
                {"label": "Sisu", "value": "Sisu"},
                {"label": "Situação", "value": "Situação"},
                {"label": "UF SISU", "value": "UF SISU"},
            ],
            value="Ano de ingresso",
            placeholder="Selecione uma estátistica de comparação",
            searchable=True,
        ),
        html.H1(
            "Gráfico Principal",
            style={"textAlign": "center", "color": "#503D36", "font-size": 25},
        ),
        html.Div(dcc.Graph(id="chart")),
        html.P(
            "Selecione uma subdivisão:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 15},
        ),
        dcc.Dropdown(
            id="sub",
            options=[
                {"label": "Ano de ingresso", "value": "Ano de ingresso"},
                {"label": "Branco", "value": "Branco"},
                {"label": "Brasileiro", "value": "Brasileiro"},
                {"label": "Cotista", "value": "Cotista"},
                {"label": "Curitiba", "value": "Curitiba"},
                {
                    "label": "Disciplinas matriculadas",
                    "value": "Disciplinas matriculadas",
                },
                {"label": "Disciplinas aprovadas", "value": "Disciplinas aprovadas"},
                {"label": "Disciplinas reprovadas", "value": "Disciplinas reprovadas"},
                {
                    "label": "Disciplinas reprovadas por nota",
                    "value": "Disciplinas reprovadas por nota",
                },
                {
                    "label": "Disciplinas reprovadas por frequência",
                    "value": "Disciplinas reprovadas por frequência",
                },
                {
                    "label": "Disciplinas consignadas",
                    "value": "Disciplinas consignadas",
                },
                {"label": "Evadiu", "value": "Evadiu"},
                {"label": "Evadiu nesse semestre", "value": "Evadiu nesse semestre"},
                {"label": "Forma de ingresso", "value": "Forma de ingresso"},
                {"label": "Formou", "value": "Formou"},
                {"label": "Formou nesse semestre", "value": "Formou nesse semestre"},
                {"label": "Mulher", "value": "Mulher"},
                {"label": "Mudou de curso", "value": "Mudou de curso"},
                {"label": "Paraná", "value": "Paraná"},
                {"label": "Período", "value": "Período"},
                {"label": "Semestre de ingresso", "value": "Semestre de ingresso"},
                {"label": "Sisu", "value": "Sisu"},
                {"label": "Situação", "value": "Situação"},
            ],
            value="Branco",
            placeholder="Selecione uma subdivisão",
        ),
        html.H1(
            "Gráfico de proporções da subdivisão",
            style={"textAlign": "center", "color": "#503D36", "font-size": 25},
        ),
        html.Div(dcc.Graph(id="pie")),
        html.H1(
            "Gráfico de estatísticas para cada subdivisão",
            style={"textAlign": "center", "color": "#503D36", "font-size": 25},
        ),
        html.Div(dcc.Graph(id="sub_plot")),
        html.H1(
            "Gráfico de correlações entre  as variáveis",
            style={"textAlign": "center", "color": "#503D36", "font-size": 25},
        ),
        html.Div(dcc.Graph(id="corr")),
    ]
)


# Plot first Graph
@app.callback(
    Output(component_id="chart", component_property="figure"),
    [
        Input(component_id="df_name", component_property="value"),
        Input(component_id="y", component_property="value"),
        Input(component_id="x", component_property="value"),
    ],
)
def get_chart(df_name, y, x):
    selected_df = select_df(df_name)
    grouped_df = selected_df.groupby(x)[y].mean()
    f = px.bar(grouped_df, y=y)
    return f


# Pie
@app.callback(
    Output(component_id="pie", component_property="figure"),
    [
        Input(component_id="df_name", component_property="value"),
        Input(component_id="sub", component_property="value"),
    ],
)
def get_chart(df_name, sub):
    selected_df = select_df(df_name)
    f = px.pie(selected_df, names=sub)
    return f


# Subplots
@app.callback(
    Output(component_id="sub_plot", component_property="figure"),
    [
        Input(component_id="df_name", component_property="value"),
        Input(component_id="y", component_property="value"),
        Input(component_id="x", component_property="value"),
        Input(component_id="sub", component_property="value"),
    ],
)
def get_chart(df_name, y, x, sub):
    selected_df = select_df(df_name)
    values = selected_df[sub].unique()
    fig = make_subplots(
        rows=1, cols=values.size, shared_yaxes=True, y_title=y, x_title=x
    )
    i = 0
    for value in values:
        i += 1
        sub_df = selected_df[selected_df[sub] == value]
        grouped_df = sub_df.groupby(x)[y].mean()
        fig.add_trace(
            go.Bar(
                x=list(dict(grouped_df).keys()),
                y=list(dict(grouped_df).values()),
                name=str(value),
            ),
            row=1,
            col=i,
        )
    return fig


# Correlation
@app.callback(
    Output(component_id="corr", component_property="figure"),
    Input(component_id="df_name", component_property="value"),
)
def get_corr(df_name):
    selected_df = select_df(df_name)

    fig = go.Figure(
        data=go.Heatmap(
            z=selected_df.select_dtypes(include="number").corr(),
            x=selected_df.select_dtypes(include="number").corr().columns,
            y=selected_df.select_dtypes(include="number").corr().columns,
            colorscale="bluered",
        )
    )

    fig.update_layout(
        autosize=False,
        width=1500,
        height=1500,
    )
    return fig


def select_df(df_name):
    if df_name == "first_df":
        return first_df
    elif df_name == "last_df":
        return last_df
    elif df_name == "left_df":
        return left_df
    elif df_name == "late_df":
        return late_df
    elif df_name == "allTrajetory_df":
        return allTrajetory_df
    return df


# Run the app
if __name__ == "__main__":
    app.run_server()
