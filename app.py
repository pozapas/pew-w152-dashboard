"""
Pew W152 American Trends Panel — Interactive Analytics Dashboard
================================================================
A PhD-level, Q1-journal-quality Streamlit application for exploring
the August 2024 Pew Research Center Wave 152 survey (N = 5,410).

Two thematic blocks:
  • AI Perceptions & Attitudes
  • Driving Safety in America

Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import chi2_contingency
import math

import config as C

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pew W152 Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* --- Global --- */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.main .block-container { padding-top: 2rem; max-width: 1200px; }

/* --- Header Gradient --- */
.header-gradient {
    background: linear-gradient(135deg, #0A6E78 0%, #6C5CE7 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(10, 110, 120, 0.25);
}
.header-gradient h1 {
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.7rem !important;
    margin-bottom: 0.2rem !important;
    letter-spacing: -0.02em;
}
.header-gradient p {
    color: rgba(255,255,255,0.85) !important;
    font-size: 0.95rem !important;
    margin: 0 !important;
}

/* --- Metric Cards --- */
.metric-card {
    background: linear-gradient(145deg, #1A2634 0%, #0F1923 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(10,110,120,0.2);}
.metric-card .value {
    font-size: 2.2rem; font-weight: 700; color: #00B894;
    line-height: 1.15;
}
.metric-card .label {
    font-size: 0.78rem; color: #b2bec3; margin-top: 0.4rem;
    text-transform: uppercase; letter-spacing: 0.06em;
}

/* --- Section Divider --- */
.section-divider {
    height: 3px; border: none;
    background: linear-gradient(90deg, #0A6E78, #6C5CE7, #E8574A);
    border-radius: 2px; margin: 2rem 0;
}

/* --- Stat Table --- */
.stat-table {
    width: 100%; border-collapse: separate; border-spacing: 0;
    border-radius: 12px; overflow: hidden; font-size: 0.85rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.stat-table th {
    background: #0A6E78; color: white; padding: 0.65rem 1rem;
    font-weight: 600; text-align: left;
}
.stat-table td {
    padding: 0.55rem 1rem; border-bottom: 1px solid rgba(0,0,0,0.05);
}
.stat-table tr:nth-child(even) td { background: rgba(10,110,120,0.04); }
.stat-table tr:hover td { background: rgba(10,110,120,0.10); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1923 0%, #1A2634 100%);
}
section[data-testid="stSidebar"] .stRadio label {
    color: #DFE6E9 !important; font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading Pew W152 data …")
def load_data():
    return pd.read_csv(C.DATA_FILE, low_memory=False)

df = load_data()
W = C.WEIGHT_COL

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def weighted_pct(series, weights, value_map, exclude_refused=True):
    """Return a DataFrame with Value, Label, WeightedPct, WeightedN."""
    mask = series.notna()
    if exclude_refused:
        mask = mask & (series != C.REFUSED_CODE)
    s = series[mask]
    w = weights[mask]
    total_w = w.sum()
    records = []
    for val in sorted(value_map.keys()):
        if exclude_refused and val == C.REFUSED_CODE:
            continue
        sel = s == val
        wn = w[sel].sum()
        pct = wn / total_w * 100 if total_w > 0 else 0
        records.append({"value": val, "label": value_map[val],
                        "pct": round(pct, 1), "weighted_n": round(wn, 1)})
    return pd.DataFrame(records)


def weighted_crosstab(df, q_col, demo_col, q_vals, demo_vals, weight_col=W):
    """Weighted cross-tabulation returning a DataFrame of percentages."""
    mask = df[q_col].notna() & df[demo_col].notna()
    mask = mask & (df[q_col] != C.REFUSED_CODE) & (df[demo_col] != C.REFUSED_CODE)
    sub = df[mask].copy()
    records = []
    for dv, dl in demo_vals.items():
        if dv == C.REFUSED_CODE:
            continue
        dsub = sub[sub[demo_col] == dv]
        tw = dsub[weight_col].sum()
        for qv, ql in q_vals.items():
            if qv == C.REFUSED_CODE:
                continue
            wn = dsub.loc[dsub[q_col] == qv, weight_col].sum()
            pct = wn / tw * 100 if tw > 0 else 0
            records.append({"demo_label": dl, "q_label": ql, "pct": round(pct, 1)})
    return pd.DataFrame(records)


def cramers_v(contingency_table):
    """Cramér's V from a contingency table (not weighted — for illustration)."""
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    if min_dim == 0 or n == 0:
        return 0
    return math.sqrt(chi2 / (n * min_dim))


