import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from src import utils
from dash_table.Format import Format


def _check_date(df, date):
    """
    Sets a default date if none is given.
    :param df: The prepared dataframe
    :type df: pandas.Dataframe
    :param date: string representation of a date in format MM-DD-YYYY
    :type date: str
    :return: a subset of the dataframe depending on the given date
    :rtype: pandas.Dataframe
    """
    DEFAULT_DATE = '03-15-2020'

    if date is not None:
        return df[df['date'] == pd.to_datetime(date)].copy()
    else:
        return df[df['date'] == pd.to_datetime(DEFAULT_DATE)].copy()


def make_date_picker():
    """
    Creates the date picker object on the dashboard.
    :return: a date picker / calender that allows for the selection
        of a specific date.
    :rtype: dash_core_components.DatePickerSingle
    """
    min_day, max_day = utils.get_day_range()
    return dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=min_day,
        max_date_allowed=max_day,
        initial_visible_month=max_day,
        date=str(max_day),
        first_day_of_week=1,
        display_format='MM/DD/YYYY',
    )


def make_map(df, date=None):
    """
    Creates a Figure object that is used to display the world map. Additionally,
    specifics like color scale, and the hover text are defined.
    :param df: a dataframe containing the values of the various case types
        sorted by country and date.
    :type df: pandas.Dataframe
    :param date: a date formatted as DD-MM-YYYY
    :type date: str
    :return: a figure object which represents a map graph
    :rtype: plotly.graph_objs.Figure
    """

    df_map = _check_date(df, date)

    hovertemplate = \
        '<b>Confirmed</b>: %{z:,}<br>' + \
        '%{text}<extra>%{location}</extra>'

    color_scale = [
        [0, '#ffeecc'],
        [1/3, '#ffddcc'],
        [2/3, '#ffcccc'],
        [1, '#ffbbcc']
    ]

    # text that is displayed, when hovering over a country
    hover_text = [
        '<b>Deaths</b>: {:,.0f}<br>'.format(de) + \
        '<b>Recovered</b>: {:,.0f}<br>'.format(re) + \
        '<b>Active</b>: {:,.0f}'.format(ac)
        for de, re, ac in
        zip(
            list(df_map['deaths']),
            list(df_map['recovered']),
            list(df_map['active']))
    ]

    choro = go.Choroplethmapbox(
        locations=df_map['country'],
        z=df_map['confirmed'],
        text=hover_text,
        hovertemplate=hovertemplate,
        featureidkey='properties.country',
        hoverinfo='none',
        geojson=utils.load_geo_reference(),
        autocolorscale=False,
        colorscale=color_scale,
        showscale=False,
        marker={'opacity': 0.6}
    )

    layout = {
        'mapbox_style': "carto-positron",
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'margin': {'r': 0, 't': 0, 'l': 0, 'b': 0},
        'autosize': True,
    }

    fig = go.Figure(data=choro, layout=layout)

    return fig


