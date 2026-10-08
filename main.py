# Punto de entrada del videojuego.
# La lógica principal está en Python; HTML/CSS solo presenta la interfaz.
import json
import random
from js import document, window, Blob, URL
from pyodide.ffi import create_proxy

import datos
import juego
import docente
from senas import SENAS, RANGOS
from usuarios import obtener, rango, sumar_xp

DB = datos.cargar()
CATALOGO = list(SENAS)
USUARIO_ACTUAL = None
PROXIES = []

def html(texto):
    return str(texto).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def limpiar():
    document.getElementById("main").innerHTML = ""
    PROXIES.clear()

def boton(texto, funcion, clase=""):
    b = document.createElement("button")
    b.innerHTML = texto
    if clase:
        b.className = clase
    proxy = create_proxy(funcion)
    PROXIES.append(proxy)
    b.addEventListener("click", proxy)
    return b

def poner(*elementos):
    main = document.getElementById("main")
    for e in elementos:
        main.appendChild(e)

def titulo(texto):
    h = document.createElement("h2")
    h.innerHTML = texto
    return h

def tarjeta(texto):
    d = document.createElement("div")
    d.className = "card"
    d.innerHTML = texto
    return d

def rango_actual():
    return rango(obtener(DB, USUARIO_ACTUAL)["xp"])

def menu():
    limpiar()
    u = obtener(DB, USUARIO_ACTUAL)
    r = rango(u["xp"])
    poner(
        titulo(f"¡Hola, {html(USUARIO_ACTUAL)}!"),
        tarjeta(f'<div class="big">{r[1]}</div><div class="word">{html(r[2])}</div><p>⭐ {u["xp"]} puntos</p>'),
        boton("📖 Aprender", aprender),
        boton("🧠 Memoria", memoria),
        boton("❓ Trivia", trivia),
        boton("🧩 Frases", frases),
        boton("⭐ Mi progreso", progreso),
        boton("👩‍🏫 Panel docente", panel_docente),
        boton("🚪 Cambiar jugador", inicio),
    )

def inicio(event=None):
    global USUARIO_ACTUAL
    USUARIO_ACTUAL = None
    limpiar()
    poner(
        tarjeta('<div class="big">🤟</div><h2>Manos que hablan</h2><p class="desc">Aprende Lengua de Señas jugando.</p>'),
    )
    campo = document.createElement("input")
    campo.id = "nombre"
    campo.placeholder = "Escribe tu nombre"
    campo.maxLength = 25
    poner(campo, boton("▶ Entrar", entrar), boton("👩‍🏫 Panel docente", panel_docente))

def entrar(event=None):
    global USUARIO_ACTUAL
    campo = document.getElementById("nombre")
    nombre = campo.value.strip()
    if not nombre:
        window.alert("Escribe tu nombre.")
        return
    USUARIO_ACTUAL = nombre
    obtener(DB, nombre)
    datos.guardar(DB)
    menu()

def aprender(event=None):
    limpiar()
    estado = {"i": 0}
    poner(titulo("📖 Aprender señas"), tarjeta(f"{len(CATALOGO)} señas disponibles."))

    caja = document.createElement("div")
    caja.className = "card"
    poner(caja)

    def mostrar(_=None):
        s = CATALOGO[estado["i"]]
        caja.innerHTML = f'<div class="big">{s[1]}</div><div class="word">{html(s[0].upper())}</div><p class="desc">🤟 {html(s[2])}</p><p>{estado["i"]+1} de {len(CATALOGO)}</p>'

    anterior = boton("⬅ Anterior", lambda e: cambiar(-1))
    siguiente = boton("Siguiente ➡", lambda e: cambiar(1))
    poner(anterior, siguiente)
    def cambiar(p):
        estado["i"] = (estado["i"] + p) % len(CATALOGO)
        mostrar()
    mostrar()

