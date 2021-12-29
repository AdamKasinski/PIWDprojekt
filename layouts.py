import dash_core_components as dcc
import dash_html_components as html
import app
import os
import pandasql
import pandas as pd
from pandasql import sqldf
import plotly.express as px
import data
from dash.dependencies import Input, Output
from app import app

#---------------------------------------------------------------------menu_start---------------------------------------------------------------

layout_menu = html.Div(children = [
    html.H1(children='Menu'),

        html.Div(children='''
            Menu do stron
        '''),
        html.Div(id='app-menu-display-value'),
        dcc.Link('Go to plots1', href='/app1'),
        html.Div(id='app2-menu-display-value'),
        dcc.Link('Go to plots2', href='/app2'),
        html.Div(id='economy-menu-display-value'),
        dcc.Link('Go to economy plots', href='/economy'),
        html.Div(id='le-menu-display-value'),
        dcc.Link('Go to lifeExpectancy plots', href='/le'),
        html.Div(id='revenueLE-menu-display-value'),
        dcc.Link('Go to revenue-LifeExpectancvy plots', href='/revLE')
])

#---------------------------------------------------------------------menu_end---------------------------------------------------------------

#---------------------------------------------------------------------economy_start---------------------------------------------------------------

figEconomy1 = px.bar(data_frame=data.economy_sec[(data.economy_sec['Measure'] == '/capita, US$ purchasing power parity')], x= 'Country', y = 'Value',animation_frame='Year')
figEconomy2 = px.scatter(data_frame=data.economy_sec[data.economy_sec['Measure'] == '/capita, US$ exchange rate'], x='Country',y='Value',color='Continent',animation_frame='Year')
figEconomy3 = px.line(data_frame=data.dfa, x = 'year', y = 'val',color='cont')
figEconomy4 = px.bar(data_frame=data.dfa, x = 'year', y = 'val',color='cont')
figEconomy5 = px.violin(data_frame=data.dfa[data.dfa['cont'] != 'Africa'],x='cont',y='val')

layoutEconomy = html.Div(children=[
    html.Div([
        html.H1(children='Wykresy dotyczące PKB i rozwou'),

        html.Div(children='''
            PKB capita, US$
        '''),
        
        dcc.Graph(
            id='g1',
            figure=figEconomy1
        ),  

    ]),
    html.Div([
        html.Div(children='''
             PKB capita, US$ z zaznaczonymi kontynentami
        '''),

        dcc.Graph(
            id='g2',
            figure=figEconomy2
        ),  
    ]),
    html.Div([
        html.Div(children='''
            średnie PKB capita, US$ dla kontynentów
        '''),

        dcc.Graph(
            id='g3',
            figure=figEconomy3
        ),  
    ]),
    html.Div([
        html.Div(children='''
            średnie PKB capita, US$ dla kontynentów
        '''),

        dcc.Graph(
            id='g4',
            figure=figEconomy4
        ),  
    ]),
    html.Div([
        html.Div(children='''
            rozkład PKB capita z wszystkich okresów, US$ dla kontynentów 
        '''),

        dcc.Graph(
            id='g5',
            figure=figEconomy5
        ),  
    ]),
        html.Div(id='app1-display-value'),
        dcc.Link('Go to Menu', href='/')
])



#---------------------------------------------------------------------economy_end---------------------------------------------------------------

#---------------------------------------------------------------------le_start---------------------------------------------------------------

figle1 = px.histogram(data.females,x='Value',color='Variable')
figle2 = px.histogram(data.males,x='Value',color='Variable')
figle3 = px.choropleth(data.females[data.females['Variable'] == 'Females at birth'],               
              locations="COU",               
              color="Value",
              hover_name="Country",  
              animation_frame="Year",    
              color_continuous_scale='Plasma',  
              height=600             
)
figle4 = px.choropleth(data.males[data.males['Variable'] == 'Males at birth'],               
              locations="COU",               
              color="Value",
              hover_name="Country",  
              animation_frame="Year",    
              color_continuous_scale='Plasma',  
              height=600             
)

figle5 = px.histogram(data_frame=data.ttLe, x='Value',color='Variable')
figle6 = px.scatter(data_frame=data.dfe, x = 'year', y = 'val',color='var')