class TimeSeriesGraph:
    """
    A class that is used to for a time series representation of the covid-19
    data. The data may both be viewed in tabular form and as a graphical
    representation. It can be used to select specific subsets of
    countries and dates.
    """

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
            xaxis_title='days since 100th confirmed case',
            yaxis_title='total confirmed cases per country',
            paper_bgcolor='#f6f6f6',
            plot_bgcolor='#f8f8f8',
            font={
                'family': 'Roboto',
                'size': 12,
                'color': '#363636',
            },
            legend_orientation='h',
            legend={'x': 0, 'y': -0.15},
            xaxis=self.plot_lines,
            yaxis=self.plot_lines,
            margin={'r': 10, 't': 10, 'l': 10, 'b': 10},
            autosize=True,
        )
        self.fig = go.Figure(layout=self.layout)

        self._create_pivot_table()
        self._select_country(country_list)

    def _create_pivot_table(self):
        self.data_pivot = self.data.pivot(
            index='date', columns='country', values=['confirmed']
        )

    def _scale_values(self, data):
        """
        Scales the given values linearly or logarithmically.
        :param data: A series containing numerical values.
        :type data: pandas.Series
        :return: scaled values
        :rtype: pandas.Series
        """
        if self.scale == 'linear' or self.scale is None:
            return data
        elif self.scale == 'log':
            return round(np.log(data), 2)

    @staticmethod
    def _get_min_mask(data, factor):
        """
        Creates a boolean mask of a numerical series. The condition checks for
        values that are greater or equal than 'factor'.
        :param data: A series containing numerical values.
        :type data: pandas.Series
        :param factor: a value which is used as the minimum value of the sliced
            series.
        :type factor: int
        :return: a boolean mask of the given series.
        :rtype: pandas.Series.
        """
        mask = data.ge(factor)
        return mask

    def _mask_country(self, country):
        """
        Creates a boolean mask of a series depending on the value of 'country'.
        :param country: name of a country.
        :type country: str
        :return: A subset containing only values of the given country.
        :rtype: pandas.Dataframe
        """
        mask = self.data_pivot.columns.get_level_values(1) == country
        masked_country = self.data_pivot.iloc[:, mask].copy()

        return masked_country

    def _select_country(self, country_list):
        """
        Checks the type of 'country_list'. If the type is string, the value is
        converted to a list.
        :param country_list: One or more country names.
        :type country_list: str or list
        :return: None
        :rtype: None
        """
        if isinstance(country_list, str):
            self.country_list = [country_list]
        if isinstance(country_list, list):
            self.country_list = country_list

    def make_timeseries(self):
        """
        Creates a Figure object that is used to display the timeseries graph.
        :return: a figure object which contains a timeseries graph.
        :rtype: plotly.graph_objs.Figure
        """

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
    """
    Creates a table object that is used to display the various case types
    on a given date over all countries.
    :param df: The prepared dataframe
    :type df: pandas.Dataframe
    :param date: A string representation of a date in format MM-DD-YYYY
    :type date: str
    :return: A table with the dataframe contents
    :rtype: dash_table.DataTable
    """
    df_table = _check_date(df, date)

    columns = ['country', 'confirmed', 'deaths', 'recovered', 'active']
    df_table = df_table.sort_values(by=columns[1], ascending=False)

    table = dash_table.DataTable(
        id='table-info',
        columns=[
            {'name': 'Country', 'id': 'country'},
            {'name': 'Confirmed', 'id': 'confirmed',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'name': 'Deaths', 'id': 'deaths',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'name': 'Recovered', 'id': 'recovered',
             'type': 'numeric',
             'format': Format(group=',')
             },
            {'name': 'Active', 'id': 'active',
             'type': 'numeric',
             'format': Format(group=',')
             }
        ],
        data=df_table.to_dict('records'),
        style_table={
            'maxHeight': '55vh',
            'overflowY': 'auto',
            'maxWidth': '100%',
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
            {'if': {'column_id': 'country'}, 'width': '20%'},
            {'if': {'column_id': 'confirmed'}, 'width': '20%'},
            {'if': {'column_id': 'deaths'}, 'width': '20%'},
            {'if': {'column_id': 'recovered'}, 'width': '20%'},
            {'if': {'column_id': 'active'}, 'width': '20%'},
        ],
        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        sort_action='native'
    )

    return table


def make_scale():
    """
    Creates the radio item object on the dashboard, which is used for the
    selection of the timeseries value scaling.
    :return: A radio item object with the options 'linear' or 'logarithmic'
    :rtype: dash_core_components.RadioItems
    """
    return dcc.RadioItems(
        id='scale_radio',
        options=[
            {'label': 'linear', 'value': 'linear'},
            {'label': 'logarithmic', 'value': 'log'},
        ],
        value='linear',
        labelStyle={'display': 'inline-block'},
    )


