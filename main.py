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

# IMPORTANTE: las descripciones son de REFERENCIA. Deben ser validadas por un docente o intérprete
# de lengua de señas antes de usarse con los niños (cada país tiene su propia lengua de señas).
CATS = [("saludos", "👋", "Saludos"), ("personas", "👪", "Personas y familia"), ("acciones", "🏃", "Acciones"),
        ("comida", "🍎", "Comida"), ("escuela", "🏫", "Casa y escuela"), ("animales", "🐶", "Animales y naturaleza"),
        ("emociones", "😊", "Emociones"), ("cuerpo", "🖐️", "Cuerpo y salud"), ("tiempo", "⏰", "Tiempo y orden"),
        ("numeros", "🔢", "Números"), ("colores", "🎨", "Colores"), ("otras", "✨", "Otras")]


def _c(cat, filas):
    return [(w, p, d, cat) for w, p, d in filas]


SENAS = (
    _c("saludos", [
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
        ("buenos días", "🌅", "Haz la seña de 'día' (la mano sube como el sol) y luego saluda con la mano."),
        ("buenas noches", "🌙", "Haz la seña de 'noche' (la mano baja) y junta las manos junto a la mejilla."),
        ("con permiso", "🙇", "Abre camino con la mano plana hacia adelante, inclinando un poco la cabeza."),
        ("de nada", "😊", "Mueve la mano abierta hacia adelante con una sonrisa."),
        ("mucho gusto", "🥰", "Toca tu pecho y luego extiende la mano con una sonrisa."),
    ]) +
    _c("personas", [
        ("yo", "🙋", "Señala tu pecho con el dedo índice."),
        ("tú", "🫵", "Señala con el dedo índice a la otra persona."),
        ("mamá", "👩", "Toca la barbilla con el pulgar de la mano abierta."),
        ("papá", "👨", "Toca la frente con el pulgar de la mano abierta."),
        ("bebé", "👶", "Mece los brazos como si cargaras un bebé."),
        ("amigo", "🤝", "Engancha los dedos índices de ambas manos."),
        ("maestro", "🧑‍🏫", "Mueve las manos abiertas desde la frente hacia adelante."),
        ("hermano", "👦", "Toca la sien con el índice y luego junta ambos índices, uno al lado del otro."),
        ("hermana", "👧", "Toca la mejilla con el índice y luego junta ambos índices, uno al lado del otro."),
        ("abuelo", "👴", "Haz la seña de 'papá' y baja la mano como acariciando una barba larga."),
        ("abuela", "👵", "Haz la seña de 'mamá' y baja la mano como acariciando un moño."),
        ("tío", "🧔", "Haz la letra T con la mano y tócate cerca de la frente."),
        ("niño", "🧒", "Con la mano plana, muestra una altura baja, a la altura de tu cintura."),
        ("familia", "👨‍👩‍👧", "Haz la letra F con ambas manos y dibuja un círculo uniéndolas."),
        ("nosotros", "👥", "Señala tu pecho y luego a los demás, haciendo un círculo con el índice."),
    ]) +
    _c("acciones", [
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
        ("abrir", "🔓", "Junta las manos planas y sepáralas, como abriendo una puerta."),
        ("cerrar", "🔒", "Separa las manos planas y júntalas, como cerrando una puerta."),
        ("esperar", "⏳", "Mueve los dedos de una mano abierta, con la palma hacia arriba, esperando."),
        ("dar", "🎁", "Extiende ambas manos hacia adelante, como entregando algo."),
        ("compartir", "👐", "Mueve una mano plana de lado a lado sobre la palma de la otra, repartiendo."),
        ("cantar", "🎤", "Mueve la mano en ondas frente a la boca, como notas que salen."),
        ("bailar", "💃", "Balancea los dedos índice y medio sobre la palma de la otra mano, como bailando."),
        ("dibujar", "🖍️", "Con el dedo índice, 'dibuja' líneas sobre la palma de la otra mano."),
        ("escuchar", "👂", "Lleva la mano en forma de C detrás de la oreja."),
        ("hablar", "🗣️", "Mueve el dedo índice hacia adelante frente a la boca, varias veces."),
        ("sentarse", "🪑", "Apoya dos dedos de una mano sobre los dedos de la otra, como sentándose."),
        ("lavar", "🧼", "Frota las manos una contra la otra, como lavándote."),
        ("pensar", "🤔", "Toca la frente con el índice y haz un pequeño círculo."),
        ("aprender", "🧠", "Toma algo de la palma de una mano con la otra y llévalo a la frente."),
        ("saltar", "🤸", "Con dos dedos sobre la palma de la otra mano, haz que salten."),
    ]) +
    _c("comida", [
        ("agua", "💧", "Toca la barbilla con tres dedos extendidos, como una W."),
        ("pan", "🍞", "Con una mano 'corta' el dorso de la otra, como rebanando pan."),
        ("leche", "🥛", "Abre y cierra el puño, como ordeñando."),
        ("manzana", "🍎", "Con el puño cerrado, gira suavemente sobre la mejilla."),
        ("banana", "🍌", "Finge pelar una banana con una mano sobre el dedo índice de la otra."),
        ("arroz", "🍚", "Con los dedos en pellizco, 'siembra' granitos sobre la palma de la otra mano."),
        ("huevo", "🥚", "Golpea suavemente dos dedos sobre la otra mano y ábrelos, como quebrando un huevo."),
        ("queso", "🧀", "Presiona la base de una mano contra la palma de la otra, girando."),
        ("sopa", "🍲", "Finge llevar una cuchara desde la palma de una mano hasta la boca."),
        ("jugo", "🧃", "Haz la letra J en el aire y luego finge beber."),
        ("galleta", "🍪", "Con una mano en C, presiona sobre la palma de la otra, como cortando una galleta."),
        ("pollo", "🍗", "Pellizca con los dedos frente a la boca, como un pico, y mueve el codo como un ala."),
        ("fruta", "🍇", "Toca la mejilla con la letra F y gírala."),
        ("helado", "🍦", "Finge lamer un helado con la mano cerrada frente a la boca."),
        ("carne", "🥩", "Pellizca suavemente la parte carnosa entre el pulgar y el índice."),
    ]) +
    _c("escuela", [
        ("casa", "🏠", "Une las puntas de las manos formando un techo."),
        ("escuela", "🏫", "Aplaude suavemente dos veces."),
        ("libro", "📚", "Junta las palmas y ábrelas como un libro."),
        ("pelota", "⚽", "Curva ambas manos como sosteniendo una pelota."),
        ("carro", "🚗", "Mueve las manos como si manejaras un volante."),
        ("lápiz", "✏️", "Finge sostener un lápiz y escribe en el aire."),
        ("cuaderno", "📓", "Junta las palmas, ábrelas y finge escribir en una de ellas."),
        ("silla", "💺", "Golpea dos dedos sobre otros dos dedos de la otra mano, como una silla."),
        ("mochila", "🎒", "Lleva las manos a los hombros, como sujetando las correas."),
        ("tijeras", "✂️", "Abre y cierra los dedos índice y medio, como tijeras."),
        ("puerta", "🚪", "Con las manos planas, ábrelas y ciérralas como una puerta que gira."),
        ("computadora", "💻", "Abre una mano como pantalla y mueve los dedos de la otra como si tecleara."),
        ("teléfono", "📱", "Lleva el puño, con pulgar y meñique extendidos, a la oreja."),
        ("bicicleta", "🚲", "Gira los puños uno tras otro, como pedaleando."),
        ("juguete", "🧸", "Haz el gesto de 'jugar' y luego sujeta algo pequeño con las manos."),
        ("música", "🎵", "Mueve la mano en ondas, balanceando el brazo suavemente."),
        ("cama", "🛏️", "Junta las manos junto a la mejilla e inclina la cabeza, como en una cama."),
    ]) +
    _c("animales", [
        ("sol", "☀️", "Dibuja un círculo sobre tu cabeza y abre los dedos hacia abajo."),
        ("luna", "🌙", "Forma una C con la mano y súbela, como una luna creciente."),
        ("perro", "🐶", "Da palmadas suaves en el muslo, como llamando a un perro."),
        ("gato", "🐱", "Estira los dedos junto a la mejilla, como bigotes."),
        ("pájaro", "🐦", "Abre y cierra pulgar e índice frente a la boca, como un pico."),
        ("pez", "🐟", "Mueve la mano plana de lado a lado, como un pez nadando."),
        ("vaca", "🐮", "Lleva el pulgar a la sien y mueve la mano, como un cuerno."),
        ("caballo", "🐴", "Con el pulgar en la sien, mueve los dedos como orejas de caballo."),
        ("gallina", "🐔", "Abre y cierra los dedos frente a la boca, como un pico, y mueve los codos como alas."),
        ("conejo", "🐰", "Cruza las muñecas y mueve los dedos como orejas largas."),
        ("mono", "🐵", "Rasca los costados del cuerpo con los dedos curvos, como un mono."),
        ("león", "🦁", "Pasa la mano por la cabeza hacia atrás, como una melena."),
        ("tortuga", "🐢", "Cubre un puño con la otra mano y asoma el pulgar, como una cabeza."),
        ("mariposa", "🦋", "Cruza las manos y mueve los dedos como alas."),
        ("árbol", "🌳", "Apoya el codo en la otra mano y abre los dedos, como ramas."),
        ("flor", "🌸", "Junta los dedos y llévalos a la nariz, como oliendo una flor."),
        ("lluvia", "🌧️", "Baja las manos moviendo los dedos, como gotas que caen."),
        ("nube", "☁️", "Pasa las manos curvas sobre tu cabeza, como una nube."),
        ("estrella", "⭐", "Choca suavemente los índices hacia arriba, como estrellitas."),
        ("mar", "🌊", "Mueve las manos planas en ondas, como las olas."),
    ]) +
    _c("emociones", [
        ("feliz", "😊", "Sube la mano abierta por el pecho con una sonrisa."),
        ("triste", "😢", "Baja la mano abierta frente a la cara con gesto triste."),
        ("enojado", "😠", "Curva los dedos frente a la cara, como garras, con gesto de enojo."),
        ("miedo", "😨", "Lleva las manos abiertas al pecho con gesto de susto."),
        ("amor", "❤️", "Cruza los brazos sobre el pecho, como un abrazo."),
        ("frío", "🥶", "Abraza tu cuerpo con los puños cerrados, temblando."),
        ("calor", "🥵", "Abanica tu cara con la mano."),
        ("cansado", "🥱", "Deja caer las manos sobre el pecho con los hombros hacia abajo."),
        ("sorprendido", "😮", "Abre los ojos y lleva ambas manos hacia arriba, abriendo los dedos."),
        ("tranquilo", "😌", "Baja las manos abiertas despacio frente al pecho, soltando el aire."),
        ("aburrido", "😑", "Toca la nariz con el índice y gíralo, con cara de aburrido."),
        ("vergüenza", "🙈", "Pasa el dorso de la mano por la mejilla, hacia arriba."),
        ("preocupado", "😟", "Alterna los puños frente a la frente, con el ceño fruncido."),
    ]) +
    _c("cuerpo", [
        ("mano", "✋", "Pasa el dorso de una mano sobre la palma de la otra."),
        ("boca", "👄", "Señala tu boca con el dedo índice."),
        ("ojo", "👁️", "Señala tu ojo con el dedo índice."),
        ("oreja", "👂", "Toca tu oreja con el dedo índice."),
        ("nariz", "👃", "Toca tu nariz con el dedo índice."),
        ("cabeza", "🙂", "Toca tu cabeza con la mano abierta."),
        ("pie", "🦶", "Señala tu pie con el dedo índice."),
        ("dolor", "🤕", "Señala la parte que te duele, con gesto de dolor."),
        ("enfermo", "🤒", "Toca la frente y el estómago con el dedo medio, con gesto de malestar."),
        ("médico", "🧑‍⚕️", "Toca la muñeca con dos dedos, como tomando el pulso."),
        ("hambre", "🤤", "Pasa la mano en forma de C por el pecho hacia abajo."),
        ("sed", "🚰", "Pasa el dedo índice por la garganta hacia abajo."),
        ("baño", "🚽", "Mueve la mano en forma de T de lado a lado."),
        ("descanso", "🛋️", "Cruza los brazos sobre el pecho y deja caer los hombros."),
    ]) +
    _c("tiempo", [
        ("hoy", "📅", "Baja las manos abiertas, con la palma hacia arriba, frente a ti."),
        ("mañana", "🌄", "Mueve el pulgar desde la mejilla hacia adelante."),
        ("ayer", "⏪", "Mueve el pulgar desde la mejilla hacia atrás."),
        ("ahora", "⏰", "Baja ambas manos con un movimiento corto, como señalando 'aquí'."),
        ("después", "⏭️", "Mueve la mano hacia adelante desde el hombro."),
        ("antes", "⏮️", "Mueve la mano hacia atrás por encima del hombro."),
        ("día", "🌞", "Sube el brazo con el codo apoyado, como el sol que sale."),
        ("noche", "🌃", "Cruza las manos sobre la cabeza, bajando, como cuando oscurece."),
        ("primero", "🥇", "Muestra el dedo índice frente a ti, con la otra mano a su lado."),
        ("luego", "➡️", "Mueve la mano hacia adelante en arco."),
        ("terminado", "✅", "Gira las manos abiertas hacia afuera, como diciendo 'acabé'."),
        ("más", "➕", "Junta las puntas de los dedos de ambas manos, varias veces."),
        ("otra vez", "🔁", "Gira la mano plana en curva hasta caer sobre la palma de la otra."),
        ("rápido", "🐇", "Mueve el índice hacia adelante con un tirón veloz."),
        ("despacio", "🐌", "Pasa una mano lentamente sobre el dorso de la otra."),
    ]) +
    _c("numeros", [
        ("cero", "0️⃣", "Forma un círculo con los dedos, como la letra O."),
        ("uno", "1️⃣", "Levanta el dedo índice."),
        ("dos", "2️⃣", "Levanta los dedos índice y medio."),
        ("tres", "3️⃣", "Levanta los dedos índice, medio y anular."),
        ("cuatro", "4️⃣", "Levanta cuatro dedos, sin el pulgar."),
        ("cinco", "5️⃣", "Levanta la mano abierta, con los cinco dedos."),
        ("seis", "6️⃣", "Muestra una mano abierta y suma un dedo de la otra mano."),
        ("siete", "7️⃣", "Muestra una mano abierta y suma dos dedos de la otra mano."),
        ("ocho", "8️⃣", "Muestra una mano abierta y suma tres dedos de la otra mano."),
        ("nueve", "9️⃣", "Muestra una mano abierta y suma cuatro dedos de la otra mano."),
        ("diez", "🔟", "Muestra las dos manos abiertas."),
    ]) +
    _c("colores", [
        ("rojo", "🔴", "Pasa el dedo índice por los labios, de arriba hacia abajo."),
        ("azul", "🔵", "Con la letra B, mueve la muñeca de lado a lado."),
        ("amarillo", "🟡", "Con la letra Y, mueve la muñeca de lado a lado."),
        ("verde", "🟢", "Con la letra V, mueve la muñeca de lado a lado."),
        ("naranja", "🟠", "Aprieta y suelta el puño junto a la boca, como exprimiendo una naranja."),
        ("morado", "🟣", "Con la letra M, mueve la muñeca de lado a lado."),
        ("negro", "⚫", "Pasa el dedo índice por la frente, de lado a lado."),
        ("blanco", "⚪", "Toca el pecho con la mano abierta y aléjala cerrando los dedos."),
        ("café", "🟤", "Con la letra C, mueve la muñeca de lado a lado."),
        ("rosado", "💗", "Con la letra R, mueve la muñeca de lado a lado."),
    ])
)
CAT_DE = {w: c for w, _, _, c in SENAS}

