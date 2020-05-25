import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly
import IndianMapCoordinates

import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px

from scipy.interpolate import interp1d

app = dash.Dash(__name__)
# category_colors = {''}

# loading the dataset
death_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
# print(f'Country: {country_df.shape}')
# print(f'Recovered: {recovered_df.shape}')
# print(f'confirmed: {confirmed_df.shape}')

# Pre processing the data
death_df.drop('Province/State', axis=1, inplace=True)
confirmed_df.drop('Province/State', axis=1, inplace=True)
recovered_df.drop('Province/State', axis=1, inplace=True)
country_df.drop(['People_Tested', 'People_Hospitalized'], axis=1, inplace=True)

# change columns name
death_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
confirmed_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
recovered_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
country_df.rename(columns={'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)

# sorting country_df with highest confirm case
country_df.sort_values('Confirmed', ascending=False, inplace=True)


# plotting world map
# fixing the size of circle
margin = country_df['Confirmed'].values.tolist()
circle_range = interp1d([1, max(margin)], [0.2, 12])
circle_radius = circle_range(margin)

# navbar
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.A("The Covid Info Store", href="/static/covidinfo.html", style={'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Daily Data", href="#nav-daily-graph", style={'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Most Affected", href="#nav-top-country-graph", style={'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Comparison", href="#nav-cr-link", style={'color': '#fff'}), className="mr-5"),
    ],
    brand="COVID-19",
    brand_href="/",
    color="#001011",
    dark=True,
    className="p-3 fixed-top"
)

# main heading
main_heading = dbc.Container(
    [
        html.H1(["COVID-19 Pandemic Analysis Dashboard"], className="my-5 pt-5 text-center"),
    ]
    , className='pt-3')

# what is covid-19
what_is_covid = dbc.Container(
    [
        html.Div([
            html.H3('What is COVID-19?'),
            html.P(
                "A coronavirus is a kind of common virus that causes an infection in your nose, sinuses, or upper "
                "throat. Most coronaviruses aren't dangerous."),
            html.P(
                "COVID-19 is a disease that can cause what doctors call a respiratory tract infection. It can affect "
                "your upper respiratory tract (sinuses, nose, and throat) or lower respiratory tract (windpipe and "
                "lungs). It's caused by a coronavirus named SARS-CoV-2."),
            html.P(
                "It spreads the same way other coronaviruses do, mainly through person-to-person contact. Infections "
                "range from mild to serious."),
            html.Span('More information '),
            dcc.Link(' here', href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019')
        ])
    ]
    , className="mb-5")

# select, country, no of days and category
# dropdown slider
world_tally = dbc.Container(
    [
        html.H2('World Data', style={'text-align': 'center'}),

        dbc.Row(
            [
                dbc.Col(children=[html.H4('Confirmed'),
                                  html.Div(country_df['Confirmed'].sum(), className='text-info',
                                           style={'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2',
                        style={'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),

                dbc.Col(children=[html.H4('Recovered', style={'padding-top': '0px'}),
                                  html.Div(country_df['Recovered'].sum(), className='text-success',
                                           style={'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),

                dbc.Col(children=[html.H4('Death', style={'padding-top': '0px'}),
                                  html.Div(country_df['Deaths'].sum(), className='text-danger',
                                            style={'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),

                dbc.Col(children=[html.H4('Active'),
                                  html.Div(country_df['Active'].sum(), className='text-warning',
                                           style={'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light p-2',
                        style={'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
            , className='my-4 shadow justify-content-center'),

    ]
)

token = 'pk.eyJ1IjoicmF1bml0LXgiLCJhIjoiY2thajN6Y2ZkMDZ4ajJzdGR2MGhyb3lzZiJ9.DFPDbhbYg2sEzQFHLCdPpw'
# global map heading
global_map_heading = html.H2(children='World map view', className='mt-5 py-4 pb-3 text-center')

# plotting the global map
map_fig = px.scatter_mapbox(country_df, lat="Lat", lon="Long", hover_name="Country",
                            hover_data=["Confirmed", "Deaths", "Active"],
                            color_discrete_sequence=["#e60039"], zoom=1.25, height=500, size_max=50,
                            size=circle_radius,
                            color_continuous_scale=px.colors.sequential.Viridis, color="Confirmed")

map_fig.update_layout(mapbox_style="dark", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=520,
                      mapbox_accesstoken=token)

# daily data heading
daily_graph_heading = html.H2(id='nav-daily-graph', children='COVID-19 Daily Data and Total Cases ',
                              className='mt-5 pb-3 text-center')

# dropdown to select the country, category and number of days
daily_country = confirmed_df['Country'].unique().tolist()
daily_country_list = []

my_df_type = ['Confirmed cases', 'Death rate', 'Recovered cases']
my_df_type_list = []

for i in daily_country:
    daily_country_list.append({'label': i, 'value': i})

for i in my_df_type:
    my_df_type_list.append({'label': i, 'value': i})

# dropdown to select country
country_dropdown = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children=[html.Label('Select Country'),
                                  html.Div(
                                      dcc.Dropdown(id='select-country', options=daily_country_list, value='India'))],
                        width=3, className='p-2 mr-5'),

                dbc.Col(children=[html.Label('Drage to choose no of Days', style={'padding-top': '0px'}),
                                  html.Div(dcc.Slider(id='select-date',
                                                      min=10,
                                                      max=len(death_df.columns[3:]),
                                                      step=1,
                                                      value=40
                                                      , className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-5'),

                dbc.Col(children=[html.Label('Select category', style={'padding-top': '0px'}),
                                  html.Div(dcc.Dropdown(id='select-category', options=my_df_type_list,
                                                        value='Confirmed cases'))],
                        width=3, className='p-2 ml-5'),
            ]
            , className='my-4 justify-content-center'),

    ]
)


# create graph for daily report
def daily_graph_gen(new_df, category):
    daily_data = []
    daily_data.append(go.Scatter(
        x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')))

    layout = {
        'title': 'Daily ' + category + ' in ' + new_df['Country'].values[0],
        'title_font_size': 26,
        'height': 450,
        'xaxis': dict(
            title='Date',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )),
        'yaxis': dict(
            title='Covid-19 cases',
            titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
    }

    figure = [{
        'data': daily_data,
        'layout': layout
    }]

    return figure


# Top Affected countries with COVID-19
top_country_heading = html.H2(id='nav-top-country-graph', children='Top Most Affected Countries with COVID-19',
                              className='mt-5 pb-3 text-center')

# dropdown to select no of country
no_of_country = []

top_category = country_df.loc[0:, ['Confirmed', 'Active', 'Deaths', 'Recovered', 'Mortality_Rate']].columns.tolist()
top_category_list = []

for i in range(1, 180):
    no_of_country.append({'label': i, 'value': i})

for i in top_category:
    top_category_list.append({'label': i, 'value': i})

# country dropdown object
top_10_country = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children=[html.Label('Select no of Country'),
                                  html.Div(dcc.Dropdown(id='no-of-country', options=no_of_country, value=10))],
                        width=3, className='p-2 mr-5'),

                dbc.Col(children=[html.Label('Select category', style={'padding-top': '0px'}),
                                  html.Div(
                                      dcc.Dropdown(id='top-category', options=top_category_list, value='Confirmed'))],
                        width=3, className='p-2 ml-5'),
            ]
            , className='my-4 justify-content-center'),

    ]
)

# heading
cr_heading = html.H2(id='nav-cr-link', children='Confirmed and Recovered case', className='mt-5 pb-3 text-center')

# confirm and recovered cases
top_country = country_df.head(10)
top_country_name = list(top_country['Country'].values)

cr = go.Figure(data=[
    go.Bar(name='Confirmed', marker_color='#f36', x=top_country_name, y=list(top_country['Confirmed'])),
    go.Bar(name='Recovered', marker_color='#1abc9c', x=top_country_name, y=list(top_country['Recovered'])),
])

# Change the bar mode
cr.update_layout(barmode='group', height=600, title_text="Top 10 countries with Confirmed and Recovered case")


# Conclusion
end = html.Div(children=[
    html.H3('Sources:'),
    html.Div([html.Span('1. The data is taken from '),
              dcc.Link('Johns Hopkins University', href='https://github.com/CSSEGISandData/COVID-19')]),
    html.Div([html.Span('2. Built this Dashboard using '),
              dcc.Link('Dash by Plotly!', href='https://github.com/CSSEGISandData/COVID-19')]),
    html.H5('Note: Will be updating this Dashboard with more features and better visualization.',
            style={'margin-top': '20px', 'margin-bottom': '140px'})
])

# india_df = IndianMapCoordinates.get_indian_map_details()
# print(india_df)
# indian_map_heading = html.H2(children='Indian map view', className='mt-5 py-4 pb-3 text-center')
# print("here!")
# india_map_fig = px.scatter_mapbox(india_df, lat="Lat", lon="Long", hover_name="State",
#                                   hover_data=["Confirmed", "Deaths"],
#                                   color_discrete_sequence=["#e60039"], zoom=10, height=500, size_max=50,
#                                   size=circle_radius,
#                                   color_continuous_scale=px.colors.cyclical.IceFire, color="Confirmed")
#
# india_map_fig.update_layout(mapbox_style="dark", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=520,
#                       mapbox_accesstoken=token)

# main layout for Dash
app.layout = html.Div(
    [navbar,
     main_heading,
     what_is_covid,
     world_tally,

     # global map
     html.Div(children=[global_map_heading,
                        dcc.Graph(
                            id='global_graph',
                            figure=map_fig
                        )
                        ]
              ),

     dbc.Container([daily_graph_heading,
                    country_dropdown,
                    html.Div(id='country-total'),
                    dcc.Graph(
                        id='daily-graphs'
                    )
                    ]
                   ),

     # top countries
     dbc.Container([top_country_heading,
                    top_10_country,
                    dcc.Graph(
                        id='top-country-graph'
                    )
                    ]
                   ),

     # confirmed and recovered cases
     dbc.Container(children=[cr_heading,
                             dcc.Graph(
                                 id='cr',
                                 figure=cr
                             )
                             ]
                   ),
     dbc.Container(
         end
     )
     ]
)

# start the server

server = app.server


# call back function to make change on click
@app.callback(
    [Output('daily-graphs', 'figure')],
    [Input('select-country', 'value'),
     Input('select-category', 'value'),
     Input('select-date', 'value')]
)
def country_wise(country_name, df_type, number):
    # on select of category copy the dataframe to group by country
    if df_type == 'Confirmed cases':
        df_type = confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'

    elif df_type == 'Death rate':
        df_type = death_df.copy(deep=True)
        category = 'COVID-19 Death rate'

    else:
        df_type = recovered_df.copy(deep=True)
        category = 'COVID-19 recovered cases'

    # group by country name
    country = df_type.groupby('Country')

    # select the given country
    country = country.get_group(country_name)

    # store daily death rate along with the date
    daily_cases = []
    case_date = []

    # iterate over each row
    for i, cols in enumerate(country):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(country[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)

            # creata a data frame
            new_df = pd.DataFrame(data=zip_all_list, columns=['Date', 'coronavirus'])

    # append the country to the data frame
    new_df['Country'] = country['Country'].values[0]

    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) - 1):
        new_df.iloc[i + 1, 1] = new_df.iloc[1 + i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i + 1, 1] < 0:
            new_df.iloc[i + 1, 1] = 0

    new_df = new_df.iloc[-number:]

    return daily_graph_gen(new_df, category)


# show total data for each country
@app.callback(
    [Output('country-total', 'children')],
    [Input('select-country', 'value')]
)
def total_of_country(country):
    my_country = country_df[country_df['Country'] == country].loc[:, ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    country_total = dbc.Container(
        [
            html.H4(f'Total cases in {country}'),
            dbc.Row(
                [
                    dbc.Col(children=[html.H6('Confirmed'),
                                      html.Div(my_country['Confirmed'].sum(), className='text-info',
                                               style={'font-size': '28px', 'font-weight': '700'})],
                            width=3, className='text-center bg-light border-right pt-2',
                            style={'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),

                    dbc.Col(children=[html.H6('Recovered', style={'padding-top': '0px'}),
                                      html.Div(my_country['Recovered'].sum(), className='text-success',
                                               style={'font-size': '28px', 'font-weight': '700'})],
                            width=3, className='text-center bg-light border-right pt-2'),

                    dbc.Col(children=[html.H6('Death', style={'padding-top': '0px'}),
                                      html.Div(my_country['Deaths'].sum(), className='text-danger',
                                               style={'font-size': '28px', 'font-weight': '700'})],
                            width=3, className='text-center bg-light border-right pt-2'),

                    dbc.Col(children=[html.H6('Active'),
                                      html.Div(my_country['Active'].sum(), className='text-warning',
                                               style={'font-size': '28px', 'font-weight': '700'})],
                            width=3, className='text-center bg-light pt-2',
                            style={'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
                ]
                , className='mt-1 justify-content-center'),

        ]
    )
    return [country_total]


# Callback to show cases for top most affected countries
@app.callback(
    [Output('top-country-graph', 'figure')],
    [Input('no-of-country', 'value'),
     Input('top-category', 'value')]
)
def top_ten(number, sort_by):
    # sorting the columns with top death rate
    country_df2 = country_df.sort_values(by=sort_by, ascending=False)

    # sort country with highest number of cases
    country_df2 = country_df2.head(number)

    top_country_data = [go.Bar(x=country_df2['Country'], y=country_df2[sort_by])]

    layout = {
        'title': 'Top ' + str(number) + ' Country - ' + sort_by + ' case',
        'title_font_size': 26,
        'height': 500,
        'xaxis': dict(title='Countries'),
        'yaxis': dict(title=sort_by)
    }

    figure = [{
        'data': top_country_data,
        'layout': layout
    }]

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