layoutLE = html.Div(children=[
    html.Div([
        html.H1(children='Wykresy dotyczące długości życia'),

        html.Div(children='''
            Rozkład oczekiwanej długości życia w zależności od wieku dla kobiet.
        '''),
        dcc.Graph(
            id='le1',
            figure=figle1
        ),  


    ]),
    # New Div for all elements in the new 'row' of the page 
    html.Div([
        html.Div(children='''
            Rozkład oczekiwanej długości życia w zależności od wieku dla mężczyzn.
        '''),

        dcc.Graph(
            id='le2',
            figure=figle2
        ),  
    ]),
    html.Div([
        html.Div(children='''
            Oczekiwana długość życia dla kobiet urodzonych w danym roku
        '''),
        dcc.Graph(
            id='le3',
            figure=figle3
        ),  


    ]),
    # New Div for all elements in the new 'row' of the page 
    html.Div([
        html.Div(children='''
            Oczekiwana długość życia dla mężczyzn urodzonych w danym roku
        '''),

        dcc.Graph(
            id='le4',
            figure=figle4
        ),  
    ]),
    html.Div([
        html.Div(children='''
            Rozkład oczekwianej długości życia dla poszczególnych grup wiekowych - dla wszystkich lat
        '''),
        
            html.Br(),

            dcc.Dropdown(
        id='test_dropdowLE',
        options=[
                    {'label': 'at birth', 'value':'birth'},
                    {'label': 'at age 40', 'value':'age 40'},
                    {'label': 'at age 60', 'value':'age 60'},
                    {'label': 'at age 65', 'value':'age 65'},
                    {'label': 'at age 80', 'value':'age 80'},

        ],

        placeholder='Select value',
        disabled=False,
        value= 'birth'
        ),

        dcc.Graph(
            id='le5',
            figure=figle5
            )
        ]),

    html.Div([
        html.Div(children='''
            Rozkład oczekwianej długości życia dla poszczególnych grup wiekowych - dla poszczególnych lat
        '''),
        
            html.Br(),

            dcc.Dropdown(
        id='test_dropdowLE2',
        options=[
                    {'label': 'at birth', 'value':'birth'},
                    {'label': 'at age 40', 'value':'age 40'},
                    {'label': 'at age 60', 'value':'age 60'},
                    {'label': 'at age 65', 'value':'age 65'},
                    {'label': 'at age 80', 'value':'age 80'},

        ],

        placeholder='Select value',
        disabled=False,
        value= 'birth'
        ),

        dcc.Graph(
            id='le6',
            figure=figle6
        ),  
    ]),
        html.Div(id='app1-display-value'),
        dcc.Link('Go to Menu', href='/')
])


#ttLe = lifeExpectancy_sec[(lifeExpectancy_sec['Measure'] == 'Years') & ((lifeExpectancy_sec['Variable'] == 'Females at birth') | (lifeExpectancy_sec['Variable'] == 'Males at birth'))]


#---------------------------------------------------------------------le_end---------------------------------------------------------------

#---------------------------------------------------------------------page1_start---------------------------------------------------------------

fig = px.scatter(
    data.d,
    x='Val_Economy',
    y="LifeExpentancy",
    color="Country",
    log_x=True,
    size_max=60,
    animation_frame='Year'
)

fig2 = px.choropleth(data.d,               
              locations="COU",               
              color="LifeExpentancy",
              hover_name="Country",  
              animation_frame="Year",    
              color_continuous_scale='Plasma',  
              height=600             
)

