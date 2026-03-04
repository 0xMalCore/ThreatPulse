import sqlite3
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "attackers.db")
print("DASHBOARD DB PATH:", DB_PATH)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

app.title = "Intelligent Honeypot SOC Dashboard"


# ================= DATABASE =================

def load_data():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM attacks ORDER BY id DESC", conn)
    conn.close()
    return df


# ================= BRUTE FORCE DETECTION =================
# Only count SSH + HTTP auth attempts within last 1 minute

def detect_bruteforce(df):
    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    now = datetime.now()

    # Only authentication attempts
    auth_df = df[df["protocol"].isin(["SSH", "HTTP"])]

    # Only last 1 minute
    recent = auth_df[auth_df["timestamp"] >= now - timedelta(minutes=1)]

    ip_counts = recent.groupby("ip").size()
    suspicious = ip_counts[ip_counts >= 5]

    return suspicious.index.tolist()


# ================= RISK SCORE =================
# Only based on authentication attempts

def risk_score(df):
    if df.empty:
        return 0

    auth_df = df[df["protocol"].isin(["SSH", "HTTP"])]

    attempts = len(auth_df)

    return min(attempts * 5, 100)


# ================= LAYOUT =================

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("🛡 Intelligent Honeypot SOC Dashboard",
                        className="text-center my-4 text-info"))
    ]),

    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),

    html.Div(id="live-dashboard")

], fluid=True, style={
    "backgroundColor": "black",
    "minHeight": "100vh"
})


# ================= CALLBACK =================

@app.callback(
    Output("live-dashboard", "children"),
    Input("interval-component", "n_intervals")
)
def update_dashboard(n):

    try:
        df = load_data()

        if df.empty:
            return dbc.Alert("No attack data yet...", color="warning")

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

        # ---------------- Charts (All Activity) ----------------

        ip_counts = df.groupby("ip").size().reset_index(name="count")

        fig_ips = px.bar(
            ip_counts,
            x="ip",
            y="count",
            title="Top Attacking IPs (All Activity)",
            template="plotly_dark"
        )

        fig_protocol = px.pie(
            df,
            names="protocol",
            title="Protocol Distribution",
            template="plotly_dark"
        )

        df["hour"] = df["timestamp"].dt.hour
        timeline = df.groupby("hour").size().reset_index(name="count")

        fig_timeline = px.line(
            timeline,
            x="hour",
            y="count",
            title="Attacks Per Hour",
            template="plotly_dark"
        )

        # ---------------- Brute Force Section ----------------

        brute_ips = detect_bruteforce(df)

        brute_section = dbc.Alert(
            f"⚠ Suspicious IPs (5+ auth attempts in 1 min): {', '.join(brute_ips)}",
            color="danger"
        ) if brute_ips else dbc.Alert("No brute-force detected", color="success")

        # ---------------- Risk Score ----------------

        risk = risk_score(df)

        risk_bar = dbc.Progress(
            value=risk,
            label=f"Risk Score: {risk}%",
            striped=True,
            animated=True,
            color="danger" if risk > 60 else "warning"
        )

        # ---------------- Latest Logs ----------------

        latest_logs = df.sort_values("timestamp", ascending=False).head(10)

        logs_table = dbc.Table.from_dataframe(
            latest_logs[["ip", "username", "protocol", "country", "timestamp"]],
            striped=True,
            bordered=True,
            hover=True,
        )

        return dbc.Container([

            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_ips), md=6),
                dbc.Col(dcc.Graph(figure=fig_protocol), md=6),
            ]),

            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_timeline), md=12),
            ], className="mt-4"),

            dbc.Row([
                dbc.Col(brute_section, md=12),
            ], className="mt-4"),

            dbc.Row([
                dbc.Col(risk_bar, md=12),
            ], className="mt-2"),

            dbc.Row([
                dbc.Col(html.H4("Latest Attack Logs"), width=12)
            ], className="mt-4"),

            dbc.Row([
                dbc.Col(logs_table, width=12)
            ])

        ], fluid=True)

    except Exception as e:
        return dbc.Alert(f"Dashboard Error: {str(e)}", color="danger")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
