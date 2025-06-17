# Import packages
import numpy as np
import sympy as sp
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from dash import dash_table

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H2("Axial Beam Displacement Calculator"),
    html.Label("Young's modulus (E [Pa]):"),
    dcc.Input(id='E', type='number', value=210e9),
    html.Br(),
    html.Label("Density (rho [kg/m^3]):"),
    dcc.Input(id='rho', type='number', value=7850),
    html.Br(),
    html.Label("Cross-sectional area (A [m^2]):"),
    dcc.Input(id='A', type='number', value=0.01),
    html.Br(),
    html.Label("Length of the beam (l [m]):"),
    dcc.Input(id='l', type='number', value=1.0),
    html.Br(),
    html.Label("Number of nodes:"),
    dcc.Input(id='nodes', type='number', value=5),
    html.Br(),
    html.Label("Force at last node (N):"),
    dcc.Input(id='force', type='number', value=1000),
    html.Br(),
    html.Button('Calculate', id='calc-btn', n_clicks=0),
    dcc.Graph(id='disp-plot'),
    html.Div(id='disp-table'),
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

@app.callback(
    Output('disp-plot', 'figure'),
    Output('disp-table', 'children'),
    Input('calc-btn', 'n_clicks'),
    State('E', 'value'),
    State('rho', 'value'),
    State('A', 'value'),
    State('l', 'value'),
    State('nodes', 'value'),
    State('force', 'value')
)
def update_plot(n_clicks, E, rho, A, l, i, force):
    if n_clicks == 0:
        return go.Figure(), ""
    # Element length and stiffness
    L = l / (i - 1)
    k = E * A / L
    # Force vector: all zeros except last node
    F = np.zeros(i)
    F[-1] = force
    # Stiffness matrix assembly
    K = np.zeros((i, i))
    for n in range(i - 1):
        K[n, n]     += k
        K[n, n+1]   -= k
        K[n+1, n]   -= k
        K[n+1, n+1] += k
    # Boundary condition: u0 = 0
    K[0, :] = 0
    K[0, 0] = 1
    F[0] = 0
    # Solve
    u = np.linalg.solve(K, F)
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(i)), y=u, mode='lines+markers', name='Displacement'))
    fig.update_layout(title="Nodal Displacement vs Node Number",
                      xaxis_title="Node Number",
                      yaxis_title="Displacement (m)",
                      template="plotly_white")
    # Table
    table = html.Table([
        html.Tr([html.Th("Node"), html.Th("Displacement (m)")])] +
        [html.Tr([html.Td(str(n)), html.Td(f"{u[n]:.6e}")]) for n in range(i)]
    )
    return fig, table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
