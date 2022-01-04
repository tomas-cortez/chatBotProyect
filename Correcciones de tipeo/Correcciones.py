# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:49:24 2021

@author: Diego
"""

# ---------------------------------------------------------------------
# Corrección de errores de tipeo!
# ------------------------------

# Letras repetidas

import re
import spacy
nlp=spacy.load('es_core_news_lg')

# Cargar lista de palabras y frecuencias
palabra_frecuencia = {}
ruta=r"C:\Users\Diego\Desktop\PLN\RAE"
with open(ruta+r"\palabra_frecuencia.txt",encoding='utf-8') as f:
    for linea in f:
       (key, val) = linea.split('#')
       palabra_frecuencia[key] = int(val)


def frecuencia(p):
    try:
        return palabra_frecuencia[p]
    except:
        return 0


# IMPORTANTE! Estrategia a considerar para armar el set de palabras/funciones de validación
"""
- nlp.vocab.strings contiene muchas palabras inútiles, e incluso también erróneas
- El archivo gigante que me bajé directamente de la RAE también: está lleno de errores incluso!
- el archivo que bajé de esa investigación privada sobre la RAE contiene un conjunto "perfecto", pero no están los plurales ni los verbos conjugados
- El lematizador de Spacy resuelve súper bien los plurales y los verbos conjugados
- Puede hacerse algún algoritmo con eso... hay que pensarlo
- Una posible aplicación: escanear la cadena a corregir, y buscar contra la lista de palabras válidas el lemma_ y no el token así natural
- Ver qué se puede hacer con los verbos conjugados...

"""

desconocidas = [x for x in palabra_frecuencia.keys() if x not in nlp.vocab.strings]
len(desconocidas)
for x in desconocidas[:100]:
    print(x)
    
almacen=[x for x in nlp.vocab.strings]
for x in almacen[1000:1100]:
    print(x)

doc=nlp('El hombre bajo, toca el bajo, bajo la luna')
for p in doc:
    print("Original: ", p)
    print("POS: ", p.pos_)
    print("TAG: ", p.tag_)
    print("Lemma: ", p.lemma_)
    print('Morph: ', p.morph)
    print('-----------')


# Función choreada de eliminación de letras repetidas según diccionario
def remove_repeated_characters(tokens,s=10):
   
   repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
   #                             CALL  L  L ES -> "CALLLLES"
   #                             CAL   L  L ES -> "CALLLES"
   #                             CA    L  L ES -> "CALLES"
   #                             CA    L    ES -> "CALES"
   match_substitution = r'\1\2\3'
   
   def replace(old_word):
      if frecuencia(old_word)>s:
         return old_word
      new_word = repeat_pattern.sub(match_substitution, old_word)
      return replace(new_word) if new_word != old_word else new_word
    
   correct_tokens = [replace(word) for word in tokens]
   return correct_tokens

# Probar ------------------
doc = nlp('Mi amigoooo: mi calllllle es la mejoooooooorrrrrr')
tokens_str=[str(x) for x in doc]
print(tokens_str)
print(remove_repeated_characters(tokens_str))


# --------------------------------------------------------
# --------------------------------------------------------

# Errores de tipeo como inversiones u omisiones
# Algoritmo de Peter Norvig

import re

def words(text): return re.findall(r'\w+', text.lower())

WORDS = palabra_frecuencia

def corregir(oracion):
    oracion_corregida=''
    for palabra in re.findall(r'\w+',oracion):
        oracion_corregida += correction(palabra)[0] + ' '
    return oracion_corregida

def correction(word): 
    "Most probable spelling correction for word."
    return [max(candidates(word), key=frecuencia)]

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or 
            known(edits1(word)) or 
            #known(edits2(word)) or 
            [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnñopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    #Para "caso":
    #    [('','caso'), -> 'aso
    #     ('c','aso'), -> 'cso
    #     ('ca','so'), -> 'cao
    #     ('cas','o'), -> 'cas
    #     ('caso','')
    #        ]
    
    deletes    = [L + R[1:]               for L, R in splits if R]
    #Para "caso":
    #   ['aso','csa','cao','cas']
    
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    #Para "caso":
    #   ['acso','csao','caos']
    
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    #Para "caso":
    #   ['xaso'...,'cxso'..., 'caxo'..., 'casx'...]
    
    inserts    = [L + c + R               for L, R in splits for c in letters]
    #Para "caso":
    #   ['xcaso'...,'cxaso'..., 'caxso'..., 'casxo'..., 'casox'...]
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# Prueba y Funciones útiles ----------

# Recibe una palabra y devuelve una lista de sólo un elemento con la coincidencia más probable
correction('caño')

# Recibe una lista de palabras y devuelve otra que contiene sólo las palabras conocidas
known(['la','casa','es','linda'])

# Devuelve la frecuencia de un término en el diccionario
frecuencia('rápido')

# Corrige una oración completa (Helper Function: Corregir)
Oracion="ahora escribo cualquir cosa ráipdo"
corregir(Oracion)

corregir('Que hoar es en londes')

corregir('que gnaas d pegame una duha')

corregir('en tooooooda decicion ay que ogservar la acion')

remove_repeated_characters(['toooooooooooda'],3)

#------------------------------------