# Cada palabra es "seña" o "seña:como_se_escribe" (así el verbo sale conjugado).
FRASES = ["hola amigo", "yo comer:como", "tú beber:bebes", "yo dormir:duermo", "gracias amigo",
          "yo feliz:estoy_feliz", "yo querer:quiero agua", "yo querer:quiero comer", "yo leer:leo libro",
          "tú jugar:juegas pelota", "yo ver:veo perro", "mamá dormir:duerme", "papá ver:ve carro",
          "yo caminar:camino", "tú escribir:escribes", "yo beber:bebo agua", "yo correr:corro",
          "buenos_días maestro", "buenas_noches mamá", "yo querer:quiero jugar", "yo querer:quiero manzana",
          "yo comer:como arroz", "yo dibujar:dibujo casa", "yo bailar:bailo", "tú cantar:cantas",
          "yo lavar:me_lavo mano:las_manos", "yo abrir:abro puerta:la_puerta", "yo escuchar:escucho música",
          "yo hambre:tengo_hambre", "yo sed:tengo_sed", "yo cansado:estoy_cansado", "hermano jugar:juega pelota",
          "abuela cantar:canta", "abuelo ver:ve pájaro", "yo tranquilo:estoy_tranquilo"]

BACK = '<button class="ghost back" data-a="go" data-v="menu">⬅ Salir</button>'


