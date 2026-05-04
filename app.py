import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
from folium.plugins import HeatMap, MarkerCluster
import pycountry
import time
import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    layout="wide",
    page_title="HRIS — Conflict Risk AI",
    page_icon="🌍"
)

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0f1923;
    color: #ccd9e3;
}
.stApp { background: #0f1923; }
.block-container { padding: 1.6rem 2.8rem 3rem; max-width: 1500px; }

h1,h2,h3,h4 {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: #eaf2f8;
}

[data-testid="metric-container"] {
    background: #162330;
    border: 1px solid #243648;
    border-top: 3px solid #38b6d4;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}
[data-testid="metric-container"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.67rem !important;
    color: #4e7d96 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #38b6d4 !important;
    line-height: 1.15 !important;
}

.sh {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #eaf2f8;
    border-left: 4px solid #38b6d4;
    padding-left: 0.8rem;
    margin: 2.2rem 0 0.3rem;
    letter-spacing: 0.04em;
}
.sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: #2f5a72;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-left: 1.1rem;
}

.ticker-wrap {
    background: #0b1520;
    border-top: 1px solid #1e3448;
    border-bottom: 1px solid #1e3448;
    padding: 7px 0;
    overflow: hidden;
    margin: 1rem 0 1.8rem;
}
.ticker-inner {
    display: inline-block;
    white-space: nowrap;
    animation: scroll 80s linear infinite;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.71rem;
    color: #e05555;
    letter-spacing: 0.07em;
}
@keyframes scroll {
    from { transform: translateX(100vw); }
    to   { transform: translateX(-100%); }
}

.ac {
    background: #162330;
    border: 1px solid #243648;
    border-left: 4px solid #e05555;
    border-radius: 5px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.45rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ac-name { font-family:'Barlow Condensed',sans-serif; font-size:0.97rem; font-weight:700; color:#eaf2f8; }
.ac-meta { font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4e7d96; margin-top:2px; }
.ac-badge {
    background: rgba(224,85,85,0.12);
    border: 1px solid rgba(224,85,85,0.35);
    color: #e07070;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    border-radius: 3px;
    padding: 3px 8px;
    white-space: nowrap;
    margin-left: 10px;
    flex-shrink: 0;
}

.nc {
    background: #162330;
    border: 1px solid #243648;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
}
.nc:hover { border-color: #2a5070; }
.nc a { font-family:'Barlow Condensed',sans-serif; font-size:0.95rem; font-weight:600; color:#a8cfe0; text-decoration:none; line-height:1.3; }
.nc a:hover { color:#38b6d4; }
.nc-meta { font-family:'Share Tech Mono',monospace; font-size:0.60rem; color:#2f5a72; margin-top:4px; }
.nc-desc { font-size:0.78rem; color:#617d8c; margin-top:5px; line-height:1.4; }
.rdot { width:7px; height:7px; border-radius:50%; background:#e05555; display:inline-block; margin-right:9px; flex-shrink:0; margin-top:3px; }

.stButton > button {
    font-family: 'Share Tech Mono', monospace;
    background: transparent;
    border: 1px solid #38b6d4;
    color: #38b6d4;
    border-radius: 4px;
    letter-spacing: 0.09em;
    font-size: 0.77rem;
    padding: 0.45rem 1.4rem;
    transition: all 0.18s;
}
.stButton > button:hover {
    background: rgba(56,182,212,0.10);
    box-shadow: 0 0 14px rgba(56,182,212,0.22);
    color: #6ecfe8;
}

.stTextInput > div > div > input {
    background: #162330 !important;
    border: 1px solid #243648 !important;
    color: #ccd9e3 !important;
    border-radius: 5px !important;
    font-family: 'Barlow', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #38b6d4 !important;
    box-shadow: 0 0 0 2px rgba(56,182,212,0.18) !important;
}

[data-baseweb="select"] > div {
    background: #162330 !important;
    border: 1px solid #243648 !important;
    border-radius: 5px !important;
    color: #ccd9e3 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: transparent;
    border-bottom: 1px solid #243648;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.71rem;
    letter-spacing: 0.1em;
    color: #4e7d96;
    background: transparent;
    border: none;
    padding: 0.5rem 1.2rem;
    border-radius: 3px 3px 0 0;
}
.stTabs [aria-selected="true"] {
    color: #38b6d4 !important;
    background: rgba(56,182,212,0.08) !important;
    border-bottom: 2px solid #38b6d4 !important;
}

.streamlit-expanderHeader {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #4e7d96 !important;
    background: #162330 !important;
    border: 1px solid #243648 !important;
    border-radius: 5px !important;
}

hr { border-color: #1e3448; margin: 1.8rem 0; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#0f1923; }
::-webkit-scrollbar-thumb { background:#243648; border-radius:3px; }
.stAlert > div { border-radius:5px !important; font-family:'Barlow',sans-serif !important; font-size:0.85rem !important; }

.card { background:#162330; border:1px solid #243648; border-radius:7px; padding:1rem 1.3rem; }

.footer {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.60rem;
    color: #243648;
    letter-spacing: 0.15em;
    text-align: center;
    padding: 2rem 0 0.5rem;
    border-top: 1px solid #1e3448;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DATA & MODEL
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=120)
def generate_data(seed: int) -> pd.DataFrame:
    rng       = np.random.default_rng(seed)
    countries = list(pycountry.countries)
    rows      = []
    for c in countries:
        lat          = float(rng.uniform(-55, 70))
        lon          = float(rng.uniform(-180, 180))
        event        = int(rng.integers(1, 60))
        sentiment    = int(rng.integers(-8, 8))
        displacement = int(rng.integers(0, 500_000))
        aid_access   = round(float(rng.uniform(0, 1)), 2)
        score        = float(np.clip(
            event * 0.6 + (-sentiment) * 3.5 + (displacement / 500_000) * 15 + (1 - aid_access) * 10,
            0, 100
        ))
        if   score > 60: lvl = "HIGH"
        elif score > 35: lvl = "MEDIUM"
        else:            lvl = "LOW"
        rows.append({
            "location":        c.name,
            "alpha_3":         c.alpha_3,
            "lat":             lat,
            "lon":             lon,
            "event_intensity": event,
            "sentiment":       sentiment,
            "displacement":    displacement,
            "aid_access":      aid_access,
            "risk_score":      round(score, 2),
            "risk_level":      lvl,
            "updated":         datetime.utcnow().strftime("%H:%M UTC"),
        })
    return pd.DataFrame(rows)


@st.cache_resource
def train_model(df: pd.DataFrame):
    feats  = ["event_intensity", "sentiment", "displacement", "aid_access"]
    scaler = StandardScaler()
    mdl    = LinearRegression()
    mdl.fit(scaler.fit_transform(df[feats]), df["risk_score"])
    return mdl, scaler


@st.cache_data(ttl=600)
def fetch_news() -> list:
    try:
        r = requests.get(
            "https://newsapi.org/v2/everything"
            "?q=humanitarian+crisis+OR+conflict+OR+displacement+OR+war"
            "&sortBy=publishedAt&language=en"
            "&apiKey=e530a68fd1a4477d947fa57ec6d2f981",
            timeout=6,
        ).json()
        return [
            {
                "title":  a.get("title", ""),
                "source": a.get("source", {}).get("name", "Unknown"),
                "url":    a.get("url", "#"),
                "date":   a.get("publishedAt", "")[:10],
                "desc":   (a.get("description") or "")[:130],
            }
            for a in r.get("articles", [])[:8]
            if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
    except Exception:
        return []


_seed         = int(time.time() // 120)
df            = generate_data(_seed)
model, scaler = train_model(df)
high_df       = df[df["risk_level"] == "HIGH"].sort_values("risk_score", ascending=False)

LEVEL_COLORS = {"HIGH": "#e05555", "MEDIUM": "#f0a830", "LOW": "#3dba7e"}
LEVEL_ICONS  = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}

# ── Helper: standard chart layout (NO plot_bgcolor / margin conflicts) ──
def chart_layout(title="", height=420, show_legend=True, extra_margin=None):
    m = dict(l=10, r=10, t=44, b=10)
    if extra_margin:
        m.update(extra_margin)
    return dict(
        title=dict(text=title, font=dict(family="Barlow Condensed", size=15, color="#eaf2f8")),
        paper_bgcolor="#0f1923",
        plot_bgcolor="#162330",
        font=dict(family="Barlow Condensed", color="#ccd9e3", size=12),
        margin=m,
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)) if show_legend else dict(),
        showlegend=show_legend,
    )


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
hc1, hc2 = st.columns([6, 1])
with hc1:
    st.markdown(
        '<h1 style="font-size:1.9rem;margin-bottom:0;color:#eaf2f8;">'
        '🌍&nbsp; HRIS — Humanitarian Risk Intelligence System</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="sub" style="padding-left:0;margin-top:5px;">'
        f'AI-POWERED CONFLICT MONITORING  ·  {len(df)} COUNTRIES  ·  UPDATED {df["updated"].iloc[0]}</p>',
        unsafe_allow_html=True,
    )
with hc2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# Animated ticker
ticker_items = "   ·   ".join(
    f"⚠ {r['location'].upper()} [{r['risk_score']}]"
    for _, r in high_df.head(15).iterrows()
)
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner">'
    f'🔴 LIVE RISK ALERTS  ·  {ticker_items}  ·  🔴 LIVE RISK ALERTS  ·  {ticker_items}'
    f'</div></div>',
    unsafe_allow_html=True,
)

# KPI Metrics
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🌍 Countries",      len(df))
k2.metric("🔴 High Risk",      int((df["risk_level"] == "HIGH").sum()))
k3.metric("🟡 Medium Risk",    int((df["risk_level"] == "MEDIUM").sum()))
k4.metric("🟢 Low Risk",       int((df["risk_level"] == "LOW").sum()))
k5.metric("📊 Avg Risk Score", round(df["risk_score"].mean(), 1))

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# UAE STATUS
# ══════════════════════════════════════════════════════════════
uae = df[df["location"] == "United Arab Emirates"]
if not uae.empty:
    u = uae.iloc[0]
    st.markdown('<div class="sh">🇦🇪 UAE Intelligence Status</div>', unsafe_allow_html=True)
    uc1, uc2, uc3, uc4 = st.columns(4)
    uc1.metric("Risk Score",          u["risk_score"])
    uc2.metric("Event Intensity",     u["event_intensity"])
    uc3.metric("Aid Access",          f"{int(u['aid_access']*100)}%")
    uc4.metric("Displacement Est.",   f"{u['displacement']:,}")
    lc   = LEVEL_COLORS[u["risk_level"]]
    icon = LEVEL_ICONS[u["risk_level"]]
    msgs = {
        "HIGH":   "Immediate monitoring required — elevated threat indicators detected.",
        "MEDIUM": "Elevated vigilance advised — situation is developing.",
        "LOW":    "Situation stable — routine monitoring active.",
    }
    st.markdown(
        f'<div class="card" style="border-left:4px solid {lc};margin-top:0.6rem;">'
        f'<span style="font-family:Barlow Condensed,sans-serif;font-size:1.05rem;font-weight:700;color:{lc};">'
        f'{icon} STATUS: {u["risk_level"]} RISK</span>'
        f'<span style="color:#617d8c;font-size:0.85rem;margin-left:1rem;">{msgs[u["risk_level"]]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# ALERT CENTER  +  NEWS FEED
# ══════════════════════════════════════════════════════════════
left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="sh">🚨 Alert Center — Top 10</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub">HIGH PRIORITY ZONES · RANKED BY RISK SCORE</p>', unsafe_allow_html=True)
    for _, r in high_df.head(10).iterrows():
        st.markdown(
            f'<div class="ac">'
            f'  <div>'
            f'    <div class="ac-name">{r["location"]}</div>'
            f'    <div class="ac-meta">'
            f'EVENTS {r["event_intensity"]}  ·  '
            f'DISPLACED {r["displacement"]:,}  ·  '
            f'AID {int(r["aid_access"]*100)}%'
            f'    </div>'
            f'  </div>'
            f'  <span class="ac-badge">RISK {r["risk_score"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with right:
    st.markdown('<div class="sh">📰 Live Conflict Intelligence Feed</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub">CONFLICT · DISPLACEMENT · HUMANITARIAN CRISIS</p>', unsafe_allow_html=True)
    news = fetch_news()
    if news:
        for a in news:
            desc_html = f'<div class="nc-desc">{a["desc"]}…</div>' if a["desc"] else ""
            st.markdown(
                f'<div class="nc">'
                f'  <div style="display:flex;align-items:flex-start;">'
                f'    <span class="rdot"></span>'
                f'    <div style="flex:1;min-width:0;">'
                f'      <div><a href="{a["url"]}" target="_blank">{a["title"]}</a></div>'
                f'      <div class="nc-meta">{a["source"].upper()}  ·  {a["date"]}</div>'
                f'      {desc_html}'
                f'    </div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("Live news unavailable. Sign up at newsapi.org and replace the apiKey in fetch_news().")

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# GLOBAL MAP
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sh">🗺️ Global Intelligence Map</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📍 CIRCLE MARKERS + HEATMAP", "🌐 CHOROPLETH WORLD MAP"])

with tab1:
    cmap = cm.LinearColormap(
        ["#3dba7e", "#f0a830", "#e05555"],
        vmin=df["risk_score"].min(),
        vmax=df["risk_score"].max(),
        caption="Risk Score",
    )
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb dark_matter")
    cluster = MarkerCluster(options={"maxClusterRadius": 40, "disableClusteringAtZoom": 5})
    for _, row in df.iterrows():
        col = cmap(row["risk_score"])
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5 + row["risk_score"] / 22,
            color=col, fill=True, fill_color=col, fill_opacity=0.80,
            popup=folium.Popup(
                f"<b>{row['location']}</b><br>"
                f"Risk: <b>{row['risk_score']}</b> ({row['risk_level']})<br>"
                f"Events: {row['event_intensity']}<br>"
                f"Displaced: {row['displacement']:,}<br>"
                f"Aid Access: {int(row['aid_access']*100)}%",
                max_width=210,
            ),
        ).add_to(cluster)
    cluster.add_to(m)
    HeatMap(
        [[r["lat"], r["lon"], r["risk_score"]] for _, r in df.iterrows()],
        radius=18, blur=15, min_opacity=0.25,
    ).add_to(m)
    cmap.add_to(m)
    st_folium(m, use_container_width=True, height=540, returned_objects=[])

with tab2:
    # ✅ locationmode="ISO-3" with alpha_3 codes — correct, no duplicate keys
    fig_choro = px.choropleth(
        df,
        locations="alpha_3",
        locationmode="ISO-3",
        color="risk_score",
        hover_name="location",
        hover_data={
            "risk_level":      True,
            "event_intensity": True,
            "displacement":    True,
            "alpha_3":         False,
        },
        color_continuous_scale=[
            [0.00, "#0d2235"],
            [0.35, "#1a4a6e"],
            [0.60, "#f0a830"],
            [1.00, "#e05555"],
        ],
        template="plotly_dark",
    )
    fig_choro.update_layout(
        paper_bgcolor="#0f1923",
        plot_bgcolor="#0f1923",
        font=dict(family="Barlow Condensed", color="#ccd9e3", size=12),
        margin=dict(l=0, r=0, t=20, b=0),
        height=550,
        title=dict(
            text="Global Humanitarian Risk Score",
            font=dict(family="Barlow Condensed", size=16, color="#eaf2f8"),
        ),
        geo=dict(
            bgcolor="#0f1923",
            showframe=False,
            showcoastlines=True,  coastlinecolor="#243648",
            showland=True,        landcolor="#162330",
            showocean=True,       oceancolor="#0b1520",
            showlakes=False,
            showcountries=True,   countrycolor="#243648",
        ),
        coloraxis_colorbar=dict(
            title="Risk",
            thickness=13,
            len=0.65,
            bgcolor="#162330",
            bordercolor="#243648",
            tickfont=dict(family="Share Tech Mono", size=10),
        ),
    )
    st.plotly_chart(fig_choro, use_container_width=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sh">📊 Risk Analytics</div>', unsafe_allow_html=True)
st.markdown('<p class="sub">GLOBAL PATTERNS · DISTRIBUTION · TOP RISK ZONES</p>', unsafe_allow_html=True)

an1, an2 = st.columns(2, gap="medium")

with an1:
    fig_s = px.scatter(
        df, x="event_intensity", y="risk_score",
        color="risk_level", size="displacement", size_max=22,
        hover_name="location",
        color_discrete_map=LEVEL_COLORS,
        template="plotly_dark",
        labels={"event_intensity": "Event Intensity", "risk_score": "Risk Score"},
    )
    fig_s.update_layout(**chart_layout("Event Intensity vs Risk Score"))
    fig_s.update_traces(marker_line_width=0)
    st.plotly_chart(fig_s, use_container_width=True)

with an2:
    fig_b = px.bar(
        high_df.head(15).sort_values("risk_score"),
        x="risk_score", y="location", orientation="h",
        color="risk_score",
        color_continuous_scale=["#f0a830", "#e05555"],
        template="plotly_dark",
        labels={"risk_score": "Score", "location": ""},
    )
    fig_b.update_layout(**chart_layout("Top 15 Highest Risk Countries", show_legend=False))
    fig_b.update_traces(marker_line_width=0)
    st.plotly_chart(fig_b, use_container_width=True)

fig_h = px.histogram(
    df, x="risk_score", nbins=35,
    color="risk_level",
    color_discrete_map=LEVEL_COLORS,
    template="plotly_dark",
    barmode="overlay", opacity=0.72,
    labels={"risk_score": "Risk Score"},
)
fig_h.update_layout(**chart_layout("Global Risk Score Distribution"))
st.plotly_chart(fig_h, use_container_width=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# AI PREDICTION
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sh">🔮 AI Prediction Tool</div>', unsafe_allow_html=True)
st.markdown('<p class="sub">SET PARAMETERS · RUN MODEL · INSPECT FACTOR CONTRIBUTIONS</p>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)
pred_event  = p1.slider("Event Intensity",   0, 60,  15)
pred_sent   = p2.slider("Sentiment Score",  -8,  8,   0)
pred_disp   = p3.slider("Displaced (000s)",  0, 500, 50) * 1000
pred_aid    = p4.slider("Aid Access %",      0, 100, 60) / 100

if st.button("⚡ Run AI Prediction"):
    with st.spinner("Analysing…"):
        time.sleep(0.5)

    X_in  = scaler.transform([[pred_event, pred_sent, pred_disp, pred_aid]])
    score = float(np.clip(model.predict(X_in)[0], 0, 100))
    ce    = pred_event * 0.6
    cs    = (-pred_sent) * 3.5
    cd    = (pred_disp / 500_000) * 15
    ca    = (1 - pred_aid) * 10
    avg   = df["risk_score"].mean()
    level = "HIGH" if score > 60 else "MEDIUM" if score > 35 else "LOW"
    lc    = LEVEL_COLORS[level]
    icon  = LEVEL_ICONS[level]

    res1, res2 = st.columns([1, 2], gap="medium")

    with res1:
        st.markdown(
            f'<div class="card" style="border-left:4px solid {lc};margin-bottom:1rem;">'
            f'<div style="font-family:Barlow Condensed,sans-serif;font-size:1.05rem;font-weight:700;color:{lc};">'
            f'{icon} PREDICTED: {level} RISK</div>'
            f'<div style="font-family:Barlow Condensed,sans-serif;font-size:2.6rem;font-weight:700;'
            f'color:{lc};margin:5px 0;line-height:1;">'
            f'{score:.1f}'
            f'<span style="font-size:1rem;color:#4e7d96;font-weight:400;"> / 100</span></div>'
            f'<div style="font-family:Share Tech Mono,monospace;font-size:0.62rem;color:#2f5a72;">'
            f'GLOBAL AVG: {avg:.1f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-family:Share Tech Mono,monospace;font-size:0.62rem;'
            'color:#2f5a72;letter-spacing:0.12em;margin-bottom:0.4rem;">FACTOR BREAKDOWN</p>',
            unsafe_allow_html=True,
        )
        for lbl, val in [("Events", ce), ("Sentiment", cs), ("Displacement", cd), ("Aid Blockage", ca)]:
            st.metric(lbl, f"+{val:.1f}" if val >= 0 else f"{val:.1f}")

    with res2:
        # ── Gauge ──
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={"reference": avg, "valueformat": ".1f"},
            title={"text": "Predicted Risk Score",
                   "font": {"family": "Barlow Condensed", "color": "#ccd9e3", "size": 14}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#2f5a72",
                         "tickfont": {"family": "Share Tech Mono", "size": 9}},
                "bar":  {"color": lc, "thickness": 0.22},
                "bgcolor": "#162330",
                "borderwidth": 1,
                "bordercolor": "#243648",
                "steps": [
                    {"range": [0,  35], "color": "#0d2218"},
                    {"range": [35, 60], "color": "#201800"},
                    {"range": [60,100], "color": "#200808"},
                ],
                "threshold": {
                    "line": {"color": "#38b6d4", "width": 2},
                    "thickness": 0.75,
                    "value": avg,
                },
            },
            number={"font": {"family": "Barlow Condensed", "color": "#eaf2f8", "size": 42}},
        ))
        fig_g.update_layout(
            paper_bgcolor="#0f1923",
            height=295,
            margin=dict(l=30, r=30, t=50, b=10),
        )
        st.plotly_chart(fig_g, use_container_width=True)

        # ── Waterfall ──
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Events", "Sentiment", "Displacement", "Aid Blockage", "TOTAL"],
            y=[ce, cs, cd, ca, 0],
            connector={"line": {"color": "#243648", "width": 1}},
            decreasing={"marker": {"color": "#3dba7e", "line": {"width": 0}}},
            increasing={"marker": {"color": "#e05555", "line": {"width": 0}}},
            totals={"marker":    {"color": "#38b6d4", "line": {"width": 0}}},
            text=[f"{v:+.1f}" for v in [ce, cs, cd, ca, score]],
            textposition="outside",
        ))
        fig_wf.update_layout(
            title=dict(
                text="Risk Factor Contributions",
                font=dict(family="Barlow Condensed", size=14, color="#eaf2f8"),
            ),
            paper_bgcolor="#0f1923",
            plot_bgcolor="#162330",
            font=dict(family="Barlow Condensed", color="#ccd9e3", size=12),
            height=270,
            margin=dict(l=10, r=10, t=44, b=10),
            yaxis=dict(gridcolor="#1e3448"),
            xaxis=dict(gridcolor="#1e3448"),
            showlegend=False,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# EVACUATION PLANNER
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sh">🧭 AI-Assisted Evacuation Planning</div>', unsafe_allow_html=True)
st.markdown('<p class="sub">GENERATE OPTIMAL ROUTES · RISK DELTA · SAFETY CHECKLIST</p>', unsafe_allow_html=True)

ev1, ev2, ev3 = st.columns([2, 2, 1], gap="medium")
origin      = ev1.text_input("🔴 Risk Zone",  placeholder="e.g. Khartoum, Sudan")
destination = ev2.text_input("🟢 Safe Zone",  placeholder="e.g. Nairobi, Kenya")
travel_mode = ev3.selectbox("Travel Mode", ["driving", "walking", "transit"])

TIPS = {
    "driving": [
        "🔋 Full fuel tank before departure",
        "📻 Radio tuned to emergency broadcasts",
        "🛑 Avoid checkpoints — use secondary roads",
        "🌙 Travel in daylight hours when possible",
    ],
    "walking": [
        "👟 Sturdy footwear — minimal load",
        "💧 At least 3L of water per person",
        "🗺️ Download offline maps before leaving",
        "👥 Travel in groups — never alone",
    ],
    "transit": [
        "📅 Check schedule disruptions first",
        "🎫 Carry cash — cards may not work",
        "🏥 Know medical checkpoints en route",
        "📞 Share itinerary with a contact",
    ],
}

if st.button("📡 Generate Evacuation Route"):
    if origin and destination:
        gm_url  = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={requests.utils.quote(origin)}"
            f"&destination={requests.utils.quote(destination)}"
            f"&travelmode={travel_mode}"
        )
        osm_url = (
            f"https://www.openstreetmap.org/directions"
            f"?engine=fossgis_osrm_{travel_mode}"
            f"&route={requests.utils.quote(origin)};{requests.utils.quote(destination)}"
        )

        rc1, rc2 = st.columns([3, 2], gap="large")

        with rc1:
            st.markdown(
                f'<div class="card" style="border-left:4px solid #38b6d4;margin-bottom:0.8rem;">'
                f'<div style="font-family:Barlow Condensed,sans-serif;font-size:1rem;'
                f'font-weight:700;color:#eaf2f8;margin-bottom:10px;">'
                f'✅ Route Generated: '
                f'<span style="color:#e07070;">{origin}</span>'
                f'<span style="color:#4e7d96;"> → </span>'
                f'<span style="color:#3dba7e;">{destination}</span></div>'
                f'<a style="display:inline-block;font-family:Share Tech Mono,monospace;font-size:0.7rem;'
                f'color:#38b6d4;border:1px solid rgba(56,182,212,0.3);border-radius:3px;'
                f'padding:5px 12px;margin-right:8px;text-decoration:none;" '
                f'href="{gm_url}" target="_blank">🗺️ GOOGLE MAPS</a>'
                f'<a style="display:inline-block;font-family:Share Tech Mono,monospace;font-size:0.7rem;'
                f'color:#38b6d4;border:1px solid rgba(56,182,212,0.3);border-radius:3px;'
                f'padding:5px 12px;text-decoration:none;" '
                f'href="{osm_url}" target="_blank">🌐 OPENSTREETMAP</a>'
                f'</div>',
                unsafe_allow_html=True,
            )
            om = df[df["location"].str.lower().str.contains(
                origin.lower().split(",")[0].strip(), na=False)]
            dm = df[df["location"].str.lower().str.contains(
                destination.lower().split(",")[0].strip(), na=False)]
            if not om.empty and not dm.empty:
                os_, ds_ = om.iloc[0]["risk_score"], dm.iloc[0]["risk_score"]
                diff      = round(os_ - ds_, 1)
                arrow_c   = "#3dba7e" if diff > 0 else "#f0a830"
                arrow_txt = f"↓ {diff} SAFER AT DEST." if diff > 0 else f"⚠ +{abs(diff)} HIGHER RISK AT DEST."
                st.markdown(
                    f'<div class="card" style="margin-top:0.6rem;">'
                    f'<span style="font-family:Share Tech Mono,monospace;font-size:0.60rem;color:#2f5a72;">RISK DELTA</span><br>'
                    f'<span style="color:#e07070;">{om.iloc[0]["location"]}: {os_}</span>'
                    f'<span style="color:#4e7d96;"> → </span>'
                    f'<span style="color:#3dba7e;">{dm.iloc[0]["location"]}: {ds_}</span>'
                    f'<span style="font-family:Share Tech Mono,monospace;font-size:0.68rem;'
                    f'color:{arrow_c};margin-left:10px;">{arrow_txt}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        with rc2:
            tip_rows = "".join(
                f'<div style="font-size:0.82rem;color:#ccd9e3;padding:5px 0;'
                f'border-bottom:1px solid #1e3448;">{t}</div>'
                for t in TIPS[travel_mode]
            )
            st.markdown(
                f'<div class="card">'
                f'<div style="font-family:Share Tech Mono,monospace;font-size:0.60rem;'
                f'color:#2f5a72;letter-spacing:0.12em;margin-bottom:0.6rem;">'
                f'🛡 SAFETY CHECKLIST — {travel_mode.upper()}</div>'
                f'{tip_rows}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.warning("⚠ Enter both origin and destination to generate a route.")

st.markdown("---")


# ══════════════════════════════════════════════════════════════
# FULL DATASET
# ══════════════════════════════════════════════════════════════
with st.expander("📁 View & Export Full Dataset"):
    filt = st.multiselect(
        "Filter by risk level", ["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"],
    )
    sub = df[df["risk_level"].isin(filt)].sort_values("risk_score", ascending=False)
    st.dataframe(
        sub[["location", "risk_level", "risk_score", "event_intensity",
             "sentiment", "displacement", "aid_access"]],
        use_container_width=True, height=400,
    )
    st.download_button(
        "⬇ Download CSV",
        sub.to_csv(index=False).encode(),
        "hris_conflict_data.csv", "text/csv",
    )

st.markdown(
    '<div class="footer">'
    'HRIS v3.1  ·  AI-POWERED HUMANITARIAN RISK INTELLIGENCE  ·  '
    'DATA REFRESHES EVERY 120 SECONDS  ·  FOR DEMONSTRATION PURPOSES ONLY'
    '</div>',
    unsafe_allow_html=True,
)