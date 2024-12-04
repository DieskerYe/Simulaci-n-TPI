import folium
from folium import Map, LayerControl
from folium.plugins import HeatMap
import pandas as pd

# Ruta del archivo de salidas de AnyLogic
file_path = "C:\\Users\\VIRGI\\Desktop\\TPI_Simulacion\\Corridas_Optimos.xlsx"
data = pd.read_excel(file_path)

# Coordenadas del centro de Rosario
coordenadas_rosario_centro = [-32.940, -60.645]
mapa = Map(location=coordenadas_rosario_centro, zoom_start=15)

# Combinar todas las coordenadas (sin filtrar por base)
coordenadas = []

for i in range(1, 6):
    latitud_base = f'H {i} latitud'
    longitud_base = f'H {i} longitud'

    if latitud_base in data.columns and longitud_base in data.columns:
        data[latitud_base].fillna(0, inplace=True)
        data[longitud_base].fillna(0, inplace=True)
        
        data[latitud_base] = data[latitud_base] / 1000  # Ajustar el formato de las coordenadas
        data[longitud_base] = data[longitud_base] / 1000

        # Filtrar coordenadas válidas
        coordenadas_validas = data[(data[latitud_base] != 0) & (data[longitud_base] != 0)][[latitud_base, longitud_base]]
        coordenadas += coordenadas_validas.values.tolist()

# Crear capa de mapa de calor con todas las coordenadas
if coordenadas:
    heat_layer = HeatMap(
        coordenadas,
        gradient={0: "blue", 0.5: "yellow", 1: "red"},  # Zonas más densas en rojo
        radius=25,
        blur=15
    )
    mapa.add_child(heat_layer)

# Guardar el mapa generado
output_path = "C:\\Users\\VIRGI\\Desktop\\TPI_Simulacion\\Mapas de calor\\mapa_calor_atenciones.html"
mapa.save(output_path)
print(f"Mapa de calor generado y guardado en: {output_path}")
