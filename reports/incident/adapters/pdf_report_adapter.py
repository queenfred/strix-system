# 📄 reports/incident/adapters/pdf_report_adapter.py

from reports.incident.utils.verificador.generar_informe_pdf import generar_informe_pdf

class PDFReportAdapter:
    @staticmethod
    def build(df, output_path):
        """
        Genera el informe PDF de verificación de siniestros usando el motor avanzado.

        Args:
            df (pd.DataFrame): DataFrame de incidentes verificados.
            output_path (str): Ruta donde se guardará el PDF.

        Returns:
            str: Ruta del archivo PDF generado.
        """
        return generar_informe_pdf(df, ruta_salida=output_path)