# ------------------------------ Datos (en el aparato) ------------------------------
def leer():
    try:
        raw = window.localStorage.getItem(KEY)
        d = json.loads(raw) if raw else {}
    except Exception:
        d = {}
    d.setdefault("signs", [{"w": w, "p": p, "d": t, "c": c} for w, p, t, c in SENAS])
    d.setdefault("users", {})
    d.setdefault("last", None)
    d.setdefault("pin", None)
    # Actualización v1.1: a quien ya tenía datos guardados se le agregan las señas nuevas y las categorías.
    if d.get("ver", 1) < 2:
        have = {s["w"] for s in d["signs"]}
        for w, p, t, c in SENAS:
            if w not in have:
                d["signs"].append({"w": w, "p": p, "d": t, "c": c})
        d["ver"] = 2
    for s in d["signs"]:
        s.setdefault("c", CAT_DE.get(s["w"], "otras"))
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
    return w.replace("_", " "), (f or w).replace("_", " ")


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
                      '<button class="tile ghost" data-a="logout">🚪 Cambiar jugador</button>'
                      '<button class="tile space" data-a="go" data-v="space">🌈 Mi espacio tranquilo</button></div>')


def v_learn():
    if not DB["signs"]:
        return aviso("Todavía no hay señas cargadas.")
    S["g"] = {"i": 0, "c": "todas"}
    render_learn()


