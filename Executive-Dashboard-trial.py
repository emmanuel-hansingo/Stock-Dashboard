# =========================
# IMPORTS
# =========================
from dash import Dash, html, dcc
from dash import Input, Output
from dash import dash_table

import pandas as pd
import plotly.express as px


# =========================
# SAMPLE DATA
# =========================
df = pd.DataFrame({

    "Region":[
        "North","North","South","South",
        "East","East","West","West"
    ],

    "Product":[
        "A","B","A","B",
        "A","B","A","B"
    ],

    "Revenue":[
        250000,180000,220000,190000,
        210000,170000,240000,200000
    ],

    "Profit":[
        65000,40000,58000,43000,
        52000,39000,61000,45000
    ]

})


# =========================
# REUSABLE KPI COMPONENT
# =========================
def kpi_card(title, value):

    return html.Div([

        html.H4(title, style={"marginBottom":"5px"}),

        html.H2(value)

    ],

    style={
        "padding":"20px",
        "borderRadius":"15px",
        "boxShadow":"2px 2px 8px lightgray",
        "width":"30%",
        "textAlign":"center",
        "backgroundColor":"#ffffff"
    }

)


# =========================
# APP INITIALIZATION
# =========================
app = Dash(__name__)


# =========================
# LAYOUT
# =========================
app.layout = html.Div([

    # ---------------------
    # TITLE
    # ---------------------
    html.H1(
        "Executive Sales Dashboard",
        style={"textAlign":"center"}
    ),

    # ---------------------
    # FILTERS
    # ---------------------
    html.Div([

        dcc.Dropdown(
            id="region-filter",
            options=[{"label":"All","value":"All"}] + [
                {"label":r,"value":r}
                for r in df.Region.unique()
            ],
            value="All",
            placeholder="Select Region"
        ),

        dcc.Dropdown(
            id="product-filter",
            options=[{"label":"All","value":"All"}] + [
                {"label":p,"value":p}
                for p in df.Product.unique()
            ],
            value="All",
            placeholder="Select Product"
        )

    ],
    style={
        "display":"flex",
        "gap":"20px",
        "marginBottom":"20px"
    }),

    # ---------------------
    # KPI ROW
    # ---------------------
    html.Div(
        id="kpi-row",
        style={
            "display":"flex",
            "gap":"20px",
            "marginBottom":"30px"
        }
    ),

    # ---------------------
    # CHARTS
    # ---------------------
    html.Div([

        dcc.Graph(id="revenue-chart"),
        dcc.Graph(id="profit-chart")

    ],
    style={
        "display":"flex",
        "gap":"20px"
    }),

    # ---------------------
    # TABLE
    # ---------------------
    html.H3("Detailed Data"),

    dash_table.DataTable(
        id="detail-table",
        page_size=8,
        style_table={"overflowX":"auto"},
        style_cell={"textAlign":"left"},
        style_header={"fontWeight":"bold"}
    )

],
style={
    "padding":"30px",
    "backgroundColor":"#f5f5f5"
})


# =========================
# CALLBACK
# =========================
@app.callback(

    Output("kpi-row","children"),
    Output("revenue-chart","figure"),
    Output("profit-chart","figure"),
    Output("detail-table","data"),
    Output("detail-table","columns"),

    Input("region-filter","value"),
    Input("product-filter","value")

)
def update_dashboard(region, product):

    # ---------------------
    # FILTER DATA
    # ---------------------
    filtered = df.copy()

    if region != "All":
        filtered = filtered[filtered.Region == region]

    if product != "All":
        filtered = filtered[filtered.Product == product]


    # ---------------------
    # KPIs
    # ---------------------
    revenue = filtered["Revenue"].sum()
    profit = filtered["Profit"].sum()

    margin = (profit / revenue * 100) if revenue != 0 else 0


    kpis = [

        kpi_card(
            "Revenue",
            f"${revenue:,.0f}"
        ),

        kpi_card(
            "Profit",
            f"${profit:,.0f}"
        ),

        kpi_card(
            "Margin",
            f"{margin:.1f}%"
        )

    ]


    # ---------------------
    # CHARTS
    # ---------------------
    revenue_fig = px.bar(
        filtered,
        x="Region",
        y="Revenue",
        color="Product",
        title="Revenue by Region"
    )

    profit_fig = px.bar(
        filtered,
        x="Region",
        y="Profit",
        color="Product",
        title="Profit by Region"
    )


    # ---------------------
    # TABLE
    # ---------------------
    table_data = filtered.to_dict("records")

    table_columns = [
        {"name": col, "id": col}
        for col in filtered.columns
    ]


    # ---------------------
    # RETURN ALL OUTPUTS
    # ---------------------
    return (
        kpis,
        revenue_fig,
        profit_fig,
        table_data,
        table_columns
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
