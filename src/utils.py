import pandas as pd
from fpdf import FPDF
import io

def generate_excel(results: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        results["missing_values"].to_excel(writer, sheet_name='Nulos')
        results["stats"].to_excel(writer, sheet_name='Estadisticas')
    return buffer

def generate_pdf(results: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Reporte de Calidad de Datos", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Total de filas: {results['num_rows']}", ln=True)
    pdf.cell(200, 10, txt=f"Total de columnas: {results['num_columns']}", ln=True)
    pdf.cell(200, 10, txt=f"Duplicados detectados: {results['duplicates']}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')