def lista_learn():
    c = S["g"].get("c", "todas")
    if c == "todas":
        return DB["signs"]
    return [s for s in DB["signs"] if s.get("c", "otras") == c]


def render_learn():
    c = S["g"].get("c", "todas")
    sg = lista_learn()
    if not sg:
        S["g"]["c"], c = "todas", "todas"
        sg = DB["signs"]
    i = S["g"]["i"] % len(sg)
    S["g"]["i"] = i
    s = sg[i]
    hay = {x.get("c", "otras") for x in DB["signs"]}
    chips = [f'<button class="chip{" on" if c == "todas" else ""}" data-a="learn_cat" data-v="todas">🌟 Todas ({len(DB["signs"])})</button>']
    for k, e, n in CATS:
        if k in hay:
            cuantas = sum(1 for x in DB["signs"] if x.get("c", "otras") == k)
            chips.append(f'<button class="chip{" on" if c == k else ""}" data-a="learn_cat" data-v="{k}">{e} {n} ({cuantas})</button>')
    main.innerHTML = (BACK + f'<h2>Aprender señas</h2><div class="chips">{"".join(chips)}</div>'
                      f'<p class="sub">{i + 1} de {len(sg)}</p>'
                      f'<div class="card"><div class="big">{esc(s["p"])}</div><div class="word">{esc(s["w"].upper())}</div>'
                      f'<p class="desc">🤟 {esc(s["d"])}</p></div>'
                      '<div class="row"><button data-a="learn_mv" data-v="-1">⬅ Anterior</button>'
                      '<button data-a="learn_mv" data-v="1">Siguiente ➡</button></div>'
                      '<p class="sub" style="font-size:14px;text-align:center;opacity:.75">Descripción de referencia: '
                      'tu maestra o intérprete te muestra la seña exacta.</p>')


