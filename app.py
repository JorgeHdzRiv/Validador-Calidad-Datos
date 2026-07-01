import streamlit as st
import pandas as pd
from src.validator import run_validation
import io

st.set_page_config(page_title="Data Quality Validator", layout="wide")

st.title("📊 Validador Automático de Calidad de Datos")

with st.sidebar:
    st.header("Carga de Datos")
    uploaded_file = st.file_uploader("Sube CSV o Excel", type=['csv', 'xlsx'])

if uploaded_file:
    # Lógica de carga
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        results = run_validation(df)

        if "error" in results:
            st.error(results["error"])
        else:
            # Layout profesional usando columnas para KPIs
            c1, c2, c3 = st.columns(3)
            c1.metric("Filas", results["num_rows"])
            c2.metric("Columnas", results["num_columns"])
            c3.metric("Duplicados", results["duplicates"])

            st.divider()

            # Organización por pestañas (Tabs) para no saturar la vista
            tab1, tab2, tab3 = st.tabs(["Nulos", "Tipos de Datos", "Estadísticas"])
            
            with tab1:
                st.write("Análisis de valores faltantes:")
                st.dataframe(results["missing_values"], width='stretch')
            
            with tab2:
                st.write("Esquema detectado:")
                st.dataframe(results["dtypes"], width='stretch')
                
            with tab3:
                st.write("Resumen numérico:")
                st.dataframe(results["stats"], width='stretch')

    except Exception as e:
        st.error(f"Error procesando archivo: {e}")