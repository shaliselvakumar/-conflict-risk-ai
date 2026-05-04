# 🌍 HRIS — Humanitarian Risk Intelligence System

> AI-powered conflict risk monitoring dashboard built with Python & Streamlit

## 🎯 Overview

HRIS is a proactive AI system designed to anticipate humanitarian risks 
before they escalate. Unlike traditional tools that are reactive, this 
system combines multiple data signals to generate real-time risk 
predictions and actionable guidance for civilians and aid organizations 
operating in conflict zones.

## ✨ Features

- 🔴 **Live Risk Ticker** — scrolling real-time alerts for high-risk zones
- 🗺️ **Interactive Global Map** — circle markers, heatmap & choropleth world view
- 🚨 **Alert Center** — top 10 highest risk countries ranked by AI score
- 📰 **Live News Feed** — real-time conflict & displacement intelligence
- 📊 **Risk Analytics** — scatter, bar and distribution charts
- 🔮 **AI Prediction Tool** — risk scoring with gauge chart & factor breakdown
- 🧭 **Evacuation Planner** — Google Maps & OpenStreetMap route generation
- ⬇️ **Data Export** — download full dataset as CSV

## 🧠 How It Works

The system analyses four key indicators per country:
1. **Event Intensity** — frequency and severity of conflict events
2. **Sentiment Score** — media and social signal analysis
3. **Displacement Volume** — estimated civilian displacement
4. **Aid Access** — humanitarian corridor availability

These feed into a machine learning pipeline (Linear Regression with 
StandardScaler normalization) that outputs a 0–100 risk score, 
classified as LOW / MEDIUM / HIGH.

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/conflict-risk-ai
cd conflict-risk-ai
pip install -r requirements.txt
streamlit run app.py
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Maps | Folium + Plotly Choropleth |
| ML Model | Scikit-learn (LinearRegression) |
| Charts | Plotly Express + Graph Objects |
| News | NewsAPI |
| Routing | Google Maps API + OpenStreetMap |
| Data | Pycountry + Synthetic conflict indicators |

## 📌 Use Case

Originally designed as a submission for an AI innovation challenge 
focused on conflict zones and humanitarian response. The system 
demonstrates how AI can shift crisis management from reactive to 
proactive — giving civilians, NGOs, and aid organizations an 
early-warning advantage.

## ⚠️ Disclaimer

This application uses synthetic data for demonstration purposes. 
It is not intended for real operational use without verified data sources.
