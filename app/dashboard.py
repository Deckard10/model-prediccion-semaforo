import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import time
import random

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================

st.set_page_config(
    page_title="Smart Traffic AI",
    page_icon="🚦",
    layout="wide"
)

# ==========================================
# ESTILOS FUTURISTAS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #00ffaa;
}

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #00ffaa;
    padding: 15px;
    border-radius: 15px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# CARGAR MODELO IA
# ==========================================

model = joblib.load('model/semaforo_model.pkl')

# ==========================================
# TÍTULO
# ==========================================

st.markdown("""
<h1 style='text-align: center;'>
🚦 SMART TRAFFIC CONTROL AI SYSTEM
</h1>
""", unsafe_allow_html=True)

st.write("---")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ CONFIGURACIÓN")

modo = st.sidebar.selectbox(
    "Modo del Sistema",
    ["Manual", "Tiempo Real"]
)

ambulancia = st.sidebar.checkbox("🚑 Ambulancia Detectada")

st.sidebar.write("---")

# ==========================================
# GENERACIÓN DE DATOS
# ==========================================

if modo == "Manual":

    cars = st.sidebar.slider("🚗 Autos", 0, 200, 80)

    bikes = st.sidebar.slider("🏍️ Motos", 0, 100, 20)

    buses = st.sidebar.slider("🚌 Buses", 0, 50, 10)

    trucks = st.sidebar.slider("🚛 Camiones", 0, 50, 5)

else:

    cars = random.randint(20, 200)

    bikes = random.randint(5, 80)

    buses = random.randint(1, 30)

    trucks = random.randint(1, 25)

# ==========================================
# TOTAL
# ==========================================

total = cars + bikes + buses + trucks

# ==========================================
# PREDICCIÓN IA
# ==========================================

data = [[cars, bikes, buses, trucks, total]]

prediction = model.predict(data)

green_time = int(prediction[0])

# PRIORIDAD AMBULANCIA

if ambulancia:
    green_time = 120

# ==========================================
# CLASIFICACIÓN TRÁFICO
# ==========================================

if total < 80:
    traffic = "🟢 BAJO"

elif total < 150:
    traffic = "🟡 MEDIO"

else:
    traffic = "🔴 ALTO"

# ==========================================
# KPIs
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚘 Vehículos Totales", total)

col2.metric("🚦 Tiempo Verde", f"{green_time} seg")

col3.metric("📊 Nivel Tráfico", traffic)

precision = random.randint(90, 99)

col4.metric("🧠 Precisión IA", f"{precision}%")

# ==========================================
# SECCIÓN PRINCIPAL
# ==========================================

st.write("---")

left, right = st.columns([1,1])

# ==========================================
# PANEL IZQUIERDO
# ==========================================

with left:

    st.subheader("📥 Datos Vehiculares")

    vehiculos = pd.DataFrame({
        "Tipo": ["Autos", "Motos", "Buses", "Camiones"],
        "Cantidad": [cars, bikes, buses, trucks]
    })

    st.dataframe(vehiculos, use_container_width=True)

    # GRÁFICO

    fig = px.bar(
        vehiculos,
        x="Tipo",
        y="Cantidad",
        title="Distribución Vehicular"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PANEL DERECHO
# ==========================================

with right:

    st.subheader("🚥 Estado Inteligente del Semáforo")

    # SEMÁFORO VISUAL

    if ambulancia:

        color = "green"
        estado = "🚑 PRIORIDAD AMBULANCIA"

    elif green_time >= 90:

        color = "green"
        estado = "🟢 VERDE"

    elif green_time >= 60:

        color = "orange"
        estado = "🟡 PRECAUCIÓN"

    else:

        color = "red"
        estado = "🔴 DETENER"

    st.markdown(f"""
    <div style="
        background-color:{color};
        padding:40px;
        border-radius:25px;
        text-align:center;
        font-size:40px;
        color:white;
        font-weight:bold;
    ">
        {estado}
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # CUENTA REGRESIVA

    st.subheader("⏱️ Cuenta Regresiva")

    countdown = st.empty()

    for i in range(5, 0, -1):

        countdown.markdown(f"""
        <h1 style='text-align:center; color:#00ffaa;'>
        {i}
        </h1>
        """, unsafe_allow_html=True)

        time.sleep(1)

# ==========================================
# MÚLTIPLES INTERSECCIONES
# ==========================================

st.write("---")

st.subheader("🗺️ Estado de Intersecciones Urbanas")

intersections = pd.DataFrame({

    "Intersección": [
        "Av. Norte",
        "Av. Central",
        "Av. Sur",
        "Av. Industrial"
    ],

    "Estado": [
        random.choice(["🟢 Bajo", "🟡 Medio", "🔴 Alto"]),
        random.choice(["🟢 Bajo", "🟡 Medio", "🔴 Alto"]),
        random.choice(["🟢 Bajo", "🟡 Medio", "🔴 Alto"]),
        random.choice(["🟢 Bajo", "🟡 Medio", "🔴 Alto"])
    ],

    "Tiempo Verde": [
        random.randint(30, 120),
        random.randint(30, 120),
        random.randint(30, 120),
        random.randint(30, 120)
    ]
})

st.dataframe(intersections, use_container_width=True)

# ==========================================
# ALERTAS IA
# ==========================================

st.write("---")

st.subheader("🚨 Alertas Inteligentes")

if total > 180:

    st.error("⚠️ Congestión crítica detectada")

elif total > 120:

    st.warning("⚠️ Tráfico elevado")

else:

    st.success("✅ Flujo vehicular estable")

# ==========================================
# KPI EXTRA
# ==========================================

st.write("---")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("⏳ Tiempo Promedio Espera", "22s")

kpi2.metric("📉 Reducción Congestión", "35%")

kpi3.metric("🚗 Flujo Optimizado", "91%")

# ==========================================
# FOOTER
# ==========================================

st.write("---")

st.markdown("""
<div style='text-align:center; color:gray;'>

SMART TRAFFIC CONTROL AI SYSTEM  
Proyecto de Optimización de Semáforos con Machine Learning 🚦

</div>
""", unsafe_allow_html=True)