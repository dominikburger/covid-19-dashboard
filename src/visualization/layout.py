import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from pathlib import Path
import pandas as pd
import src.visualization.dashboard_objects as dbo

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def generate_dataframe():
    dataframe = pd.DataFrame()

    for day in days:
        temp = pd.read_csv(processed_dir / f'{day}.csv')
        temp.loc[:, 'date'] = pd.to_datetime(day)
        dataframe = dataframe.append(temp)

    return dataframe


base_dir = Path().cwd()
processed_dir = base_dir / 'data' / 'processed' / 'daily_report'

days = pd.date_range('01/22/2020', '04/13/2020', normalize=True)
days = days.strftime('%m-%d-%Y')

df = generate_dataframe()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    id='main-window',
    style={'backgroundColor': '#232e4a'},
    children=[
        # set page header
        html.H4(children='COVID-Dashboard'),
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
                            style=dbo.caption_confirmed_style
                        ),
                        html.P(
                            id='value_confirmed_cases_total',
                            children='123456',
                            style=dbo.value_confirmed_style
                        ),
                        html.Div(
                            id='caption_confirmed_deaths_total',
                            children='Confirmed Deaths Total',
                            style=dbo.caption_confirmed_style
                        ),
                        html.P(
                            id='value_confirmed_deaths_total',
                            children='123456',
                            style=dbo.value_confirmed_style
                        ),
                        html.Div(
                            id='caption_confirmed_recovered_total',
                            children='Confirmed Recovered Total',
                            style=dbo.caption_confirmed_style
                        ),
                        html.P(
                            id='value_confirmed_recovered_total',
                            children='123456',
                            style=dbo.value_confirmed_style
                        ),
                        html.Div(
                            id='caption_confirmed_active_total',
                            children='Confirmed Active Total',
                            style=dbo.caption_confirmed_style
                        ),
                        html.P(
                            id='value_confirmed_active_total',
                            children='123456',
                            style=dbo.value_confirmed_style
                        )

                    ],
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
            style={'display': 'flex'},
            children=[
                # place timeseries
                html.Div(
                    children=dcc.Graph(
                        id='timeseries',
                        figure=dbo.generate_ccd(df)),
                    style=dbo.timeseries_style
                ),

                # place country selector
                html.Div(
                    children=dbo.generate_country_picker(df),
                    style=dbo.country_picker_style
                ),
            ],
        )
    ])


@app.callback(

    [Output('graph-map', 'figure'),

     Output('table-info-div', 'children')],
    [Input('date-picker', 'date')])
def update_output(date):
    map_graph = dbo.generate_map(df, date=pd.to_datetime(date))
    table_info = dbo.generate_table(df, date=pd.to_datetime(date))

    return map_graph, table_info


if __name__ == '__main__':
    app.run_server(debug=True)
