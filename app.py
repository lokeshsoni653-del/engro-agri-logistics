import streamlit as st
import pandas as pd
import folium
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
 
# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Engro Agri-Logistics Engine | Supply Chain Optimizer",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ═══════════════════════════════════════════════════════════════
#  DESIGN TOKENS & GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
 
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
 
/* ── Root Variables (Dark Green Agriculture Theme) ── */
:root {
    --forest-950:   #05120A;
    --forest-900:   #0A1E12;
    --forest-800:   #0F2A1A;
    --forest-700:   #143622;
    --forest-600:   #1A4529;
    --slate-900:    #0F172A;
    --slate-800:    #1E293B;
    --slate-700:    #334155;
    --slate-600:    #475569;
    --slate-400:    #94A3B8;
    --slate-300:    #CBD5E1;
    --emerald-500:  #10B981;
    --emerald-400:  #34D399;
    --emerald-300:  #6EE7B7;
    --lime-500:     #84CC16;
    --lime-400:     #A3E635;
    --amber-500:    #F59E0B;
    --amber-400:    #FBBF24;
    --red-500:      #EF4444;
    --red-400:      #F87171;
    --blue-500:     #3B82F6;
    --text-pri:     #F1F5F9;
    --text-sec:     #94A3B8;
    --text-mut:     #64748B;
    --border:       rgba(16,185,129,0.12);
    --border-md:    rgba(16,185,129,0.18);
    --r-xl: 16px;
    --r-lg: 12px;
    --r-md: 8px;
    --shadow: 0 4px 28px rgba(0,0,0,0.5), 0 1px 6px rgba(0,0,0,0.4);
}
 
/* ── App Background (Dark Forest Gradient) ── */
.stApp {
    background: linear-gradient(155deg, #05120A 0%, #0A1E12 35%, #0F2A1A 70%, #0A1E12 100%);
    font-family: 'Outfit', system-ui, sans-serif;
}
 
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1E12 0%, #05120A 100%) !important;
    border-right: 1px solid var(--border-md) !important;
}
[data-testid="stSidebar"] * { color: var(--text-sec) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--text-pri) !important; }
[data-testid="stSidebar"] .stSlider > label,
[data-testid="stSidebar"] .stNumberInput > label { 
    color: var(--text-sec) !important; 
    font-size: 0.75rem !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.07em; 
}
[data-testid="stSidebar"] hr { border-color: var(--border-md) !important; }
 
/* ── Slider emerald thumb ── */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--emerald-400) !important;
    box-shadow: 0 0 10px rgba(16,185,129,0.6) !important;
}
 
/* ── Number inputs ── */
[data-testid="stNumberInput"] input {
    background: rgba(15,42,26,0.5) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-pri) !important;
}
 
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(16,185,129,0.04) !important;
    border-bottom: 1px solid var(--border-md) !important;
    border-radius: var(--r-lg) var(--r-lg) 0 0 !important;
    padding: 0 8px !important;
    gap: 6px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: var(--text-mut) !important;
    padding: 11px 20px !important;
    border-radius: var(--r-md) var(--r-md) 0 0 !important;
    letter-spacing: 0.03em !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--emerald-400) !important;
    background: rgba(16,185,129,0.08) !important;
    border-bottom: 2px solid var(--emerald-400) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-xl) var(--r-xl) !important;
    padding: 24px !important;
}
 
/* ── Plotly charts transparent ── */
.js-plotly-plot .plotly { background: transparent !important; }
 
