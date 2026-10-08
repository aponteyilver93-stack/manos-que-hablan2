# Lógica de las actividades del videojuego.
import random
from senas import SENAS
from evaluacion import crear_memoria, crear_trivia, crear_frases, comprobar_frase
from evaluacion import xp_memoria, xp_trivia, xp_frases

def catalogo():
    return SENAS[:]

def nueva_memoria():
    return crear_memoria(4)

def nueva_trivia():
    return crear_trivia(5)

def nuevas_frases():
    return crear_frases(3)

def barajar(items):
    copia = list(items)
    random.shuffle(copia)
    return copia

def evaluar_frase(elegidas, correcta):
    return comprobar_frase(elegidas, correcta)

def premio_memoria(correctas):
    return xp_memoria(correctas)

def premio_trivia(correctas):
    return xp_trivia(correctas)

def premio_frases(correctas):
    return xp_frases(correctas)
