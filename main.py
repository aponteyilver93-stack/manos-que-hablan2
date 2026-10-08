"""
MANOS QUE HABLAN - Software educativo para aprender señas (Python en la web con PyScript)
© 2026 Yilver Aponte, McGrady Torrealba y Mileidi Ventura. Todos los derechos reservados.
Proyecto sociotecnológico Trayecto II - UPT de Aragua "Federico Brito Figueroa"

Toda la lógica del juego está escrita en Python y corre en el navegador (teléfono o computador).
El progreso se guarda en el propio aparato (localStorage).
"""
import json
import random

from pyscript import document, window
from pyscript.ffi import create_proxy

KEY = "mqh_py_v1"

# (puntos mínimos, emoji, nombre)
RK = [(0, "🌱", "Semilla"), (50, "🐣", "Pollito"), (120, "🦋", "Mariposa"), (220, "🐬", "Delfín"),
      (350, "🦁", "León"), (520, "🦉", "Búho sabio"), (750, "🦅", "Águila"),
      (1000, "🏆", "Campeón de las señas"), (1500, "👑", "Maestro de las señas")]

# IMPORTANTE: validar las descripciones con un docente o intérprete de lengua de señas.
SENAS = [
    ("hola", "👋", "Mueve la mano abierta de lado a lado, como saludando."),
    ("adiós", "🖐️", "Abre y cierra la mano frente a ti, como despidiéndote."),
    ("gracias", "🙏", "Lleva la mano plana desde la barbilla hacia adelante."),
    ("por favor", "🤲", "Frota la palma de la mano sobre tu pecho en círculos."),
    ("perdón", "😔", "Frota el puño cerrado sobre tu pecho en círculos."),
    ("sí", "👍", "Mueve el puño cerrado arriba y abajo, como cabeceando."),
    ("no", "🙅", "Mueve el dedo índice de lado a lado."),
    ("bien", "👌", "Une pulgar e índice en círculo y estira los otros dedos."),
    ("mal", "👎", "Cierra el puño y apunta el pulgar hacia abajo."),
    ("ayuda", "🆘", "Pon un puño sobre la palma de la otra mano y súbelas juntas."),
    ("yo", "🙋", "Señala tu pecho con el dedo índice."),
    ("tú", "🫵", "Señala con el dedo índice a la otra persona."),
    ("mamá", "👩", "Toca la barbilla con el pulgar de la mano abierta."),
    ("papá", "👨", "Toca la frente con el pulgar de la mano abierta."),
    ("bebé", "👶", "Mece los brazos como si cargaras un bebé."),
    ("amigo", "🤝", "Engancha los dedos índices de ambas manos."),
    ("maestro", "🧑‍🏫", "Mueve las manos abiertas desde la frente hacia adelante."),
    ("comer", "🍽️", "Junta los dedos y llévalos a la boca varias veces."),
    ("beber", "🥤", "Forma una C con la mano y llévala a la boca, inclinándola."),
    ("dormir", "😴", "Apoya la mano abierta en la mejilla e inclina la cabeza."),
    ("jugar", "🎮", "Agita las manos con pulgares y meñiques extendidos."),
    ("correr", "🏃", "Mueve los brazos doblados adelante y atrás, como corriendo."),
    ("leer", "📖", "Con dos dedos 'lee' sobre la palma de la otra mano."),
    ("escribir", "✍️", "Finge escribir con un lápiz sobre la palma de la otra mano."),
    ("caminar", "🚶", "Mueve dos dedos como piernas caminando sobre la palma."),
    ("ver", "👀", "Lleva dos dedos desde los ojos hacia afuera."),
    ("querer", "🤗", "Lleva las manos abiertas hacia ti cerrando los dedos."),
    ("casa", "🏠", "Une las puntas de las manos formando un techo."),
    ("escuela", "🏫", "Aplaude suavemente dos veces."),
    ("libro", "📚", "Junta las palmas y ábrelas como un libro."),
    ("agua", "💧", "Toca la barbilla con tres dedos extendidos, como una W."),
    ("pan", "🍞", "Con una mano 'corta' el dorso de la otra, como rebanando pan."),
    ("leche", "🥛", "Abre y cierra el puño, como ordeñando."),
    ("pelota", "⚽", "Curva ambas manos como sosteniendo una pelota."),
    ("carro", "🚗", "Mueve las manos como si manejaras un volante."),
    ("sol", "☀️", "Dibuja un círculo sobre tu cabeza y abre los dedos hacia abajo."),
    ("luna", "🌙", "Forma una C con la mano y súbela, como una luna creciente."),
    ("perro", "🐶", "Da palmadas suaves en el muslo, como llamando a un perro."),
    ("gato", "🐱", "Estira los dedos junto a la mejilla, como bigotes."),
    ("pájaro", "🐦", "Abre y cierra pulgar e índice frente a la boca, como un pico."),
    ("pez", "🐟", "Mueve la mano plana de lado a lado, como un pez nadando."),
    ("feliz", "😊", "Sube la mano abierta por el pecho con una sonrisa."),
    ("triste", "😢", "Baja la mano abierta frente a la cara con gesto triste."),
    ("enojado", "😠", "Curva los dedos frente a la cara, como garras, con gesto de enojo."),
    ("miedo", "😨", "Lleva las manos abiertas al pecho con gesto de susto."),
    ("amor", "❤️", "Cruza los brazos sobre el pecho, como un abrazo."),
    ("frío", "🥶", "Abraza tu cuerpo con los puños cerrados, temblando."),
    ("calor", "🥵", "Abanica tu cara con la mano."),
    ("uno", "1️⃣", "Levanta el dedo índice."),
    ("dos", "2️⃣", "Levanta los dedos índice y medio."),
    ("tres", "3️⃣", "Levanta los dedos índice, medio y anular."),
]