def make_country_picker(df=None):
    """
    Creates the dropdown object on the dashboard, which is used for the
    selection of countries that are displayed in the graphs for timeseries
    and case delta.
    :param df: The prepared dataframe
    :type df: pandas.Dataframe
    :return: A dropdown list with country names to choose from.
    :rtype: dash_core_components.Dropdown
    """
    country_list = sorted(df['country'].unique())
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
    """
    Used for loading the preprocessed csv files. It also allows to load a
    specific day range instead of all days available.
    """
    def __init__(self):
        self.data = None
        self.day_range = None

    def _get_days(self, start_date, end_date):
        """
        Creates a list of days in format MM-DD-YYY.
        :param start_date: Start of the time interval.
        :type start_date: str
        :param end_date: End of the time interval.
        :type end_date: str
        :return: a list of converted days.
        :rtype: DatetimeIndex
        """
        days = pd.date_range(start_date, end_date)
        self.day_range = days.strftime('%m-%d-%Y')

    def load_data(self, data_path, start_date, end_date):
        """
        Create a dataset from multiple csv files by concatenating them.
        :param data_path: Path where the csv files are stored
        :type data_path: pathlib.Path
        :param start_date: Start of the time interval.
        :type start_date: str
        :param end_date: End of the time interval.
        :type end_date: str
        :return: None
        :rtype: None
        """

        self._get_days(start_date, end_date)

        self.data = pd.DataFrame()

        for day in self.day_range:
            temp_data = pd.read_csv(data_path / f'{day}.csv')
            temp_data.loc[:, 'date'] = pd.to_datetime(day)
            self.data = self.data.append(temp_data)


class DataParser(DataLoader):
    """
    Used to prepare the data for the day-to-day case difference plot. For a
    selected country the daily difference in cases and the moving average
    is calculated.
    """
    def __init__(self):
        super().__init__()
        self.country = None

    def set_country(self, country=None):
        """
        Creates a separate dataframe containing only case numbers for the
        selected country.
        :param country: Country name.
        :type country: str
        :return: Subset dataframe for the given country.
        :rtype: pandas.Dataframe
        """
        mask_country = self.data['country'] == country
        self.country = self.data[mask_country].copy()
        self.country = self.country.set_index('date').sort_index()

    def get_column_delta(self, column=None):
        """
        Calculates the one day delta for total cases and appends it as a new
        column to the dataframe. Note: This method can be partially replaced
        by using the pandas.Dataframe.diff method.
        :param column: Column name on which the diff calculation is applied.
        :type column: str
        :return: None
        :rtype: None
        """
        shift_column = self.country[column].shift(1).squeeze()
        delta_column = self.country[column] - shift_column
        self.country.loc[:, f'{column}_delta'] = delta_column

    def get_moving_average(self, column=None, **kwargs):
        """
        Calculates the moving average of a chosen window size and appends it
        as a new column to the dataframe.
        :param column: Column name on which the moving average calculation is
            applied.
        :type column: str
        :param kwargs: kwargs to be used for the pandas.Dataframe.rolling
            method.
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        df_ma = self.country[column].rolling(**kwargs).mean()
        self.country.loc[:, f'{column}_moving_avg'] = df_ma


def make_delta_graph(dataframe=None, country=None):
    """
    Creates the graph object that is used to visualize the new daily cases
    on the dashboard (includes moving average).
    :param dataframe: The dataframe containing prepared data.
    :type dataframe: pandas.Dataframe
    :param country: Country name.
    :type country: str
    :return: a figure object which contains a daily new cases graph
    :rtype: plotly.graph_objs.Figure
    """
    MA_WINDOW_SIZE = 7

    parser = DataParser()
    parser.data = dataframe.copy()

    parser.set_country(country)
    parser.get_column_delta('confirmed')
    parser.get_moving_average(
        'confirmed_delta',
        window=MA_WINDOW_SIZE,
        center=True
    )

    hovertemplate = '%{y:,.0f}<extra></extra>'

    scatter_trace = go.Scatter(
        name=f'{MA_WINDOW_SIZE}-day moving average',
        x=parser.country.index,
        y=parser.country['confirmed_delta_moving_avg'],
        marker_color='#e14a4a',
        hoverinfo='skip'
    )

    bar_trace = go.Bar(
        name='actual data',
        x=parser.country.index,
        y=parser.country['confirmed_delta'],
        hovertemplate=hovertemplate,
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
        yaxis_title='confirmed new cases',
        font={'family': 'Roboto', 'size': 12, 'color': '#363636'},
        legend_orientation='h',
        legend={'x': 0, 'y': -0.15},
        paper_bgcolor='#f6f6f6',
        plot_bgcolor='#f8f8f8',
        xaxis=plot_lines,
        yaxis=plot_lines,
        margin={'t': 10, 'l': 5, 'r': 5, 'b': 5},
        autosize=True,
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig
