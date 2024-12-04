import folium
from folium import Map, LayerControl
from folium.plugins import HeatMap
import pandas as pd

# Ruta del archivo de salidas de AnyLogic
file_path = "C:\\Users\\VIRGI\\Desktop\\TPI_Simulacion\\Corridas_Optimos.xlsx"
data = pd.read_excel(file_path)

coordenadas_rosario_centro = [-32.940, -60.645] # Coordenadas del centro de Rosario
mapa = Map(location=coordenadas_rosario_centro, zoom_start=15)

color_base = {
    1: "blue",
    2: "green",
    3: "red",
    4: "purple",
    5: "orange"
}

for i in range(1, 6):
    latitud_base = f'H {i} latitud'
    longitud_base = f'H {i} longitud'

    if latitud_base in data.columns and longitud_base in data.columns:
        data[latitud_base].fillna(0, inplace=True)
        data[longitud_base].fillna(0, inplace=True)
        
        data[latitud_base] = data[latitud_base] / 1000   # Recordar dividir las coordenadas por 1000 para que coincida el formato con excel
        data[longitud_base] = data[longitud_base] / 1000
        
        coordenadas_validas = data[(data[latitud_base] != 0) & (data[longitud_base] != 0)][[latitud_base, longitud_base]]
        
        coordenadas_agrupadas = coordenadas_validas.groupby([latitud_base, longitud_base]).size().reset_index(name='count')
        max_densidad = coordenadas_agrupadas[coordenadas_agrupadas['count'] == coordenadas_agrupadas['count'].max()]
        heat_data = max_densidad[[latitud_base, longitud_base]].values.tolist()
        
        if heat_data:  # Si hay datos válidos
            heat_layer = HeatMap(
                heat_data,
                gradient={0.2: color_base[i], 0.5: color_base[i], 1: color_base[i]},
                radius=25,
                blur=15,
                name=f"Base Operativa {i}"  # Etiqueta de filtro para mapa de calor
            )
            mapa.add_child(heat_layer)

# Leyenda de mapa de calor para entendimiento de usuario
leyenda_html = """
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: 180px; 
            background-color: white; z-index:1000; 
            border:2px solid grey; border-radius:5px; padding: 10px; font-size:14px;">
    <b>Referencias de Base Operativa</b><br>
    <i style="background:blue; width:10px; height:10px; display:inline-block;"></i> Base Operativa 1<br>
    <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Base Operativa 2<br>
    <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Base Operativa 3<br>
    <i style="background:purple; width:10px; height:10px; display:inline-block;"></i> Base Operativa 4<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Base Operativa 5<br>
</div>
"""
mapa.get_root().html.add_child(folium.Element(leyenda_html))

LayerControl().add_to(mapa)

# Guardar el mapa generado
output_path = "C:\\Users\\VIRGI\\Desktop\\TPI_Simulacion\\Mapas de calor\\mapa_calor_atenciones_porbases.html"
mapa.save(output_path)
print(f"Mapa de calor generado y guardado en: {output_path}")
