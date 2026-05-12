# 🚜 Engro Eximp: Agri-Logistics & Supply Chain Optimizer

**Dynamic Route Calculation & Freight Manifest Generation**

### 📌 Overview
This project is a functional proof-of-concept web application designed to optimize agricultural commodity routing for large-scale supply chains like Engro Fertilizers and Engro Eximp. It calculates the most cost-effective paths for freight trucks navigating between regional agricultural sectors and centralized hubs.

### 🚀 Key Features
* **Dynamic Route Calculation:** Uses algorithmic logic to solve localized routing efficiency problems for commercial fleets.
* **Real-World GPS Math:** Implements the Haversine Formula to calculate actual Earth-surface distances without relying on expensive third-party APIs.
* **Live Financial Metrics:** Instantly calculates Estimated Driving Time and Total Fuel Cost based on adjustable fleet parameters (truck capacity, average speed, live diesel prices).
* **Interactive Cartography:** Supply chain managers can click directly on the interactive map to add new collection sectors, triggering real-time route recalculation.

### 💻 Technical Architecture
* **Frontend:** Streamlit (Python)
* **Geospatial Visualization:** Folium, Plotly Express
* **Core Logic:** Python math library for geospatial distance modeling.
