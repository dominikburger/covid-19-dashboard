from datetime import datetime as dt
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from dash_table.Format import Format

import yaml
from pathlib import Path


filepath = Path().cwd() / 'src' / 'visualization' / 'styles.yml'
styles = yaml.safe_load(open(filepath))


def generate_date_picker():
    return dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=dt(2020, 1, 22),
        max_date_allowed=dt(2020, 4, 13),
        initial_visible_month=dt(2020, 3, 15),
        date=str(dt(2020, 3, 15)),
        display_format='MM/DD/YYYY',
    )


def generate_map(df, date=None):
    if date is not None:
        df_map = df[df['date'] == pd.to_datetime(date)]
    else:
        df_map = df[df['date'] == pd.to_datetime('03-15-2020')]

    choro = go.Choropleth(
        locations=df_map['country'],
        locationmode='country names',
        z=df_map['confirmed'],
        text=df_map['country'],
        autocolorscale=False,
        colorscale="YlOrRd",
        showscale=False,
    )

    fig = go.Figure(choro)

    fig.update_layout(
        # title_text = 'World Map',
        geo_scope='world',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.update_geos(
        resolution=110,
        showcoastlines=True, coastlinecolor="black",
        showland=False, landcolor="LightGreen",
        showocean=True, oceancolor='#bfc4dc',
        showlakes=False, lakecolor="Blue",
        showrivers=False, rivercolor="Blue",
        showframe=False
    )

    return fig


class TimeSeriesGraph:

    def __init__(self, data, country_list, scale):
        self.data = data.copy()
        self.data_pivot = None
        self.scale = scale
        self.fig = go.Figure()

        self.fig.update_layout(
            margin={"r": 25, "t": 25, "l": 25, "b": 25},
            paper_bgcolor='#232e4a',
            font={
                'family': 'sans-serif',
                'size': 12,
                'color': 'white',
            }
        )

        self._create_pivot_table()
        self._select_country(country_list)

    def _create_pivot_table(self):
        self.data_pivot = self.data.pivot(
            index='date', columns='country', values=['confirmed']
        )

    def _scale_values(self, data):
        if self.scale == 'linear' or self.scale is None:
            return data
        elif self.scale == 'log':
            return np.log(data)

    @staticmethod
    def _get_min_mask(data, factor):
        mask = data.ge(factor)
        return mask

    def _mask_country(self, country):
        mask = self.data_pivot.columns.get_level_values(1) == country
        masked_country = self.data_pivot.iloc[:, mask].copy()

        return masked_country

    def _select_country(self, country_list):

        if isinstance(country_list, str):
            self.country_list = [country_list]
        if isinstance(country_list, list):
            self.country_list = country_list

    def generate_timeseries(self):

        for country in self.country_list:
            masked_country = self._mask_country(country)
            masked_country = masked_country.squeeze()

            # get disease outbreak day
            mask_min = self._get_min_mask(masked_country, 100)
            masked_country = masked_country[mask_min]
            masked_country = masked_country.reset_index(drop=True)
            masked_country = self._scale_values(masked_country)


            # create graph
            graph = go.Scatter(
                x=masked_country.index,
                y=masked_country,
                name=country,
                mode='lines+markers'
            )

            # add graph to figure
            self.fig.add_trace(graph)

        return self.fig


def generate_table(df=None, date=None):
    if date is not None:
        df = df[df['date'] == pd.to_datetime(date)]
    else:
        df = df[df['date'] == pd.to_datetime('04-04-2020')]

    columns = ['country', 'confirmed', 'deaths', 'recovered']

    df = df[columns].copy()
    df = df.sort_values(by=columns[1], ascending=False)

    table = dash_table.DataTable(
        id='table-info',
        columns=[{"name": i.capitalize(), "id": i} for i in columns],
        data=df.to_dict('records'),
        style_table={
            'maxHeight': '26em',
            'overflowY': 'auto',
            # 'border': 'thin lightgrey solid'
        },
        style_header={
            'fontWeight': 'bold'
        },
        style_cell={
            'fontSize': 16,
            'font-family': 'sans-serif',
            'color': '#bfc4dc',
            'backgroundColor': '#232e4a'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'country'},
             'width': '50%'},
            {'if': {'column_id': 'confirmed'},
             'type': 'numeric',
             'format': Format(group=',')
             }
            # {'if': {'column_id': 'Region'}, 'width': '30%'},
        ],
        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        sort_action='native'
    )

    return table


def generate_scale():
    return dcc.RadioItems(
        id='scale_radio',
        options=[
            {'label': 'linear', 'value': 'linear'},
            {'label': 'logarithmic', 'value': 'log'},
        ],
        value='linear',
        labelStyle={'display': 'inline-block'},
        style=styles['scale_style']
    )


def generate_country_picker(dataframe=None):
    country_list = sorted(dataframe['country'].unique())
    country_options = [{"label": country, "value": country}
                       for country in country_list]

    checklist = dcc.Dropdown(
        id='country_picker_dropdown',
        options=country_options,
        value=['Germany', 'France', 'Spain', 'Italy'],
        multi=True,
        style=styles['country_picker_style']
    )
    return checklist