# Cada palabra es "seña" o "seña:como_se_escribe" (así el verbo sale conjugado).
FRASES = ["hola amigo", "yo comer:como", "tú beber:bebes", "yo dormir:duermo", "gracias amigo",
          "yo feliz:estoy_feliz", "yo querer:quiero agua", "yo querer:quiero comer", "yo leer:leo libro",
          "tú jugar:juegas pelota", "yo ver:veo perro", "mamá dormir:duerme", "papá ver:ve carro",
          "yo caminar:camino", "tú escribir:escribes", "yo beber:bebo agua", "yo correr:corro"]

BACK = '<button class="ghost back" data-a="go" data-v="menu">⬅ Salir</button>'


# ------------------------------ Datos (en el aparato) ------------------------------
def leer():
    try:
        raw = window.localStorage.getItem(KEY)
        d = json.loads(raw) if raw else {}
    except Exception:
        d = {}
    d.setdefault("signs", [{"w": w, "p": p, "d": t} for w, p, t in SENAS])
    d.setdefault("users", {})
    d.setdefault("last", None)
    d.setdefault("pin", None)
    return d


def guardar():
    try:
        window.localStorage.setItem(KEY, json.dumps(DB))
    except Exception:
        pass


DB = leer()
S = {"user": None, "ep": 0, "gain": 0, "r0": 0, "g": {}}
main = document.getElementById("main")
nav = document.getElementById("nav")


# ------------------------------------ Utilidades ------------------------------------
def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def cap(t):
    return t[:1].upper() + t[1:]


def later(fn, ms):
    """Ejecuta fn después de ms, solo si el jugador no cambió de pantalla."""
    ep = S["ep"]

    def run():
        if ep == S["ep"]:
            fn()

    window.setTimeout(create_proxy(run), ms)


def val(id_):
    return str(document.getElementById(id_).value or "").strip()


def pic(w):
    for s in DB["signs"]:
        if s["w"] == w:
            return s["p"]
    return "❔"


def token(t):
    w, _, f = t.partition(":")
    return w, (f or w).replace("_", " ")