def memoria(event=None):
    limpiar()
    pares = juego.nueva_memoria()
    cartas = []
    for i, s in enumerate(pares):
        cartas.append({"id": i, "tipo": "emoji", "s": s})
        cartas.append({"id": i, "tipo": "desc", "s": s})
    random.shuffle(cartas)
    estado = {"seleccion": [], "bloqueado": False, "correctas": 0, "intentos": 0}

    poner(titulo("🧠 Memoria"), tarjeta("Une cada emoji con su explicación."))
    cont = document.createElement("div")
    cont.className = "grid"
    poner(cont)

    def revelar(indice):
        c = cartas[indice]
        return f'{c["s"][1]}<br>{html(c["s"][0])}' if c["tipo"] == "emoji" else f'🤟 {html(c["s"][2])}'

    for i in range(len(cartas)):
        b = document.createElement("button")
        b.className = "mc"
        b.innerHTML = "❓"
        proxy = None
        def accion(event, i=i):
            if estado["bloqueado"] or i in estado["seleccion"]:
                return
            b_local = event.currentTarget
            b_local.innerHTML = revelar(i)
            estado["seleccion"].append(i)
            if len(estado["seleccion"]) < 2:
                return
            estado["intentos"] += 1
            a, z = estado["seleccion"]
            if cartas[a]["id"] == cartas[z]["id"]:
                estado["correctas"] += 1
                document.getElementById("main").querySelectorAll("button")[0] if False else None
                estado["seleccion"] = []
                if estado["correctas"] == len(pares):
                    terminar("Memoria", estado["correctas"], len(pares), juego.premio_memoria(estado["correctas"]))
            else:
                estado["bloqueado"] = True
                def ocultar():
                    for j in (a, z):
                        botones[j].innerHTML = "❓"
                    estado["seleccion"] = []
                    estado["bloqueado"] = False
                window.setTimeout(create_proxy(ocultar), 700)
        proxy = create_proxy(accion)
        PROXIES.append(proxy)
        b.addEventListener("click", proxy)
        cont.appendChild(b)
        # Referencia mutable para el cierre.
        if "botones" not in locals():
            botones = []
        botones.append(b)

def trivia(event=None):
    limpiar()
    preguntas = juego.nueva_trivia()
    estado = {"i": 0, "correctas": 0}
    poner(titulo("❓ Trivia"))
    caja = document.createElement("div")
    poner(caja)

    def mostrar():
        caja.innerHTML = ""
        q = preguntas[estado["i"]]
        caja.appendChild(tarjeta(f'<div class="big">{q["correcta"][1]}</div><p class="desc">🤟 {html(q["correcta"][2])}</p><p>Pregunta {estado["i"]+1} de {len(preguntas)}</p>'))
        for op in q["opciones"]:
            caja.appendChild(boton(f'{op[1]} {html(op[0])}', lambda e, op=op: responder(op)))

    def responder(op):
        q = preguntas[estado["i"]]
        if op[0] == q["correcta"][0]:
            estado["correctas"] += 1
        estado["i"] += 1
        if estado["i"] >= len(preguntas):
            terminar("Trivia", estado["correctas"], len(preguntas), juego.premio_trivia(estado["correctas"]))
        else:
            mostrar()
    mostrar()

def frases(event=None):
    limpiar()
    preguntas = juego.nuevas_frases()
    estado = {"i": 0, "correctas": 0, "elegidas": []}
    poner(titulo("🧩 Construye frases"))
    caja = document.createElement("div")
    poner(caja)

    def mostrar():
        caja.innerHTML = ""
        q = preguntas[estado["i"]]
        estado["elegidas"] = []
        objetivo = [x for x in q]
        signos = {s[0]: s for s in CATALOGO}
        caja.appendChild(tarjeta('<div class="desc">Ordena las palabras para formar la frase.</div><div class="out" id="resultado"> </div>'))
        for palabra in objetivo:
            s = signos.get(palabra, (palabra, "🔹", "Palabra"))
            caja.appendChild(boton(f'{s[1]} {html(palabra)}', lambda e, palabra=palabra: elegir(palabra)))
    def elegir(palabra):
        if palabra in estado["elegidas"]:
            return
        estado["elegidas"].append(palabra)
        out = document.getElementById("resultado")
        if out:
            out.innerHTML = " ".join(estado["elegidas"])
        q = preguntas[estado["i"]]
        if len(estado["elegidas"]) == len(q):
            if juego.evaluar_frase(estado["elegidas"], q):
                estado["correctas"] += 1
            estado["i"] += 1
            if estado["i"] >= len(preguntas):
                terminar("Frases", estado["correctas"], len(preguntas), juego.premio_frases(estado["correctas"]))
            else:
                window.setTimeout(create_proxy(lambda: mostrar()), 600)
    mostrar()

