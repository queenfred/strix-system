import pandas as pd
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# BLOQUE 1 — Imports, Márgenes, Canvas, Header/Footer

# --- Márgenes ---
LEFT_MARGIN = 40
RIGHT_MARGIN = 40
TOP_MARGIN = 60
BOTTOM_MARGIN = 40

# --- Canvas personalizado ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._doc.page_count = num_pages
            header_footer(self, self._doc)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

# --- Header/Footer ---
def header_footer(canvas_obj, doc):
    width, height = A4
    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor("#505050"))
    canvas_obj.setFont("Helvetica", 10)

    canvas_obj.drawCentredString(width / 2, height - 30, "AUDIRO REPORTS")
    canvas_obj.line(LEFT_MARGIN, height - 35, width - RIGHT_MARGIN, height - 35)

    footer_y = 30
    generation_date = datetime.now().strftime("%d/%m/%Y")
    canvas_obj.drawString(LEFT_MARGIN, footer_y, generation_date)
    canvas_obj.drawCentredString(width / 2, footer_y, "STRIX")
    page_number = canvas_obj.getPageNumber()
    total_pages = getattr(doc, 'page_count', page_number)
    canvas_obj.drawRightString(width - RIGHT_MARGIN, footer_y, f"Pag. {page_number} de {total_pages}")
    canvas_obj.line(LEFT_MARGIN, footer_y + 15, width - RIGHT_MARGIN, footer_y + 15)

    canvas_obj.restoreState()

# BLOQUE 2 — Funciones de gráficos (generados en memoria)

# --- Función auxiliar para generar gráficos en memoria ---
def generar_grafico(func_plot):
    buffer = BytesIO()
    func_plot()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

# --- Gráficos individuales ---
"""def plot_distribucion_consistencia(df):
    counts = df['clasificacion'].value_counts()
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Distribución de Denuncias por Nivel de Consistencia")
    plt.ylabel("Cantidad de Denuncias")
    plt.xlabel("Nivel de Consistencia")
    plt.xticks(rotation=45)
    plt.tight_layout()"""

def plot_distribucion_consistencia(df):
    counts = df['clasificacion'].value_counts()
    mapping = {
        "Alta consistencia": "Alta",
        "Media consistencia": "Media",
        "Baja consistencia": "Baja",
        "Sin datos suficientes": "Sin datos"
    }
    renamed_index = [mapping.get(label, label) for label in counts.index]

    sns.barplot(x=renamed_index, y=counts.values)
    plt.title("Distribución de Denuncias por Nivel de Consistencia")
    plt.ylabel("Cantidad de Denuncias")
    plt.xlabel("Nivel de Consistencia")
    plt.xticks(rotation=0)
    plt.tight_layout()