def xp():
    return DB["users"][S["user"]]["xp"]


def rank_i(x=None):
    x = xp() if x is None else x
    return max(i for i, r in enumerate(RK) if x >= r[0])


def start():
    S["gain"] = 0
    S["r0"] = rank_i()


def add_xp(n):
    DB["users"][S["user"]]["xp"] += n
    S["gain"] += n
    guardar()


def rank_card():
    x = xp()
    i = rank_i(x)
    r = RK[i]
    n = RK[i + 1] if i + 1 < len(RK) else None
    pct = round(100 * (x - r[0]) / (n[0] - r[0])) if n else 100
    extra = f" · faltan {n[0] - x} para {n[1]} {n[2]}" if n else " · ¡Rango máximo!"
    return (f'<div class="card"><div class="big">{r[1]}</div><div class="word" style="font-size:26px">{r[2]}</div>'
            f'<p class="sub">⭐ {x} puntos{extra}</p><div class="bar"><i style="width:{pct}%"></i></div></div>')


def aviso(msg):
    main.innerHTML = BACK + f'<div class="card"><p class="desc">{esc(msg)}</p></div>'


def end(act, p, t, again):
    u = DB["users"][S["user"]]
    u["log"].append({"a": act, "p": p, "t": t, "f": str(window.Date.new().toLocaleString("es-VE"))})
    guardar()
    pc = 100 * p / t if t else 0
    stars = "⭐" * (3 if pc >= 80 else 2 if pc >= 50 else 1)
    up = ""
    if rank_i() > S["r0"]:
        r = RK[rank_i()]
        up = (f'<div class="card" style="background:var(--ok);color:#000"><div class="big">{r[1]}</div>'
              f'<h2 style="color:#000">¡Subiste a {r[2]}!</h2></div>')
    main.innerHTML = (f'<div class="card" style="margin-top:24px"><h2>¡Muy bien, {esc(S["user"])}!</h2>'
                      f'<div class="stars">{stars}</div><p class="desc">{act}: {p} de {t} ({pc:.0f}%)</p>'
                      f'<p class="desc"><b>⭐ +{S["gain"]} puntos</b></p></div>{up}'
                      f'<button style="width:100%;background:var(--ok);margin-bottom:10px" data-a="go" data-v="{again}">🔁 Jugar otra vez</button>'
                      '<button class="ghost" style="width:100%" data-a="go" data-v="menu">🏠 Menú</button>')


# ------------------------------------- Pantallas -------------------------------------
def v_login():
    S["user"] = None
    main.innerHTML = (
        '<div class="card" style="margin-top:24px"><div class="big">🤟</div><h2>¡Bienvenido!</h2>'
        '<p class="desc">Aprende señas jugando</p></div>'
        '<p class="sub" style="text-align:center">¿Cómo te llamas?</p>'
        '<input id="nm" placeholder="Tu nombre" maxlength="20">'
        '<button style="width:100%;margin-top:8px;background:var(--ok)" data-a="enter">▶ Entrar</button>'
        '<button class="ghost" style="width:100%;margin-top:30px;font-size:15px" data-a="go" data-v="teacher">👩‍🏫 Panel docente</button>')


def v_menu():
    tiles = [("learn", "📖 Aprender señas"), ("memory", "🧠 Memoria"), ("trivia", "❓ Trivia"),
             ("phrases", "🧩 Armar frases"), ("progress", "⭐ Mi progreso")]
    b = "".join(f'<button class="tile" data-a="go" data-v="{k}">{t}</button>' for k, t in tiles)
    main.innerHTML = (f'<h2>¡Hola, {esc(S["user"])}!</h2><p class="sub">¿Qué quieres hacer?</p>{rank_card()}'
                      f'<div class="grid" style="margin-top:12px">{b}'
                      '<button class="tile ghost" data-a="logout">🚪 Cambiar jugador</button></div>')


