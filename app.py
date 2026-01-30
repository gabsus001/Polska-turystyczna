import json
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# =====================
# GeoJSON
# =====================
GEOJSON_PATH = "polska-wojewodztwa.geojson"

with open(GEOJSON_PATH, encoding="utf-8") as f:
    geojson = json.load(f)

WOJ_FIELD = "name"
locations = [f["properties"][WOJ_FIELD] for f in geojson["features"]]

# =====================
# Mapowanie województw na strony
# =====================
LINKI = {
    "Slaskie": "https://slaskie.travel/article/1020330/wybrane-atrakcje-wojewodztwa-slaskiego-top-20",
    "Malopolskie": "https://visitmalopolska.pl/en_GB",
    "Pomorskie": "https://odkryjpomorze.pl/artykul/pomorskie-atrakcje-turystyczne",
    "Lodzkie": "https://www.lodzkie.pl/turystyka/turystyka-w-lodzkiem/odkrywaj-lodzki/przyrodniczo",
    "Swietokrzyskie": "https://swietokrzyskie.pl/atrakcje-turystyczne-w-wojewodztwie-swietokrzyskim/",
    "Dolnoslaskie": "https://dolnyslask.travel/",
    "Warminsko-Mazurskie": "https://www.polska.travel/warminsko-mazurskie/",
    "Zachodniopomorskie": "https://www.polska.travel/zachodniopomorskie/",
    "Mazowieckie": "https://mazowsze.travel/",
    "Podkarpackie": "https://podkarpackie.travel/podkarpackie--turystyczne-top-10",
    "Lubelskie": "https://www.polska.travel/lubelskie/",
    "Lubuskie": "https://atrakcjelubuskie.pl/",
    "Opolskie": "https://www.visitopolskie.pl/",
    "Podlaskie": "https://visit.podlaskie.eu/turystyka/top-10-w-podlaskiem/",
    "Wielkopolskie": "https://polskapogodzinach.pl/wielkopolska-atrakcje-turystyczne/",
    "Kujawsko-Pomorskie": "https://kujawsko-pomorskie.travel/pl/content/mapa-atrakcji-turystycznych"
}

# =====================
# Dane do mapy
# =====================
z_values = [1] * len(locations)

# =====================
# Mapa
# =====================
fig = px.choropleth_map(
    geojson=geojson,
    locations=locations,
    featureidkey=f"properties.{WOJ_FIELD}",
    color=z_values,
    color_continuous_scale=[[0, "#a8e6a3"], [1, "#a8e6a3"]],
    hover_name=locations,
    hover_data={},
    center={"lat": 52.1, "lon": 19.4},
    zoom=5
)

fig.update_traces(
    hovertemplate="<b>Województwo %{location}</b><extra></extra>",
    marker_line_color="white",
    marker_line_width=1
)

fig.update_layout(
    mapbox_style="open-street-map",
    dragmode=False,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_showscale=False  # ❗ usuwa zielony słupek
)

# =====================
# Dash App
# =====================
app = dash.Dash(__name__)
server = app.server  # potrzebne do Render

app.layout = html.Div(
    style={
        "backgroundColor": "#e6ffe6",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "padding": "40px"
    },
    children=[
        html.H1(
            "Witaj w turystycznej Polsce!",
            style={"color": "#006400"}
        ),
        html.P(
            "Na tej stronie możesz w szybki sposób sprawdzić, jakie atrakcje turystyczne "
            "czekają na Ciebie w poszczególnych regionach naszego Kraju. Kliknij województwo, aby zobaczyć atrakcje turystyczne ❤️",
            style={"maxWidth": "900px", "textAlign": "center"}
        ),
        dcc.Graph(
            id="mapa",
            figure=fig,
            style={"width": "80vw", "height": "70vh"},
            config={"displayModeBar": False}
        ),
        dcc.Location(id="url")  # do przekierowań
    ]
)

# =====================
# Callback – przekierowanie
# =====================
@app.callback(
    Output("url", "href"),
    Input("mapa", "clickData"),
    prevent_initial_call=True
)
def open_link(clickData):
    woj = clickData["points"][0]["location"]
    return LINKI.get(woj)

# =====================
# Run lokalnie
# =====================
if __name__ == "__main__":
    app.run(debug=True)
app = dash.Dash(__name__)
server = app.server




