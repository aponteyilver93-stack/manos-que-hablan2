# Persistencia local usando localStorage del navegador.
import json
from js import window

CLAVE = "manos_que_hablan_python_real_v1"

def cargar():
    try:
        texto = window.localStorage.getItem(CLAVE)
        if not texto:
            return {"usuarios": {}}
        datos = json.loads(str(texto))
        if not isinstance(datos, dict):
            return {"usuarios": {}}
        datos.setdefault("usuarios", {})
        return datos
    except Exception:
        return {"usuarios": {}}

def guardar(datos):
    window.localStorage.setItem(CLAVE, json.dumps(datos, ensure_ascii=False))

def borrar_datos():
    window.localStorage.removeItem(CLAVE)
