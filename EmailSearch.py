#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mateo Contenla"
__license__ = "Apache-2.0"
__email__ = "mcontenlaf@gmail.com"

from socket import gethostbyname
from google import search
import requests
import re
import os
import sys
from random import choice


def user_agent():
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.801.0 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.803.0 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.32 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 Safari/534.30",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11"]

    return choice(user_agents)


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
    msje_ayuda = """Uso: EmailSearch.py <Opciones>

Opciones:
  -U [url], --url [url]                      Dirección web de la página a analizar.
  -N [nivel], --nivel [nivel]                Cantidad de páginas del dominio a analizar
                                             (Default es el máximo posible).

Ejemplos:
    EmailSearch.py -U www.dominio.com        Buscar la mayor cantidad de direcciones de 
                                             correo en ese dominio.
    
    EmailSearch.py -U www.dominio.com -N 50  Buscar direcciones de correo en hasta 50 
                                             páginas de ese dominio. (Útil si quieres que 
                                             Google no bloquee tu IP).
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
        argumento = sys.argv[indice_largo + 1]

    else:
        argumento = default

    return argumento


# Función que hace todo el trabajo sucio
def email_search(dominio, maxN):
    emails_total = []
    regex_email = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')

# En caso de que maxN sea 0 (El default), ya que no sabemos el índice máximo al que llegaremos, se imprime un signo de interrogación
    max_indice = None
    if maxN == 0:
        max_indice = "?"
    else:
        max_indice = maxN

    try:
        query = "site:{}".format(dominio)
        res_busqueda = search(query, stop=maxN)
        for ind, url in enumerate(res_busqueda):
            headers = {"User-Agent": user_agent()}
            req = requests.get(url, headers=headers)
            emails = re.findall(regex_email, req.text)
            for email in emails:
                if email not in emails_total:
                    emails_total.append(email)

            sys.stdout.write("\r{bold}{amarillo}{0}/{1}{end} {bold}páginas analizadas | {bold}{amarillo}{2}{end} {bold}emails encontrados{end}".format(ind + 1, max_indice, len(emails_total), amarillo=colores.AMARILLO, end=colores.ENDC, bold=colores.BOLD))
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass

    finally:
        return emails_total


# Definimos la función main() donde se comenzará a ejecutar el programa
def main():
    dominio = None
    nivel = 0
    verbose = True
    ip = ""

    if len(sys.argv) > 1:

# Obtenemos los argumentos del programa. Feo, pero funciona :P
        try:
            dominio = get_argv("-U", "--url", None)
            nivel = int(get_argv("-N", "--nivel", 0))
            ip = gethostbyname(dominio)

        except Exception:
            ayuda()
    else:
        ayuda()

# Todo a continuación muestra graficamente la lista de correos encontrados
    print("{verde}{bold}[+] Analizando {rojo}{bold}'{pagina}' {verde}({rojo}{ip}{verde}){end}".format(verde=colores.VERDE, end=colores.ENDC, bold=colores.BOLD, rojo=colores.ROJO, pagina=dominio, ip=ip))

    emails = email_search(dominio, nivel)
    
    print("\n\n{bold}{verde}---------- {rojo}{0} Emails encontrados{verde} ----------".format(len(emails), bold=colores.BOLD, verde=colores.VERDE, rojo=colores.ROJO))

    for email in emails:
        print("{verde}[+]{end} {email}".format(verde=colores.VERDE, end=colores.ENDC, email=email))


main()
