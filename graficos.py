import pandas as pd
import matplotlib.pyplot as plt

file_path = "C:\\Users\\VIRGI\\Desktop\\TPI_Simulacion\\salidas_anylogic.xlsx"
data = pd.read_excel(file_path)

for i in range(1, 6):
    latitud_base = f'H {i} latitud'
    longitud_base = f'H {i} longitud'
    
    if latitud_base in data.columns and longitud_base in data.columns:
        data[latitud_base] = data[latitud_base] / 1000
        data[longitud_base] = data[longitud_base] / 1000

# Gráfico 1: Distribución de frecuencia por base operativa
plt.figure(figsize=(10, 6))

frecuencias = []
bases = []
for i in range(1, 6):
    latitud_base = f'H {i} latitud'
    longitud_base = f'H {i} longitud'
    
    if latitud_base in data.columns and longitud_base in data.columns:
        coordenadas_validas = data[(data[latitud_base] != 0) & (data[longitud_base] != 0)]
        frecuencias.append(len(coordenadas_validas))
        bases.append(f'Base {i}')

plt.bar(bases, frecuencias, color=['blue', 'green', 'red', 'purple', 'orange'], alpha=0.7)
plt.title("Frecuencia de eventos por Base Operativa")
plt.xlabel("Base Operativa")
plt.ylabel("Cantidad de Eventos")
plt.show()