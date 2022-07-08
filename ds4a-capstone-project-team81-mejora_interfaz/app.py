from cProfile import label

import time # Únicamente se utiliza para la generación aleatoria de datos en la gráfica de ejemplo

import dash
# import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from components.histogram import histogram
from components.model import model

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# Componentes necesarios para la construcción de nuestro tablero
# Basado en:
#   https://github.com/facultyai/dash-bootstrap-components/blob/main/examples/python/advanced-component-usage/navbars.py (Barra de logo)
#   https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/ (Pestañas)
#   https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/ (Gráfica con filtros)


# Le doy nombre a app y defino el tema a utilizar
# Se pueden ver ejemplos de más temas aquí: https://bootswatch.com/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Entry 1"),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Analysis of crime data in Medellin, Colombia.", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.correlation-one.com/data-science-for-all-colombia",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

# Contruímos el layout utilizando componentes para una mejor organización del código.

neighborhoods = ['Buenos Aires', 'Patio Bonito', 'San Isidro', 'Granizal', 'La Candelaria',
                 'Jardín Botánico', 'Las Palmas S.E.', 'Las Playas', 'Los Balsos No.1',
                 'Doce de Octubre No.2', 'Manrique Central No.2', 'El Tesoro',
                 'Cuarta Brigada', 'El Picacho', 'Ecoparque Cerro El Volador', 'Guayaquil',
                 'El Nogal-Los Almendros', 'El Salvador', 'Belén', 'Caribe', 'Las Lomas No.1',
                 'Altamira', 'Hospital San Vicente de Paúl', 'Santa Lucía',
                 'Centro Administrativo', 'La Alpujarra', 'Cerro Nutibara Ins.',
                 'Santo Domingo Savio No.1', 'El Poblado', 'Sucre', 'Los Colores',
                 'Santa María de los Ángeles', 'Santa Inés', 'Las Esmeraldas', 'Estadio',
                 'Berlin', 'Bomboná No.2', 'San Bernardo', 'La Frontera', 'Boqueron',
                 'Alfonso López', 'Lorena', 'Los Pinos', 'Simón Bolívar', 'La Milagrosa',
                 'Parque Juan Pablo II', 'Los Conquistadores', 'Villa Nueva', 'Prado',
                 'Alejandro Echavarría', 'Suramericana', 'Los Alcázares', 'Aures No.1',
                 'Moravia', 'López de Mesa', 'Fátima', 'Astorga', 'San Diego',
                 'Perpetuo Socorro', 'Barrio Colón', 'La Florida', 'Campo Valdés No.1',
                 'Naranjal', 'Calasanz', 'Castilla', 'Córdoba', 'Estación Villa', 'Calle Nueva',
                 'Manila', 'Terminal de Transporte', 'B. Cerro el Volador', 'Bolivariana',
                 'Guayabal', 'Nuevos Conquistadores', 'La Hondonada', 'El Raizal',
                 'Moscú No.1', 'Las Acacias', 'Enciso', 'Sevilla', 'Jesús Nazareno',
                 'Miraflores', 'Los Ángeles', 'El Velódromo', 'Florida Nueva', 'Las Granjas',
                 'Francisco Antonio Zea', 'La Mota', 'La Palma', 'Villa Carlota', 'La Gloria',
                 'Sin dato 60 San Cristobal', 'El Diamante No.2', 'Nueva Villa del Aburrá',
                 'Laureles', 'Los Mangos', 'Las Palmas', 'U.D. Atanasio Girardot',
                 'La Loma de los Bernal', 'Rosales', 'El Chagualo', 'San Benito',
                 'San Martín de Porres', 'Barrio Colombia', 'Asomadera No.1',
                 'La Esperanza No.2', 'La Piñuela', 'Parque Norte', 'Media Luna',
                 'La Floresta', 'Progreso', 'Campo Amor', 'Cristo Rey', 'El Diamante',
                 'Picacho', 'Oleoducto', 'Cataluña', 'Manrique Central No.1', 'San Miguel',
                 'Brasilia', 'La Castellana', 'Barrio Caycedo', 'San Javier No.1', 'Cucaracho',
                 'Andalucía', 'Santa Cruz', 'La Ladera', 'Castropol', 'La Avanzada', 'Santa Fé',
                 'Los Naranjos', 'Facultad de Minas U. Nal', 'Las Violetas', 'El Rincón',
                 'El Castillo', 'Los Alpes', 'Trinidad', 'Área Urbana Cgto. San Cristóbal',
                 'Playón de los Comuneros', 'El Pinal', 'Boyacá', 'Las Mercedes', 'San Lucas',
                 'Carlos E. Restrepo', 'Diego Echavarría', 'La Esperanza', 'Pedregal',
                 'Palenque', 'La Pilarica', 'Área de expansión San Antonio De Prado',
                 'Tricentenario', 'Calasania Parte Alta', 'Campo Alegre', 'La Colina',
                 'Bomboná No.1', 'Nueva Villa de la Iguaná', 'Santa Teresita', 'Palermo',
                 'Juan XXIIIi la Quiebra', 'El Danubio', 'La Mansión', 'Toscana', 'Boston',
                 'Aranjuez', 'La Aguacatala', 'El Pesebre', 'U.P.B', 'Robledo', 'Villa Flora',
                 'Tejelo', 'Las Independencias', 'Área de expansión Pajarito', 'Ferrini',
                 'La América', 'Las Estancias', 'Área Urbana Cgto. San Antonio de Prado',
                 'Facultad de Minas U. Nacional', 'San Germán', 'Aures No.2',
                 'Héctor Abad Gómez', 'Altavista', 'Las Lomas No.2', 'Granada',
                 'Villa del Socorro', 'San Joaquín', 'Santa Elena sector central',
                 'San Jose de La Montaña', 'Santander', 'Pajarito', 'Belalcázar', 'Belencito',
                 'El Pomar', 'Antonio Nariño', 'La Salle', 'Monteclaro', 'Volcana Guayabal',
                 'Barrio Cristóbal', 'Los Cerros el Vergel', 'Altavista Sector Central',
                 'Veinte de Julio', 'Manrique Oriental', 'Girardot',
                 'Batallón Cuarta Brigada', 'Kennedy', 'Villa Guadalupe', 'Florencia',
                 'Bosques de San Pablo', 'La Loma', 'Universidad de Antioquia',
                 'Altos del Poblado', 'El Rodeo', 'Los Balsos No.2', 'La Cruz', 'Travesias',
                 'Popular', 'Gerona', 'Asomadera No.2']

