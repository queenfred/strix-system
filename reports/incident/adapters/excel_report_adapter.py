import pandas as pd

class ExcelReportAdapter:
    """
    Adapter para generar archivos Excel con los resultados del análisis de siniestros.
    """

    @staticmethod
    def build(df_test: pd.DataFrame, df_verified: pd.DataFrame, output_base: str) -> str:
        """
        Genera un archivo Excel (.xlsx) con múltiples hojas:
        - Identificados
        - Verificados Consistencia Alta
        - Verificados Consistencia Media
        - Verificados Consistencia Baja
        - Revisar Dirección (si falta latitud o longitud)

        Args:
            df_test: DataFrame con el dataset original.
            df_verified: DataFrame con los registros verificados.
            output_base: Ruta base (sin extensión) donde guardar el archivo.

        Returns:
            Ruta completa del archivo Excel generado.
        """

        if not output_base.endswith(".xlsx"):
            xlsx_filename = output_base + ".xlsx"
        else:
            xlsx_filename = output_base

        with pd.ExcelWriter(xlsx_filename, engine="openpyxl") as writer:
            df_verified.to_excel(writer, sheet_name="Identificados", index=False)

            df_verified[df_verified["clasificacion"] == "Alta consistencia"].to_excel(
                writer, sheet_name="Verificados Consistencia Alta", index=False
            )
            df_verified[df_verified["clasificacion"] == "Media consistencia"].to_excel(
                writer, sheet_name="Verificados Consistencia Media", index=False
            )
            df_verified[df_verified["clasificacion"] == "Baja consistencia"].to_excel(
                writer, sheet_name="Verificados Consistencia Baja", index=False
            )
            df_test[df_test["latitud"].isna() | df_test["longitud"].isna()].to_excel(
                writer, sheet_name="Revisar Dirección", index=False
            )

        print(f"✅ Excel generado en: {xlsx_filename}")
        return xlsx_filename
