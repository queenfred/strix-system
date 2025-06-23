import pandas as pd
from datetime import timedelta, datetime

def to_timestamp_ms(fecha):
    """
    Convierte una fecha a timestamp en milisegundos.
    Acepta:
      - string en formato 'dd/mm/yyyy' o 'yyyy-mm-dd'
      - datetime.datetime
      - pd.Timestamp
    Suma 3 horas al resultado.
    
    Args:
        fecha (str | datetime | pd.Timestamp): Fecha a convertir.

    Returns:
        int: Timestamp en milisegundos.
    """
    if isinstance(fecha, str):
        # Probar si es dd/mm/yyyy o yyyy-mm-dd automáticamente
        try:
            if "/" in fecha:
                fecha = pd.to_datetime(fecha, dayfirst=True)
            else:
                fecha = pd.to_datetime(fecha)  # yyyy-mm-dd
        except Exception:
            raise ValueError(f"Formato de fecha inválido: {fecha}")
    elif isinstance(fecha, (datetime, pd.Timestamp)):
        pass  # Ya es fecha válida
    else:
        raise ValueError(f"Tipo de dato inválido: {type(fecha)}")

    fecha += timedelta(hours=3)
    return int(fecha.timestamp() * 1000)