def plot_distancias(df):
    sns.histplot(df['distancia_circulacion'].dropna(), kde=True, bins=20)
    plt.title("Distribución de Distancias (km)")
    plt.xlabel("Distancia (km)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()

def plot_paradas(df):
    sns.histplot(df['parada_zona'].dropna(), kde=True, bins=20)
    plt.title("Distribución de Tiempos de Parada (seg)")
    plt.xlabel("Tiempo de Parada (segundos)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()

def plot_boxplot_distancias(df):
    order = ["Alta consistencia", "Media consistencia", "Baja consistencia", "Sin datos suficientes"]
    sns.boxplot(x="clasificacion", y="distancia_circulacion", data=df, order=order)
    plt.title("Boxplot de Distancias por Clasificación")
    plt.xlabel("Clasificación")
    plt.ylabel("Distancia de Circulación (km)")
    plt.tight_layout()

"""def plot_boxplot_paradas(df):
    order = ["Alta consistencia", "Media consistencia", "Baja consistencia", "Sin datos suficientes"]
    sns.boxplot(x="clasificacion", y="parada_zona", data=df, order=order)
    plt.title("Boxplot de Tiempos de Parada por Clasificación")
    plt.xlabel("Clasificación")
    plt.ylabel("Tiempo de Parada (seg)")
    plt.tight_layout()"""

def plot_boxplot_paradas(df):
    df_plot = df.copy()
    df_plot['parada_zona'] = df_plot['parada_zona'].fillna(0)  # Forzar Sin datos
    order = ["Alta consistencia", "Media consistencia", "Baja consistencia", "Sin datos suficientes"]
    sns.boxplot(x="clasificacion", y="parada_zona", data=df_plot, order=order)
    plt.title("Boxplot de Tiempos de Parada por Clasificación")
    plt.xlabel("Clasificación")
    plt.ylabel("Tiempo de Parada (segundos)")
    plt.tight_layout()


def plot_scatter(df):
    sns.scatterplot(x="distancia_circulacion", y="parada_zona", hue="clasificacion", data=df)
    plt.title("Relación entre Distancia y Tiempo de Parada")
    plt.xlabel("Distancia de circulación (km)")
    plt.ylabel("Tiempo de parada (seg)")
    plt.tight_layout()

#BLOQUE 3 — Función principal

def generar_informe_pdf(df_verificados, ruta_salida="informe_verificacion_siniestros.pdf"):
    if df_verificados.empty:
        print("⚠️ No hay datos para generar el informe.")
        return None

    # Clasificación si no existe
    if "clasificacion" not in df_verificados.columns:
        mask_alta = (df_verificados["distancia_circulacion"] < 0.5) & (df_verificados["parada_zona"] >= 60)
        mask_baja = df_verificados["distancia_circulacion"] >= 1
        mask_media = (df_verificados["distancia_circulacion"] < 1) & (~mask_alta)
        df_verificados["clasificacion"] = "Sin datos suficientes"
        df_verificados.loc[mask_alta, "clasificacion"] = "Alta consistencia"
        df_verificados.loc[mask_media, "clasificacion"] = "Media consistencia"
        df_verificados.loc[mask_baja, "clasificacion"] = "Baja consistencia"

    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#141414"))
    subtitulo_style = ParagraphStyle('Subtitulo', parent=styles['Heading2'], textColor=colors.HexColor("#202020"))

    doc = BaseDocTemplate(
        ruta_salida, pagesize=A4,
        leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN
    )
    frame = Frame(LEFT_MARGIN, BOTTOM_MARGIN, doc.width, doc.height, id="normal")
    template = PageTemplate(id="template", frames=frame)
    doc.addPageTemplates([template])

    elementos = []

    # --- Título y Resumen Ejecutivo ---
    elementos.append(Paragraph("Informe de Verificación de Siniestros", titulo_style))
    elementos.append(Spacer(1, 12))

    total = len(df_verificados)
    altas = sum(df_verificados["clasificacion"] == "Alta consistencia")
    medias = sum(df_verificados["clasificacion"] == "Media consistencia")
    bajas = sum(df_verificados["clasificacion"] == "Baja consistencia")
    sin_datos = sum(df_verificados["clasificacion"] == "Sin datos suficientes")

    resumen = f"""
    Se analizaron {total} denuncias de siniestros vehiculares utilizando datos GPS.<br/><br/>
    Los resultados son:<br/><br/>
    • {altas} denuncias ({altas/total*100:.1f}%) muestran alta consistencia con los datos GPS.<br/>
    • {medias} denuncias ({medias/total*100:.1f}%) muestran consistencia media.<br/>
    • {bajas} denuncias ({bajas/total*100:.1f}%) muestran baja consistencia.<br/>
    • {sin_datos} denuncias ({sin_datos/total*100:.1f}%) no tienen datos GPS suficientes para verificar.<br/><br/>
    El análisis se basa en dos métricas principales:<br/><br/>
    <b>Distancia de circulacion:</b> Es la distancia más cercana a la dirección declarada donde se encontraron posiciones GPS del vehículo.<br/><br/>
    <b>Parada en zona:</b> Es el tiempo de la parada encontrada dentro del radio de 500 metros alrededor de la dirección declarada.
    """
    elementos.append(Paragraph("Resumen Ejecutivo", subtitulo_style))
    elementos.append(Paragraph(resumen, styles['Normal']))
    elementos.append(Spacer(1, 12))

    # --- Tabla de Criterios ---
    elementos.append(Paragraph("Criterios de Clasificación:", subtitulo_style))
    tabla_criterios = [
        ['Nivel', 'Criterios'],
        ['Alta consistencia', 'Distancia de circulacion < 500 m y parada en zona >= 60 seg.'],
        ['Media consistencia', 'Distancia de circulacion < 1 Km (excluyendo Alta)'],
        ['Baja consistencia', 'Distancia de circulacion >= 1 Km']
    ]
    tabla = Table(tabla_criterios, colWidths=[150, 350])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elementos.append(tabla)
    elementos.append(PageBreak())

# BLOQUE 4 — Gráficos

    # --- Gráficos agrupados en páginas específicas ---

    # Página 2: Distribución de Consistencia + Distribución de Distancias
    buffer_consistencia = generar_grafico(lambda: plot_distribucion_consistencia(df_verificados))
    buffer_distancias = generar_grafico(lambda: plot_distancias(df_verificados))

    elementos.append(Paragraph("Distribución de Denuncias por Consistencia", subtitulo_style))
    elementos.append(Image(buffer_consistencia, width=400, height=250))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("Distribución de Distancias", subtitulo_style))
    elementos.append(Image(buffer_distancias, width=400, height=250))
    elementos.append(PageBreak())

    # Página 3: Distribución de Tiempos de Parada + Boxplot de Distancias
    buffer_paradas = generar_grafico(lambda: plot_paradas(df_verificados))
    buffer_boxplot_distancias = generar_grafico(lambda: plot_boxplot_distancias(df_verificados))

    elementos.append(Paragraph("Distribución de Tiempos de Parada", subtitulo_style))
    elementos.append(Image(buffer_paradas, width=400, height=250))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("Boxplot de Distancias por Clasificación", subtitulo_style))
    elementos.append(Image(buffer_boxplot_distancias, width=400, height=250))
    elementos.append(PageBreak())

    # Página 4: Boxplot de Tiempos de Parada + Scatter
    buffer_boxplot_paradas = generar_grafico(lambda: plot_boxplot_paradas(df_verificados))
    buffer_scatter = generar_grafico(lambda: plot_scatter(df_verificados))

    elementos.append(Paragraph("Boxplot de Tiempos de Parada por Clasificación", subtitulo_style))
    elementos.append(Image(buffer_boxplot_paradas, width=400, height=250))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("Relación entre Distancia y Tiempo de Parada", subtitulo_style))
    elementos.append(Image(buffer_scatter, width=400, height=250))
    elementos.append(PageBreak())

