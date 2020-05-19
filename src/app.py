import dash
import src.paths as paths
from src.visualization.layout import layout
from src.visualization.layout import external_stylesheets
from src.visualization.layout import register_callbacks


app = dash.Dash(
    name='Covid-19 Dashboard',
    external_stylesheets=external_stylesheets,
    assets_folder=paths.dir_assets,
)
app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
