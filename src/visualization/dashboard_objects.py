from datetime import datetime as dt
from datetime import timedelta
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from dash_table.Format import Format, Scheme


def make_date_picker():
    max_date = dt.today().date() - timedelta(days=1)
    return dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=dt(2020, 1, 22),
        max_date_allowed=max_date,
        initial_visible_month=dt(2020, 3, 15),
        date=str(dt(2020, 3, 15)),
        display_format='MM/DD/YYYY',
    )


def make_map(df, date=None):
    if date is not None:
        df_map = df[df['date'] == pd.to_datetime(date)].copy()
    else:
        df_map = df[df['date'] == pd.to_datetime('03-15-2020')].copy()

    color_scale = [
        [0, '#ffeecc'],
        [1/3, '#ffddcc'],
        [2/3, '#ffcccc'],
        [1, '#ffbbcc']
    ]

    choro = go.Choropleth(
        locations=df_map['country'],
        locationmode='country names',
        z=df_map['confirmed'],
        text=df_map['country'],
        autocolorscale=False,
        colorscale=color_scale,
        showscale=False,
    )

    geo_settings = {
        'resolution': 110,
        'showcoastlines': True, 'coastlinecolor': 'black',
        'showland': False, 'landcolor': 'LightGreen',
        'showocean': True, 'oceancolor': '#aec5e0',
        'showlakes': False, 'lakecolor': "Blue",
        'showrivers': False, 'rivercolor': "Blue",
        'showframe': True,
        'projection_type': 'equirectangular',

    }

    layout = {
        'geo_scope': 'world',
        'margin': {"r": 10, "t": 0, "l": 10, "b": 0},
        'width': 790,
        'height': 410,
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'geo': geo_settings
    }

    fig = go.Figure(data=choro, layout=layout)

    return fig


class TimeSeriesGraph:

    def __init__(self, data, country_list, scale):
        self.data = data.copy()
        self.data_pivot = None
        self.scale = scale
        self.hovertemplate = \
            '<b>Confirmed</b>: %{y:,}<br>' + \
            '<b>Day</b>: %{x}<br>' + \
            '<b>Date</b>: %{text|%x}'

        self.plot_lines = dict(
            linecolor='lightgrey',
            gridcolor='lightgrey',
            zerolinecolor='lightgrey',
        )
        self.layout = dict(
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            width=790,
            height=410,
            paper_bgcolor='#f6f6f6',
            plot_bgcolor='#f8f8f8',
            font={
                'family': 'Roboto',
                'size': 14,
                'color': '#363636',
            },
            legend_orientation='h',
            xaxis=self.plot_lines,
            yaxis=self.plot_lines
        )
        self.fig = go.Figure(layout=self.layout)

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
            return round(np.log(data), 2)

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

    def make_timeseries(self):

        for country in self.country_list:
            masked_country = self._mask_country(country)
            masked_country = masked_country.squeeze()

            # get disease outbreak day
            mask_min = self._get_min_mask(masked_country, 100)
            masked_country = masked_country[mask_min]
            masked_country = masked_country.reset_index()
            masked_country.columns = masked_country.columns.droplevel(1)
            masked_country.loc[:, 'confirmed'] = \
                self._scale_values(masked_country['confirmed'])

            # create graph
            graph = go.Scatter(
                x=masked_country.index,
                y=masked_country['confirmed'],
                text=masked_country['date'],
                hovertemplate=self.hovertemplate,
                hoverlabel={'align': 'left'},
                # hoverinfo={'bgcolor': 'black'},
                name=country,
                mode='lines+markers'
            )

            # add graph to figure
            self.fig.add_trace(graph)

        return self.fig