neighborhood_options = []
for neighborhood in neighborhoods:
    neighborhood_options.append({"label": neighborhood, "value": neighborhood})

select = dbc.Select(
    id="neighborhood",
    options=neighborhood_options,
)

form = dbc.Form([select])

form2 = dbc.Form([
    dbc.Label("Comune Number", html_for="comuna_number"),
    dbc.Input(type="text", id="comuna_number",
              placeholder="Commune number", value="14"),
    dbc.Label("Sex Femaie", html_for="comuna_number"),
    dbc.Input(type="text", id="sex_female",
              placeholder="Sex Femaie", value="1"),
    dbc.Label("Sex Male", html_for="comuna_number"),
    dbc.Input(type="text", id="sex_male", placeholder="Sex Male", value="0"),
    dbc.Label("Age", html_for="comuna_number"),
    dbc.Input(type="text", id="age", placeholder="Age", value="33"),
    dbc.Label("Hour", html_for="comuna_number"),
    dbc.Input(type="text", id="hour", placeholder="Hour", value="1"),
    dbc.Label("Weekday", html_for="comuna_number"),
    dbc.Input(type="text", id="weekday", placeholder="Weekday", value="6"),
])

row_content = [
    dbc.Col(html.Div(
        [
            dbc.Label("Select a Neighborhood (Statistics tab)"),
            form,

            dbc.Label("Model Input Data"),
            form2
        ]
    ), width=3),
    dbc.Col(html.Div(id="tab-content", className="p-4"), width=9),
]

row = html.Div(
    [
        dbc.Row(
            row_content,
            justify="start",
        ),
    ]
)

app.layout = dbc.Container(
    [
        logo,
        dbc.Tabs(
            [
                dbc.Tab(label="Statistics", tab_id="scatter"),
                dbc.Tab(label="Model", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(
            [
                dbc.Row(
                    row_content,
                    justify="start",
                ),
            ]
        ),
    ]
)


## Definimos los callbacks que permiten la interactividad entre el dashboard, las gráficas y el modelo

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input('neighborhood', 'value')],
    Input('comuna_number', 'value'),
    Input('sex_female', 'value'),
    Input('sex_male', 'value'),
    Input('age', 'value'),
    Input('hour', 'value'),
    Input('weekday', 'value'),
)
def render_tab_content(active_tab, neighborhood, comuna_number, sex_female, sex_male, age, hour, weekday):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "scatter":
            graphs = histogram.Histogram(neighborhood)

            return graphs
        elif active_tab == "histogram":
            models = model.Model(comuna_number, sex_female, sex_male, age, hour, weekday)

            return models
    return "No tab selected"


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks
# NOTA: No necesitamos este bucle, podemos referenciar el callback directamente al componente que escogimos (logo)
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

if __name__ == '__main__':
    app.run_server(app.run_server(host='127.0.0.1',port='8050',debug=True))