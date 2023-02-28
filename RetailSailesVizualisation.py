import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template('LUX')


sales = pd.read_csv("/Users/macbookpro/Desktop/LinkedIn Work/LinkedIn Posts/Retail Store/sales.csv")

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    html.H1("Retail Sales Dashboard", style={"text-align": "center"}),
    html.Div([
        html.Div([
            html.Label("Choose Stores to Display:"),
            dcc.Dropdown(
                id="store-dropdown",
                options=[{"label": s, "value": s} for s in sales["Store"].unique()],
                value=[sales["Store"].unique()[0]],
                multi=True,
            ),
            dcc.Graph(id="sales-graph"),
        ], className="six columns"),
        html.Div([
            html.Div([
                dcc.Graph(id="sales-pie"),
            ], style={"display": "flex", "justify-content": "center", "text-align": "center"}),
            html.Div([
                html.P("This visualization shows the sales trends and total sales by store for the selected stores.", style={"font-size": "20px"}),
            ], style={"text-align": "center"}),
        ], className="six columns")
    ], className="row"),
])

@app.callback(
    [dash.dependencies.Output("sales-graph", "figure"), dash.dependencies.Output("sales-pie", "figure")],
    [dash.dependencies.Input("store-dropdown", "value")]
)
def update_sales(selected_stores):
    fig_sales = go.Figure()
    sales_by_store = sales.groupby("Store").sum().reset_index()

    for store in selected_stores:
        filtered_sales = sales[sales["Store"] == store]
        sales_by_week = filtered_sales.groupby("Date").sum().reset_index()

        fig_sales.add_trace(go.Scatter(x=sales_by_week['Date'], y=sales_by_week['Weekly_Sales'], mode='lines', name=store))

    fig_sales.update_layout(title={"text": "Sales Trends for Selected Stores", "x": 0.5}, xaxis_title="Date", yaxis_title="Weekly Sales", legend=dict(x=0, y=1))

    fig_pie = px.pie(sales_by_store, values='Weekly_Sales', names='Store', title="Total Sales by Store")
    fig_pie.update_traces(marker=dict(colors=px.colors.qualitative.Pastel))
    fig_pie.update_layout(height=600, width=600, margin=dict(t=50, b=50)) # Set the height and width to 3 times their default value

    return fig_sales, fig_pie

if __name__ == "__main__":
    app.run_server(debug=True)