def a_learn_mv(v):
    n = len(lista_learn()) or 1
    S["g"]["i"] = (S["g"]["i"] + int(v)) % n
    render_learn()


def a_learn_cat(v):
    S["g"]["c"], S["g"]["i"] = v, 0
    render_learn()


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


# --------------------- Mi espacio tranquilo (apoyo para niños con autismo) ---------------------
# Principios: sin puntos, sin cronómetro, sin sonidos ni luces fuertes, todo predecible y opcional.
# Cada herramienta es un apoyo visual: rutina, emociones, comunicación, "primero-luego" y calma.
# IMPORTANTE: estas actividades deben ser revisadas y adaptadas por la docente o el especialista.
RUTINA = [("🚪", "Llegar a la escuela"), ("👋", "Saludar"), ("📖", "Aprender"), ("🎮", "Jugar"),
          ("🍽️", "Comer"), ("🛋️", "Descansar"), ("🏠", "Ir a casa")]

# (emoji, palabra, mensaje, ayudas, ¿ofrecer respirar?)
SENTIR = [
    ("😊", "feliz", "¡Qué bien! Puedes sonreír y contárselo a alguien.", ["👋 Contarle a un amigo", "🎮 Jugar"], False),
    ("😢", "triste", "Está bien sentirse triste. No estás solo.",
     ["🤗 Pedir un abrazo", "🆘 Decirle a un adulto", "🛋️ Descansar un rato"], True),
    ("😠", "enojado", "Está bien sentir enojo. Vamos a calmarnos despacio.",
     ["🤫 Pedir silencio", "🛋️ Ir a un lugar tranquilo", "🆘 Pedir ayuda"], True),
    ("😨", "miedo", "Estás seguro. Puedes pedir ayuda cuando quieras.", ["🆘 Pedir ayuda", "🤗 Pedir un abrazo"], True),
    ("😟", "preocupado", "Respira. Un adulto puede ayudarte.", ["🆘 Contarle a un adulto", "🧸 Abrazar algo suave"], True),
    ("🥱", "cansado", "Tu cuerpo necesita descansar.", ["🛋️ Pedir un descanso", "💧 Tomar agua"], False),
    ("🤕", "dolor", "Si algo te duele, díselo a un adulto.", ["🆘 Pedir ayuda", "☝️ Señalar dónde te duele"], False),
    ("😌", "tranquilo", "¡Qué bien! Disfruta este momento.", ["📖 Aprender una seña", "🎵 Escuchar música"], False),
]

