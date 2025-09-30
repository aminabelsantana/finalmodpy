# =========================================
# DASHBOARD - Marketing Campaign Analysis
# Grupo 2 - Talendig Data Science
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Configuración inicial

st.set_page_config(page_title="Proyecto Final Grupo 2", layout="wide")
st.title('📊 TALENDIG DATA SCIENCE ')
st.subheader('MODULO 3 - Proyecto Final - Grupo #2 ')

# 1. Cargar el dataset
# ================================
# CARGA Y PREPARACIÓN DE DATOS
# ================================
# Función para cargar y preparar los datos con cache
@st.cache_data
def cargar_datos(path: str):
    """
    Carga y prepara los datos para el dashboard

    Args:
        path (str): Ruta del archivo CSV

    Returns:
        pandas.DataFrame: DataFrame con datos procesados
    """
    # Carga el archivo Excel
    df = pd.read_csv(path, sep=';')

# upload_file = st.file_uploader("Seleccione el archivo a cargar:", type=["csv", "xlsx"])

# if upload_file is not None:
#     if upload_file.name.endswith(".csv"):
#         df = pd.read_csv(upload_file, sep=";")
#     else:
#         df = pd.read_excel(upload_file)

    # Vista previa
    st.subheader("Vista previa de los datos")
    st.write(df.head())

    # Resumen estadístico
    st.subheader("📑 Resumen estadístico")
    st.write(df.describe())

    # 2. Limpieza y columnas derivadas

    categorias = ["MntWines", "MntFruits", "MntMeatProducts",
                  "MntFishProducts", "MntSweetProducts", "MntGoldProds"]

    df["GastosTotalesMnt"] = df[categorias].sum(axis=1)
    df["Edad"] = 2025 - df["Year_Birth"]
    df["Numero_Hijos"] = df["Teenhome"] + df["Kidhome"]
    df["Gasto_Wine_Meat"] = df["MntWines"] + df["MntMeatProducts"]

    # 3. Gasto promedio por categoría

    st.header("📌 Gasto Promedio por Categoría")

    gasto_promedio = df[categorias].mean().sort_values(ascending=False).reset_index()
    gasto_promedio.columns = ["Categoria", "Promedio"]

    figg = px.bar(
        gasto_promedio,
        x="Categoria",
        y="Promedio",
        color="Categoria",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Ordenado de mayor a menor"
    )
    st.plotly_chart(figg, use_container_width=True)

    # Producto estrella
    producto_top = gasto_promedio.loc[gasto_promedio["Promedio"].idxmax(), "Categoria"]
    valor_top = gasto_promedio["Promedio"].max()
    st.write(f"🔝 El producto más comprado en promedio es: **{producto_top}** con un gasto máximo de **{valor_top:.2f}**")

    # 4. Relación Ingresos vs Vinos/Carne

    st.header("💰 Ingresos vs Gasto en Vinos y Carne")
    fig_ing = px.scatter(
        df, x="Income", y="Gasto_Wine_Meat", color="Education",
        size="Gasto_Wine_Meat", hover_data=["Marital_Status"],
        title="Relación entre ingresos y gasto en Vinos/Carne"
    )
    st.plotly_chart(fig_ing, use_container_width=True)

    # 5. Educación vs Gasto Total

    st.header("🎓 Educación vs Gasto Total")
    promedio_educacion = (
        df.groupby("Education")["GastosTotalesMnt"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_edu = px.bar(
        promedio_educacion,
        x="Education",
        y="GastosTotalesMnt",
        color="Education",
        title="Promedio de Gasto Total por Educación"
    )
    st.plotly_chart(fig_edu, use_container_width=True)

    # 6. Filtros dinámicos
    st.header("🔎 Filtrar Data a Demanda")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Seleccionar columna a filtrar", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Seleccionar valor", unique_values)
    filtered_df = df[df[selected_column] == selected_value]
    st.write(f"Total registros filtrados: {filtered_df[selected_column].count()}")
    st.dataframe(filtered_df)

    # 7. Auto-gráficos
    st.header("📈 Auto-Graficar Data")
    x_column = st.selectbox("Seleccionar columna X", columns, index=0)
    y_column = st.selectbox("Seleccionar columna Y", columns, index=1)
    chart_type = st.selectbox("Seleccionar tipo de gráfico", ["Scatter", "Line", "Bar", "Pie"])

    if st.button("Generar gráfico"):
        if chart_type == "Scatter":
            fig = px.scatter(df, x=x_column, y=y_column)
        elif chart_type == "Line":
            fig = px.line(df, x=x_column, y=y_column)
        elif chart_type == "Pie":
            fig = px.pie(df, values=y_column, names=x_column)
        else:
            fig = px.bar(df, x=x_column, y=y_column)
        st.plotly_chart(fig, use_container_width=True)

    # 8. Conclusión final

    st.header("📊 Conclusión Final")
    st.markdown(f"""
    - ✅ El producto estrella es: **{producto_top}**
    - 🎯 Segmentación por **ingresos, educación, género y número de hijos** es clave.
    - 🍷🥩 **Vinos y carnes dominan** el gasto.
    - 📢 El análisis de campañas permite optimizar futuras promociones.
    - 👥 El comportamiento de compra y visitas web ayuda a identificar clientes más activos y rentables.
    """)

# else:
#     st.warning("⚠️ Cargue un archivo CSV o Excel para iniciar el análisis.")


# Footer

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    padding: 10px 0;
}
.footer a:link, .footer a:visited {color: blue; text-decoration: underline;}
.footer a:hover, .footer a:active {color: red; text-decoration: underline;}
</style>

<div class="footer">
    <p>👨‍💻 GRUPO #2 | Integrantes: Angie / Joan Fernandez / Sebastián Bello / Amin Abel Santana</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