/* ── Metrics (Green Agriculture Theme) ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(10,30,18,0.9) 0%, rgba(15,42,26,0.8) 100%) !important;
    border: 1px solid var(--border-md) !important;
    border-radius: var(--r-xl) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow) !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--emerald-500), var(--lime-500));
}
[data-testid="stMetricLabel"] > div {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 800 !important;
    color: var(--text-mut) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.10em !important;
}
[data-testid="stMetricValue"] > div {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: var(--text-pri) !important;
    letter-spacing: -0.03em !important;
}
[data-testid="stMetricDelta"] > div {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"][data-color="positive"] { color: var(--emerald-400) !important; }
[data-testid="stMetricDelta"][data-color="negative"] { color: var(--red-400) !important; }
 
/* ── st.info ── */
[data-testid="stInfo"] {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(110,231,183,0.2) !important;
    border-radius: var(--r-lg) !important;
    color: var(--emerald-300) !important;
    font-size: 0.85rem !important;
    padding: 14px 18px !important;
}
 
/* ── Buttons (Emerald Accent) ── */
.stButton > button {
    background: linear-gradient(135deg, var(--emerald-500), var(--lime-500)) !important;
    color: #05120A !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.8rem !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 11px 24px !important;
    box-shadow: 0 2px 14px rgba(16,185,129,0.4) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    box-shadow: 0 4px 26px rgba(16,185,129,0.6) !important;
    transform: translateY(-1px) !important;
}
 
/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(16,185,129,0.12) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    color: var(--emerald-300) !important;
    font-weight: 700 !important;
    border-radius: var(--r-md) !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(16,185,129,0.18) !important;
    border-color: var(--emerald-400) !important;
}
 
/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
}
 
/* ── Markdown text ── */
.main [data-testid="stMarkdownContainer"] h1,
.main [data-testid="stMarkdownContainer"] h2,
.main [data-testid="stMarkdownContainer"] h3,
.main [data-testid="stMarkdownContainer"] h4 { 
    color: var(--text-pri) !important; 
    font-weight: 800 !important;
}
.main [data-testid="stMarkdownContainer"] p,
.main [data-testid="stMarkdownContainer"] li { color: var(--text-sec) !important; }
.main [data-testid="stMarkdownContainer"] strong { color: var(--emerald-400) !important; }
.main [data-testid="stMarkdownContainer"] code {
    background: rgba(16,185,129,0.1) !important;
    color: var(--emerald-300) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.80em !important;
    padding: 2px 7px !important;
}
 
/* ── Divider ── */
hr { border-color: var(--border-md) !important; }
 
/* ── Column gaps ── */
[data-testid="column"] { padding: 0 6px !important; }
 
/* ── Subheader text ── */
[data-testid="stSubheader"] { color: var(--text-pri) !important; font-weight: 800 !important; }
 