def make_bar(data, x="label", y="pct", color=None, palette=None,
             title="", orientation="v", height=420, text_auto=True):
    """Quick Plotly bar chart with the project design system."""
    if palette is None:
        palette = C.PLOTLY_PALETTE
    if color is None:
        fig = px.bar(data, x=x, y=y, text=y if text_auto else None,
                     color=x, color_discrete_sequence=palette,
                     title=title, height=height)
    else:
        fig = px.bar(data, x=x, y=y, color=color, text=y if text_auto else None,
                     color_discrete_sequence=palette, barmode="group",
                     title=title, height=height)
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                      marker_line_width=0)
    fig.update_layout(
        font_family="Inter", font_color="#2D3436",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=16, title_font_color="#2D3436", title_x=0,
        xaxis_title="", yaxis_title="Weighted %",
        margin=dict(l=40, r=20, t=50, b=60),
        showlegend=False if color is None else True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25,
                    xanchor="center", x=0.5, font_size=11),
    )
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.05)", range=[0, max(data[y]) * 1.18])
    return fig


def make_horizontal_stacked_bar(items, values, title, palette=None, height=None):
    """100% stacked horizontal bar for Likert-type battery items."""
    if palette is None:
        n_vals = len([v for v in values if v != C.REFUSED_CODE])
        palette = C.LIKERT_PALETTE_4 if n_vals <= 4 else (
            C.LIKERT_PALETTE_5 if n_vals <= 5 else C.LIKERT_PALETTE_6)
    if height is None:
        height = max(320, len(items) * 52 + 100)

    # Build data
    rows = []
    for col, item_label in items.items():
        pdata = weighted_pct(df[col], df[W], values)
        for _, r in pdata.iterrows():
            rows.append({"Item": item_label, "Response": r["label"], "pct": r["pct"]})
    plot_df = pd.DataFrame(rows)
    if plot_df.empty:
        return go.Figure()

    # Determine category order
    cat_order = [v for k, v in sorted(values.items()) if k != C.REFUSED_CODE]
    fig = px.bar(plot_df, y="Item", x="pct", color="Response",
                 orientation="h", text="pct", title=title,
                 category_orders={"Response": cat_order},
                 color_discrete_sequence=palette, height=height)
    fig.update_traces(texttemplate="%{text:.0f}%", textposition="inside",
                      insidetextanchor="middle", textfont_size=11,
                      marker_line_width=0)
    fig.update_layout(
        barmode="stack",
        font_family="Inter", font_color="#2D3436",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=16, title_x=0,
        xaxis_title="Weighted %", yaxis_title="",
        xaxis=dict(range=[0, 102]),
        margin=dict(l=20, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22,
                    xanchor="center", x=0.5, font_size=11,
                    title_text=""),
        yaxis=dict(autorange="reversed"),
    )
    return fig


