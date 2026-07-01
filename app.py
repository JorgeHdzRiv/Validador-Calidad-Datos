import streamlit as st
import pandas as pd
from src.validator import run_validation
from src.utils import generate_excel, generate_pdf

st.set_page_config(page_title="Data Quality Validator", layout="wide")

st.title("📊 Validador Automático de Calidad de Datos")

# Instrucciones
with st.expander("ℹ️ Cómo usar esta herramienta"):
    st.markdown("""
    1. **Sube tu archivo**: Haz clic en el botón de la barra lateral.
    2. **Auditoría automática**: La app detectará nulos, duplicados y tipos de datos.
    3. **Explora**: Revisa las pestañas de resultados.
    4. **Descarga**: Exporta el diagnóstico a Excel o PDF para tu reporte.
    """)

with st.sidebar:
    st.header("Carga de Datos")
    uploaded_file = st.file_uploader("Sube CSV o Excel", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        results = run_validation(df)

        if "error" in results:
            st.error(results["error"])
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Filas", results["num_rows"])
            c2.metric("Columnas", results["num_columns"])
            c3.metric("Duplicados", results["duplicates"])

            st.divider()

            tab1, tab2, tab3 = st.tabs(["Nulos", "Tipos de Datos", "Estadísticas"])
            with tab1: st.dataframe(results["missing_values"], width='stretch')
            with tab2: st.dataframe(results["dtypes"], width='stretch')
            with tab3: st.dataframe(results["stats"], width='stretch')

            # Zona de descarga
            st.subheader("📥 Descargar Reporte")
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.download_button(
                    label="Descargar en Excel",
                    data=generate_excel(results),
                    file_name="reporte_calidad.xlsx",
                    mime="application/vnd.ms-excel"
                )
            with col_d2:
                st.download_button(
                    label="Descargar en PDF",
                    data=generate_pdf(results),
                    file_name="reporte_calidad.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"Error procesando archivo: {e}")