layout = html.Div(children=[
    html.Div([
        html.H1(children='Wykresy dotyczące oczekiwanej długości życia i PKB'),

        html.Div(children='''
            LifeExpentancy ~ 'Purchasing Power Parities for GDP, US$'.
        '''),
        
            html.Br(),

            dcc.Dropdown(
        id='test_dropdow1',
        options=[
                    {'label': 'Females at birth', 'value': 'Females at birth'},
                    {'label': 'Males at birth', 'value': 'Males at birth'},
                    {'label': 'Females at age 40', 'value': 'Females at age 40'},
                    {'label': 'Females at age 60', 'value': 'Females at age 60'},
                    {'label': 'Females at age 65', 'value': 'Females at age 65'},
                    {'label': 'Males at age 40', 'value': 'Males at age 40'},
                    {'label': 'Males at age 60', 'value': 'Males at age 60'},
                    {'label': 'Males at age 65', 'value': 'Males at age 65'},
                    {'label': 'Males at age 80', 'value': 'Males at age 80'},
                    {'label': 'Females at age 80', 'value': 'Females at age 80'},
        ],

        placeholder='Select value',
        disabled=False,
        value='Females at age 40'
        ),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),  


    ]),
    # New Div for all elements in the new 'row' of the page 
    html.Div([
        html.Div(children='''
            Life Expentancy
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
        html.Div(id='app1-display-value'),
        dcc.Link('Go to Menu', href='/')
])

#---------------------------------------------------------------------page1_end---------------------------------------------------------------

#---------------------------------------------------------------------revenueLE_start---------------------------------------------------------------

figRevenueLE1 = px.scatter(data.revenueLE2, x="rev_unit", y="le_value", animation_frame="Year", animation_group="Country", color="Country", hover_name="Country", facet_col="Continent",
           size_max=45, log_x=True)

layoutRevenueLE = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Wykres dotyczący przewidywanej długości życia dla osób urodzonych w danym roku a całkowitymi przychodami z podatków'),

        html.Div(children='''
            LifeExpentancy ~ total_tax_revenue.
        '''),

        dcc.Graph(
            id='graph1',
            figure=figRevenueLE1
        ),  

        html.Div(id='revenueLE-display-value'),
        dcc.Link('Go to Menu', href='/')
    ])
])

#---------------------------------------------------------------------page2_start---------------------------------------------------------------

figttr2 = px.line(
    data.ttrEuro,
    x = 'Year',
    y = 'Value',
    color = 'Country'
)

figttr3 = px.choropleth(data.ttrAll,               
              locations="COU",               
              color="Value",
              hover_name="Country",  
              animation_frame="Year",    
              color_continuous_scale='Plasma',  
              height=600             
)

figttr4 = px.scatter(
    data.ttrNotEuro,
    x = 'Year',
    y = 'Value',
    color = 'Unit',
    size = 'Value'
)


layout2 = html.Div(children=[

    html.Div([
        html.Div(children='''
            Przychód z podatków dla państw w strefie Euro
        '''),

        dcc.Graph(
            id='graph2',
            figure=figttr2
        ),  
    ]),

    html.Div([
        html.Div(children='''
            Przychód z podatków dla państw niezależnie od waluty
        '''),

        dcc.Graph(
            id='graph3',
            figure=figttr3
        ),  
    ]),

    html.Div([
        html.Div(children='''
            Przychód z podatków dla państw spoza strefy Euro
        '''),

        dcc.Graph(
            id='graph4',
            figure=figttr4
        ),  
    ]),
        html.Div(id='app2-display-value'),
        dcc.Link('Go to Menu', href='/')
])


@app.callback(
Output('graph1', 'figure'),
Input('test_dropdow1', 'value')
)
def change_value(selected_value):
    k = selected_value

    updated_fig = px.scatter(
        data.a[data.a['Variable'] == k][['Country','Val_Economy','Variable','LifeExpentancy','Year','COU']],
        x="Val_Economy",
        y="LifeExpentancy",
        color="Country",
        log_x=True,
        size_max=60,
        animation_frame='Year',
    )
    return updated_fig

@app.callback(
    Output('le5','figure'),
    Input('test_dropdowLE','value')
)
def set_variable(selected_value):
    data.kLe = selected_value
    ttLe = data.lifeExpectancy_sec[(data.lifeExpectancy_sec['Measure'] == 'Years') & ((data.lifeExpectancy_sec['Variable'] == f'Females at {data.kLe}') | (data.lifeExpectancy_sec['Variable'] == f'Males at {data.kLe}'))]
    fig5 = px.histogram(data_frame=ttLe, x='Value',color='Variable')

    return fig5

@app.callback(
    Output('le6','figure'),
    Input('test_dropdowLE2','value')
)
def set_variable2(selected_value):
    kle2 = selected_value
    dfe = data.df[(data.df['var'] == f'Females at {kle2}') | (data.df['var'] == f'Males at {kle2}')]
    fig6 = px.scatter(data_frame=dfe, x='year',y = 'val',color='var')

    return fig6