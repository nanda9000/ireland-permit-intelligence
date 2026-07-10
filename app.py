import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page config ───
st.set_page_config(
    page_title="Ireland Work Permit Intelligence",
    page_icon="🇮🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { padding-top: 1rem; }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 1rem;
        color: #8B949E;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #00B4D8;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00B4D8;
        margin: 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8B949E;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #E6EDF3;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00B4D8;
        display: inline-block;
    }
    
    .insight-box {
        background: #161B22;
        border-left: 4px solid #00B4D8;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #C9D1D9;
        font-size: 0.95rem;
    }
    
    .search-result {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.5rem 0;
    }
    .company-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E6EDF3;
    }
    .company-detail {
        font-size: 0.9rem;
        color: #8B949E;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
        color: #8B949E;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #0D1117;
        border-bottom: 2px solid #00B4D8;
        color: #00B4D8;
    }
    
    div[data-testid="stDataFrame"] {
        border: 1px solid #30363D;
        border-radius: 8px;
    }

    .footer {
        text-align: center;
        color: #484F58;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #21262D;
    }
</style>
""", unsafe_allow_html=True)


# ─── Load data ───
@st.cache_data
def load_data():
    companies = pd.read_csv("companies_clean.csv")
    sectors = pd.read_csv("sectors_clean.csv")
    nationality = pd.read_csv("nationality_clean.csv")
    return companies, sectors, nationality

companies, sectors, nationality = load_data()

# ─── Hero header ───
st.markdown('<p class="hero-title">🇮🇪 Ireland Work Permit Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Official employment permit data — January to May 2026 — Department of Enterprise, Trade and Employment</p>', unsafe_allow_html=True)

# ─── KPI cards ───
total_permits = int(companies["total"].sum())
total_companies = len(companies)
total_nationalities = len(nationality)
total_sectors = len(sectors)
avg_approval = round(nationality["approval_rate"].mean(), 1)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_permits:,}</p>
        <p class="metric-label">Total Permits</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_companies:,}</p>
        <p class="metric-label">Companies</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_nationalities}</p>
        <p class="metric-label">Nationalities</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_sectors}</p>
        <p class="metric-label">Sectors</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{avg_approval}%</p>
        <p class="metric-label">Avg Approval Rate</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ───
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Company Explorer", "🎯 Your Chances"])

# ═══════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════
with tab1:
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<p class="section-title">Top 10 Sectors</p>', unsafe_allow_html=True)
        top_sectors = sectors.nlargest(10, "total")[["sector", "total"]].reset_index(drop=True)
        top_sectors = top_sectors.sort_values("total", ascending=True)
        fig1 = px.bar(top_sectors, x="total", y="sector", orientation="h",
                      color_discrete_sequence=["#00B4D8"], height=400)
        fig1.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                           font_color="#C9D1D9", xaxis_title="", yaxis_title="",
                           margin=dict(l=0, r=10, t=10, b=0))
        fig1.update_xaxes(showgrid=False)
        fig1.update_yaxes(showgrid=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        st.markdown('<p class="section-title">Top 10 Nationalities</p>', unsafe_allow_html=True)
        top_nat = nationality.nlargest(10, "issued")[["nationality", "issued"]].reset_index(drop=True)
        top_nat = top_nat.sort_values("issued", ascending=True)
        fig2 = px.bar(top_nat, x="issued", y="nationality", orientation="h",
                      color_discrete_sequence=["#0096C7"], height=400)
        fig2.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                           font_color="#C9D1D9", xaxis_title="", yaxis_title="",
                           margin=dict(l=0, r=10, t=10, b=0))
        fig2.update_xaxes(showgrid=False)
        fig2.update_yaxes(showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Key insights
    st.markdown('<p class="section-title">Key Insights</p>', unsafe_allow_html=True)
    
    col_i1, col_i2, col_i3 = st.columns(3)
    
    with col_i1:
        single_permit = len(companies[companies["total"] == 1])
        pct_single = round(single_permit / total_companies * 100)
        st.markdown(f"""
        <div class="insight-box">
            <strong>{pct_single}% of companies</strong> sponsored just 1 person. 
            Sponsorship isn't locked up by giants — thousands of smaller firms go through the process for the right hire.
        </div>
        """, unsafe_allow_html=True)
    
    with col_i2:
        top10_share = round(companies.nlargest(10, "total")["total"].sum() / total_permits * 100, 1)
        st.markdown(f"""
        <div class="insight-box">
            <strong>Top 10 companies hold just {top10_share}%</strong> of all permits.
            This is a long-tail market — your best odds may be with mid-sized sponsors, not household names.
        </div>
        """, unsafe_allow_html=True)
    
    with col_i3:
        health = sectors[sectors["sector"].str.contains("Health", case=False, na=False)]["total"].sum()
        health_pct = round(health / total_permits * 100, 1)
        st.markdown(f"""
        <div class="insight-box">
            <strong>Health & Social Work accounts for {health_pct}%</strong> of all permits — 
            driven by nursing and care worker shortages. IT & Communications is second at ~10%.
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════
# TAB 2: COMPANY EXPLORER
# ═══════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">Search Companies</p>', unsafe_allow_html=True)
    
    col_search, col_filter = st.columns([3, 1])
    
    with col_search:
        search = st.text_input(
            "Type a company name",
            placeholder="e.g. Google, TCS, Accenture, Dawn Meats...",
            label_visibility="collapsed"
        )
    
    with col_filter:
        size_options = ["All"] + sorted(companies["size_category"].unique().tolist())
        size_filter = st.selectbox("Size", size_options, label_visibility="collapsed")
    
    # Filter data
    filtered = companies.copy()
    
    if search:
        filtered = filtered[filtered["employer"].str.contains(search, case=False, na=False)]
    
    if size_filter != "All":
        filtered = filtered[filtered["size_category"] == size_filter]
    
    filtered = filtered.sort_values("total", ascending=False)
    
    # Results count
    st.markdown(f"**{len(filtered):,}** companies found", unsafe_allow_html=True)
    
    # Show top results as cards if searching
    if search and len(filtered) > 0 and len(filtered) <= 20:
        for _, row in filtered.head(10).iterrows():
            months_list = []
            for m in ["jan", "feb", "mar", "apr", "may"]:
                if row[m] > 0:
                    months_list.append(m.capitalize())
            active_months = ", ".join(months_list)
            
            st.markdown(f"""
            <div class="search-result">
                <span class="company-name">{row['employer']}</span><br>
                <span class="company-detail">
                    <strong>{int(row['total'])}</strong> permits &nbsp;|&nbsp; 
                    Active in: {active_months} &nbsp;|&nbsp;
                    Avg {row['avg_per_month']:.1f}/month &nbsp;|&nbsp;
                    {row['size_category']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show as table
        display_df = filtered[["employer", "total", "months_active", "avg_per_month", "size_category"]].copy()
        display_df.columns = ["Company", "Total Permits", "Months Active", "Avg/Month", "Size"]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )
    
    # Hidden gems section
    if not search:
        st.markdown('<p class="section-title">Hidden Gems — Consistent Mid-Size Sponsors</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
            Companies with 5–20 permits, active in 3+ months. They sponsor regularly but get fewer applicants than the big names.
        </div>
        """, unsafe_allow_html=True)
        
        gems = companies[
            (companies["total"].between(5, 20)) & 
            (companies["months_active"] >= 3)
        ].sort_values("total", ascending=False)
        
        gems_display = gems[["employer", "total", "months_active", "avg_per_month"]].copy()
        gems_display.columns = ["Company", "Total Permits", "Months Active", "Avg/Month"]
        st.dataframe(gems_display, use_container_width=True, hide_index=True, height=350)


