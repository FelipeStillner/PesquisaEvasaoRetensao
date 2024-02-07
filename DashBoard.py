# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3 as sql
import numpy as np
import seaborn as sns
import plotly.graph_objects as go

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
app.layout = html.Div(children=[html.H1('Pesquisa Evasão e Retensão',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='dropdownDataframe',
                                    options=[
                                        {'label': 'Total', 'value': 'df'},
                                        {'label': 'Primeira Situação', 'value': 'first_df'},
                                        {'label': 'Última Situação', 'value': 'last_df'},
                                        {'label': 'Evadidos', 'value': 'left_df'},
                                        {'label': 'Atrasados', 'value': 'late_df'},
                                        {'label': 'Trajetória Completa', 'value': 'allTrajetory_df'},
                                    ],
                                    value='df',
                                    placeholder="Select the Dataframe",
                                    searchable=True
                                    ),
                                html.Br(),

                                dcc.Dropdown(id='dropdownStatistics',
                                    options=[
                                        {'label': 'Coeficiente de rendimento', 'value': 'CR'},
                                        {'label': 'Atraso', 'value': 'Atraso'},
                                        {'label': 'Evadiu', 'value': 'Evadiu'},
                                        {'label': 'Disciplinas aprov/matr', 'value': 'Disciplinas aprov/matr'},
                                        {'label': 'Disciplinas aprov/matr acumuladas', 'value': 'Disciplinas aprov/matr acumuladas'},
                                    ],
                                    value='CR',
                                    placeholder="Select a Statistics",
                                    searchable=True
                                    ),
                                html.Br(),

                                dcc.Dropdown(id='dropdown2',
                                    options=[
                                        {'label': 'Ano de ingresso', 'value': 'Ano de ingresso'},
                                        {'label': 'Ano de nascimento', 'value': 'Ano de nascimento'},
                                        {'label': 'Atraso', 'value': 'Atraso'},
                                        {'label': 'Branco', 'value': 'Branco'},
                                        {'label': 'Brasileiro', 'value': 'Brasileiro'},
                                        {'label': 'Cotista', 'value': 'Cotista'},
                                        {'label': 'CR', 'value': 'CR'},
                                        {'label': 'Curitiba', 'value': 'Curitiba'},
                                        {'label': 'Data', 'value': 'Data'},
                                        {'label': 'Disciplinas matriculadas', 'value': 'Disciplinas matriculadas'},
                                        {'label': 'Disciplinas matriculadas acumuladas', 'value': 'Disciplinas matriculadas acumuladas'},
                                        {'label': 'Disciplinas aprovadas', 'value': 'Disciplinas aprovadas'},
                                        {'label': 'Disciplinas aprovadas acumuladas', 'value': 'Disciplinas aprovadas acumuladas'},
                                        {'label': 'Disciplinas aprov/matr', 'value': 'Disciplinas aprov/matr'},
                                        {'label': 'Disciplinas aprov/matr acumuladas', 'value': 'Disciplinas aprov/matr acumuladas'},
                                        {'label': 'Disciplinas reprovadas', 'value': 'Disciplinas reprovadas'},
                                        {'label': 'Disciplinas reprovadas acumuladas', 'value': 'Disciplinas reprovadas acumuladas'},
                                        {'label': 'Disciplinas reprovadas por nota', 'value': 'Disciplinas reprovadas por nota'},
                                        {'label': 'Disciplinas reprovadas por nota acumuladas', 'value': 'Disciplinas reprovadas por nota acumuladas'},
                                        {'label': 'Disciplinas reprovadas por frequência', 'value': 'Disciplinas reprovadas por frequência'},
                                        {'label': 'Disciplinas reprovadas por frequência acumuladas', 'value': 'Disciplinas reprovadas por frequência acumuladas'},
                                        {'label': 'Disciplinas consignadas', 'value': 'Disciplinas consignadas'},
                                        {'label': 'Disciplinas consignadas acumuladas', 'value': 'Disciplinas consignadas acumuladas'},
                                        {'label': 'Evadiu', 'value': 'Evadiu'},
                                        {'label': 'Forma de ingresso', 'value': 'Forma de ingresso'},
                                        {'label': 'Formou', 'value': 'Formou'},
                                        {'label': 'Mulher', 'value': 'Mulher'},
                                        {'label': 'Idade', 'value': 'Idade'},
                                        {'label': 'Ingresso', 'value': 'Ingresso'},
                                        {'label': 'Mudou de curso', 'value': 'Mudou de curso'},
                                        {'label': 'Paraná', 'value': 'Paraná'},
                                        {'label': 'Período', 'value': 'Período'},
                                        {'label': 'Semestre de ingresso', 'value': 'Semestre de ingresso'},
                                        {'label': 'Sisu', 'value': 'Sisu'},
                                        {'label': 'Situação', 'value': 'Situação'},
                                        {'label': 'UF SISU', 'value': 'UF SISU'},
                                    ],
                                    value='Ano de ingresso',
                                    placeholder="Select a value",
                                    searchable=True
                                    ),
                                html.Br(),

                                html.Div(dcc.Graph(id='chart')),
                                html.Br(),

                                html.Div(dcc.Graph(id='corr')),
                                ])

@app.callback(Output(component_id='chart', component_property='figure'),
              [Input(component_id='dropdownDataframe', component_property='value'), Input(component_id='dropdownStatistics', component_property='value'), Input(component_id='dropdown2', component_property='value')])
def get_chart(dataframe, statistics, st2):
    if dataframe == "first_df":
        new_df = first_df
    elif dataframe == "last_df":
        new_df = last_df
    elif dataframe == "left_df":
        new_df = left_df
    elif dataframe == "late_df":
        new_df = late_df
    elif dataframe == "allTrajetory_df":
        new_df = allTrajetory_df
    else:
        new_df = df

    if new_df[st2].dtype == object:
        tmp_df = new_df.groupby(st2)[statistics].mean()
        f = px.bar(tmp_df, y=statistics)
    else:
        if new_df[st2].unique().shape[0] < 4:
            tmp_df = new_df.groupby(st2)[statistics].mean()
            f = px.bar(tmp_df, y=statistics)
        else:
            tmp_df = new_df.groupby(st2)[statistics].mean()
            f = px.line(tmp_df, y=statistics)
    return f

@app.callback(Output(component_id='corr', component_property='figure'),
              Input(component_id='dropdownDataframe', component_property='value'))
def get_corr(dataframe):
    if dataframe == "first_df":
        new_df = first_df
    elif dataframe == "last_df":
        new_df = last_df
    elif dataframe == "left_df":
        new_df = left_df
    elif dataframe == "late_df":
        new_df = late_df
    elif dataframe == "allTrajetory_df":
        new_df = allTrajetory_df
    else:
        new_df = df

    fig = go.Figure(data=go.Heatmap(
        z= new_df.corr(),
        x= new_df.corr().columns,
        y= new_df.corr().columns,
        colorscale="jet"))

    fig.update_layout(
    autosize=False,
    width=1500,
    height=1500,
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