# BLOQUE 5 — Tablas de Denuncias y Análisis Detallado
    # --- Detalle de Denuncias por nivel de consistencia ---

    elementos.append(Paragraph("Detalle de Denuncias", subtitulo_style))

    niveles = [
        ("Alta consistencia", colors.green),
        ("Media consistencia", colors.orange),
        ("Baja consistencia", colors.red)
    ]

    for nivel, color in niveles:
        df_nivel = df_verificados[df_verificados['clasificacion'] == nivel]
        if not df_nivel.empty:
            elementos.append(Paragraph(f"Denuncias con {nivel}", ParagraphStyle(
                nivel.replace(' ', '_'), parent=styles['Heading3'], textColor=color)))
            tabla_data = [['Dominio', 'Fecha Siniestro', 'Distancia (km)', 'Parada (seg)']]

            for _, row in df_nivel.iterrows():
                tabla_data.append([
                    row['domain'],
                    row['fecha_ocurrencia'].strftime('%d/%m/%Y') if pd.notnull(row['fecha_ocurrencia']) else 'N/A',
                    f"{row['distancia_circulacion']:.2f}" if pd.notnull(row['distancia_circulacion']) else 'N/A',
                    f"{row['parada_zona']:.0f}" if pd.notnull(row['parada_zona']) else 'N/A'
                ])

            tabla = Table(tabla_data, colWidths=[90, 90, 90, 90])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elementos.append(tabla)
            elementos.append(Spacer(1, 12))

            # --- Análisis Detallado de un ejemplo ---
            if not df_nivel.empty:
                caso = df_nivel.iloc[0]
                elementos.append(Paragraph(f"Análisis Detallado (Ejemplo): Dominio {caso['domain']}", styles['Heading4']))

                fecha_siniestro = caso['fecha_ocurrencia'].strftime('%d/%m/%Y %H:%M') if pd.notnull(caso['fecha_ocurrencia']) else 'N/A'
                fecha_punto = caso['fecha_circulacion'].strftime('%d/%m/%Y') if pd.notnull(caso['fecha_circulacion']) else 'N/A'
                hora_punto = caso['hora_circulacion'] if pd.notnull(caso['hora_circulacion']) else 'N/A'
                parada_str = f"{caso['parada_zona']:.0f}" if pd.notnull(caso['parada_zona']) else "N/A"

                detalle = f"""
                • <b>Dominio:</b> {caso['domain']}<br/>
                • <b>Fecha del siniestro:</b> {fecha_siniestro}<br/>
                • <b>Coordenadas geocodificadas:</b> ({caso['latitud']:.6f}, {caso['longitud']:.6f})<br/>
                • <b>Distancia mínima al recorrido GPS:</b> {caso['distancia_circulacion']:.2f} km<br/>
                • <b>Fecha/hora del punto más cercano:</b> {fecha_punto} {hora_punto}<br/>
                • <b>Tiempo de parada en zona:</b> {parada_str} segundos
                """
                elementos.append(Paragraph(detalle, styles['Normal']))
                elementos.append(PageBreak())

# BLOQUE 6 — Cierre final del PDF
    # --- Cierre del documento ---

    doc.build(elementos, canvasmaker=NumberedCanvas)
    print(f"✅ Informe generado exitosamente en {ruta_salida}")
    return ruta_salida
