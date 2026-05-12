import streamlit as st
import pandas as pd
import folium
import math
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium

# Corporate Branding
st.set_page_config(page_title="Engro Agri-Logistics Engine", page_icon="🚜", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2e8b57;'>Engro Eximp: Agri-Logistics & Supply Chain Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Dynamic Route Calculation & Freight Manifest Generation</p>", unsafe_allow_html=True)
st.divider()

st.info("💡 **Operational Goal:** Optimize freight routing for Engro Fertilizers and Eximp commodities, reducing fuel expenditure and improving regional delivery ETAs.")

# --- Core Math: Haversine Formula ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- Dummy Data Generation ---
def generate_farm_data(num_farms=8):
    hub_lat, hub_lon = 31.7167, 73.9850 # Sheikhupura Hub
    np.random.seed(42)
    lats = hub_lat + np.random.uniform(-0.15, 0.15, num_farms)
    lons = hub_lon + np.random.uniform(-0.15, 0.15, num_farms)
    volumes = np.random.randint(5, 40, num_farms) # Changed to Tons
    
    data = {
        'Center_ID': ['Central Silo (Hub)'] + [f'Agri_Sector_{i}' for i in range(1, num_farms)],
        'Latitude': [hub_lat] + list(lats[1:]),
        'Longitude': [hub_lon] + list(lons[1:]),
        'Commodity_Volume_Tons': [0] + list(volumes[1:]),
        'Type': ['Hub'] + ['Collection Center'] * (num_farms - 1)
    }
    return pd.DataFrame(data)

# --- Initialize Session State ---
if 'farm_df' not in st.session_state:
    st.session_state.farm_df = generate_farm_data(8)
if 'last_added_coord' not in st.session_state:
    st.session_state.last_added_coord = None

# --- Routing Logic ---
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

# --- Sidebar Controls ---
st.sidebar.header("Fleet & Cost Parameters")

if st.sidebar.button("🔄 Reset Map Data", use_container_width=True):
    st.session_state.farm_df = generate_farm_data(np.random.randint(6, 15))
    st.session_state.last_added_coord = None
    st.rerun()

st.sidebar.markdown("---")
truck_capacity = st.sidebar.number_input("Truck Capacity (Tons)", value=150, step=10)
truck_speed_kmh = st.sidebar.slider("Avg Truck Speed (km/h)", 20, 80, 40)
fuel_efficiency = st.sidebar.number_input("Fuel Efficiency (km per Liter)", value=4.5, step=0.5)
diesel_price = st.sidebar.number_input("Diesel Price (PKR/Liter)", value=290, step=5)

# --- Main Layout Calculations ---
df_centers = st.session_state.farm_df
optimized_indices, total_route_km = calculate_optimal_route(df_centers)
df_route = df_centers.iloc[optimized_indices].reset_index(drop=True)

total_volume = df_centers['Commodity_Volume_Tons'].sum()
est_hours = total_route_km / truck_speed_kmh
total_fuel_cost = (total_route_km / fuel_efficiency) * diesel_price

# --- Top Metrics Row ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Commodity Volume", f"{total_volume:,} Tons", "Capacity OK" if total_volume <= truck_capacity else "OVERLOADED", delta_color="inverse" if total_volume > truck_capacity else "normal")
m2.metric("Total Route Distance", f"{total_route_km:.1f} km")
m3.metric("Est. Driving Time", f"{est_hours:.1f} hrs")
m4.metric("Est. Fuel Cost", f"Rs. {total_fuel_cost:,.0f}")

st.markdown("---")

# --- Map & Data Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    tab1, tab2 = st.tabs(["🗺️ Interactive Map (Click to Add)", "📸 Exportable Map (Download Picture)"])
    
    with tab1:
        hub_lat, hub_lon = df_centers.iloc[0]['Latitude'], df_centers.iloc[0]['Longitude']
        m = folium.Map(location=[hub_lat, hub_lon], zoom_start=11, tiles="CartoDB positron")
        
        route_coords = df_route[['Latitude', 'Longitude']].values.tolist()
        folium.PolyLine(locations=route_coords, color="#27AE60", weight=4, opacity=0.8).add_to(m)
        
        for idx, row in df_centers.iterrows():
            is_hub = row['Type'] == 'Hub'
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=9 if is_hub else 6,
                popup=folium.Popup(f"<b>{row['Center_ID']}</b><br>Volume: {row['Commodity_Volume_Tons']} Tons", max_width=200),
                color="#E74C3C" if is_hub else "#2980B9",
                fill=True,
                fill_color="#E74C3C" if is_hub else "#2980B9",
                fill_opacity=1
            ).add_to(m)

        map_data = st_folium(m, width=800, height=500, key="routing_map")
        
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
            color_discrete_sequence=["#2E86C1"], zoom=10, height=500
        )
        fig.add_scattermapbox(
            lat=df_centers["Latitude"], lon=df_centers["Longitude"],
            hovertext=df_centers["Center_ID"],
            marker=dict(
                size=[15 if t == 'Hub' else 10 for t in df_centers['Type']],
                color=['red' if t == 'Hub' else '#F39C12' for t in df_centers['Type']]
            )
        )
        fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Logistics Route Manifest")
    st.dataframe(df_route[['Center_ID', 'Commodity_Volume_Tons']], use_container_width=True, hide_index=True, height=400)
    
    csv_data = df_route.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Manifest (CSV)",
        data=csv_data,
        file_name='engro_eximp_route_plan.csv',
        mime='text/csv',
        use_container_width=True
    )
