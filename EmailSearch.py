#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import gethostbyname
from google import search
import requests
import re
import os
import sys

# Clase que contiene colores para la CLI
class colores:
    AMARILLO = '\033[93m'
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    

# Función que hace todo el trabajo sucio
def email_search(dominio, maxN, verbose):
    emails_total = []
    regex_email = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')

    try:
        query = "site:{}".format(dominio)
        res_busqueda = search(query, stop=maxN)
        for ind, url in enumerate(res_busqueda):
            if verbose:
                sys.stdout.write("\r{bold}{amarillo}{0}/{1}{end} {bold}páginas analizadas | {bold}{amarillo}{2}{end} {bold}emails encontrados{end}".format(ind + 1, maxN, len(emails_total), amarillo=colores.AMARILLO, end=colores.ENDC, bold=colores.BOLD))
                sys.stdout.flush()
            req = requests.get(url, allow_redirects=False)
            emails = re.findall(regex_email, req.text)
            for email in emails:
			    if email not in emails_total:
			        emails_total.append(email)

    except KeyboardInterrupt:
        pass
        
    finally:
        return emails_total


# Definimos la función main() donde se comenzará a ejecutar el programa
def main():
    dominio = ""
    nivel = 20
    verbose = False

# Obtenemos los argumentos del programa. Feo, pero funciona :P
    if len(sys.argv) > 1:
        try:
            if "-d" in sys.argv:
                indice_d = sys.argv.index("-d")
                dominio = sys.argv[indice_d + 1]
                ip = gethostbyname(dominio)
            if "-n" in sys.argv:
                indice_n = sys.argv.index("-n")
                nivel = int(sys.argv[indice_n + 1])
            if "-v" in sys.argv:
                verbose = True
        except Exception:
            pass
            # ayuda()
            
# Todo a continuación muestra graficamente la lista de correos encontrados
    print("{verde}{bold}[+] Escaneando {rojo}{bold}'{pagina}' {verde}({rojo}{ip}{verde}){end}".format(verde=colores.VERDE, end=colores.ENDC, bold=colores.BOLD, rojo=colores.ROJO, pagina=dominio, ip=ip))
            
    emails = email_search(dominio, nivel, verbose)
    
    print("\n\n{bold}{verde}---------- {rojo}{0} Emails encontrados{verde} ----------".format(len(emails), bold=colores.BOLD, verde=colores.VERDE, rojo=colores.ROJO))
    
    for email in emails:
        print("{verde}[+]{end} {email}".format(verde=colores.VERDE, end=colores.ENDC, email=email))
            

main()
