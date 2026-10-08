# Usuarios, XP, rangos y progreso.
from datetime import datetime
from datos import guardar
from senas import RANGOS

def rango(xp):
    actual = RANGOS[0]
    for item in RANGOS:
        if xp >= item[0]:
            actual = item
    return actual

def obtener(datos, nombre):
    usuarios = datos.setdefault("usuarios", {})
    if nombre not in usuarios:
        usuarios[nombre] = {"nombre": nombre, "xp": 0, "historial": []}
    return usuarios[nombre]

def sumar_xp(datos, nombre, cantidad, actividad, correctas, total):
    usuario = obtener(datos, nombre)
    usuario["xp"] += int(cantidad)
    usuario["historial"].append({
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "actividad": actividad,
        "correctas": int(correctas),
        "total": int(total),
        "xp": int(cantidad),
    })
    guardar(datos)

def promedio(usuario):
    historial = usuario.get("historial", [])
    if not historial:
        return 0
    return round(sum((x["correctas"] / max(1, x["total"])) * 100 for x in historial) / len(historial))