# ═══════════════════════════════════════
# TAB 3: YOUR CHANCES
# ═══════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">Check Your Nationality</p>', unsafe_allow_html=True)
    
    # Nationality selector
    nat_list = nationality.sort_values("issued", ascending=False)["nationality"].tolist()
    selected_nat = st.selectbox(
        "Select your nationality",
        nat_list,
        index=nat_list.index("India") if "India" in nat_list else 0
    )
    
    # Get selected nationality data
    nat_data = nationality[nationality["nationality"] == selected_nat].iloc[0]
    
    # Display profile card
    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    
    with col_n1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{int(nat_data['issued']):,}</p>
            <p class="metric-label">Permits Issued</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_n2:
        color = "#27AE60" if nat_data['approval_rate'] >= 90 else "#F39C12" if nat_data['approval_rate'] >= 80 else "#E74C3C"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value" style="color: {color}">{nat_data['approval_rate']}%</p>
            <p class="metric-label">Approval Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_n3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{int(nat_data['refused'])}</p>
            <p class="metric-label">Refused</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_n4:
        rank = int(nationality.sort_values("issued", ascending=False).reset_index(drop=True).index[
            nationality.sort_values("issued", ascending=False)["nationality"] == selected_nat
        ][0]) + 1
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">#{rank}</p>
            <p class="metric-label">Rank by Volume</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Context insight
    if nat_data['approval_rate'] >= 90:
        verdict = f"Strong position — {selected_nat} nationals have a high approval rate of {nat_data['approval_rate']}%."
    elif nat_data['approval_rate'] >= 80:
        verdict = f"Good position — {selected_nat} nationals have a solid approval rate of {nat_data['approval_rate']}%, above the average."
    else:
        verdict = f"Challenging — {selected_nat} nationals face a {nat_data['refusal_rate']}% refusal rate. Strong employer backing and documentation are critical."
    
    st.markdown(f"""
    <div class="insight-box">
        {verdict} Out of {int(nat_data['total_decisions']):,} total decisions, {int(nat_data['issued']):,} were approved.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Approval rate comparison
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<p class="section-title">Approval Rates — Top Nations</p>', unsafe_allow_html=True)
        top_nat_rates = nationality[nationality["total_decisions"] >= 50].nlargest(15, "issued")[["nationality", "approval_rate"]].copy()
        top_nat_rates = top_nat_rates.sort_values("approval_rate", ascending=True)
        
        fig3 = px.bar(top_nat_rates, x="approval_rate", y="nationality", orientation="h",
                      color_discrete_sequence=["#27AE60"], height=400)
        fig3.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                           font_color="#C9D1D9", xaxis_title="", yaxis_title="",
                           margin=dict(l=0, r=10, t=10, b=0))
        fig3.update_xaxes(showgrid=False, range=[80, 100])
        fig3.update_yaxes(showgrid=False)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_right:
        st.markdown('<p class="section-title">Permits by Continent</p>', unsafe_allow_html=True)
        continent_data = nationality.groupby("continent")["issued"].sum().reset_index()
        continent_data = continent_data.sort_values("issued", ascending=True)
        
        fig4 = px.bar(continent_data, x="issued", y="continent", orientation="h",
                      color_discrete_sequence=["#0077B6"], height=400)
        fig4.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                           font_color="#C9D1D9", xaxis_title="", yaxis_title="",
                           margin=dict(l=0, r=10, t=10, b=0))
        fig4.update_xaxes(showgrid=False)
        fig4.update_yaxes(showgrid=False)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Full nationality table
    st.markdown('<p class="section-title">Full Nationality Breakdown</p>', unsafe_allow_html=True)
    nat_table = nationality[["nationality", "issued", "refused", "approval_rate", "refusal_rate", "pct_of_all_issued", "continent"]].copy()
    nat_table.columns = ["Nationality", "Issued", "Refused", "Approval %", "Refusal %", "% of All Permits", "Continent"]
    nat_table = nat_table.sort_values("Issued", ascending=False)
    st.dataframe(nat_table, use_container_width=True, hide_index=True, height=400)


# ─── Footer ───
st.markdown("""
<div class="footer">
    Data source: Department of Enterprise, Trade and Employment — Employment Permit Statistics 2026<br>
    Built by <strong style="color:#FFFFFF;">Nandakumar Balaji</strong> | 
    <a href="https://www.linkedin.com/in/nandakumar-balaji-890bba25b/" style="color: #00B4D8;">LinkedIn</a> | 
    <a href="https://github.com/nanda9000" style="color: #00B4D8;">GitHub</a>
</div>
""", unsafe_allow_html=True)