/* ── Fade-up animation for metrics ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stMetric"] {
    animation: fadeUp 0.5s ease both;
}
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.05s; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.10s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.15s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.20s; }
</style>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  PLOTLY THEME HELPER
# ═══════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    font_family="Outfit, system-ui, sans-serif",
    font_color="#94A3B8",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=35, b=10),
    legend=dict(
        bgcolor="rgba(16,185,129,0.05)",
        bordercolor="rgba(16,185,129,0.15)",
        borderwidth=1,
        font=dict(color="#CBD5E1", size=11),
    ),
    title_font=dict(size=13, color="#F1F5F9", family="Outfit"),
    xaxis=dict(
        gridcolor="rgba(16,185,129,0.06)",
        linecolor="rgba(16,185,129,0.1)",
        tickfont=dict(color="#64748B", size=10),
        showgrid=False,
    ),
    yaxis=dict(
        gridcolor="rgba(16,185,129,0.06)",
        linecolor="rgba(16,185,129,0.1)",
        tickfont=dict(color="#64748B", size=10),
        showgrid=False,
    ),
    colorway=["#10B981", "#84CC16", "#34D399", "#F59E0B", "#3B82F6"],
)
EMERALD = "#10B981"
LIME    = "#84CC16"
GREEN   = "#34D399"
ORANGE  = "#F59E0B"
 
# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(16,185,129,0.10) 0%, rgba(10,30,18,0.7) 100%);
    border: 1px solid rgba(16,185,129,0.18);
    border-left: 4px solid #10B981;
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 28px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 14px;
">
    <div>
        <div style="font-family:'Outfit',sans-serif; font-size:1.85rem; font-weight:900;
                    color:#F1F5F9; letter-spacing:-0.03em; line-height:1.1; margin-bottom:6px;">
            🚜 Engro Eximp: Agri-Logistics &amp; Supply Chain Optimizer
        </div>
        <div style="font-family:'Outfit',sans-serif; font-size:0.88rem; color:#94A3B8; line-height:1.5;">
            Dynamic Route Calculation &amp; Freight Manifest Generation
        </div>
    </div>
    <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
        <span style="
            font-family:'Outfit',sans-serif; font-size:0.70rem; font-weight:800;
            color:#34D399; background:rgba(16,185,129,0.12); border:1px solid rgba(110,231,183,0.25);
            padding:6px 14px; border-radius:99px; text-transform:uppercase; letter-spacing:.10em;
            display:flex; align-items:center; gap:6px;">
            <span style="width:6px;height:6px;background:#34D399;border-radius:50%;
                         box-shadow:0 0 8px #34D399;display:inline-block"></span>
            Enterprise Platform
        </span>
        <span style="
            font-family:'Outfit',sans-serif; font-size:0.70rem; font-weight:800;
            color:#84CC16; background:rgba(132,204,22,0.10); border:1px solid rgba(163,230,53,0.25);
            padding:6px 14px; border-radius:99px; letter-spacing:.05em;">
            Optimized for Engro Fertilizers &amp; Eximp
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
 
st.info("💡 **Operational Goal:** Optimize freight routing for Engro Fertilizers and Eximp commodities, reducing fuel expenditure and improving regional delivery ETAs.")
 
# ═══════════════════════════════════════════════════════════════
#  CORE MATH: HAVERSINE (unchanged)
# ═══════════════════════════════════════════════════════════════
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
 
# ═══════════════════════════════════════════════════════════════
#  DUMMY DATA GENERATION (unchanged)
# ═══════════════════════════════════════════════════════════════
def generate_farm_data(num_farms=8):
    hub_lat, hub_lon = 31.7167, 73.9850  # Sheikhupura Hub
    np.random.seed(42)
    lats = hub_lat + np.random.uniform(-0.15, 0.15, num_farms)
    lons = hub_lon + np.random.uniform(-0.15, 0.15, num_farms)
    volumes = np.random.randint(5, 40, num_farms)
    
    data = {
        'Center_ID': ['Central Silo (Hub)'] + [f'Agri_Sector_{i}' for i in range(1, num_farms)],
        'Latitude': [hub_lat] + list(lats[1:]),
        'Longitude': [hub_lon] + list(lons[1:]),
        'Commodity_Volume_Tons': [0] + list(volumes[1:]),
        'Type': ['Hub'] + ['Collection Center'] * (num_farms - 1)
    }
    return pd.DataFrame(data)
 
# ═══════════════════════════════════════════════════════════════
#  SESSION STATE (unchanged)
# ═══════════════════════════════════════════════════════════════
if 'farm_df' not in st.session_state:
    st.session_state.farm_df = generate_farm_data(8)
if 'last_added_coord' not in st.session_state:
    st.session_state.last_added_coord = None
 
# ═══════════════════════════════════════════════════════════════
#  ROUTING LOGIC (unchanged)
# ═══════════════════════════════════════════════════════════════
def calculate_optimal_route(df):
    coords = df[['Latitude', 'Longitude']].values
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = haversine_distance(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            
    unvisited = list(range(1, n))
    current_node = 0 
    route = [current_node]
    total_km = 0.0
    
    while unvisited:
        nearest_node = min(unvisited, key=lambda x: dist_matrix[current_node][x])
        total_km += dist_matrix[current_node][nearest_node]
        route.append(nearest_node)
        unvisited.remove(nearest_node)
        current_node = nearest_node
        
    total_km += dist_matrix[current_node][0]
    route.append(0)
    return route, total_km
 
# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo area
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 18px;">
        <div style="font-size:2.8rem; margin-bottom:8px;">🚜</div>
        <div style="font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:900;
                    color:#F1F5F9; letter-spacing:-0.02em;">Engro Logistics</div>
        <div style="font-family:'Outfit',sans-serif; font-size:0.68rem; font-weight:800;
                    color:#10B981; text-transform:uppercase; letter-spacing:.14em;">Engine v2.3</div>
        <div style="margin-top:12px; padding:5px 14px; border-radius:99px;
                    background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2);
                    display:inline-block; font-size:0.68rem; font-weight:700; color:#34D399;">
            Sheikhupura Region
        </div>
    </div>
    <hr style="border-color:rgba(16,185,129,0.12); margin: 0 0 18px;">
    """, unsafe_allow_html=True)
 
    st.header("Fleet & Cost Parameters")
 
    if st.button("🔄 Reset Map Data", use_container_width=True):
        st.session_state.farm_df = generate_farm_data(np.random.randint(6, 15))
        st.session_state.last_added_coord = None
        st.rerun()
 
    st.markdown("---")
    
    truck_capacity  = st.number_input("Truck Capacity (Tons)", value=150, step=10)
    truck_speed_kmh = st.slider("Avg Truck Speed (km/h)", 20, 80, 40)
    fuel_efficiency = st.number_input("Fuel Efficiency (km per Liter)", value=4.5, step=0.5)
    diesel_price    = st.number_input("Diesel Price (PKR/Liter)", value=290, step=5)
 
    st.markdown("---")
 
    # Developer card
    st.markdown("""
    <div style="
        background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.15);
        border-radius:12px; padding:14px 16px; margin-top:6px;
    ">
        <div style="font-family:'Outfit',sans-serif; font-size:0.70rem; font-weight:800;
                    color:#10B981; text-transform:uppercase; letter-spacing:.10em; margin-bottom:6px;">
            Platform Engineer
        </div>
        <div style="font-family:'Outfit',sans-serif; font-size:0.88rem; font-weight:700;
                    color:#F1F5F9;">Lokesh Kumar</div>
        <div style="font-size:0.72rem; color:#94A3B8; margin-top:3px;">
            Supply Chain Analytics &amp; Optimization
        </div>
    </div>
    <div style="font-family:'Outfit',sans-serif; font-size:0.68rem; color:#64748B;
                margin-top:12px; padding-left:2px; line-height:1.6;">
        Real-world GPS math · Haversine Formula · No third-party APIs
    </div>
    """, unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  CALCULATIONS (unchanged logic)
# ═══════════════════════════════════════════════════════════════
df_centers = st.session_state.farm_df
optimized_indices, total_route_km = calculate_optimal_route(df_centers)
df_route = df_centers.iloc[optimized_indices].reset_index(drop=True)
 
total_volume     = df_centers['Commodity_Volume_Tons'].sum()
est_hours        = total_route_km / truck_speed_kmh
total_fuel_cost  = (total_route_km / fuel_efficiency) * diesel_price
is_overloaded    = total_volume > truck_capacity
 
# ═══════════════════════════════════════════════════════════════
#  TOP KPI METRICS
# ═══════════════════════════════════════════════════════════════
m1, m2, m3, m4 = st.columns(4)
 
with m1:
    delta_text = "⚠ OVERLOADED" if is_overloaded else "✓ Capacity OK"
    st.metric(
        "🌾 Total Commodity Volume",
        f"{total_volume:,} Tons",
        delta_text,
        delta_color="inverse" if is_overloaded else "normal"
    )
with m2:
    st.metric("🗺️ Total Route Distance", f"{total_route_km:.1f} km")
with m3:
    st.metric("⏱️ Est. Driving Time", f"{est_hours:.1f} hrs")
with m4:
    st.metric("⛽ Est. Fuel Cost", f"Rs. {total_fuel_cost:,.0f}")
 
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  MAIN LAYOUT: MAP + MANIFEST
# ═══════════════════════════════════════════════════════════════
col_map, col_manifest = st.columns([1.8, 1], gap="large")
 
with col_map:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:0.72rem; font-weight:800;
                color:#64748B; text-transform:uppercase; letter-spacing:.12em;
                margin:0 0 14px; padding-left:2px;">
        Route Visualization &amp; Interactive Planner
    </div>""", unsafe_allow_html=True)
 
    tab1, tab2 = st.tabs(["🗺️ Interactive Map (Click to Add)", "📸 Exportable Map (Download Picture)"])
    
    with tab1:
        hub_lat, hub_lon = df_centers.iloc[0]['Latitude'], df_centers.iloc[0]['Longitude']
        m = folium.Map(location=[hub_lat, hub_lon], zoom_start=11, tiles="CartoDB positron")
        
        route_coords = df_route[['Latitude', 'Longitude']].values.tolist()
        folium.PolyLine(locations=route_coords, color="#10B981", weight=4, opacity=0.85).add_to(m)
        
        for idx, row in df_centers.iterrows():
            is_hub = row['Type'] == 'Hub'
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=10 if is_hub else 7,
                popup=folium.Popup(f"<b style='color:#0F2A1A'>{row['Center_ID']}</b><br><span style='color:#10B981;font-weight:600'>Volume: {row['Commodity_Volume_Tons']} Tons</span>", max_width=220),
                color="#EF4444" if is_hub else "#10B981",
                fill=True,
                fill_color="#EF4444" if is_hub else "#10B981",
                fill_opacity=1
            ).add_to(m)
 
        map_data = st_folium(m, width="100%", height=480, key="routing_map")
        
        # Interactive click handler (unchanged)
        if map_data and map_data.get("last_clicked"):
            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lon = map_data["last_clicked"]["lng"]
            current_coord = (clicked_lat, clicked_lon)
            
            if current_coord != st.session_state.last_added_coord:
                new_id = f"Dynamic_Sector_{len(st.session_state.farm_df)}"
                new_row = pd.DataFrame({
                    'Center_ID': [new_id],
                    'Latitude': [clicked_lat],
                    'Longitude': [clicked_lon],
                    'Commodity_Volume_Tons': [np.random.randint(5, 30)],
                    'Type': ['Collection Center']
                })
                st.session_state.farm_df = pd.concat([st.session_state.farm_df, new_row], ignore_index=True)
                st.session_state.last_added_coord = current_coord
                st.rerun()
 
    with tab2:
        fig = px.line_mapbox(
            df_route, lat="Latitude", lon="Longitude", 
            hover_name="Center_ID", hover_data=["Commodity_Volume_Tons"],
            color_discrete_sequence=[EMERALD], zoom=10, height=480
        )
        fig.add_scattermapbox(
            lat=df_centers["Latitude"], lon=df_centers["Longitude"],
            hovertext=df_centers["Center_ID"],
            marker=dict(
                size=[16 if t == 'Hub' else 11 for t in df_centers['Type']],
                color=['#EF4444' if t == 'Hub' else '#84CC16' for t in df_centers['Type']]
            )
        )
        fig.update_layout(
            mapbox_style="carto-positron", 
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig, use_container_width=True)
 
with col_manifest:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:0.72rem; font-weight:800;
                color:#64748B; text-transform:uppercase; letter-spacing:.12em;
                margin:0 0 14px; padding-left:2px;">
        Logistics Route Manifest
    </div>""", unsafe_allow_html=True)
    
    st.dataframe(
        df_route[['Center_ID', 'Commodity_Volume_Tons']], 
        use_container_width=True, 
        hide_index=True, 
        height=340
    )
    
    csv_data = df_route.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Manifest (CSV)",
        data=csv_data,
        file_name='engro_eximp_route_plan.csv',
        mime='text/csv',
        use_container_width=True
    )
 
    # Additional stats card
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(10,30,18,0.5) 100%);
        border: 1px solid rgba(16,185,129,0.2); border-left: 3px solid #10B981;
        border-radius: 12px; padding: 16px 18px;
        font-family: 'Outfit', sans-serif;
    ">
        <div style="font-size:.72rem;font-weight:800;color:#64748B;
                    text-transform:uppercase;letter-spacing:.10em;margin-bottom:8px">
            📊 Route Performance Metrics
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
            <div>
                <div style="font-size:.68rem;color:#94A3B8;margin-bottom:3px">Avg. km per Center</div>
                <div style="font-size:1.15rem;font-weight:800;color:#34D399">{(total_route_km / len(df_centers)):.1f} km</div>
            </div>
            <div>
                <div style="font-size:.68rem;color:#94A3B8;margin-bottom:3px">Fuel Efficiency</div>
                <div style="font-size:1.15rem;font-weight:800;color:#84CC16">{fuel_efficiency} km/L</div>
            </div>
            <div>
                <div style="font-size:.68rem;color:#94A3B8;margin-bottom:3px">Centers Visited</div>
                <div style="font-size:1.15rem;font-weight:800;color:#F1F5F9">{len(df_centers)}</div>
            </div>
            <div>
                <div style="font-size:.68rem;color:#94A3B8;margin-bottom:3px">Tons per Hour</div>
                <div style="font-size:1.15rem;font-weight:800;color:#FBBF24">{(total_volume / est_hours):.1f}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
 
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  ADDITIONAL ANALYTICS SECTION
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="font-family:'Outfit',sans-serif; font-size:0.72rem; font-weight:800;
            color:#64748B; text-transform:uppercase; letter-spacing:.12em;
            margin:0 0 14px; padding-left:2px;">
    Supply Chain Analytics Dashboard
</div>""", unsafe_allow_html=True)
 
chart_col1, chart_col2 = st.columns(2, gap="large")
 
with chart_col1:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:.88rem; font-weight:800;
                color:#F1F5F9; margin-bottom:12px;">
        Commodity Volume by Collection Center
    </div>""", unsafe_allow_html=True)
    
    df_collection = df_centers[df_centers['Type'] == 'Collection Center'].copy()
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_collection['Center_ID'],
        y=df_collection['Commodity_Volume_Tons'],
        marker_color=EMERALD,
        marker_line_color=LIME,
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Volume: %{y} Tons<extra></extra>'
    ))
    fig_bar.update_layout(
        **PLOTLY_LAYOUT,
        height=280,
        xaxis_title="",
        yaxis_title="Volume (Tons)",
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
 
with chart_col2:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:.88rem; font-weight:800;
                color:#F1F5F9; margin-bottom:12px;">
        Cost Breakdown (PKR)
    </div>""", unsafe_allow_html=True)
    
    # Simple pie chart for cost breakdown
    cost_per_km = diesel_price / fuel_efficiency
    labor_estimate = est_hours * 500  # dummy labor cost
    other_costs = total_fuel_cost * 0.15  # 15% misc
    
    cost_df = pd.DataFrame({
        'Category': ['Fuel', 'Labor', 'Maintenance & Misc'],
        'Amount': [total_fuel_cost, labor_estimate, other_costs]
    })
    
    fig_pie = px.pie(
        cost_df, names='Category', values='Amount',
        hole=0.5,
        color='Category',
        color_discrete_map={
            'Fuel': EMERALD,
            'Labor': LIME,
            'Maintenance & Misc': ORANGE
        }
    )
    fig_pie.update_traces(
        textposition='outside', textinfo='label+percent',
        marker=dict(line=dict(color='rgba(0,0,0,0.3)', width=2)),
        hovertemplate="<b>%{label}</b><br>Rs. %{value:,.0f}<br>%{percent}<extra></extra>"
    )
    fig_pie.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=False,
        height=280,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
