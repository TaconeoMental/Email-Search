#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import gethostbyname
from google import search
import requests
import re
import os
import sys


# Función que devuelve el sistema operativo utilizado
def ver_SO():
    if os.name == "nt":
        sistema_operativo = "windows"
    if os.name == "posix":
        sistema_operativo = "posix"
    return sistema_operativo

if ver_SO() == "posix":

# Clase que contiene colores para la CLI
    class colores:
        AMARILLO = '\033[93m'
        VERDE = '\033[92m'
        ROJO = '\033[91m'
        BOLD = '\033[1m'
        ENDC = '\033[0m'

# En caso de estar en un SO como windows, definimos los colores como nada
else:

    class colores:
        AMARILLO = ''
        VERDE = ''
        ROJO = ''
        BOLD = ''
        ENDC = ''

def ayuda():
    msje_ayuda = """Uso: EmailSearch.py [opciones]

Opciones:
  -H, --help                  Muestra este mensaje de ayuda
  -U [url], --url [url]
                              Dirección web de la página a analizar
  -N [nivel], --nivel [nivel]
                              Cantidad de páginas a analizar (Todas dentro del mismo dominio)
  -nV, --no-verbose
                              Desactiva el output a stdout
    """
    print(msje_ayuda)
    sys.exit()

# Función para obtener argumentos de dos tipos (Por ejemplo: "-U" y "--url")
def get_argv(tipo_corto, tipo_largo, default):
    if tipo_corto in sys.argv:
        indice_corto = sys.argv.index(tipo_corto)
        argumento = sys.argv[indice_corto + 1]

    elif tipo_largo in sys.argv:
        indice_largo = sys.argv.index(tipo_largo)
        argumento = sys.argv[indice_corto + 1]

    else:
        argumento = default

    return argumento


# Función que hace todo el trabajo sucio
def email_search(dominio, maxN, verbose):
    emails_total = []
    regex_email = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')

    try:
        query = "site:{}".format(dominio)
        res_busqueda = search(query, stop=maxN)
        for ind, url in enumerate(res_busqueda):
            req = requests.get(url, allow_redirects=False)
            emails = re.findall(regex_email, req.text)
            for email in emails:
                if email not in emails_total:
                    emails_total.append(email)

            if verbose:
                sys.stdout.write("\r{bold}{amarillo}{0}/{1}{end} {bold}páginas analizadas | {bold}{amarillo}{2}{end} {bold}emails encontrados{end}".format(ind + 1, maxN, len(emails_total), amarillo=colores.AMARILLO, end=colores.ENDC, bold=colores.BOLD))
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass

    finally:
        return emails_total


# Definimos la función main() donde se comenzará a ejecutar el programa
def main():
    dominio = None
    nivel = 20
    verbose = True
    ip = ""

    if len(sys.argv) > 1:

# Obtenemos los argumentos del programa. Feo, pero funciona :P
        try:
            dominio = get_argv("-U", "--url", None)
            nivel = int(get_argv("-N", "--nivel", 20))
            verbose = get_argv("-nV", "--no-verbose", True)
            ip = gethostbyname(dominio)

        except Exception as e:
            print(str(e))
            ayuda()
    else:
        ayuda()

# Todo a continuación muestra graficamente la lista de correos encontrados
    print("{verde}{bold}[+] Escaneando {rojo}{bold}'{pagina}' {verde}({rojo}{ip}{verde}){end}".format(verde=colores.VERDE, end=colores.ENDC, bold=colores.BOLD, rojo=colores.ROJO, pagina=dominio, ip=ip))

    emails = email_search(dominio, nivel, verbose)

    print("\n\n{bold}{verde}---------- {rojo}{0} Emails encontrados{verde} ----------".format(len(emails), bold=colores.BOLD, verde=colores.VERDE, rojo=colores.ROJO))

    for email in emails:
        print("{verde}[+]{end} {email}".format(verde=colores.VERDE, end=colores.ENDC, email=email))


main()