def make_heatmap(ct_df, title, height=450):
    """Heatmap from a cross-tabulation DataFrame."""
    pivot = ct_df.pivot_table(index="q_label", columns="demo_label", values="pct", aggfunc="first")
    fig = px.imshow(pivot, text_auto=".1f", aspect="auto",
                    color_continuous_scale=["#F8F9FA", "#0A6E78"],
                    title=title, height=height)
    fig.update_layout(
        font_family="Inter", font_color="#2D3436",
        title_font_size=16, title_x=0,
        xaxis_title="", yaxis_title="",
        margin=dict(l=20, r=20, t=50, b=40),
        coloraxis_colorbar_title="(%)",
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <span style="font-size:2.2rem;">📊</span>
        <h3 style="color:#00B894; margin:0.3rem 0 0; font-weight:700;">Pew W152</h3>
        <p style="color:#b2bec3; font-size:0.78rem; margin:0;">Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:0.5rem 0;'>",
                unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["Survey Overview",
         "AI Perceptions",
         "Driving Safety",
         "Cross-Tabulations",
         "Statistical Analysis"],
        label_visibility="collapsed",
    )
    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:0.5rem 0;'>",
                unsafe_allow_html=True)
    st.caption(f"**Source:** {C.SURVEY_TITLE}")
    st.caption(f"**Field dates:** {C.SURVEY_DATES}")
    st.caption(f"**N =** {C.SURVEY_N:,}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: SURVEY OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Survey Overview":
    # Header
    st.markdown("""
    <div class="header-gradient">
        <h1>Survey Overview &amp; Demographic Profile</h1>
        <p>Pew Research Center — American Trends Panel, Wave 152 · August 2024</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    total_weighted = df[W].sum()
    completion_rate = df["INTERVIEW_END_W152"].notna().mean() * 100
    web_pct = (df["SVYMODE_W152"] == 1).mean() * 100 if "SVYMODE_W152" in df.columns else 0
    english_pct = (df["LANG_W152"] == 1).mean() * 100 if "LANG_W152" in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    for col_st, val, lbl in [
        (c1, f"{len(df):,}", "Respondents"),
        (c2, f"{total_weighted:,.0f}", "Weighted N"),
        (c3, f"{completion_rate:.1f}%", "Completion Rate"),
        (c4, f"{english_pct:.0f}% / {100-english_pct:.0f}%", "English / Spanish"),
    ]:
        col_st.markdown(f"""
        <div class="metric-card">
            <div class="value">{val}</div>
            <div class="label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Demographic profile
    st.subheader("Demographic Profile (Weighted)")

    # Pick top demographics to show
    demo_keys = ["F_AGECAT", "F_GENDER", "F_EDUCCAT", "F_RACETHNMOD",
                 "F_PARTYSUM_FINAL", "F_IDEO", "F_INC_TIER2", "F_USR_SELFID"]

    cols_per_row = 2
    for i in range(0, len(demo_keys), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, dk in enumerate(demo_keys[i:i+cols_per_row]):
            if dk not in C.DEMO_VALUES or dk not in df.columns:
                continue
            pdata = weighted_pct(df[dk], df[W], C.DEMO_VALUES[dk])
            label = C.DEMO_LABELS.get(dk, dk)
            fig = make_bar(pdata, title=label, height=350)
            cols[j].plotly_chart(fig, use_container_width=True)

    # Survey device / mode breakdown
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.subheader("Survey Administration")
    sa1, sa2 = st.columns(2)
    if "DEVICE_TYPE_W152" in df.columns:
        dev_map = {1: "Desktop/Laptop", 2: "Tablet", 3: "Smartphone", 99: "Refused"}
        dev_data = weighted_pct(df["DEVICE_TYPE_W152"], df[W], dev_map)
        fig_dev = px.pie(dev_data, names="label", values="pct",
                         color_discrete_sequence=C.PLOTLY_PALETTE,
                         title="Device Type", hole=0.45, height=350)
        fig_dev.update_traces(textinfo="label+percent", textfont_size=12,
                              marker_line_width=0)
        fig_dev.update_layout(font_family="Inter", showlegend=False,
                              margin=dict(l=20,r=20,t=50,b=20))
        sa1.plotly_chart(fig_dev, use_container_width=True)
    if "SVYMODE_W152" in df.columns:
        mode_map = {1: "Web (online)", 2: "CATI (phone)"}
        mode_data = weighted_pct(df["SVYMODE_W152"], df[W], mode_map)
        fig_mode = px.pie(mode_data, names="label", values="pct",
                          color_discrete_sequence=[C.COLORS["accent2"], C.COLORS["accent3"]],
                          title="Survey Mode", hole=0.45, height=350)
        fig_mode.update_traces(textinfo="label+percent", textfont_size=12,
                               marker_line_width=0)
        fig_mode.update_layout(font_family="Inter", showlegend=False,
                               margin=dict(l=20,r=20,t=50,b=20))
        sa2.plotly_chart(fig_mode, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: AI PERCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "AI Perceptions":
    st.markdown("""
    <div class="header-gradient">
        <h1>Artificial Intelligence — Public Perceptions &amp; Attitudes</h1>
        <p>How Americans view AI: awareness, excitement, concerns, fairness, regulation &amp; chatbot usage</p>
    </div>
    """, unsafe_allow_html=True)

    tab_names = ["Awareness & Sentiment", "Future Impact", "Jobs & Economy",
                 "Concerns & Fairness", "Chatbots", "Regulation & Trust"]
    tabs = st.tabs(tab_names)

    # ── Tab 1: Awareness & Sentiment ─────────────────────────────────────────
    with tabs[0]:
        a1, a2 = st.columns(2)
        pdata1 = weighted_pct(df["AI_HEARD_W152"], df[W], C.AI_HEARD_VALUES)
        a1.plotly_chart(make_bar(pdata1, title="How much have you heard about AI?"),
                        use_container_width=True)

        pdata2 = weighted_pct(df["CNCEXC_W152"], df[W], C.CNCEXC_VALUES)
        a2.plotly_chart(make_bar(pdata2, title="More concerned or excited about AI?",
                                palette=[C.COLORS["accent3"], C.COLORS["accent1"],
                                         C.COLORS["secondary"]]),
                        use_container_width=True)

        b1, b2 = st.columns(2)
        pdata3 = weighted_pct(df["USEAI_W152"], df[W], C.USEAI_VALUES)
        b1.plotly_chart(make_bar(pdata3, title="Ever use AI-based tools?"),
                        use_container_width=True)

        pdata4 = weighted_pct(df["PERSBENHRM_W152"], df[W], C.PERSBENHRM_VALUES)
        b2.plotly_chart(make_bar(pdata4, title="Will AI benefit or harm you personally?",
                                palette=[C.COLORS["accent3"], C.COLORS["neutral"],
                                         C.COLORS["secondary"]]),
                        use_container_width=True)

        # AI impact on U.S. overall
        pdata5 = weighted_pct(df["AICHANGE_W152"], df[W], C.AICHANGE_VALUES)
        st.plotly_chart(make_bar(pdata5, title="AI impact on U.S. over the next 20 years",
                                palette=C.DIVERGING_PALETTE, height=380),
                        use_container_width=True)

    # ── Tab 2: Future Impact ─────────────────────────────────────────────────
    with tabs[1]:
        fig_fi = make_horizontal_stacked_bar(
            C.AIFUTRIMPCT_ITEMS, C.AIFUTRIMPCT_VALUES,
            "Expected AI Impact Across Sectors (Next 20 Years)",
            palette=C.DIVERGING_PALETTE[:4])
        st.plotly_chart(fig_fi, use_container_width=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("#### AI Predictions — Will These Happen in 20 Years?")
        fig_fp = make_horizontal_stacked_bar(
            C.FUTRAI_ITEMS, C.FUTRAI_VALUES,
            "Likelihood of Future AI Scenarios",
            palette=C.PLOTLY_PALETTE[:6])
        st.plotly_chart(fig_fp, use_container_width=True)

    # ── Tab 3: Jobs & Economy ────────────────────────────────────────────────
    with tabs[2]:
        j1, j2 = st.columns([1, 1])
        pdata_j = weighted_pct(df["AIJOBS_W152"], df[W], C.AIJOBS_VALUES)
        j1.plotly_chart(make_bar(pdata_j, title="AI will lead to more or fewer jobs overall?",
                                palette=C.DIVERGING_PALETTE, height=380),
                        use_container_width=True)

        fig_ji = make_horizontal_stacked_bar(
            C.AIJOBIMPCT_ITEMS, C.AIJOBIMPCT_VALUES,
            "Expected Job Impact by Sector",
            palette=C.LIKERT_PALETTE_4)
        j2.plotly_chart(fig_ji, use_container_width=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("#### Human vs. AI — Who Does It Better?")
        fig_hv = make_horizontal_stacked_bar(
            C.HUMANVAI_ITEMS, C.HUMANVAI_VALUES,
            "Human vs. AI Competency Across Domains",
            palette=[C.COLORS["primary"], C.COLORS["accent3"],
                     C.COLORS["accent1"], C.COLORS["secondary"]])
        st.plotly_chart(fig_hv, use_container_width=True)

    # ── Tab 4: Concerns & Fairness ───────────────────────────────────────────
    with tabs[3]:
        st.markdown("#### Level of Concern About AI Issues")
        fig_ac = make_horizontal_stacked_bar(
            C.AICONCERN_ITEMS, C.AICONCERN_VALUES,
            "How concerned are you about each of the following?",
            palette=C.LIKERT_PALETTE_5)
        st.plotly_chart(fig_ac, use_container_width=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("#### Confidence in AI Fairness Across Groups")
        fig_disc = make_horizontal_stacked_bar(
            C.DISCRIM1_ITEMS, C.DISCRIM1_VALUES,
            "Confidence that AI treats these groups fairly",
            palette=C.LIKERT_PALETTE_5)
        st.plotly_chart(fig_disc, use_container_width=True)

    # ── Tab 5: Chatbots ──────────────────────────────────────────────────────
    with tabs[4]:
        ch1, ch2, ch3 = st.columns(3)
        pdata_ca = weighted_pct(df["CHATAWARE_W152"], df[W], C.CHATAWARE_VALUES)
        ch1.plotly_chart(make_bar(pdata_ca, title="Chatbot Awareness", height=360),
                         use_container_width=True)

        mask_cu = df["CHATUSE_W152"].notna()
        pdata_cu = weighted_pct(df.loc[mask_cu, "CHATUSE_W152"],
                                df.loc[mask_cu, W], C.CHATUSE_VALUES)
        ch2.plotly_chart(make_bar(pdata_cu, title="Ever Used a Chatbot?",
                                 palette=[C.COLORS["accent3"], C.COLORS["secondary"]],
                                 height=360),
                         use_container_width=True)

        mask_ch = df["CHATHELPFUL_W152"].notna() & (df["CHATHELPFUL_W152"] != C.REFUSED_CODE)
        pdata_ch = weighted_pct(df.loc[mask_ch, "CHATHELPFUL_W152"],
                                df.loc[mask_ch, W], C.CHATHELPFUL_VALUES)
        ch3.plotly_chart(make_bar(pdata_ch, title="How Helpful Was the Chatbot?",
                                 palette=C.DIVERGING_PALETTE, height=360),
                         use_container_width=True)

        # Chatbot use by demographics
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("#### Chatbot Usage by Demographics")
        demo_chat = st.selectbox("Select demographic variable:",
                                 ["F_AGECAT", "F_GENDER", "F_EDUCCAT", "F_RACETHNMOD",
                                  "F_PARTYSUM_FINAL"],
                                 format_func=lambda x: C.DEMO_LABELS.get(x, x),
                                 key="chat_demo")
        ct_chat = weighted_crosstab(df, "CHATUSE_W152", demo_chat,
                                    C.CHATUSE_VALUES, C.DEMO_VALUES[demo_chat])
        fig_chat = make_heatmap(ct_chat, f"Chatbot Usage × {C.DEMO_LABELS[demo_chat]}")
        st.plotly_chart(fig_chat, use_container_width=True)

    # ── Tab 6: Regulation & Trust ────────────────────────────────────────────
    with tabs[5]:
        r1, r2 = st.columns(2)
        pdata_reg = weighted_pct(df["AIREG_W152"], df[W], C.AIREG_VALUES)
        r1.plotly_chart(make_bar(pdata_reg, title="Should government regulate AI more or less?",
                                palette=[C.COLORS["primary"], C.COLORS["neutral"],
                                         C.COLORS["secondary"]], height=380),
                        use_container_width=True)

        pdata_trust = weighted_pct(df["TRSTAIPRS_W152"], df[W], C.TRSTAIPRS_VALUES)
        r2.plotly_chart(make_bar(pdata_trust,
                                title="Trust companies developing AI to act responsibly?",
                                palette=[C.COLORS["accent3"], C.COLORS["accent1"],
                                         C.COLORS["secondary"]], height=380),
                        use_container_width=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("#### Confidence in Government vs. Industry Managing AI")
        fig_rc = make_horizontal_stacked_bar(
            C.REGCONF_ITEMS, C.REGCONF_VALUES,
            "Confidence in Responsible AI Management",
            palette=C.PLOTLY_PALETTE[:6])
        st.plotly_chart(fig_rc, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: DRIVING SAFETY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Driving Safety":
    st.markdown("""
    <div class="header-gradient">
        <h1>Driving Safety — American Perceptions</h1>
        <p>Driving frequency, perceived hazards, safety changes, and road rage</p>
    </div>
    """, unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    pdata_dr1 = weighted_pct(df["DRIVE1_W152"], df[W], C.DRIVE1_VALUES)
    d1.plotly_chart(make_bar(pdata_dr1, title="How often do you drive?",
                             palette=C.PLOTLY_PALETTE, height=380),
                    use_container_width=True)

    pdata_dr3 = weighted_pct(df["DRIVE3_W152"], df[W], C.DRIVE3_VALUES)
    d2.plotly_chart(make_bar(pdata_dr3,
                             title="How has driving safety changed in the last 5 years?",
                             palette=C.DIVERGING_PALETTE, height=380),
                    use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Driving hazards stacked bar
    st.markdown("#### Perceived Driving Hazards")
    fig_dh = make_horizontal_stacked_bar(
        C.DRIVE2_ITEMS, C.DRIVE2_VALUES,
        "How much of a problem are these driving behaviors?",
        palette=[C.COLORS["secondary"], C.COLORS["accent1"], C.COLORS["accent3"]])
    st.plotly_chart(fig_dh, use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Road rage
    rd1, rd2 = st.columns([1, 1])
    pdata_rage = weighted_pct(df["DRIVER_W152"], df[W], C.DRIVER_VALUES)
    rd1.plotly_chart(make_bar(pdata_rage, title="How often do you witness road rage?",
                              height=380),
                     use_container_width=True)

    # Road rage by age
    ct_rage = weighted_crosstab(df, "DRIVER_W152", "F_AGECAT",
                                C.DRIVER_VALUES, C.DEMO_VALUES["F_AGECAT"])
    rd2.plotly_chart(make_heatmap(ct_rage, "Road Rage Frequency × Age Group"),
                     use_container_width=True)

    # Safety change by party
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### Safety Perceptions by Demographics")
    demo_drv = st.selectbox("Select demographic:",
                            ["F_AGECAT", "F_GENDER", "F_EDUCCAT",
                             "F_PARTYSUM_FINAL", "F_USR_SELFID", "F_CREGION"],
                            format_func=lambda x: C.DEMO_LABELS.get(x, x),
                            key="drive_demo")
    ct_safe = weighted_crosstab(df, "DRIVE3_W152", demo_drv,
                                C.DRIVE3_VALUES, C.DEMO_VALUES[demo_drv])
    fig_safe = px.bar(ct_safe, x="demo_label", y="pct", color="q_label",
                      barmode="group", color_discrete_sequence=C.DIVERGING_PALETTE,
                      title=f"Perceived Safety Change × {C.DEMO_LABELS[demo_drv]}",
                      height=420, text="pct")
    fig_safe.update_traces(texttemplate="%{text:.0f}%", textposition="outside",
                           marker_line_width=0)
    fig_safe.update_layout(
        font_family="Inter", font_color="#2D3436",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=16, title_x=0,
        xaxis_title="", yaxis_title="Weighted %",
        legend=dict(orientation="h", yanchor="bottom", y=-0.28,
                    xanchor="center", x=0.5, font_size=11, title_text=""),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    st.plotly_chart(fig_safe, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: CROSS-TABULATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Cross-Tabulations":
    st.markdown("""
    <div class="header-gradient">
        <h1>Interactive Cross-Tabulations</h1>
        <p>Explore any survey question by any demographic variable — weighted percentages &amp; heatmaps</p>
    </div>
    """, unsafe_allow_html=True)

    # Build combined question list
    all_questions = {}
    all_question_values = {}
    for name, (items, vals) in {**C.AI_BATTERIES, **C.DRIVING_BATTERIES}.items():
        for col, lbl in items.items():
            all_questions[col] = f"[{name}] {lbl}"
            all_question_values[col] = vals
    for col, lbl in {**C.AI_SINGLE_QUESTIONS, **C.DRIVING_SINGLE_QUESTIONS}.items():
        all_questions[col] = lbl
        all_question_values[col] = {**C.AI_SINGLE_VALUES, **C.DRIVING_SINGLE_VALUES}.get(col, {})

    ct1, ct2 = st.columns(2)
    sel_q = ct1.selectbox("Select survey question:",
                          list(all_questions.keys()),
                          format_func=lambda x: all_questions[x],
                          key="xtab_q")
    sel_d = ct2.selectbox("Select demographic variable:",
                          list(C.DEMO_LABELS.keys()),
                          format_func=lambda x: C.DEMO_LABELS[x],
                          key="xtab_d")

    q_vals = all_question_values.get(sel_q, {})
    d_vals = C.DEMO_VALUES.get(sel_d, {})

    if q_vals and d_vals and sel_q in df.columns and sel_d in df.columns:
        ct_data = weighted_crosstab(df, sel_q, sel_d, q_vals, d_vals)
        if not ct_data.empty:
            ht1, ht2 = st.columns(2)
            fig_hm = make_heatmap(ct_data,
                                  f"{all_questions[sel_q]} × {C.DEMO_LABELS[sel_d]}",
                                  height=max(360, len(q_vals)*45+120))
            ht1.plotly_chart(fig_hm, use_container_width=True)

            fig_gb = px.bar(ct_data, x="demo_label", y="pct", color="q_label",
                            barmode="group", text="pct",
                            color_discrete_sequence=C.PLOTLY_PALETTE,
                            title="Grouped Bar View", height=max(360, len(q_vals)*45+120))
            fig_gb.update_traces(texttemplate="%{text:.0f}%", textposition="outside",
                                 marker_line_width=0)
            fig_gb.update_layout(
                font_family="Inter", font_color="#2D3436",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                title_font_size=16, title_x=0,
                xaxis_title="", yaxis_title="Weighted %",
                legend=dict(orientation="h", yanchor="bottom", y=-0.30,
                            xanchor="center", x=0.5, font_size=11, title_text=""),
                margin=dict(l=40, r=20, t=50, b=40),
            )
            ht2.plotly_chart(fig_gb, use_container_width=True)

            # Show data table
            with st.expander("📄 View data table"):
                pivot_display = ct_data.pivot_table(
                    index="q_label", columns="demo_label", values="pct", aggfunc="first"
                )
                st.dataframe(pivot_display.style.format("{:.1f}%").background_gradient(
                    cmap="YlGnBu", axis=None), use_container_width=True)
        else:
            st.warning("No data available for this combination.")
    else:
        st.info("Select a question and a demographic variable to begin.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: STATISTICAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Statistical Analysis":
    st.markdown("""
    <div class="header-gradient">
        <h1>Statistical Analysis</h1>
        <p>Chi-square tests of independence, Cramér's V effect sizes, weighted proportions with 95% CIs</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Section 1: Automated Chi-Square Battery ──────────────────────────────
    st.subheader("Chi-Square Tests of Independence")
    st.markdown("""
    Testing whether responses to key survey questions differ significantly across
    demographic groups. **Cramér's V** quantifies the effect size:
    ≤ 0.10 *negligible*, 0.10–0.30 *small*, 0.30–0.50 *medium*, > 0.50 *large*.
    """)

    test_questions = {
        "CNCEXC_W152": ("More concerned or excited about AI?", C.CNCEXC_VALUES),
        "USEAI_W152": ("Ever use AI-based tools?", C.USEAI_VALUES),
        "AIREG_W152": ("Should government regulate AI?", C.AIREG_VALUES),
        "PERSBENHRM_W152": ("Will AI benefit or harm you?", C.PERSBENHRM_VALUES),
        "CHATUSE_W152": ("Ever used a chatbot?", C.CHATUSE_VALUES),
        "DRIVE3_W152": ("Driving safety changed in 5 yrs?", C.DRIVE3_VALUES),
    }
    test_demos = ["F_AGECAT", "F_GENDER", "F_EDUCCAT", "F_PARTYSUM_FINAL", "F_INC_TIER2"]

    chi2_results = []
    for q_col, (q_label, q_vals) in test_questions.items():
        for d_col in test_demos:
            if q_col not in df.columns or d_col not in df.columns:
                continue
            mask = (df[q_col].notna() & df[d_col].notna() &
                    (df[q_col] != C.REFUSED_CODE) & (df[d_col] != C.REFUSED_CODE))
            ct = pd.crosstab(df.loc[mask, q_col], df.loc[mask, d_col])
            if ct.shape[0] < 2 or ct.shape[1] < 2:
                continue
            chi2, p, dof, _ = chi2_contingency(ct)
            v = cramers_v(ct)
            sig = "★★★" if p < 0.001 else ("★★" if p < 0.01 else ("★" if p < 0.05 else "n.s."))
            effect = "Large" if v > 0.5 else ("Medium" if v > 0.3 else ("Small" if v > 0.1 else "Negligible"))
            chi2_results.append({
                "Question": q_label,
                "Demographic": C.DEMO_LABELS.get(d_col, d_col),
                "χ²": round(chi2, 2),
                "df": dof,
                "p-value": f"{p:.2e}" if p < 0.001 else f"{p:.4f}",
                "Cramér's V": round(v, 3),
                "Effect": effect,
                "Sig.": sig,
            })

    chi2_df = pd.DataFrame(chi2_results)
    if not chi2_df.empty:
        # Style the table
        def highlight_sig(val):
            if val == "★★★":
                return "color: #E8574A; font-weight: bold;"
            elif val == "★★":
                return "color: #F5A623; font-weight: bold;"
            elif val == "★":
                return "color: #00B894;"
            return "color: #636E72;"

        styled = chi2_df.style.applymap(highlight_sig, subset=["Sig."])
        st.dataframe(styled, use_container_width=True, height=500)

        # ── Summary heatmap of Cramér's V ────────────────────────────────────
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.subheader("Cramér's V Effect-Size Heatmap")
        v_pivot = chi2_df.pivot_table(index="Question", columns="Demographic",
                                       values="Cramér's V", aggfunc="first")
        fig_v = px.imshow(v_pivot, text_auto=".3f", aspect="auto",
                          color_continuous_scale=["#F8F9FA", "#F5A623", "#E8574A"],
                          title="Cramér's V — Strength of Association",
                          height=max(350, len(v_pivot) * 55 + 100))
        fig_v.update_layout(font_family="Inter", title_font_size=16, title_x=0,
                            margin=dict(l=20, r=20, t=50, b=40),
                            coloraxis_colorbar_title="V")
        st.plotly_chart(fig_v, use_container_width=True)

    # ── Section 2: Weighted Proportions with 95% CI ──────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.subheader("Weighted Proportions with 95% Confidence Intervals")

    ci_q = st.selectbox("Select question for CI analysis:",
                        list(test_questions.keys()),
                        format_func=lambda x: test_questions[x][0],
                        key="ci_q")
    q_label_ci, q_vals_ci = test_questions[ci_q]

    mask_ci = df[ci_q].notna() & (df[ci_q] != C.REFUSED_CODE)
    sub_ci = df[mask_ci]
    total_w_ci = sub_ci[W].sum()
    n_eff = total_w_ci**2 / (sub_ci[W]**2).sum()  # effective sample size

    ci_records = []
    for val, label in q_vals_ci.items():
        if val == C.REFUSED_CODE:
            continue
        sel = sub_ci[ci_q] == val
        p_hat = sub_ci.loc[sel, W].sum() / total_w_ci
        se = math.sqrt(p_hat * (1 - p_hat) / n_eff)
        ci_lo = max(0, p_hat - 1.96 * se)
        ci_hi = min(1, p_hat + 1.96 * se)
        ci_records.append({
            "Response": label,
            "Weighted %": round(p_hat * 100, 2),
            "SE": round(se * 100, 2),
            "95% CI Lower": round(ci_lo * 100, 2),
            "95% CI Upper": round(ci_hi * 100, 2),
            "Eff. N": round(n_eff, 0),
        })
    ci_df = pd.DataFrame(ci_records)
    st.dataframe(ci_df.style.format({
        "Weighted %": "{:.2f}%", "SE": "{:.2f}%",
        "95% CI Lower": "{:.2f}%", "95% CI Upper": "{:.2f}%",
        "Eff. N": "{:.0f}",
    }).background_gradient(subset=["Weighted %"], cmap="YlGnBu"),
                 use_container_width=True)

    # CI forest plot
    fig_ci = go.Figure()
    for i, row in ci_df.iterrows():
        fig_ci.add_trace(go.Scatter(
            x=[row["Weighted %"]], y=[row["Response"]],
            error_x=dict(type="data",
                         symmetric=False,
                         array=[row["95% CI Upper"] - row["Weighted %"]],
                         arrayminus=[row["Weighted %"] - row["95% CI Lower"]],
                         color=C.PLOTLY_PALETTE[i % len(C.PLOTLY_PALETTE)],
                         thickness=2.5, width=8),
            mode="markers",
            marker=dict(size=12, color=C.PLOTLY_PALETTE[i % len(C.PLOTLY_PALETTE)],
                        line=dict(width=1.5, color="white")),
            name=row["Response"],
            showlegend=False,
        ))
    fig_ci.update_layout(
        title=f"95% Confidence Intervals — {q_label_ci}",
        font_family="Inter", font_color="#2D3436",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=16, title_x=0,
        xaxis_title="Weighted %", yaxis_title="",
        margin=dict(l=20, r=40, t=50, b=40),
        height=max(280, len(ci_df) * 60 + 100),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
    )
    st.plotly_chart(fig_ci, use_container_width=True)

    # ── Section 3: Custom chi-square test ────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.subheader("Custom Chi-Square Test")

    all_q_for_test = {**C.AI_SINGLE_QUESTIONS, **C.DRIVING_SINGLE_QUESTIONS}
    for _, (items, _) in {**C.AI_BATTERIES, **C.DRIVING_BATTERIES}.items():
        for col, lbl in items.items():
            all_q_for_test[col] = lbl

    cq1, cq2 = st.columns(2)
    custom_q = cq1.selectbox("Question variable:",
                             [c for c in all_q_for_test if c in df.columns],
                             format_func=lambda x: all_q_for_test.get(x, x),
                             key="custom_chi_q")
    custom_d = cq2.selectbox("Demographic variable:",
                             [c for c in C.DEMO_LABELS if c in df.columns],
                             format_func=lambda x: C.DEMO_LABELS.get(x, x),
                             key="custom_chi_d")

    if custom_q and custom_d:
        mask_cust = (df[custom_q].notna() & df[custom_d].notna() &
                     (df[custom_q] != C.REFUSED_CODE) & (df[custom_d] != C.REFUSED_CODE))
        ct_cust = pd.crosstab(df.loc[mask_cust, custom_q], df.loc[mask_cust, custom_d])
        if ct_cust.shape[0] >= 2 and ct_cust.shape[1] >= 2:
            chi2_c, p_c, dof_c, expected = chi2_contingency(ct_cust)
            v_c = cramers_v(ct_cust)
            effect_c = "Large" if v_c > 0.5 else ("Medium" if v_c > 0.3 else (
                "Small" if v_c > 0.1 else "Negligible"))

            rc1, rc2, rc3, rc4 = st.columns(4)
            rc1.metric("χ² Statistic", f"{chi2_c:.2f}")
            rc2.metric("Degrees of Freedom", f"{dof_c}")
            rc3.metric("p-value", f"{p_c:.2e}" if p_c < 0.001 else f"{p_c:.4f}")
            rc4.metric("Cramér's V", f"{v_c:.3f} ({effect_c})")

            with st.expander("📋 Observed contingency table"):
                st.dataframe(ct_cust, use_container_width=True)
            with st.expander("📋 Expected frequencies"):
                exp_df = pd.DataFrame(expected, index=ct_cust.index, columns=ct_cust.columns)
                st.dataframe(exp_df.round(1), use_container_width=True)
        else:
            st.warning("Not enough categories to perform chi-square test.")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#636E72; font-size:0.78rem;'>"
    "Data: Pew Research Center, American Trends Panel Wave 152 · Aug 2024 · "
    "Dashboard built for research purposes only — not for redistribution of raw data."
    "</div>",
    unsafe_allow_html=True,
)