# (emoji, seña, frase que se dice)
QUIERO = [("💧", "agua", "Quiero agua"), ("🍽️", "comer", "Quiero comer"), ("🚽", "baño", "Necesito ir al baño"),
          ("🆘", "ayuda", "Necesito ayuda"), ("🎮", "jugar", "Quiero jugar"), ("🛋️", "descanso", "Quiero descansar"),
          ("🤫", "silencio", "Necesito silencio"), ("🤗", "abrazo", "Quiero un abrazo"), ("➕", "más", "Quiero más"),
          ("✅", "terminado", "Ya terminé"), ("🙅", "no", "No"), ("👍", "sí", "Sí")]

PRIMERO = [("📖", "aprender"), ("✍️", "escribir"), ("🧼", "lavarme las manos"), ("🍽️", "comer"),
           ("🎒", "guardar mi mochila"), ("🧩", "armar frases")]
LUEGO = [("🎮", "jugar"), ("🎵", "escuchar música"), ("⚽", "jugar pelota"), ("🛋️", "descansar"),
         ("🍪", "comer galleta"), ("🖍️", "dibujar")]

BACK_E = '<button class="ghost back" data-a="go" data-v="space">⬅ Mi espacio</button>'


def calma(html):
    main.innerHTML = '<div class="calm">' + html + "</div>"


def sdesc(w):
    for s in DB["signs"]:
        if s["w"] == w:
            return s["d"]
    return ""


def v_space():
    items = [("routine", "📅", "Mi rutina"), ("feel", "😊", "¿Cómo me siento?"), ("want", "🗣️", "Quiero…"),
             ("firstthen", "1️⃣➡️", "Primero y luego"), ("calm", "🫧", "Respirar")]
    b = "".join(f'<button class="big-btn" data-a="go" data-v="{k}"><span>{e}</span> {t}</button>' for k, e, t in items)
    calma(BACK + '<h2>🌈 Mi espacio tranquilo</h2>'
          '<p class="sub">Aquí no hay puntos ni tiempo. Elige lo que necesites.</p>' + f'<div class="stack">{b}</div>')


