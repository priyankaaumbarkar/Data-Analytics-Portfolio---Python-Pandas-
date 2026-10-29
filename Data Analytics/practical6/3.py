"""
Standard Interactive Dashboard Template (Plotly Dash)

Install:
pip install dash pandas numpy plotly

Run:
python dash_dashboard.py

Open:
http://127.0.0.1:8050
"""

import numpy as np
import pandas as pd
import plotly.express as px

from dash import Dash, Input, Output, dcc, html


# ----------------------------------------------------------
# 1. DATA LAYER
# ----------------------------------------------------------

rng = np.random.default_rng(42)
n = 5000

df = pd.DataFrame(
    {
        "date": (
            pd.to_datetime("2025-01-01")
            + pd.to_timedelta(
                rng.integers(0, 365, n),
                unit="D"
            )
        ),
        "region": rng.choice(
            ["North", "South", "East", "West"], n
        ),
        "category": rng.choice(
            ["Electronics", "Clothing", "Home", "Sports"], n
        ),
        "units": rng.integers(1, 10, n),
        "unit_price": rng.uniform(10, 200, n).round(2),
    }
)

df["revenue"] = df["units"] * df["unit_price"]


# ----------------------------------------------------------
# 2. APP + LAYOUT
# ----------------------------------------------------------

app = Dash(__name__)
app.title = "Sales Dashboard"

CARD = {
    "background": "#f7f7f9",
    "padding": "16px",
    "borderRadius": "8px",
    "textAlign": "center",
    "flex": "1",
}

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "maxWidth": "1200px",
        "margin": "auto",
    },
    children=[
        html.H1("Sales Performance Dashboard"),

        # Filters
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.Label("Region"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": r, "value": r}
                                for r in sorted(df["region"].unique())
                            ],
                            value=sorted(df["region"].unique()),
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.Label("Category"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[
                                {"label": c, "value": c}
                                for c in sorted(df["category"].unique())
                            ],
                            value=sorted(df["category"].unique()),
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    children=[
                        html.Label("Date Range"),
                        html.Br(),
                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["date"].min().date(),
                            max_date_allowed=df["date"].max().date(),
                            start_date=df["date"].min().date(),
                            end_date=df["date"].max().date(),
                        ),
                    ]
                ),
            ],
        ),

        # KPI Cards
        html.Div(
            id="kpi-row",
            style={
                "display": "flex",
                "gap": "16px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
        ),

        # Monthly Trend Chart
        dcc.Graph(id="trend-chart"),

        # Category and Region Charts
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },
            children=[
                dcc.Graph(
                    id="category-chart",
                    style={"flex": "1", "minWidth": "300px"},
                ),
                dcc.Graph(
                    id="region-chart",
                    style={"flex": "1", "minWidth": "300px"},
                ),
            ],
        ),
    ],
)


# ----------------------------------------------------------
# 3. HELPER FUNCTIONS
# ----------------------------------------------------------

def filter_data(regions, categories, start, end) -> pd.DataFrame:
    """Filter sales data according to the selected inputs."""

    regions = regions or []
    categories = categories or []

    return df[
        df["region"].isin(regions)
        & df["category"].isin(categories)
        & df["date"].between(
            pd.Timestamp(start),
            pd.Timestamp(end),
        )
    ]


def kpi_card(title: str, value: str) -> html.Div:
    """Create a KPI summary card."""

    return html.Div(
        style=CARD,
        children=[
            html.Div(
                title,
                style={"color": "#666"},
            ),
            html.H2(
                value,
                style={"margin": "4px 0 0"},
            ),
        ],
    )


# ----------------------------------------------------------
# 4. CALLBACKS
# ----------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("category-chart", "figure"),
    Output("region-chart", "figure"),
    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(regions, categories, start, end):
    """Update KPI cards and charts when filters change."""

    d = filter_data(regions, categories, start, end)

    # Handle empty selections or date ranges
    if d.empty:
        empty_fig = px.scatter(
            title="No data for the selected filters"
        )

        return (
            [kpi_card("Total Revenue", "$0")],
            empty_fig,
            empty_fig,
            empty_fig,
        )

    # KPI Cards
    kpis = [
        kpi_card(
            "Total Revenue",
            f"${d['revenue'].sum():,.0f}",
        ),
        kpi_card(
            "Orders",
            f"{len(d):,}",
        ),
        kpi_card(
            "Avg Order Value",
            f"${d['revenue'].mean():,.2f}",
        ),
        kpi_card(
            "Units Sold",
            f"{d['units'].sum():,}",
        ),
    ]

    # Monthly Revenue Trend
    monthly = (
        d.set_index("date")
        .resample("MS")["revenue"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        monthly,
        x="date",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={
            "date": "Month",
            "revenue": "Revenue ($)",
        },
    )

    # Revenue by Category
    by_cat = (
        d.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue")
    )

    fig_cat = px.bar(
        by_cat,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
        labels={
            "revenue": "Revenue ($)",
            "category": "Category",
        },
    )

    # Revenue by Region
    by_reg = (
        d.groupby("region", as_index=False)["revenue"]
        .sum()
    )

    fig_reg = px.bar(
        by_reg,
        x="region",
        y="revenue",
        title="Revenue by Region",
        labels={
            "region": "Region",
            "revenue": "Revenue ($)",
        },
    )

    return kpis, fig_trend, fig_cat, fig_reg


# ----------------------------------------------------------
# 5. RUN THE APPLICATION
# ----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
    