
import os
import pandas as pd
import zipfile
from sqlalchemy import text
from reports.incident.adapters.pdf_report_adapter import PDFReportAdapter
from reports.incident.adapters.excel_report_adapter import ExcelReportAdapter
from reports.incident.adapters.map_adapter import MapAdapter
from core.services.event_service import EventService

from reports.incident.services.incident_service import IncidentService



class ExportService:
    def __init__(self, uow):
        self.uow = uow
        self.event_service = EventService(uow)
        self.incident_service = IncidentService(uow)

    def generate_report_zip(self, titulo_informe="audiro_report", output_dir="output"):
        #output_dir = os.path.join(os.getcwd(), "output")
        #os.makedirs(output_dir, exist_ok=True)

        with self.uow:

            rows = self.incident_service.get_all_incidents()
            df = pd.DataFrame(rows) # df_verificados

        if df.empty:
            print("⚠️ No hay registros verificados para generar informe.")
            return None

        # PDF
        pdf_path = f"{output_dir}/informe_verificacion_siniestros.pdf"
        PDFReportAdapter.build(df.copy(), pdf_path)


        # Excel
        excel_path = ExcelReportAdapter.build(df.copy(), df.copy(), os.path.join(output_dir, "informe_verificacion_siniestros"))

        ######### Mapas

        #from core.adapters.map_adapter import MapAdapter
        from datetime import timedelta

        mapas_generados = []


        for idx in df.index:
            try:
                id_domain = int(df.loc[idx, "id_domain"])
                fecha = df.loc[idx, "fecha_ocurrencia"]

                start_date = fecha.normalize()
                end_date = start_date + timedelta(days=1) - timedelta(seconds=1)

                print("⏱️", fecha)
                recorrido = self.event_service.get_events_by_domain_and_date(id_domain, start_date, end_date) #df_final
                

                if recorrido is not None and isinstance(recorrido, list) and len(recorrido) > 0:
                    recorrido_df = pd.DataFrame(recorrido)
                    recorrido_df["domain"] = df.loc[idx, "domain"]  
                    mapa = MapAdapter.build_map(idx, df, recorrido_df,output_dir)
                    if mapa:
                        mapas_generados.append(os.path.join(output_dir, mapa))
                else:
                    print(f"⚠️ No hay recorrido para ID {id_domain}")
            except Exception as e:
                print(f"⚠️ Error generando mapa del siniestro ID {idx}: {e}")

        print("🗺️ Mapas generados:", mapas_generados)


        # ZIP final
        from datetime import datetime

        #zip_filename = f"{titulo_informe}.zip" if not titulo_informe.endswith(".zip") else titulo_informe
        zip_filename = f"I{titulo_informe}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"

        zip_path = f"{output_dir}/{zip_filename}"
        #zip_path = os.path.join(output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in [pdf_path, excel_path] + mapas_generados:
                if os.path.exists(file_path):
                    zipf.write(file_path, arcname=os.path.basename(file_path))
        
        # 🔥 Borrar archivos individuales después de empaquetarlos
        for file_path in [pdf_path, excel_path] + mapas_generados:
            if os.path.exists(file_path):
                os.remove(file_path)

        print(f"✅ ZIP generado: {zip_path}")
        return zip_path
