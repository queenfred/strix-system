
import geopandas as gpd
from shapely.geometry import Point
import movingpandas as mpd
from datetime import timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class StopsAdapter:
    @staticmethod
    def detect_stop(df, reference_point, search_radius=500, min_stop=10, max_stop=36000):
        gdf = StopsAdapter._create_geodataframe(df)
        if gdf is None:
            return 0, None, None

        gdf_buffer = StopsAdapter._project_and_filter(gdf, reference_point, search_radius)
        if gdf_buffer is None or gdf_buffer.empty:
            return 0, None, None

        traj = StopsAdapter._build_trajectory(gdf_buffer)
        if traj is None:
            return 0, None, None

        stops_df = StopsAdapter._detect_stops(traj, search_radius, min_stop)
        if stops_df is None or stops_df.empty:
            return 0, None, None

        return StopsAdapter._extract_longest_stop(stops_df)

    @staticmethod
    def _create_geodataframe(df):
        try:
            gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['longitude'], df['latitude'])], crs='EPSG:4326')
            gdf['timestamp'] = pd.to_datetime(gdf['timestamp'], errors='coerce')
            gdf = gdf.dropna(subset=['timestamp']).sort_values('timestamp')
            gdf.set_index('timestamp', inplace=True)
            gdf["dummy"] = 1
            return gdf
        except Exception as e:
            logger.error(f"❌ Error creando GeoDataFrame: {e}")
            return None

    @staticmethod
    def _project_and_filter(gdf, reference_point, search_radius):
        try:
            proj_crs = "EPSG:32721"
            ref_point = Point(reference_point[1], reference_point[0])
            ref_gdf = gpd.GeoDataFrame({'geometry': [ref_point]}, crs='EPSG:4326')

            gdf_proj = gdf.to_crs(proj_crs)
            ref_proj = ref_gdf.to_crs(proj_crs)
            buffer = ref_proj.geometry.buffer(search_radius).iloc[0]
            gdf_buffer = gdf_proj[gdf_proj.geometry.within(buffer)]
            return gdf_buffer
        except Exception as e:
            logger.error(f"❌ Error en proyección CRS o filtrado por buffer: {e}")
            return None

    @staticmethod
    def _build_trajectory(gdf_buffer):
        try:
            traj_collection = mpd.TrajectoryCollection(gdf_buffer, "dummy", t="timestamp")
            return list(traj_collection.trajectories)[0]
        except Exception as e:
            logger.error(f"❌ Error generando trayectoria: {e}")
            return None

    @staticmethod
    def _detect_stops(traj, search_radius, min_stop):
        try:
            detector = mpd.TrajectoryStopDetector(traj)
            stops_df = detector.get_stop_points(
                min_duration=timedelta(seconds=min_stop),
                max_diameter=search_radius
            )
            return stops_df
        except Exception as e:
            logger.error(f"❌ Error detectando paradas: {e}")
            return None

    @staticmethod
    def _extract_longest_stop(stops_df):
        try:
            stops_df = stops_df[stops_df['duration_s'] >= 10]
            if stops_df.empty:
                return 0, None, None
            max_row = stops_df.loc[stops_df['duration_s'].idxmax()]
            if hasattr(max_row, 'geometry') and max_row.geometry is not None:
                point = gpd.GeoSeries([max_row.geometry], crs="EPSG:32721").to_crs("EPSG:4326").iloc[0]
                return max_row['duration_s'], point.y, point.x
        except Exception as e:
            logger.error(f"❌ Error extrayendo parada más larga: {e}")
        return 0, None, None
