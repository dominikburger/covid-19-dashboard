import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from pathlib import Path
import pandas as pd
import src.visualization.dashboard_objects as dbo

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def generate_dataframe(path=None, days=None):
    dataframe = pd.DataFrame()

    for day in days:
        temp = pd.read_csv(path / f'{day}.csv')
        temp.loc[:, 'date'] = pd.to_datetime(day)
        dataframe = dataframe.append(temp)

    return dataframe


base_dir = Path().cwd()
processed_dir = base_dir / 'data' / 'processed' / 'daily_report'

days = pd.date_range('01/22/2020', '04/13/2020', normalize=True)
days = days.strftime('%m-%d-%Y')

df = generate_dataframe(path=processed_dir, days=days)

cl = ['Germany', 'France', 'Spain', 'Italy']

ts = dbo.TimeSeriesGraph(data=df, scale='linear', country_list=cl)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    id='main-window',
    style={'backgroundColor': '#232e4a'},
    children=[
        # set page header
        html.H4(children='COVID-19 Dashboard', style={'color': 'white'}),
        # 1st row place date picker
        html.Div(
            children=dbo.generate_date_picker(),
            style=dbo.date_picker_style
        ),
        # 2nd row place map and country table
        html.Div(
            id='second_div_row',
            className='row',
            style={'display': 'flex'},
            children=[
                html.Div(
                    id='cumulated_info',
                    children=[
                        html.Div(
                            id='caption_confirmed_cases_total',
                            children='Confirmed Cases Total',
                            style=dbo.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_cases_total',
                            children='123456',
                            style=dbo.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_deaths_total',
                            children='Deaths Total',
                            style=dbo.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_deaths_total',
                            children='123456',
                            style=dbo.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_recovered_total',
                            children='Recovered Total',
                            style=dbo.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_recovered_total',
                            children='123456',
                            style=dbo.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_active_total',
                            children='Active Total',
                            style=dbo.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_active_total',
                            children='123456',
                            style=dbo.value_case_style
                        )

                    ],
                    style=dbo.cumulated_info_style
                ),
                # place map graph
                html.Div(
                    dcc.Graph(
                        id='graph-map',
                        figure=dbo.generate_map(df)),
                    style=dbo.graph_map_style
                ),
                # place country table
                html.Div(
                    id='table-info-div',
                    children=dbo.generate_table(df),
                    style=dbo.table_style
                )
            ],
        ),
        # 3rd row place timeseries and country selector
        html.Div(
            id='third_div_row',
            className='row',
            style={'display': 'flex', 'marginTop': 10},
            children=[
                html.Div(
                    children=[
                        html.Div(
                            id='scale_selector',
                            children=dcc.RadioItems(
                                id='scale_radio',
                                options=[
                                    {'label': 'linear', 'value': 'linear'},
                                    {'label': 'logarithmic', 'value': 'log'},
                                ],
                                value='linear'
                            ),
                            style={'color': 'white', 'padding': 10}
                        ),
                        # place country selector
                        html.Div(
                            id='country_picker',
                            children=dbo.generate_country_picker(df),
                            style=dbo.country_picker_style
                        )
                    ],
                    style={'width': '20%'}
                ),
                # place timeseries
                html.Div(
                    children=dcc.Graph(
                        id='timeseries',
                        figure=ts.generate_timeseries(),
                        style=dbo.timeseries_style
                    ),
                )
            ],
        )
    ]
)


@app.callback(
    [
        Output('graph-map', 'figure'),
        Output('table-info-div', 'children'),
        Output('value_confirmed_cases_total', 'children'),
        Output('value_confirmed_deaths_total', 'children'),
        Output('value_confirmed_recovered_total', 'children'),
        Output('value_confirmed_active_total', 'children')
    ],
    [Input('date-picker', 'date')])
def update_output(date):
    map_graph = dbo.generate_map(df, date=pd.to_datetime(date))
    table_info = dbo.generate_table(df, date=pd.to_datetime(date))

    day_mask = df['date'] == pd.to_datetime(date)
    cases_total = df[day_mask]['confirmed'].sum()
    deaths_total = df[day_mask]['deaths'].sum()
    recovered_total = df[day_mask]['recovered'].sum()
    active_total = df[day_mask]['active'].sum()

    return (
        map_graph, table_info, cases_total,
        deaths_total, recovered_total, active_total
    )


@app.callback(
    [Output('timeseries', 'figure')],
    [
        Input('scale_radio', 'value'),
        Input('country_picker_dropdown', 'value')
    ])
def update_output(scale, country_list):
    print(scale)
    print(country_list)
    ts = dbo.TimeSeriesGraph(data=df, country_list=country_list, scale=scale)
    fig = ts.generate_timeseries()
    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)