def v_learn():
    if not DB["signs"]:
        return aviso("Todavía no hay señas cargadas.")
    S["g"] = {"i": 0}
    render_learn()


def render_learn():
    sg = DB["signs"]
    i = S["g"]["i"]
    s = sg[i]
    main.innerHTML = (BACK + f'<h2>Aprender señas</h2><p class="sub">{i + 1} de {len(sg)}</p>'
                      f'<div class="card"><div class="big">{esc(s["p"])}</div><div class="word">{esc(s["w"].upper())}</div>'
                      f'<p class="desc">🤟 {esc(s["d"])}</p></div>'
                      '<div class="row"><button data-a="learn_mv" data-v="-1">⬅ Anterior</button>'
                      '<button data-a="learn_mv" data-v="1">Siguiente ➡</button></div>')


def v_memory():
    if len(DB["signs"]) < 4:
        return aviso("Se necesitan al menos 4 señas para jugar a la memoria.")
    start()
    pick = random.sample(DB["signs"], 4)
    cards = []
    for s in pick:
        cards.append({"k": s["w"], "t": "p", "s": s})
        cards.append({"k": s["w"], "t": "s", "s": s})
    random.shuffle(cards)
    S["g"] = {"cards": cards, "sel": [], "done": [], "tries": 0, "lock": False}
    render_memory()


def render_memory():
    g = S["g"]
    out = []
    for i, c in enumerate(g["cards"]):
        shown = i in g["sel"] or i in g["done"]
        if not shown:
            label, cls = "❓", "mc"
        elif c["t"] == "p":
            label = f'<span style="font-size:32px">{esc(c["s"]["p"])}</span><br>{esc(c["s"]["w"])}'
            cls = "mc open"
        else:
            label, cls = "🤟 " + esc(c["s"]["d"]), "mc open sg"
        dis = ""
        if i in g["done"]:
            cls += " ok"
            dis = " disabled"
        out.append(f'<button class="{cls}" data-a="mem" data-v="{i}"{dis}>{label}</button>')
    main.innerHTML = (BACK + '<h2>Memoria</h2><p class="sub">Une el dibujo con su seña</p><div class="grid">'
                      + "".join(out) + "</div>")


