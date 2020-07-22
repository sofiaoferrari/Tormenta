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

def mostrar_promedio_anual(lista_promedios,opcion):
    """
    Precondición:Muestra los datos de la opción escogida
    y muestra por pantalla el año y el promedio de ese año.
    Recibe la opción escogida como un str
    y la lista de promedios como un diccionario.
    """
    maximo_valor = 0
    maximo_año = ""
    if opcion == "3":
        print("\nMilímetros máximos de lluvia de los últimos 5 años.")
        unidades = "mm"
    else:
        print("Temperatura máxima de los últimos 5 años.")
        unidades = "°C"
    for año, datos in lista_promedios.items():
        promedio_año = '%.2f' % (lista_promedios[año][1] / lista_promedios[año][0])
        print("\n",año+":",promedio_año+unidades)
        if float(promedio_año) > float(maximo_valor):
            maximo_valor = promedio_año
            maximo_año = año
    print("\n El año",maximo_año,"tuvo el mayor valor: ",maximo_valor+unidades)
    continuar = input("\nPresione enter para continuar.")

def guardar_promedios(promedio,año,lista_promedios):
    """
    Precondición: Guardo los promedios por año y el contador
    de días en una lista dentro del diccionario.
    El promedio como un float, el año como un string,
    y la lista de promedios como un diccionario.
    """
    if año not in lista_promedios.keys():
        lista_promedios[año] = [1,promedio]
    else:
        lista_promedios[año][0] += 1
        lista_promedios[año][1] += promedio

def cargar_datos_anuales(opcion,ruta):
    """
    Precondición: Lee el archivo csv, guarda los datos, y dependiendo
    de la opción llama a una función o a otra.
    Recibe la ruta del archivo csv como un str
    y la opción como un str.
    """
    lista_promedios = {}
    titulo = 0
    with open(ruta) as csvfile:
        for linea in csvfile:
            if titulo != 0: #Porque la primera linea del CSV es el encabezado.
                linea = linea.split(",")
                fecha = linea[0].replace('"', '')
                año = fecha[-4::1]
                if opcion == "1":
                    max = float(linea[4].replace('"',''))
                    min = float(linea[5].replace('"',''))
                    promedio = (max + min) / 2
                if opcion == "2":
                    promedio = float(linea[8].replace('"',''))
                if opcion == "3":
                    promedio = float(linea[6].replace('"', ''))
                if opcion == "4":
                    promedio = float(linea[4].replace('"', ''))
                guardar_promedios(promedio,año,lista_promedios)
            else:
                titulo += 1
    if opcion == "1" or opcion == "2":
        graficar_promedios_anuales(lista_promedios,opcion)
    if opcion == "3" or opcion == "4":
        mostrar_promedio_anual(lista_promedios,opcion)

def historico_temperatura_humedad():
    """
    Le pide al usuario la ruta del archivo csv, y si esta es valida,
    muestra las opciones de los distintos datos del csv.
    """
    continuar = "si"
    ruta = input("Introduzca la ruta del archivo CSV en su computador: ") #C:/Users/nanim/Downloads/weatherdata--389-603_edd.csv
    while os.path.exists(ruta) and ruta.endswith(".csv") and continuar == "si":
        print("\nHistórico de temperatura y humedad de Argetina.\n")
        print("1)   Gráfico con el promedio de temperaturas anuales de los últimos 5 años.")
        print("2)   Gráfico con el promedio de humedad de los últimos 5 años.")
        print("3)   Milímetros máximos de lluvia de los últimos 5 años.")
        print("4)   Temperatura máxima de los últimos 5 años.")
        print("5)   Salir.\n")
        opcion = input("Elija que opción desea ver: ")
        if opcion != "5" and opcion in ["1","2","3","4"]:
            cargar_datos_anuales(opcion,ruta)
        elif opcion == "5":
            continuar = "no"
        else:
            print("Opción no valida. Intente nuevamente.")
    if os.path.exists(ruta) == False:
        print("La ruta ingresada no se encuentra en su computador.")
    elif ruta.endswith(".csv") == False:
        print("El formato del archivo ingresado es invalido.")

def identificar_tormentas(detectados,provincia):
    """
    Precondición: Recibe como parametro una lista con la cantidad de
    pixeles de cada tipo de tormenta, y una provincia como un str.
    Cuenta la cantidad de pixeles de cada tipo de tormenta
    y determina que clase de tormenta hay.
    """
    alerta = ""
    if (detectados[0]//6) > (detectados[1]+detectados[2]+detectados[3]+detectados[4]):
        tormenta_actual = "Sin alerta próxima"
    else:
        if detectados[1] > (detectados[2]+detectados[3]+detectados[4]):
            tormenta_actual = "Tormenta débil"
        if detectados[2] > (detectados[1]*0.29):
            tormenta_actual = "Tormenta moderada"
        if detectados[3] > (detectados[1]*0.29):
            tormenta_actual = "Tormenta fuerte"
            alerta = "ALERTA!"
        if detectados[4] > (detectados[1]*0.29):
            tormenta_actual = "Tormenta fuerte con posibilidad de granizo"
            alerta = "ALERTA!"
    print("\n",provincia+":",tormenta_actual+".",alerta)