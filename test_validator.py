import pandas as pd
import numpy as np
from src.validator import run_validation

def test_validator():
    # 1. Crear un DataFrame con un duplicado exacto
    data = {
        'id': [1, 2, 2, 4, 5],
        'valor': [10.5, 20.0, 20.0, 15.0, np.nan], 
        'categoria': ['A', 'B', 'B', 'C', 'D']
    }
    df = pd.DataFrame(data)

    print("--- Ejecutando test de Validación ---")
    print("DataFrame Original:")
    print(df)
    
    # 2. Correr la validación
    results = run_validation(df)

    # 3. Inspeccionar resultados
    if "error" in results:
        print(f"Error encontrado: {results['error']}")
    else:
        print("\nResultados obtenidos:")
        print(f"Filas totales: {results['num_rows']}")
        print(f"Duplicados detectados: {results['duplicates']}")
        print("\nResumen de Nulos:")
        print(results['missing_values'])
        
        # Validación de aserciones simples (para verificar lógica)
        assert results['duplicates'] == 1, "Error: Debería detectar 1 duplicado"
        assert results['num_rows'] == 5, "Error: El conteo de filas es incorrecto"
        print("\n✅ Test pasado exitosamente.")

if __name__ == "__main__":
    test_validator()