def a_mem(v):
    g = S["g"]
    i = int(v)
    if g["lock"] or i in g["sel"] or i in g["done"]:
        return
    g["sel"].append(i)
    if len(g["sel"]) == 2:
        a, b = g["sel"]
        g["tries"] += 1
        if g["cards"][a]["k"] == g["cards"][b]["k"]:
            g["done"] += [a, b]
            g["sel"] = []
            add_xp(10)
            if len(g["done"]) == len(g["cards"]):
                render_memory()
                later(lambda: end("Memoria", len(g["done"]) // 2, g["tries"], "memory"), 700)
                return
        else:
            g["lock"] = True

            def ocultar():
                g["sel"] = []
                g["lock"] = False
                render_memory()

            render_memory()
            later(ocultar, 1000)
            return
    render_memory()


def v_trivia():
    sg = DB["signs"]
    if len(sg) < 4:
        return aviso("Se necesitan al menos 4 señas para la trivia.")
    start()
    S["g"] = {"q": random.sample(sg, min(5, len(sg))), "i": 0, "ok": 0, "ans": None, "opts": []}
    nueva_pregunta()


def nueva_pregunta():
    g = S["g"]
    s = g["q"][g["i"]]
    ops = random.sample([x for x in DB["signs"] if x is not s], 3) + [s]
    random.shuffle(ops)
    g["opts"], g["ans"] = ops, None
    render_trivia()


def render_trivia():
    g = S["g"]
    s = g["q"][g["i"]]
    btns = []
    for k, o in enumerate(g["opts"]):
        cls, dis = "tile", ""
        if g["ans"] is not None:
            dis = " disabled"
            if o is s:
                cls += " ok"
            elif k == g["ans"]:
                cls += " bad"
        btns.append(f'<button class="{cls}" data-a="tri" data-v="{k}"{dis}>{esc(o["p"])} {esc(o["w"])}</button>')
    main.innerHTML = (BACK + f'<h2>Trivia {g["i"] + 1}/{len(g["q"])}</h2><p class="sub">¿Qué palabra es esta seña?</p>'
                      f'<div class="card"><p class="desc" style="font-size:22px">🤟 {esc(s["d"])}</p></div>'
                      f'<div class="grid">{"".join(btns)}</div>')


def a_tri(v):
    g = S["g"]
    if g["ans"] is not None:
        return
    g["ans"] = int(v)
    if g["opts"][g["ans"]] is g["q"][g["i"]]:
        g["ok"] += 1
        add_xp(10)
    render_trivia()

    def siguiente():
        g["i"] += 1
        if g["i"] >= len(g["q"]):
            end("Trivia", g["ok"], len(g["q"]), "trivia")
        else:
            nueva_pregunta()

    later(siguiente, 1100)


def v_phrases():
    ph = [[token(t) for t in f.lower().split()] for f in FRASES]
    ph = [f for f in ph if len(f) >= 2 and all(pic(w) != "❔" for w, _ in f)]
    if not ph:
        return aviso("No hay frases disponibles con las señas actuales.")
    start()
    S["g"] = {"ph": random.sample(ph, min(3, len(ph))), "i": 0, "ok": 0}
    nueva_frase()


def nueva_frase():
    g = S["g"]
    ws = list(g["ph"][g["i"]])
    random.shuffle(ws)
    g["ws"], g["used"], g["res"] = ws, [], None
    render_phrases()


def render_phrases():
    g = S["g"]
    meta = g["ph"][g["i"]]
    txt = cap(" ".join(g["ws"][k][1] for k in g["used"])) if g["used"] else "&nbsp;"
    cls = "out"
    if g["res"] is True:
        txt, cls = esc(txt) + ".", "out ok"
    elif g["res"] is False:
        txt, cls = esc(txt), "out bad"
    elif g["used"]:
        txt = esc(txt)
    btns = "".join(
        f'<button class="opt" data-a="ph" data-v="{k}"{" disabled" if k in g["used"] else ""}>{pic(w)} {esc(f)}</button>'
        for k, (w, f) in enumerate(g["ws"]))
    main.innerHTML = (BACK + f'<h2>Arma la frase {g["i"] + 1}/{len(g["ph"])}</h2>'
                      '<p class="sub">Toca las palabras en el orden de los dibujos</p>'
                      f'<div class="card"><div class="big" style="font-size:40px">{" ➜ ".join(pic(w) for w, _ in meta)}</div></div>'
                      f'<div class="{cls}">{txt}</div><div class="row">{btns}</div>')


def a_ph(v):
    g = S["g"]
    k = int(v)
    if g["res"] is not None or k in g["used"]:
        return
    g["used"].append(k)
    meta = g["ph"][g["i"]]
    if len(g["used"]) == len(meta):
        good = [g["ws"][j] for j in g["used"]] == list(meta)
        g["res"] = good
        if good:
            g["ok"] += 1
            add_xp(5 * len(meta))
        render_phrases()

        def siguiente():
            if not good:
                return nueva_frase()
            g["i"] += 1
            if g["i"] >= len(g["ph"]):
                end("Frases", g["ok"], len(g["ph"]), "phrases")
            else:
                nueva_frase()

        later(siguiente, 1300)
    else:
        render_phrases()


def v_progress():
    log = DB["users"][S["user"]]["log"]
    if log:
        rows = "".join(f'<tr><td>{esc(r["f"])}</td><td>{esc(r["a"])}</td><td>{r["p"]}/{r["t"]}</td></tr>'
                       for r in reversed(log[-20:]))
        body = f'<div class="card"><table><tr><th>Fecha</th><th>Actividad</th><th>Resultado</th></tr>{rows}</table></div>'
    else:
        body = '<div class="card"><p class="desc">Aún no has jugado. ¡Prueba una actividad!</p></div>'
    main.innerHTML = f'<h2>⭐ Mi progreso</h2>{rank_card()}{body}'


def v_ranks():
    i = rank_i()
    cards = []
    for k, r in enumerate(RK):
        borde = "border:3px solid var(--ac);" if k == i else ""
        opaco = "opacity:.65;" if k > i else ""
        marca = " ✅" if k < i else " · ¡Tu rango!" if k == i else ""
        cards.append(f'<div class="card" style="display:flex;align-items:center;gap:14px;text-align:left;{borde}{opaco}">'
                     f'<div class="big" style="font-size:40px">{r[1]}</div>'
                     f'<div><b style="font-size:20px">{esc(r[2])}</b><br>{r[0]} puntos{marca}</div></div>')
    main.innerHTML = '<h2>🏅 Rangos</h2><p class="sub">¡Gana puntos para subir de rango!</p>' + "".join(cards)


# ------------------------------------ Panel docente ------------------------------------
def v_teacher():
    nuevo = not DB["pin"]
    campo2 = '<input id="pin2" type="password" inputmode="numeric" maxlength="6" placeholder="Repite el PIN">' if nuevo else ""
    main.innerHTML = ('<h2>👩‍🏫 Panel docente</h2><p class="sub">'
                      + ("Crea un PIN de 4 a 6 números para entrar al panel" if nuevo else "Ingresa el PIN") + "</p>"
                      '<input id="pin" type="password" inputmode="numeric" maxlength="6" placeholder="PIN">' + campo2 +
                      f'<button style="width:100%" data-a="pin_ok">{"Guardar y entrar" if nuevo else "Entrar"}</button>'
                      '<button class="ghost" style="width:100%;margin-top:10px" data-a="logout_soft">⬅ Volver</button>')


def a_pin_ok(_):
    v = val("pin")
    if not DB["pin"]:
        if v.isdigit() and 4 <= len(v) <= 6 and val("pin2") == v:
            DB["pin"] = v
            guardar()
            go("panel")
        else:
            window.alert("Usa 4 a 6 números y repítelos igual.")
    elif v == DB["pin"]:
        go("panel")
    else:
        window.alert("PIN incorrecto.")


def v_panel():
    filas = "".join(f'<tr><td>{esc(s["p"])} {esc(s["w"])}</td>'
                    f'<td><button class="bad" style="padding:4px 10px;font-size:14px" data-a="del_sign" data-v="{i}">🗑</button></td></tr>'
                    for i, s in enumerate(DB["signs"]))
    grupo = ""
    for n, u in sorted(DB["users"].items()):
        log = u["log"]
        prom = f"{sum(100 * r['p'] / r['t'] for r in log if r['t']) / len(log):.0f}%" if log else "-"
        grupo += f'<tr><td>{esc(n)}</td><td>{len(log)}</td><td>{prom}</td><td>{RK[rank_i(u["xp"])][1]}</td></tr>'
    salir = "menu" if S["user"] else "login"
    main.innerHTML = (
        '<h2>👩‍🏫 Panel docente</h2>'
        f'<div class="card"><b>📚 Señas ({len(DB["signs"])})</b><table>{filas}</table></div>'
        '<div class="card"><b>➕ Nueva seña</b><input id="nw" placeholder="Palabra"><input id="np" placeholder="Emoji (🤟)">'
        '<input id="nd" placeholder="Cómo se hace la seña"><button style="width:100%" data-a="add_sign">Agregar</button></div>'
        '<div class="card"><b>📊 Progreso del grupo</b><table><tr><th>Alumno</th><th>Actividades</th><th>Promedio</th><th>Rango</th></tr>'
        f'{grupo}</table><button class="ghost" style="width:100%;margin-top:10px" data-a="csv">📄 Exportar CSV</button></div>'
        '<button class="ghost" style="width:100%;margin-bottom:10px" data-a="chg_pin">🔑 Cambiar PIN</button>'
        f'<button class="ghost" style="width:100%" data-a="go" data-v="{salir}">⬅ Salir</button>')


def a_add_sign(_):
    w, p, d = val("nw").lower(), val("np") or "🤟", val("nd")
    if w and d and not any(s["w"] == w for s in DB["signs"]):
        DB["signs"].append({"w": w, "p": p, "d": d})
        guardar()
    go("panel")


def a_del_sign(v):
    del DB["signs"][int(v)]
    guardar()
    go("panel")


def a_csv(_):
    filas = ["Estudiante;Actividad;Puntaje;Total;Fecha"]
    for n, u in sorted(DB["users"].items()):
        for r in u["log"]:
            filas.append(f'{n};{r["a"]};{r["p"]};{r["t"]};{r["f"]}')
    a = document.createElement("a")
    a.href = "data:text/csv;charset=utf-8," + str(window.encodeURIComponent("\ufeff" + "\n".join(filas)))
    a.download = "reporte_progreso.csv"
    a.click()


def a_chg_pin(_):
    DB["pin"] = None
    guardar()
    go("teacher")


# ----------------------------- Navegación y eventos -----------------------------
VIEWS = {"login": v_login, "menu": v_menu, "learn": v_learn, "memory": v_memory, "trivia": v_trivia,
         "phrases": v_phrases, "progress": v_progress, "ranks": v_ranks, "teacher": v_teacher, "panel": v_panel}


def go(view):
    if not S["user"] and view not in ("login", "teacher", "panel"):
        view = "login"
    S["ep"] += 1
    S["g"] = {}
    if S["user"] and view not in ("teacher", "panel"):
        items = [("menu", "🏠"), ("ranks", "🏅"), ("progress", "⭐")]
        nav.innerHTML = "".join(
            f'<button class="{"on" if k == view else ""}" data-a="go" data-v="{k}">{i}</button>' for k, i in items)
        nav.hidden = False
    else:
        nav.hidden = True
    VIEWS[view]()
    window.scrollTo(0, 0)


def a_enter(_):
    partes = val("nm").split()
    n = " ".join(p[:1].upper() + p[1:].lower() for p in partes)
    if not n:
        return
    DB["users"].setdefault(n, {"xp": 0, "log": []})
    DB["last"] = n
    guardar()
    S["user"] = n
    go("menu")


def a_logout(_):
    DB["last"] = None
    guardar()
    S["user"] = None
    go("login")


def a_theme(_):
    raiz = document.documentElement
    t = "light" if raiz.getAttribute("data-theme") == "dark" else "dark"
    raiz.setAttribute("data-theme", t)
    document.getElementById("th").textContent = "🌙" if t == "dark" else "☀️"


ACT = {"go": lambda v: go(v), "enter": a_enter, "logout": a_logout, "logout_soft": lambda v: go("menu" if S["user"] else "login"),
       "learn_mv": lambda v: (S["g"].update(i=(S["g"]["i"] + int(v)) % len(DB["signs"])), render_learn()),
       "mem": a_mem, "tri": a_tri, "ph": a_ph, "pin_ok": a_pin_ok, "add_sign": a_add_sign, "del_sign": a_del_sign,
       "csv": a_csv, "chg_pin": a_chg_pin, "theme": a_theme}


def on_click(ev):
    el = ev.target.closest("[data-a]")
    if el is None:
        return
    ACT[el.getAttribute("data-a")](el.getAttribute("data-v") or "")


def on_key(ev):
    if ev.key == "Enter" and ev.target.id == "nm":
        a_enter("")


app = document.getElementById("app")
app.addEventListener("click", create_proxy(on_click))
app.addEventListener("keydown", create_proxy(on_key))
document.documentElement.setAttribute("data-theme", "dark")

if DB["last"] in DB["users"]:
    S["user"] = DB["last"]
    go("menu")
else:
    go("login")
