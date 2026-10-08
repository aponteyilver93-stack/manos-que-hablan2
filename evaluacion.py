# Generación de preguntas y cálculo de resultados.
import random
from senas import SENAS, FRASES

def opciones_sena(correcta, cantidad=4):
    otras = [s for s in SENAS if s[0] != correcta[0]]
    random.shuffle(otras)
    opciones = [correcta] + otras[:cantidad-1]
    random.shuffle(opciones)
    return opciones

def crear_trivia(cantidad=5):
    pool = SENAS[:]
    random.shuffle(pool)
    preguntas = []
    for correcta in pool[:cantidad]:
        preguntas.append({
            "correcta": correcta,
            "opciones": opciones_sena(correcta)
        })
    return preguntas

def crear_memoria(pares=4):
    pool = SENAS[:]
    random.shuffle(pool)
    return pool[:pares]

def crear_frases(cantidad=3):
    pool = FRASES[:]
    random.shuffle(pool)
    return pool[:cantidad]

def comprobar_frase(elegidas, correcta):
    return list(elegidas) == list(correcta)

def xp_memoria(correctas):
    return correctas * 10

def xp_trivia(correctas):
    return correctas * 10

def xp_frases(correctas):
    return correctas * 5
