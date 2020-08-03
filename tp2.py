import requests
import matplotlib.pyplot as plt
from PIL import Image
import ipinfo
import os

def titulo():
    print(" _____                               _        ")
    print("|_   _|                             | |       ")
    print("  | | ___  _ __ _ __ ___   ___ _ __ | |_ __ _ ")
    print("  | |/ _ \| '__| '_ ` _ \ / _ \ '_ \| __/ _` |")
    print("  | | (_) | |  | | | | | |  __/ | | | || (_| |")
    print("  \_/\___/|_|  |_| |_| |_|\___|_| |_|\__\__,_|")
    print("")

def edicion_descripcion(descripcion):
    '''
    Precondición: Recibe la descripción como un string y la fragmenta cada 120 caracteres por linea.
    Postcondición: Retorna el texto modificado, como string.
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

def volver_a_intentar(valor):
    '''
    Precondicion: Le permite al usuario volver a intentar.
    Postcondicion: Retorna un booleano.
    '''
    intentar = False
    decision = input(f'\nDesea volver a intentar con otra {valor}? (Si/No): ').lower().replace("í", "i")
    opciones = ['si', 'no', 's', 'n']
    while decision not in opciones:
        decision = input('Opción no valida! Vuelva a ingresar. (Si/No): ').lower().replace("í", "i")
    if decision in ['si', 's']:
        intentar = True
    elif decision in ['no', 'n']:
        intentar = False
    os.system('cls')
    titulo()
    return intentar

def graficar_promedios_anuales(lista_promedios,opcion):
    """
    Precondicion: recibe 2 parámetros, un diccionario con los años y sus promedios de temperatura o humedad por cada dia,
                y la opcion elegida por el usuario de tipo string. Usando la librería matplotlib se muestra gráficamente 
                lo elegido por el usuario
    """
    if opcion == "1":
        etiquetas = ["Temperaturas (°C)","Promedio de temperaturas anuales de los últimos 5 años."]
    else:
        etiquetas = ["Humedad Relativa (Fracción)","Promedio de humedad de los últimos 5 años."]
    anios = []
    lista_promedios_total = []
    for anio,datos in lista_promedios.items():
        if int(anio) >= 2015:
            anios.append(anio)
            promedio_anio = lista_promedios[anio][1] / lista_promedios[anio][0]
            lista_promedios_total.append(promedio_anio)
    plt.style.use("seaborn")
    plt.bar(anios,lista_promedios_total, width = 0.5, color = 'b')
    plt.xlabel("Años")
    plt.ylabel(etiquetas[0])
    plt.title(etiquetas[1])
    plt.tight_layout()
    plt.show()
    os.system('cls')
    titulo()

def mostrar_promedio_anual(lista_promedios,opcion):
    """
    Precondición:Muestra los datos de la opción escogida y muestra por pantalla el año y
    el promedio de ese año.
    Recibe la opción escogida como un string y la lista de promedios como un diccionario.
    """
    maximo_valor = 0
    maximo_anio = ""
    if opcion == "3":
        print("\nMilímetros máximos de lluvia de los últimos 5 años.")
        unidades = "mm"
    else:
        print("\nTemperatura máxima de los últimos 5 años.")
        unidades = "°C"
    for anio, datos in lista_promedios.items():
        if int(anio) >= 2015:
            promedio_anio = '%.2f' % (lista_promedios[anio][1] / lista_promedios[anio][0])
            print("\n",anio+":",promedio_anio+unidades)
            if float(promedio_anio) > float(maximo_valor):
                maximo_valor = promedio_anio
                maximo_anio = anio
    print("\n El año",maximo_anio,"tuvo el mayor valor: ",maximo_valor+unidades)
    continuar = input("\nPresione enter para continuar.")
    os.system('cls')
    titulo()
    print('\nR E G I S T R O S  A N U A L E S\n')

def guardar_promedios(promedio,anio,lista_promedios):
    """
    Precondición: Guardo los promedios por año y el contador de días en una lista dentro del diccionario.
    Recibe el promedio como un float, el año como un string, y la lista de promedios como un diccionario.
    """
    if anio not in lista_promedios.keys():
        lista_promedios[anio] = [1,promedio]
    else:
        lista_promedios[anio][0] += 1
        lista_promedios[anio][1] += promedio

def cargar_datos_anuales(opcion,ruta):
    """
    Precondición: Lee el archivo csv, guarda los datos, y dependiendo de la opción llama a una función o a otra.
    Recibe la ruta del archivo csv como un str y la opción como un str.
    """
    lista_promedios = {}
    titulo = 0
    with open(ruta) as csvfile:
        for linea in csvfile:
            if titulo != 0: #Porque la primera linea del CSV es el encabezado.
                linea = linea.split(",")
                fecha = linea[0].replace('"', '')
                anio = fecha[-4::1]
                if opcion == "1":
                    max = float(linea[4].replace('"',''))
                    min = float(linea[5].replace('"',''))
                    promedio = (max + min) / 2
                elif opcion == "2":
                    promedio = float(linea[8].replace('"',''))
                elif opcion == "3":
                    promedio = float(linea[6].replace('"', ''))
                elif opcion == "4":
                    promedio = float(linea[4].replace('"', ''))
                guardar_promedios(promedio,anio,lista_promedios)
            else:
                titulo += 1
    if opcion == "1" or opcion == "2":
        graficar_promedios_anuales(lista_promedios,opcion)
    elif opcion == "3" or opcion == "4":
        mostrar_promedio_anual(lista_promedios,opcion)

def historico_temperatura_humedad():
    """
    Precondición: Le pide al usuario la ruta del archivo csv, y si esta es valida, muestra las
    opciones de los distintos datos del csv.
    """
    continuar = True
    while continuar is True:
        print('\nR E G I S T R O S  A N U A L E S\n')
        ruta = input("Introduzca la ruta del archivo CSV en su computador: ")
        while os.path.exists(ruta) and ruta.endswith(".csv") and continuar == True:
            os.system('cls')
            titulo()
            print('\nR E G I S T R O S  A N U A L E S\n')
            print("\nHistórico de temperatura y humedad de Argentina.\n")
            print("1)   Gráfico con el promedio de temperaturas anuales de los últimos 5 años.")
            print("2)   Gráfico con el promedio de humedad de los últimos 5 años.")
            print("3)   Milímetros máximos de lluvia de los últimos 5 años.")
            print("4)   Temperatura máxima de los últimos 5 años.")
            print("5)   Volver.\n")
            opcion = input("Elija que opción desea ver (1-5): ")
            while opcion not in ["1", "2", "3", "4", "5"]:
                opcion = input("Opción no valida. Vuelva a intentar (1-5): ")
            if opcion != "5":
                cargar_datos_anuales(opcion,ruta)
            elif opcion == "5":
                continuar = False
        if os.path.exists(ruta) == False:
            print("La ruta ingresada no se encuentra en su computador.")
            continuar = volver_a_intentar("ruta")
        elif ruta.endswith(".csv") == False:
            print("El formato del archivo ingresado es invalido.")
            continuar = volver_a_intentar("ruta")

def identificar_tormentas(detectados,provincia):
    """
    Precondición: Recibe como parametro una lista con la cantidad de pixeles de cada tipo de tormenta,
    y una provincia como un str.
    Cuenta la cantidad de pixeles de cada tipo de tormenta y determina que clase de tormenta hay.
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

def analisis_radar(x,y,provincia,ruta_imagen):
    """
    Precondicion: se reciben 4 parámetros, provincia de tipo string que expresa la provincia a analizar,
                x e y de tipo int que expresan las coordenadas de la provincia y ruta_imagen de tipo string
                que expresa la ubicación de la imagen dentro de la computadora. Se analiza cada pixel de la
                provincia identificando el color de cada uno de ellos y agrupandolos en los diferentes tipos de tormenta
    """
    imagen_radar = Image.open(ruta_imagen).convert('RGB')
    NEGRO = ((34, 34, 34))
    AZULES_INFERIORES = ((51, 170, 221), (34, 170, 204), (34, 153, 204), (51, 136, 187), (51, 119, 170), (68, 102, 153), (68, 85, 136),(51, 85, 119), (51, 68, 102))
    VERDES = ((85, 238, 51), (85, 221, 51), (68, 204, 51), (68, 187, 51), (51, 170, 34), (51, 136, 34), (34, 119, 17))
    AMARILLOS = ((238, 238, 68), (238, 238, 51), (221, 221, 51), (204, 204, 51), (204, 170, 34))
    ROJOS = ((170, 0, 17), (204, 0, 17), (221, 51, 34), (170, 34, 34), (153, 0, 0), (238, 17, 51))
    NARANJAS = ((221, 102, 34), (204, 153, 34), (153, 102, 34), (221, 136, 17))
    MAGENTAS = ((204, 0, 204), (238, 0, 238), (221, 0, 153), (170, 0, 187),(153, 0, 153), (204, 0, 153), (221, 0, 204), (187, 0, 102))
    AZULES_SUPERIORES = ((153, 221, 204), (136, 221, 187))
    sin_alerta_proxima = 0
    tormenta_debil = 0
    tormenta_moderada = 0
    tormenta_fuerte = 0
    posibilidad_granizo = 0
    for j in range(y,y+181):
        for i in range(x,x+181):
            coordenada = i,j
            if imagen_radar.getpixel(coordenada) == NEGRO:
                sin_alerta_proxima += 1
            elif imagen_radar.getpixel(coordenada) in AZULES_INFERIORES:
                tormenta_debil += 1
            elif imagen_radar.getpixel(coordenada) in VERDES or imagen_radar.getpixel(coordenada) in AMARILLOS:
                tormenta_moderada += 1
            elif imagen_radar.getpixel(coordenada) in ROJOS or imagen_radar.getpixel(coordenada) in NARANJAS:
                tormenta_fuerte += 1
            elif imagen_radar.getpixel(coordenada) in MAGENTAS or imagen_radar.getpixel(coordenada) in AZULES_SUPERIORES:
                posibilidad_granizo += 1

    detectados = [sin_alerta_proxima,tormenta_debil,tormenta_moderada,tormenta_fuerte,posibilidad_granizo]
    identificar_tormentas(detectados,provincia)

def datos_radar():
    """
    Precondición: Le pide al usuario la ruta de la imagen, y si esta es valida, entra en la función de analisis_radar.
    """
    bahia_blanca = [336, 339, "Bahia Blanca, Buenos Aires"]
    caba = [465, 174, "C.A.B.A"]
    cordoba = [269,43,"Córdoba, Córdoba"]
    mar_del_plata = [487, 311, "Mar del Plata, Buenos Aires"]
    neuquen = [145,348,"Neuquén, Neuquén"]
    parana = [399, 54, "Paraná, Entre Rios"]
    pergamino = [394,141,"Pergamino, Buenos Aires"]
    santa_rosa = [276,249,"Santa Rosa, La Pampa"]
    provincias = [bahia_blanca,caba,cordoba,mar_del_plata,neuquen,parana,pergamino,santa_rosa]
    intentar = True
    while intentar is True:
        print('\nA N A L I S I S   R A D A R\n')
        print("Introduzca la ruta de la imagen que desea analizar:")
        print("-------------(Debe ser un archivo png)-------------")
        ruta_imagen = input()
        if os.path.exists(ruta_imagen) and ruta_imagen.endswith(".png"):
            os.system('cls')
            titulo()
            print('\nA N A L I S I S   R A D A R\n')
            print('\nA L E R T A S !\n')
            for i in range(len(provincias)):
                analisis_radar(provincias[i][0],provincias[i][1],provincias[i][2],ruta_imagen)
            print('')
            intentar = False
        elif os.path.exists(ruta_imagen) == False:
            print("La ruta ingresada no se encuentra en su computador.")
            intentar = volver_a_intentar("ruta")
        elif ruta_imagen.endswith(".png") == False:
            print("El formato del archivo ingresado es invalido.")
            intentar = volver_a_intentar("ruta")

def alertas():
    """
    Precondición: imprime las alertas actuales a nivel nacional.
    """
    url = "https://ws.smn.gob.ar/alerts/type/AL"
    if abrir_json(url):
        respuesta = requests.get(url)
        datos = respuesta.json()
        claves_necesarias = ["Titulo", "Fecha", "Hora", "\nPróxima actualización"]
        for diccionario in range(len(datos)):
            print("\nAlerta:", diccionario + 1, '\n')
            contador = 0
            claves = ['title', 'date', 'hour', 'update']
            for clave in datos[diccionario]:
                if clave in claves:
                    print(claves_necesarias[contador], ":", datos[diccionario][clave])
                    contador += 1
                elif clave == "zones":
                    texto_editado = edicion_descripcion(datos[diccionario-1]['description'])
                    print("Descripcion", ":\n", texto_editado)
                elif clave == "description":
                    print("\nZonas: ")
                    for subclave in datos[diccionario]['zones']:
                        print("", int(subclave) + 1, ":", datos[diccionario]['zones'][subclave])

def alertas_local(provincia):
    """
    Precondición: Recibe como parametro una provincia como string.
    Revisa si hay alertas en la provincia actual.
    """
    print('\nA L E R T A S !\n\n')
    if "Tierra del Fuego" in provincia:
        provincia = 'Tierra del Fuego'
    elif "Capital Federal" in provincia:
        provincia = 'Buenos Aires'
    url = "https://ws.smn.gob.ar/alerts/type/AL"
    if abrir_json(url):
        respuesta = requests.get(url)
        datos = respuesta.json()
        contador_alertas = 0
        print("Lista de alertas en la provincia", provincia, ":")
        for i in range(len(datos)):
            if provincia in str(datos[i]["zones"]):
                contador_alertas += 1
                print("\nAlerta",contador_alertas)
                print("\n",datos[i]["title"])
                print(edicion_descripcion(datos[i]["description"]))
        if contador_alertas == 0:
            print(f"\nNo hay ninguna alerta para {provincia} en este momento.")

def validar_coordenada(numero, coordenada):
    """
    Precondición: recibe 1 parámetro de tipo string y verifica que contenga al menos 3 caracteres y que no
                    contenga caracteres que no sean numeros.
    Postcondición: retorna el numero de tipo string validado.
    """
    try:
        prueba = float(numero)
        decimal = True
    except ValueError:
        decimal = False
    while len(numero) < 3 or decimal == False or not numero.startswith('-'):
        print("\nIntroduzca un número negativo de al menos dos dígitos.")
        print("Ejemplo: -34 o -34.2")
        numero = input(f'Ingrese la {coordenada}: ')
        try:
            prueba = float(numero)
            decimal = True
        except ValueError:
            decimal = False
    return numero

def geolocalizador():
    '''
    Precondicion: Le pide al usuario que ingrese las coordenadas de la ubicacion que desea ver las alertas.
                Verifica la conexion con el web service y busca la provincia a la que pertenecen, la cual luego
                ingresa como parametro en la funcion de alertas locales.
    '''
    url = 'https://ws.smn.gob.ar/map_items/forecast/'
    intentar = True
    while intentar is True:
        latitud = input('Ingrese la latitud: ')
        latitud = validar_coordenada(latitud, 'latitud')
        longitud = input('Ingrese la longitud: ')
        longitud = validar_coordenada(longitud, 'longitud')
        encontrado = False
        max_lat = 1
        max_lon = 1
        if abrir_json(url):
            respuesta = requests.get(url)
            datos = respuesta.json()
            for i in range(len(datos)):
                aprox_latitud = abs(float((datos[i]["lat"]).replace("-", "")) - float(latitud.replace("-", "")))
                aprox_longitud = abs(float((datos[i]["lon"]).replace("-", "")) - float(longitud.replace("-", "")))
                if aprox_latitud < max_lat and aprox_longitud < max_lon:
                    max_lat = aprox_latitud
                    max_lon = aprox_longitud
                    localizacion = datos[i]
                    encontrado = True
            if encontrado == True:
                print(f'\nCiudad encontrada: {localizacion["name"]} ({localizacion["lat"]}, {localizacion["lon"]})')
                alertas_local(localizacion["province"])
            elif encontrado == False:
                print(f"\nNo se encontró la localización para {latitud}, {longitud}.")
            intentar = volver_a_intentar('coordenada')

def geolocalizador_ip():
    '''
    Precondicion: Confirma el acceso a la geolocalizacion actual y llama a la funcion de alertas
                locales ingresandole como parametro la provincia de la geolocalizacion actual
    '''
    clave = '3b7428ff5f2a34'
    try:
        respuesta = ipinfo.getHandler(clave)
        datos = respuesta.getDetails()
        acceso = True
    except Exception:
        print('\nUPS! Hubo un error al obtener la ubicación actual.')
        print('Verifique su internet o vuelva a intentar mas tarde.')
        acceso = False
    if acceso:
        respuesta = ipinfo.getHandler(clave)
        datos = respuesta.getDetails()
        provincia = datos.region
        if 'Buenos Aires' in provincia:
            provincia = 'Buenos Aires'
        alertas_local(provincia)

def menu_alertas():
    '''
    Precondicion: Muestra un menu para que el usuario decida que tipo de alerta desea ver.
                Llama a otras funciones sin parámetros
    '''
    print('A L E R T A S !')
    print('\n[1] Alertas a Nivel Nacional\n[2] Alertas en mi geolocalización actual')
    print('[3] Ingresar coordenadas\n[4] Volver')
    opcion = input('\nIngrese la opción que desee realizar (1-4): ')
    while opcion not in ['1', '2', '3', '4']:
        opcion = input('Valor Incorrecto! Por favor, vuelva a ingresar (1-4): ')
    os.system('cls')
    titulo()
    if opcion == '1':
        print('A L E R T A S !')
        alertas()
    elif opcion == '2':
        print('\nAlertas en mi geolocalización')
        geolocalizador_ip()
    elif opcion == '3':
        print('\nAlertas por coordenadas')
        geolocalizador()
    elif opcion == '4':
        print('')

def mostrar_pronostico_extendido(dias):
    '''
    Precondicion: Muestra el pronostico extendido para la ciudad pedida por el usuario.
                Recibe el json de pronósticos como un diccionario.
    '''
    print('')
    for key, value in dias.items():
        if key == "name":
            print("Ciudad:", dias['name'])
            print("Provincia:", dias['province'])
            for i in range(1,4):
                print("\nDía", str(dias["weather"][i]["day"])+":")
                pronostico_dia = edicion_descripcion(dias["weather"][i]["morning_desc"])
                pronostico_tarde = edicion_descripcion(dias["weather"][i]["afternoon_desc"])
                print(str(dias["weather"][i]["morning_temp"])+"°C", "en la mañana.", pronostico_dia)
                print(str(dias["weather"][i]["afternoon_temp"])+"°C", "en la tarde.", pronostico_tarde)

def comparar_nombres(nombre_1, nombre_2):
    """
    Precondicion: recibe 2 parámetros de tipo string que expresan el nombre ingresado por el
                usuario y el nombre en el json, a ambos se les quitan los tildes y se compara su igualdad
    Postcondicion: retorna el nombre que se encuentra dentro del diccionario si ambos nombres son iguales, 
                de no ser así retorna un "No"
    """
    if nombre_2.lower() == "tierra del fuego":
        nombre_2 = "Tierra del Fuego, Antártida e Islas del Atlántico Sur"
    nombre_conseguido = 'No'
    nombre_3 = nombre_1.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    nombre_4 = nombre_2.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    if nombre_3 == nombre_4:
        nombre_conseguido = nombre_1
    return nombre_conseguido

def pronostico_extendido():
    '''
    Precondicion: Le pide al usuario que ingrese la ubicacion de la que desea saber su pronostico
                extendido. Confirma el acceso al web service y verifica que haya pronostico
                para la ubicacion ingresada, llamando a una funcion.
    '''
    url = 'https://ws.smn.gob.ar/map_items/forecast/'
    corriendo = True
    while corriendo is True:
        print('\nP R O N O S T I C O    E X T E N D I D O\n')
        ciudad_elegida = input("Ingrese el nombre de la ciudad que desea ver su pronostico extendido: ").title()
        provincia_elegida = input("Ingrese la provincia en la que se encuentra la ciudad: ").title()
        existe_ciudad_y_provincia = False
        conexion = abrir_json(url)
        if conexion is True:
            datos = url
            respuesta = requests.get(datos)
            pronosticos = respuesta.json()
            for j in range(len(pronosticos)):
                ciudad = comparar_nombres(pronosticos[j]['name'], ciudad_elegida)
                provincia = comparar_nombres(pronosticos[j]['province'], provincia_elegida)
                if ciudad.startswith('Base'):
                    existe_ciudad_y_provincia = False
                elif ciudad == pronosticos[j]['name'] and provincia == pronosticos[j]['province']:
                    existe_ciudad_y_provincia = True
                    mostrar_pronostico_extendido(pronosticos[j])
                    provincia_encontrada = pronosticos[j]['province']
        if existe_ciudad_y_provincia is False and conexion is True:
            print(f'\nLo sentimos! No se encontraron resultados para {ciudad_elegida}, {provincia_elegida}.')
        elif existe_ciudad_y_provincia is True and conexion is True:
            alertas_local(provincia_encontrada)
        corriendo = volver_a_intentar('ciudad')

def volver_o_salir():
    '''
    Precondicion: Le permite al usuario elegir si desea volver al menu o salir.
    Postcondicion: Retorna un booleano.
    '''
    volver = False
    print('\n[1] Volver a Menu del Clima\n[2] Salir')
    eleccion = input('\nIngrese la opción que desee (1,2): ')
    while eleccion not in ['1', '2']:
        eleccion = input('Valor Incorrecto! Por favor, vuelva a ingresar (1,2): ')
    if eleccion == '1':
        volver = True
    elif eleccion == '2':
        volver = False
    return volver

def main():
    programa_corriendo = True
    while programa_corriendo is True:
        titulo()
        print('\nM E N U  D E L  C L I M A\n')
        print(f'[1] ALERTAS!\n[2] Pronóstico Extendido\n[3] Análisis de Imagen Radar')
        print('[4] Histórico de temperaturas y humedad de Argentina\n[5] Salir')
        opcion = input('\nIngrese el numero de la opción que desee (1-5): ')
        while opcion not in ['1', '2', '3', '4', '5']:
            opcion = input('Valor Incorrecto! Por favor, vuelva a ingresar (1-5): ')
        os.system('cls')
        titulo()
        if opcion == '1':
            menu_alertas()
            programa_corriendo = volver_o_salir()
        elif opcion == '2':
            pronostico_extendido()
            programa_corriendo = volver_o_salir()
        elif opcion == '3':
            datos_radar()
            programa_corriendo = volver_o_salir()
        elif opcion == '4':
            historico_temperatura_humedad()
            programa_corriendo = volver_o_salir()
        elif opcion == '5':
            programa_corriendo = False
        os.system('cls')

main()