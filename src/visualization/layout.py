import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from pathlib import Path
import pandas as pd
import src.visualization.dashboard_objects as dbo
import dash_table
import src.visualization.styles as styles
from datetime import datetime as dt
from datetime import timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

max_date = dt.today().date() - timedelta(days=1)

def make_dataframe(path=None, days=None):
    dataframe = pd.DataFrame()

    for day in days:
        temp = pd.read_csv(path / f'{day}.csv')
        temp.loc[:, 'date'] = pd.to_datetime(day)
        dataframe = dataframe.append(temp)

    return dataframe


dir_base = Path().cwd()
dir_processed = dir_base / 'data' / 'processed' / 'daily_report'
dir_assets = Path().cwd() / 'src' / 'visualization' / 'assets'

days = pd.date_range('01/22/2020', max_date, normalize=True)
days = days.strftime('%m-%d-%Y')

df = make_dataframe(path=dir_processed, days=days)
ts = dbo.TimeSeriesGraph(data=df, scale='linear', country_list='')

app = dash.Dash(
    'Covid-19 Dashboard',
    external_stylesheets=external_stylesheets,
    assets_folder=dir_assets
)

app.layout = html.Div(
    id='main-window',
    style=styles.main_window_style,
    children=[
        # set page header
        html.H4(
            children='COVID-19 Dashboard',
            style={
                'color': '#f39c12',
                'padding': 10,
            }
        ),
        # 1st row place date picker
        html.Div(
            children=dbo.make_date_picker(),
            style=styles.date_picker_style
        ),
        # 2nd row place map and country table
        html.Div(
            id='second_div_row',
            className='row',
            style={'display': 'flex', 'width': '100%'},
            children=[
                html.Div(
                    id='cumulated_info',
                    className='card',
                    children=[
                        html.Div(
                            id='caption_confirmed_cases_total',
                            children='Confirmed Cases Total',
                            style=styles.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_cases_total',
                            children='123456',
                            style=styles.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_deaths_total',
                            children='Deaths Total',
                            style=styles.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_deaths_total',
                            children='123456',
                            style=styles.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_recovered_total',
                            children='Recovered Total',
                            style=styles.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_recovered_total',
                            children='123456',
                            style=styles.value_case_style
                        ),
                        html.Div(
                            id='caption_confirmed_active_total',
                            children='Active Total',
                            style=styles.caption_case_style
                        ),
                        html.P(
                            id='value_confirmed_active_total',
                            children='123456',
                            style=styles.value_case_style
                        )

                    ],
                    style=styles.cumulated_info_style
                ),
                html.Div(
                    id='main_graph_div',
                    style=styles.main_graph_div_style,
                    children=[
                        # place map graph
                        html.Div(
                            id='map_graph_div',
                            children=dcc.Graph(id='map_graph'),
                            style=styles.map_graph_style
                        ),
                        # place country table
                        html.Div(
                            id='table_info_div',
                            children=dash_table.DataTable(),
                            style=styles.table_info_style
                        )
                    ],
                )
            ]
        ),
        # 3rd row
        html.Div(
            id='third_div_row',
            className='col',
            style={'display': 'flex', 'width': '100%'},
            children=[
                # place toolbar
                html.Div(
                    id='toolbar',
                    style=styles.toolbar_style,
                    children=[
                        html.Div(
                            id='scale_selector_div',
                            children=dbo.make_scale(),
                            style=styles.scale_style
                        ),
                        # place country selector
                        html.Div(
                            id='country_checklist_div',
                            children=dbo.make_country_picker(df),
                            style=styles.country_picker_style
                        )
                    ]
                ),
                # info graphs
                html.Div(
                    id='info_graphs_div',
                    style=styles.info_graphs_style,
                    children=[
                        html.Div(
                            style=styles.timeseries_div_style,
                            children=dcc.Graph(
                                id='timeseries',
                                style={'width': '100%'},
                                figure=ts.make_timeseries(),
                            ),
                        ),
                        html.Div(
                            style=styles.tabs_div_style,
                            children=[
                                dcc.Tabs(
                                    id='tabs-example',
                                    value='tab_1',
                                    style=styles.tabs_styles,
                                    children=[
                                        dcc.Tab(
                                            label='',
                                            value='',
                                            style=styles.tab_style,
                                            selected_style=styles.tab_selected_style,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [Output('tabs-example', 'children'),
     Output('tabs-example', 'value')
     ],
    [Input('country_checklist', 'value')]
)
def update_output(country_list):
    tabs = []

    for idx, country in enumerate(country_list):
        fig = dbo.make_delta_graph(df, country)
        tabs.append(
            dcc.Tab(
                label=country,
                value=f'tab_{idx}',
                children=dcc.Graph(id=f'tab_{idx}_graph', figure=fig),
                style=styles.tab_style,
                selected_style=styles.tab_selected_style,
            )
        )

    return tabs, 'tab_0'


@app.callback(
    [
        Output('map_graph', 'figure'),
        Output('table_info_div', 'children'),
        Output('value_confirmed_cases_total', 'children'),
        Output('value_confirmed_deaths_total', 'children'),
        Output('value_confirmed_recovered_total', 'children'),
        Output('value_confirmed_active_total', 'children')
    ],
    [Input('date-picker', 'date')])
def update_output(date):
    map_graph = dbo.make_map(df, date=pd.to_datetime(date))
    table_info = dbo.make_table(df, date=pd.to_datetime(date))

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
        Input('country_checklist', 'value')
    ])
def update_output(scale, country_list):
    ts = dbo.TimeSeriesGraph(data=df, country_list=country_list, scale=scale)
    fig = ts.make_timeseries()
    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)
