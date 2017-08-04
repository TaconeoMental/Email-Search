#!/usr/bin/env python

from socket import gethostbyname
from google import search
import requests
import re
import os

def mostrar(lista):
    total = set(lista)
    print("\n\n")
    os.system("cls")
    print("{} emails encontrados:".format(len(total)))
    for email in total:
        print("[+] {}".format(email))


def sub_search(dominio, maxN=50):
    emails_total = []
    regex_email = re.compile(r'[\w\.-]+@[\w\.-]+')

    try:

        query = "site:{}".format(dominio)
        res_busqueda = search(query, stop=maxN)
        for url in res_busqueda:
            print("Buscando en [{}]".format(url))
            req = requests.get(url, allow_redirects=False)
            emails = re.findall(regex_email, req.text)
            print("{} emails encontrados".format(len(emails)))
            emails_total += emails

    except KeyboardInterrupt:
        pass

    finally:
        mostrar(emails_total)



def main():        
    dominio = input("Escribe el dominio a escanear: ")

    sub_search("http://{}".format(dominio))

main()

        
