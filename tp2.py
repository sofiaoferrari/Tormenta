import requests
import matplotlib.pyplot as plt
import csv
from PIL import Image
import ipinfo
import os


def edicion_descripcion(descripcion):
    '''
    Precondicion: Recibe la descripcion como un string y la fragmenta cada 120 caracteres por linea.
    Postcondicion: Retorna el texto modificado, como string.
    '''
    texto = list(descripcion)
    for i in range(120, len(descripcion), 120):
        separacion = [' ', '.', ',']
        while texto[i] not in separacion:
            i += 1
        texto.insert(i+1, '\n')
    texto_final = ''.join(texto)
    return texto_final


def abrir_json(url):
    '''
    Precondicion: Recibe un web service como un string e intenta abrirlo, obteniendo su estado.
    Postcondicion: Retorna un booleano.
                En el caso de que pueda abrirlo correctamente, retorna el booleano True y en el caso de que
                surja un error al abrirlo, retorna el booleano False.
    '''
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        funciona = True
    except requests.exceptions.HTTPError as errh:
        print("\nHttp Error:\n", errh)
        funciona = False
    except requests.exceptions.ConnectionError:
        print("\nConnecting Error:")
        print(f'Hubo una falla de conexion a {url}. Verifique su internet o vuelva a intentar mas tarde.')
        funciona = False
    except requests.exceptions.Timeout as errt:
        print("\nTimeout Error:\n", errt)
        funciona =  False
    except requests.exceptions.RequestException as err:
        print("\nOOps: ERROR\n", err)
        funciona = False
    return funciona


def graficar_promedios_anuales(lista_promedios,opcion):
    """
    Precondicion: recibe 2 parámetros, un diccionario con los años y sus promedios de temperatura o humedad por cada dia,
                y la opcion elegida por el usuario de tipo string. Usando la librería matplotlib se muestra gráficamente 
                lo elegido por el usuario
    """
    if opcion == "1":
        etiquetas = ["Temperaturas","Promedio de temperaturas anuales de los últimos 5 años."]
    else:
        etiquetas = ["Humedad","Promedio de humedad de los últimos 5 años."]
    años = []
    lista_promedios_total = []
    for año,datos in lista_promedios.items():
        if int(año) >= 2015:
            años.append(año)
            promedio_año = lista_promedios[año][1] / lista_promedios[año][0]
            lista_promedios_total.append(promedio_año)
    plt.style.use("seaborn")
    plt.bar(años,lista_promedios_total, width = 0.5, color = 'b')
    plt.xlabel("Años")
    plt.ylabel(etiquetas[0])
    plt.title(etiquetas[1])
    plt.tight_layout()
    plt.show()
