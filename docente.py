# Funciones del panel docente.
import csv
import io
from datos import guardar
from usuarios import promedio, rango

PIN_DOCENTE = "1234"

def verificar_pin(pin):
    return str(pin) == PIN_DOCENTE

def agregar_sena(catalogo, palabra, emoji, descripcion):
    palabra = palabra.strip()
    emoji = emoji.strip()
    descripcion = descripcion.strip()
    if not palabra or not emoji or not descripcion:
        return False
    catalogo.append((palabra, emoji, descripcion))
    return True

def eliminar_sena(catalogo, indice):
    if len(catalogo) <= 1:
        return False
    if 0 <= indice < len(catalogo):
        catalogo.pop(indice)
        return True
    return False

def resumen_grupo(datos):
    resultado = []
    for usuario in datos.get("usuarios", {}).values():
        r = rango(usuario.get("xp", 0))
        resultado.append({
            "nombre": usuario.get("nombre", ""),
            "actividades": len(usuario.get("historial", [])),
            "promedio": promedio(usuario),
            "rango": r[2],
            "xp": usuario.get("xp", 0),
        })
    return resultado

def csv_grupo(datos):
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(["Alumno", "Fecha", "Actividad", "Correctas", "Total", "XP"])
    for usuario in datos.get("usuarios", {}).values():
        for item in usuario.get("historial", []):
            escritor.writerow([
                usuario.get("nombre", ""),
                item.get("fecha", ""),
                item.get("actividad", ""),
                item.get("correctas", 0),
                item.get("total", 0),
                item.get("xp", 0),
            ])
    return salida.getvalue()

def guardar_datos(datos):
    guardar(datos)
