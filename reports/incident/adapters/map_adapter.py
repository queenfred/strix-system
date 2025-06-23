import folium
import pandas as pd

class MapAdapter:
    @staticmethod
    def build_map(id_siniestro, df_verificados, df_recorrido,output_dir):

        """
        Genera un mapa interactivo con los datos GPS alrededor del siniestro.

        Args:
            id_siniestro: Índice del siniestro en df_verificados.
            df_verificados: DataFrame de incidentes verificados (public.incidentes_verificados).
            df_recorrido: DataFrame de recorrido GPS.
        
        Returns:
            Ruta del archivo HTML generado.
        """
        # Obtener datos del siniestro
        siniestro = df_verificados.loc[id_siniestro]
        domain = siniestro['domain']
        fecha_siniestro = siniestro['fecha_ocurrencia']
        fecha_str = fecha_siniestro.strftime("%Y-%m-%d")
        direccion_str = f"{siniestro['calle']}, {siniestro['ciudad']}, {siniestro['provincia']}"
        
        print(f"En el mapa, dominio incidente: {domain}, latitud: {siniestro['latitud']}, longitud: {siniestro['longitud']}")

        # Filtrar recorrido por dominio y fecha
        recorrido_dominio = df_recorrido[
            df_recorrido['domain'].astype(str).str.strip().str.lower() == str(domain).strip().lower()
        ]
        

    # Convertir timestamp a datetime si no es ya
        recorrido_dominio['timestamp'] = pd.to_datetime(recorrido_dominio['timestamp'], unit='ms') - pd.Timedelta(hours=3)


        recorrido_fecha = recorrido_dominio[
            recorrido_dominio['timestamp'].dt.date == fecha_siniestro.date()
        ]

 
        if recorrido_fecha.empty:
            print(f"No hay datos de recorrido para {domain} el {fecha_str}")
            return None

        recorrido_fecha = recorrido_fecha.sort_values('timestamp')

        # Crear mapa centrado en incidente
        mapa = folium.Map(location=[siniestro['latitud'], siniestro['longitud']], zoom_start=14)

        # Zona de búsqueda (500 metros)
        area_popup = folium.Popup("Zona de búsqueda de parada (500 m)", max_width=300)
        folium.Circle(
            location=[siniestro['latitud'], siniestro['longitud']],
            radius=500,
            color='blue',
            fill=True,
            fill_opacity=0.1,
            popup=area_popup
        ).add_to(mapa)

        # Marcador principal: incidente
        incident_popup = folium.Popup(
            f"<b>Dominio:</b> {domain}<br><b>Fecha:</b> {fecha_str}<br><b>Dirección:</b> {direccion_str}",
            max_width=300
        )
        folium.Marker(
            [siniestro['latitud'], siniestro['longitud']],
            popup=incident_popup,
            icon=folium.Icon(color='red', icon='warning-sign')
        ).add_to(mapa)

        # Línea del recorrido
        puntos = [(row['latitude'], row['longitude']) for _, row in recorrido_fecha.iterrows()]
        folium.PolyLine(puntos, color="blue", weight=2.5, opacity=0.8).add_to(mapa)

        # Inicio y fin del recorrido
        if not recorrido_fecha.empty:
            start_popup = folium.Popup(f"Inicio Actividad: {recorrido_fecha.iloc[0]['timestamp']}", max_width=300)
            folium.Marker(
                [recorrido_fecha.iloc[0]['latitude'], recorrido_fecha.iloc[0]['longitude']],
                popup=start_popup,
                icon=folium.Icon(color='green', icon='play')
            ).add_to(mapa)

            end_popup = folium.Popup(f"Fin Actividad: {recorrido_fecha.iloc[-1]['timestamp']}", max_width=300)
            folium.Marker(
                [recorrido_fecha.iloc[-1]['latitude'], recorrido_fecha.iloc[-1]['longitude']],
                popup=end_popup,
                icon=folium.Icon(color='black', icon='stop')
            ).add_to(mapa)

        # Paradas (velocidad < 1 km/h)
        paradas = recorrido_fecha[recorrido_fecha['speed'] < 1]
        for _, parada in paradas.iterrows():
            folium.CircleMarker(
                location=[parada['latitude'], parada['longitude']],
                radius=5,
                popup=f"Parada: {parada['timestamp']}<br>Velocidad: {parada['speed']} km/h",
                color='orange',
                fill=True,
                fill_color='orange'
            ).add_to(mapa)

        # Parada calculada (parada_zona)
        stop_duration = siniestro.get('parada_zona', 0)
        stop_lat = siniestro.get('latitud_parada_zona', None)
        stop_lon = siniestro.get('longitud_parada_zona', None)

        print(f"Stop detectado: duración={stop_duration}, lat={stop_lat}, lon={stop_lon}")

        if stop_duration > 0 and stop_lat is not None and stop_lon is not None:
            stop_popup = folium.Popup(f"Parada detectada:<br>Duración: {stop_duration:.0f} seg", max_width=300)
            folium.Marker(
                location=[stop_lat, stop_lon],
                popup=stop_popup,
                icon=folium.Icon(color='yellow', icon='pause')
            ).add_to(mapa)

        # Título del mapa
        titulo_mapa = (
            f"Dominio: {domain} | Fecha: {fecha_str} | Dirección: {direccion_str} | "
            f"Distancia: {siniestro['distancia_circulacion']:.2f} km | "
            f"Parada: {siniestro['parada_zona']} seg | Consistencia: {siniestro.get('clasificacion', '')}"
        )
        mapa.get_root().html.add_child(folium.Element(f"<h3 style='text-align:center;'>{titulo_mapa}</h3>"))

        # Guardar
        nombre_archivo =f"{output_dir}/mapa_siniestro_{domain}_{fecha_str.replace('-', '_')}.html"
        mapa.save(nombre_archivo)

        return nombre_archivo






