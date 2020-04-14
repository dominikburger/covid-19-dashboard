from datetime import datetime as dt
import dash_core_components as dcc
import dash_table
import pandas as pd
import plotly.graph_objs as go


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
        paper_bgcolor='#3b5998',
        plot_bgcolor='#3b5998'
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


def generate_ccd(df):
    def get_min_mask(data, factor):
        mask = data.ge(factor)
        return mask

    df_pivot = df.pivot(index='date', columns='country', values=['confirmed'])

    country_list = [
        'Germany',
        'US',
        'France',
        'Spain',
        'Italy',
        'Belgium',
        'Denmark',
        'Switzerland'
    ]

    fig = go.Figure()

    for country in country_list:
        # select country
        mask = df_pivot.columns.get_level_values(1) == country
        df_c = df_pivot.iloc[:, mask]

        # transform dataframe to series
        df_c = df_c.squeeze()

        # get disease outbreak day
        mask_min = get_min_mask(df_c, 100)
        df_c = df_c[mask_min]
        df_c = df_c.reset_index(drop=True)

        # create graph
        graph = go.Scatter(
            x=df_c.index,
            y=df_c,
            name=country,
            mode='lines+markers'
        )

        # add graph to figure
        fig.add_trace(graph)

    fig.update_layout(
        # title_text = 'World Map',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#84A295'
    )

    return fig


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
        columns=[{"name": i.capitalize(), "id": i} for i in df[columns].columns],
        data=df.to_dict('records'),
        style_table={
            'maxHeight': '55ex',
            'overflowY': 'scroll',
            # 'border': 'thin lightgrey solid'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'country'}, 'width': '50%'},
            # {'if': {'column_id': 'Region'}, 'width': '30%'},
        ],
        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        sort_action='native'
    )

    return table


def generate_table2(df=None, date=None):
    if date is not None:
        df = df[df['date'] == pd.to_datetime(date)]
    else:
        df = df[df['date'] == pd.to_datetime('04-04-2020')]

    columns = ['country', 'confirmed', 'deaths', 'recovered']

    df = df[columns].copy()
    df = df.sort_values(by=columns[1], ascending=False)

    table = dash_table.DataTable(
        id='table-info2',
        columns=[{"name": i.capitalize(), "id": i} for i in df[columns].columns],
        data=df.to_dict('records'),
        style_table={
            'maxHeight': '55ex',
            'overflowY': 'scroll',
            # 'border': 'thin lightgrey solid'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'country'}, 'width': '50%'},
            # {'if': {'column_id': 'Region'}, 'width': '30%'},
        ],
        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        sort_action='native'
    )

    return table


def generate_country_picker(dataframe=None):
    country_list = sorted(dataframe['country'].unique())
    country_options = [{"label": country, "value": country} for country in country_list]

    checklist = dcc.Dropdown(
        options=country_options,
        value=['Germany'],
        multi=True
    )
    return checklist


date_picker_style = {
    'width': '50%',
    'display': 'inline-block',
    'marginLeft': 10,
    'marginRight': 0,
    'marginTop': 0,
    'marginBottom': 0,
    'backgroundColor': '#232e4a'
}

graph_map_style = {
    'width': '50%',
    'display': 'inline-block',
    'marginLeft': 0,
    'marginRight': 0,
    'marginTop': 0,
    'marginBottom': 0,
    'backgroundColor': '#232e4a',
}

table_style = {
                        'width': '25%',
                        'display': 'inline-block',
                        'marginLeft': 0,
                        'marginRight': 0,
                        'marginTop': 0,
                        'marginBottom': 0,
                        'backgroundColor': '#232e4a',
                    }

timeseries_style = {
                        'height': '30%',
                        'width': '66%',
                        'display': 'inline-block',
                        'marginLeft': 0,
                        'marginRight': 0,
                        'marginTop': 0,
                        'marginBottom': 0,
                        'backgroundColor': '#232e4a',
                        # 'border': '2px black solid',
                    }

country_picker_style = {
                        'height': '10%',
                        'width': '32%',
                        'display': 'inline-block',
                        'marginLeft': 0,
                        'marginRight': 0,
                        'marginTop': 0,
                        'marginBottom': 0,
                        'backgroundColor': '#232e4a',
                        # 'border': 'blue',
                    }