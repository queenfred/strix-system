
from shapely.geometry import shape, Point
import time
import os
import pandas as pd
from core.config.settings import GEO_CONFIG
import googlemaps
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
from locationiq.geocoder import LocationIQ


class GeocodingAdapter:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=GEO_CONFIG["GOOGLE_API_KEY"])
        self.osm = Nominatim(user_agent=GEO_CONFIG["USER_AGENT"], timeout=20)
        self.opencage = OpenCageGeocode(GEO_CONFIG["OPENCAGE_API_KEY"])
        self.locationiq = LocationIQ(GEO_CONFIG["LOCATIONIQ_API_KEY"])

        self.bounding_polygon = shape({
            "type": "Polygon",
            "coordinates": [[
                [-75.99801699122749, -18.75961942950842],
                [-75.99801699122749, -57.61810267259912],
                [-49.18417052077325, -57.61810267259912],
                [-49.18417052077325, -18.75961942950842],
                [-75.99801699122749, -18.75961942950842]
            ]]
        })

        self.CACHE_FILE = GEO_CONFIG["CACHE_FILE"] 
        self.query_counter = 0

    def geocode(self, address, sleep_interval=0.2, pause_interval=10, pause_every=600, 
                max_retries=5, retry_sleep=1, domain=None, fecha=None, disable_cache=False,
                use_google=True, use_osm=False, use_opencage=False, use_locationiq=False):

        # Intentar caché
        if not disable_cache and domain and fecha:
            lat, lon = self._from_cache(address, domain, fecha)
            if lat and lon:
                return lat, lon

        # Pausa
        self.query_counter += 1
        if self.query_counter % pause_every == 0:
            print(f"⏸️ Pausando {pause_interval}s tras {self.query_counter} consultas")
            time.sleep(pause_interval)
        else:
            time.sleep(sleep_interval)

        # Estrategias
        strategies = []
        if use_google:
            strategies.append(self._geocode_google)
        if use_osm:
            strategies.append(lambda a: self._geocode_osm(a, max_retries, retry_sleep))
        if use_opencage:
            strategies.append(self._geocode_opencage)
        if use_locationiq:
            strategies.append(self._geocode_locationiq)

        for strategy in strategies:
            lat, lon = strategy(address)
            if lat and lon and self._in_bounds(lat, lon):
                self._cache_result(address, domain, fecha, lat, lon)
                return lat, lon

        print(f"⚠️ No se pudo geocodificar {address}")
        return None, None

    def _geocode_google(self, address):
        try:
            result = self.gmaps.geocode(address, region="ar", language="es")
            if result:
                lat = result[0]['geometry']['location']['lat']
                lon = result[0]['geometry']['location']['lng']
                print(f"🛰️ Google encontró: {lat}, {lon}")
                return lat, lon
        except Exception as e:
            print(f"⚠️ Google error: {e}")
        return None, None

    def _geocode_osm(self, address, max_retries, retry_sleep):
        from geopy.exc import GeocoderTimedOut
        for _ in range(max_retries):
            try:
                loc = self.osm.geocode(address)
                if loc:
                    return loc.latitude, loc.longitude
            except GeocoderTimedOut:
                time.sleep(retry_sleep)
            except Exception:
                break
        return None, None

    def _geocode_opencage(self, address):
        try:
            results = self.opencage.geocode(address)
            if results:
                return results[0]["geometry"]["lat"], results[0]["geometry"]["lng"]
        except Exception:
            pass
        return None, None

    def _geocode_locationiq(self, address):
        try:
            results = self.locationiq.geocode(address)
            if results:
                return float(results[0]['latitude']), float(results[0]['longitude'])
        except Exception:
            pass
        return None, None

    def _in_bounds(self, lat, lon):
        return self.bounding_polygon.contains(Point(lon, lat))

    def _from_cache(self, address, domain, fecha):
        if not os.path.exists(self.CACHE_FILE):
            return None, None
        df = pd.read_csv(self.CACHE_FILE)
        row = df[
            (df["domain"] == domain) &
            (df["fecha"] == str(fecha)) &
            (df["direccion"] == address)
        ]
        if not row.empty:
            print(f"📦 Cache usado para {domain}: ({row.iloc[0]['latitud']}, {row.iloc[0]['longitud']})")
            return row.iloc[0]["latitud"], row.iloc[0]["longitud"]
        return None, None

    def _cache_result(self, address, domain, fecha, lat, lon):
        if not domain or not fecha:
            return
        new = pd.DataFrame([{
            "domain": domain,
            "fecha": str(fecha),
            "direccion": address,
            "latitud": lat,
            "longitud": lon
        }])
        if os.path.exists(self.CACHE_FILE):
            df = pd.read_csv(self.CACHE_FILE)
            df = pd.concat([df, new], ignore_index=True)
        else:
            df = new
        df.to_csv(self.CACHE_FILE, index=False)
        print(f"📝 Cache actualizado para {domain}")