def terminar(actividad, correctas, total, xp):
    sumar_xp(DB, USUARIO_ACTUAL, xp, actividad, correctas, total)
    limpiar()
    poner(
        tarjeta(f'<h2>🎉 Resultado</h2><p>{html(actividad)}: <b>{correctas}/{total}</b></p><p>⭐ <b>+{xp} XP</b></p>'),
        boton("🏠 Volver al menú", menu),
    )

def progreso(event=None):
    limpiar()
    u = obtener(DB, USUARIO_ACTUAL)
    r = rango(u["xp"])
    contenido = f'<div class="big">{r[1]}</div><div class="word">{html(r[2])}</div><p>⭐ {u["xp"]} puntos</p>'
    poner(titulo("⭐ Mi progreso"), tarjeta(contenido))
    if not u["historial"]:
        poner(tarjeta("Todavía no tienes actividades registradas."))
        return
    tabla = "<table><tr><th>Fecha</th><th>Actividad</th><th>Resultado</th><th>XP</th></tr>"
    for x in u["historial"]:
        tabla += f'<tr><td>{html(x["fecha"])}</td><td>{html(x["actividad"])}</td><td>{x["correctas"]}/{x["total"]}</td><td>+{x["xp"]}</td></tr>'
    tabla += "</table>"
    poner(tarjeta(tabla))

def panel_docente(event=None):
    limpiar()
    poner(titulo("👩‍🏫 Panel docente"))
    pin = document.createElement("input")
    pin.id = "pin"
    pin.type = "password"
    pin.placeholder = "PIN docente"
    poner(pin, boton("Entrar", entrar_docente))
    poner(tarjeta("PIN de demostración: 1234"))

def entrar_docente(event=None):
    if docente.verificar_pin(document.getElementById("pin").value):
        mostrar_panel()
    else:
        window.alert("PIN incorrecto.")

def mostrar_panel():
    limpiar()
    poner(titulo("👩‍🏫 Gestión docente"))
    poner(tarjeta(f"<b>📚 Catálogo:</b> {len(CATALOGO)} señas"))
    lista = document.createElement("div")
    lista.className = "card"
    for i, s in enumerate(CATALOGO):
        fila = document.createElement("div")
        fila.className = "rowitem"
        fila.innerHTML = f"{s[1]} <b>{html(s[0])}</b> — {html(s[2])}"
        fila.appendChild(boton("🗑️", lambda e, i=i: borrar_sena(i)))
        lista.appendChild(fila)
    poner(lista)

    poner(titulo("➕ Agregar seña"))
    for ident, placeholder in [("nw","Palabra"),("ne","Emoji"),("nd","Descripción")]:
        inp = document.createElement("input")
        inp.id = ident
        inp.placeholder = placeholder
        poner(inp)
    poner(boton("Agregar", agregar_sena))

    poner(titulo("📊 Progreso del grupo"))
    resumen = docente.resumen_grupo(DB)
    if resumen:
        filas = "<table><tr><th>Alumno</th><th>Act.</th><th>Prom.</th><th>XP</th><th>Rango</th></tr>"
        for x in resumen:
            filas += f'<tr><td>{html(x["nombre"])}</td><td>{x["actividades"]}</td><td>{x["promedio"]}%</td><td>{x["xp"]}</td><td>{html(x["rango"])}</td></tr>'
        filas += "</table>"
        poner(tarjeta(filas))
    else:
        poner(tarjeta("No hay alumnos registrados todavía."))
    poner(boton("📄 Exportar CSV", exportar_csv), boton("🏠 Volver", menu if USUARIO_ACTUAL else inicio))

def agregar_sena(event=None):
    p = document.getElementById("nw").value
    e = document.getElementById("ne").value
    d = document.getElementById("nd").value
    if docente.agregar_sena(CATALOGO, p, e, d):
        datos.guardar(DB)
        mostrar_panel()
    else:
        window.alert("Completa los tres campos.")

def borrar_sena(indice):
    if docente.eliminar_sena(CATALOGO, indice):
        mostrar_panel()
    else:
        window.alert("No se puede eliminar esa seña.")

def exportar_csv(event=None):
    contenido = docente.csv_grupo(DB)
    blob = Blob.new([contenido], {"type": "text/csv;charset=utf-8"})
    url = URL.createObjectURL(blob)
    a = document.createElement("a")
    a.href = url
    a.download = "manos_que_hablan_progreso.csv"
    a.click()
    URL.revokeObjectURL(url)

# Exponer funciones útiles para depuración desde la consola.
window.mqh_inicio = inicio
window.mqh_menu = menu

inicio()
