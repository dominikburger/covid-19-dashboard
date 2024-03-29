import pandas as pd
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input
from dash.dependencies import Output
import src.visualization.dashboard_objects as dbo
import src.visualization.styles as styles
import src.paths as paths
import src.utils as utils


utils.parse_covid_data()
utils.parse_geo_reference()

min_day, max_day = utils.get_day_range()
days = pd.date_range(min_day, max_day, normalize=True)
days = days.strftime('%m-%d-%Y')
df = utils.make_dataframe(path=paths.dir_processed_daily, days=days)

ts = dbo.TimeSeriesGraph(data=df, scale='linear', country_list='')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

layout = html.Div(
    id='main-window',
    style=styles.main_window_style,
    children=[
        # set page header
        html.Nav(className="nav-bar",
                 style=styles.nav_bar_style,
                 children=[
                     html.H4(
                         children='COVID-19 Dashboard',
                         style=styles.header_style
                     ),
                     # 1st row place date picker
                     html.Div(
                         children=dbo.make_date_picker(),
                         style=styles.date_picker_style
                     ),
                 ]
        ),
        # 1st row place map and country table
        html.Div(
            id='first_row_div',
            style=styles.second_row_div_style,
            children=[
                html.Div(
                    id='cumulated_info',
                    style=styles.cumulated_info_style,
                    children=[
                        html.Div(
                            id='div_confirmed_cases_total',
                            style=styles.div_case_style,
                            children=[
                                html.P(
                                    id='caption_confirmed_cases_total',
                                    children='Confirmed Cases Total',
                                    style=styles.caption_case_style
                                ),
                                html.P(
                                    id='value_confirmed_cases_total',
                                    children='',
                                    style=styles.value_case_style
                                ),
                            ]
                        ),
                        html.Div(
                            id='div_confirmed_deaths_total',
                            style=styles.div_case_style,
                            children=[
                                html.P(
                                    id='caption_confirmed_deaths_total',
                                    children='Deaths Total',
                                    style=styles.caption_case_style
                                ),
                                html.P(
                                    id='value_confirmed_deaths_total',
                                    children='',
                                    style=styles.value_case_style
                                ),
                            ]
                        ),
                        html.Div(
                            id='div_confirmed_recovered_total',
                            style=styles.div_case_style,
                            children=[
                                html.P(
                                    id='caption_confirmed_recovered_total',
                                    children='Recovered Total',
                                    style=styles.caption_case_style
                                ),
                                html.P(
                                    id='value_confirmed_recovered_total',
                                    children='',
                                    style=styles.value_case_style
                                ),
                            ]
                        ),
                        html.Div(
                            id='div_confirmed_active_total',
                            style=styles.div_case_style,
                            children=[
                                html.P(
                                    id='caption_confirmed_active_total',
                                    children='Active Total',
                                    style=styles.caption_case_style
                                ),
                                html.P(
                                    id='value_confirmed_active_total',
                                    children='',
                                    style=styles.value_case_style
                                ),
                            ]
                        ),
                    ],
                ),
                # place map graph
                html.Div(
                    id='map_graph_div',
                    style=styles.map_graph_div_style,
                    children=dcc.Graph(
                        id='map_graph',
                        style=styles.map_graph_style,
                        config={'responsive': True},
                    ),

                ),
                # place country table
                html.Div(
                    id='table_info_div',
                    children=dash_table.DataTable(),
                    style=styles.table_info_style
                )
            ]
        ),
        # second row place timeseries and datediff table
        html.Div(
            id='second_row_div',
            className='col',
            style=styles.second_row_div_style,
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
                # place timeseries graph
                html.Div(
                    style=styles.timeseries_div_style,
                    children=dcc.Graph(
                        id='timeseries',
                        style=styles.timeseries_graph_style,
                        responsive=True
                    ),
                ),
                # place date diff graph
                html.Div(
                    style=styles.tabs_div_style,
                    children=dcc.Tabs(
                        id='tabs_main',
                        value='tab_0',
                        parent_style=styles.tabs_parents_style,
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
                )
            ]
        )
    ]
)


def register_callbacks(app):
    @app.callback(
        [Output('tabs_main', 'children'),
         Output('tabs_main', 'value')
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
                    children=dcc.Graph(
                        id=f'tab_{idx}_graph',
                        figure=fig,
                        style=styles.date_diff_graph_style,
                        responsive=True
                    ),
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
        cases_total = '{:,.0f}'.format(df[day_mask]['confirmed'].sum())
        deaths_total = '{:,.0f}'.format(df[day_mask]['deaths'].sum())
        recovered_total = '{:,.0f}'.format(df[day_mask]['recovered'].sum())
        active_total = '{:,.0f}'.format(df[day_mask]['active'].sum())

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
        ts = dbo.TimeSeriesGraph(data=df, country_list=country_list,
                                 scale=scale)
        fig = ts.make_timeseries()
        return [fig]