# --- Mi rutina (agenda visual) ---
def hoy():
    return str(window.Date.new().toLocaleDateString("es-VE"))


def rut():
    u = DB["users"][S["user"]]
    r = u.get("rut")
    if not r or r.get("d") != hoy():
        r = u["rut"] = {"d": hoy(), "h": 0}
    return r


def v_routine():
    render_routine()


def render_routine():
    n = rut()["h"]
    filas = []
    for k, (e, t) in enumerate(RUTINA):
        cls, mark = ("step done", "✅") if k < n else ("step now", "👉") if k == n else ("step", "")
        filas.append(f'<div class="{cls}"><span class="e">{e}</span><span class="t">{esc(t)}</span><span class="m">{mark}</span></div>')
    if n < len(RUTINA):
        acc = f'<button class="big-btn ok" data-a="rut_ok">✅ Listo: {esc(RUTINA[n][1])}</button>'
    else:
        acc = '<div class="card"><div class="big">🌟</div><p class="desc">¡Terminaste tu día! Lo hiciste muy bien.</p></div>'
    calma(BACK_E + '<h2>📅 Mi rutina de hoy</h2><p class="sub">Vamos paso a paso. Toca “Listo” cuando termines.</p>'
          + "".join(filas) + acc +
          '<button class="ghost" style="width:100%;margin-top:10px" data-a="rut_reset">↩ Empezar de nuevo</button>')


def a_rut_ok(_):
    r = rut()
    if r["h"] < len(RUTINA):
        r["h"] += 1
        guardar()
    render_routine()


def a_rut_reset(_):
    rut()["h"] = 0
    guardar()
    render_routine()


# --- ¿Cómo me siento? ---
def v_feel():
    S["g"] = {"f": None}
    render_feel()


def render_feel():
    f = S["g"].get("f")
    if f is None:
        b = "".join(f'<button class="fc" data-a="feel" data-v="{k}"><span>{e}</span>{esc(w)}</button>'
                    for k, (e, w, _m, _a, _r) in enumerate(SENTIR))
        calma(BACK_E + '<h2>😊 ¿Cómo me siento?</h2><p class="sub">Toca la carita que se parece a ti.</p>'
              f'<div class="grid">{b}</div>')
        return
    e, w, m, ayudas, resp = SENTIR[f]
    d = sdesc(w)
    seña = f'<p class="desc">🤟 {esc(d)}</p>' if d else ""
    ay = "".join(f'<div class="step"><span class="t">{esc(a)}</span></div>' for a in ayudas)
    rb = '<button class="big-btn" data-a="go" data-v="calm"><span>🫧</span> Respirar un rato</button>' if resp else ""
    calma(BACK_E + f'<div class="card"><div class="big" style="font-size:88px">{e}</div>'
          f'<div class="word">{esc(w.upper())}</div><p class="desc">{esc(m)}</p>{seña}</div>'
          f'<p class="sub">Qué puedo hacer:</p>{ay}{rb}'
          '<button class="ghost" style="width:100%;margin-top:10px" data-a="feel_back">↩ Elegir otra carita</button>')


def a_feel(v):
    S["g"]["f"] = int(v)
    render_feel()


def a_feel_back(_):
    S["g"]["f"] = None
    render_feel()


# --- Quiero… (tablero de comunicación) ---
def v_want():
    S["g"] = {"w": None}
    render_want()


def render_want():
    w = S["g"].get("w")
    if w is None:
        b = "".join(f'<button class="fc" data-a="want" data-v="{k}"><span>{e}</span>{esc(p)}</button>'
                    for k, (e, p, _f) in enumerate(QUIERO))
        calma(BACK_E + '<h2>🗣️ Quiero…</h2><p class="sub">Toca un dibujo para decir lo que necesitas.</p>'
              f'<div class="grid">{b}</div>')
        return
    e, p, frase = QUIERO[w]
    d = sdesc(p)
    seña = f'<p class="desc">🤟 {esc(d)}</p>' if d else ""
    calma(BACK_E + f'<div class="card"><div class="big" style="font-size:96px">{e}</div>'
          f'<div class="word">{esc(frase)}</div>{seña}</div>'
          f'<button class="big-btn" data-a="say" data-v="{esc(frase)}"><span>🔊</span> Decir en voz alta</button>'
          '<button class="ghost" style="width:100%;margin-top:10px" data-a="want_back">↩ Elegir otra</button>')