def make_table(df=None, date=None):
    if date is not None:
        df_table = df[df['date'] == pd.to_datetime(date)].copy()
    else:
        df_table = df[df['date'] == pd.to_datetime('04-20-2020')].copy()

    columns = ['country', 'confirmed', 'deaths', 'recovered', 'active']
    df_table = df_table.sort_values(by=columns[1], ascending=False)

    table = dash_table.DataTable(
        id='table-info',
        columns=[{"name": i.capitalize(), "id": i} for i in columns],
        data=df_table.to_dict('records'),
        style_table={
            'maxHeight': '55vh',
            'overflowY': 'auto',
            'max_width': '100%',
            'font-family': 'Roboto'
        },
        style_header={
            'fontSize': 16,
            'color': '#363636',

        },
        style_cell={
            'fontSize': 14,
            'color': '#363636',
            'backgroundColor': '#f6f6f6',
        },
        style_cell_conditional=[
            {'if': {'column_id': 'country'},
             'width': '20%'},
            {'if': {'column_id': 'confirmed'},
             'width': '20%',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'if': {'column_id': 'deaths'},
             'width': '20%',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'if': {'column_id': 'recovered'},
             'width': '20%',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'if': {'column_id': 'active'},
             'width': '20%',
             'type': 'numeric',
             'format': Format(group=',')
             },
        ],
        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        sort_action='native'
    )

    return table


def make_scale():
    return dcc.RadioItems(
        id='scale_radio',
        options=[
            {'label': 'linear', 'value': 'linear'},
            {'label': 'logarithmic', 'value': 'log'},
        ],
        value='linear',
        labelStyle={'display': 'inline-block'},
    )


def make_country_picker(dataframe=None):
    country_list = sorted(dataframe['country'].unique())
    country_options = [{"label": country, "value": country}
                       for country in country_list]

    checklist = dcc.Dropdown(
        id='country_checklist',
        options=country_options,
        value=['Germany', 'France', 'Spain', 'Italy'],
        multi=True,
    )

    return checklist


class DataLoader:
    def __init__(self):
        self.data = None
        self.day_range = None

    def _get_days(self, start_date, end_date):
        days = pd.date_range(start_date, end_date)
        self.day_range = days.strftime('%m-%d-%Y')

    def load_data(self, data_path, start_date, end_date):
        self._get_days(start_date, end_date)

        self.data = pd.DataFrame()

        for day in self.day_range:
            temp_data = pd.read_csv(data_path / f'{day}.csv')
            temp_data.loc[:, 'date'] = pd.to_datetime(day)
            self.data = self.data.append(temp_data)


class DataParser(DataLoader):

    def __init__(self):
        super().__init__()
        self.country = None

    def set_country(self, country=None):
        mask_country = self.data['country'] == country
        self.country = self.data[mask_country].copy()
        self.country = self.country.set_index('date').sort_index()

    def get_column_delta(self, column=None):
        shift_column = self.country[column].shift(1).squeeze()
        delta_column = self.country[column] - shift_column
        self.country.loc[:, f'{column}_delta'] = delta_column

    def get_moving_average(self, column=None, **kwargs):
        df_ma = self.country[column].rolling(**kwargs).mean()
        self.country.loc[:, f'{column}_moving_avg'] = df_ma


def make_delta_graph(dataframe=None, country=None):
    parser = DataParser()
    parser.data = dataframe.copy()

    parser.set_country(country)
    parser.get_column_delta('confirmed')
    parser.get_moving_average('confirmed_delta', window=3, center=True)

    scatter_trace = go.Scatter(
        name='3-day moving average',
        x=parser.country.index,
        y=parser.country['confirmed_delta_moving_avg'],
        marker_color='#e14a4a',
        hoverinfo='skip'
    )

    bar_trace = go.Bar(
        name='actual data',
        x=parser.country.index,
        y=parser.country['confirmed_delta'],
        hoverinfo='y',
        marker=dict(
            color='#e14a4a',
            opacity=0.5,
        )
    )

    traces = [scatter_trace, bar_trace]

    plot_lines = dict(
        linecolor='lightgrey',
        gridcolor='lightgrey',
        zerolinecolor='lightgrey',
    )

    layout = go.Layout(
        width=780,
        height=380,
        legend_orientation='h',
        paper_bgcolor='#f6f6f6',
        plot_bgcolor='#f8f8f8',
        margin=dict(t=10, l=5, r=5, b=5),
        xaxis=plot_lines,
        yaxis=plot_lines
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig
