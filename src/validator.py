import pandas as pd
from typing import Dict, Any

def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la cantidad y porcentaje de valores nulos por columna."""
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df)) * 100
    return pd.DataFrame({
        'Missing_Count': missing_count,
        'Percentage': missing_pct.round(2)
    })

def get_duplicates(df: pd.DataFrame) -> int:
    """Retorna el número de filas duplicadas."""
    return int(df.duplicated().sum())

def get_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna estadísticas descriptivas básicas de columnas numéricas."""
    return df.describe().transpose()

def run_validation(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Orquestador principal que ejecuta todas las validaciones.
    Retorna un diccionario con los resultados para ser consumidos por la UI.
    """
    try:
        if df.empty:
            return {"error": "El archivo está vacío."}
        
        results = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "missing_values": get_missing_values(df),
            "duplicates": get_duplicates(df),
            "stats": get_basic_stats(df.select_dtypes(include=['number'])),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
        return results
        
    except Exception as e:
        return {"error": f"Error al procesar los datos: {str(e)}"}