def a_want(v):
    S["g"]["w"] = int(v)
    render_want()


def a_want_back(_):
    S["g"]["w"] = None
    render_want()


def a_say(v):
    """Lee la frase en voz alta (solo si la persona toca el botón)."""
    try:
        u = window.SpeechSynthesisUtterance.new(v)
        u.lang = "es-ES"
        u.rate = 0.9
        window.speechSynthesis.cancel()
        window.speechSynthesis.speak(u)
    except Exception:
        pass


# --- Primero y luego ---
def v_firstthen():
    S["g"] = {"f": None, "l": None, "d": False}
    render_ft()


def render_ft():
    g = S["g"]
    if g["f"] is None or g["l"] is None:
        primero = g["f"] is None
        lista, act = (PRIMERO, "ft_f") if primero else (LUEGO, "ft_l")
        b = "".join(f'<button class="fc" data-a="{act}" data-v="{k}"><span>{e}</span>{esc(t)}</button>'
                    for k, (e, t) in enumerate(lista))
        calma(BACK_E + '<h2>1️⃣➡️ Primero y luego</h2>'
              f'<p class="sub">{"Primero voy a…" if primero else "Luego quiero…"}</p><div class="grid">{b}</div>')
        return
    e1, t1 = PRIMERO[g["f"]]
    e2, t2 = LUEGO[g["l"]]
    hecho = g["d"]
    c1 = f'<div class="ftc{" done" if hecho else " now"}"><small>PRIMERO</small><span>{e1}</span>{esc(t1)}{" ✅" if hecho else ""}</div>'
    c2 = f'<div class="ftc{" now" if hecho else ""}"><small>LUEGO</small><span>{e2}</span>{esc(t2)}</div>'
    if hecho:
        acc = f'<div class="card"><div class="big">🎉</div><p class="desc">¡Muy bien! Ahora toca: {e2} {esc(t2)}</p></div>'
    else:
        acc = '<button class="big-btn ok" data-a="ft_done">✅ Ya terminé lo primero</button>'
    calma(BACK_E + '<h2>1️⃣➡️ Primero y luego</h2>'
          f'<div class="ftb">{c1}<div class="arr">➜</div>{c2}</div>{acc}'
          '<button class="ghost" style="width:100%;margin-top:10px" data-a="ft_reset">↩ Hacer otro</button>')


def a_ft_f(v):
    S["g"]["f"] = int(v)
    render_ft()


def a_ft_l(v):
    S["g"]["l"] = int(v)
    render_ft()


def a_ft_done(_):
    S["g"]["d"] = True
    render_ft()


def a_ft_reset(_):
    S["g"] = {"f": None, "l": None, "d": False}
    render_ft()


# --- Respirar ---
def v_calm():
    calma(BACK_E + '<h2>🫧 Respirar</h2><p class="sub">Mira el círculo. Respira despacio con él.</p>'
          '<div class="resp-wrap"><div class="resp"></div></div>'
          '<p class="desc" style="text-align:center">Cuando quieras, toca “Mi espacio”.</p>')


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
         "phrases": v_phrases, "progress": v_progress, "ranks": v_ranks, "teacher": v_teacher, "panel": v_panel,
         "space": v_space, "routine": v_routine, "feel": v_feel, "want": v_want, "firstthen": v_firstthen,
         "calm": v_calm}


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
       "learn_mv": a_learn_mv, "learn_cat": a_learn_cat,
       "rut_ok": a_rut_ok, "rut_reset": a_rut_reset, "feel": a_feel, "feel_back": a_feel_back,
       "want": a_want, "want_back": a_want_back, "say": a_say,
       "ft_f": a_ft_f, "ft_l": a_ft_l, "ft_done": a_ft_done, "ft_reset": a_ft_reset,
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
