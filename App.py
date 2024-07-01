#importar paquetes
import json
import requests
import uuid


#Clases
from Cliente import Clientee
#from Order import Order
from Producto import Producto
from Restaurante import Restaurante
from Estadio import Estadio
from Equipo import Equipo
from Ticket import Ticket
from Partido import Partido

class App():
    def __init__(self):
        self.Lista_Cliente = []
        self.Lista_Partido = []
        self.Lista_Producto = []
        self.Lista_Restaurante = []
        self.Lista_Estadio = []
        self.Lista_Equipo = []
        self.Lista_Ticket = []

    def menu(self, opciones):
        for i, opcion in enumerate(opciones):
            print(f"{i+1}. {opcion}")
        
        opcion = input("ingrese el numero de la opcion que desea elegir: ")
        while not opcion.isnumeric() or not int(opcion) in range(1, len(opciones)+1):
            opcion = input("Error, ingrese el numero de la opcion que desea elegir: ")

        opcion = int(opcion)-1

        return opcion

    def run(self):
        self.API()

        opciones = ["Gestión de partidos y estadios", "Gestión de venta de entradas", "Gestión de asistencia a partidos", "Gestión de restaurantes", "Gestión de venta de restaurantes", "Indicadores de gestión (estadísticas)", "salir"]
        print("Bienvenido")
        
        while True:
            opcion = self.menu(opciones)

            if opcion == 0:
                self.modulo_1()
            elif opcion == 1:
                self.modulo_2()
            elif opcion == 2:
                self.modulo_3()
            elif opcion == 3:
                self.modulo_4()
            elif opcion == 4:
                self.modulo_5()
            elif opcion == 5:
                self.modulo_6()
            else:
                print("Hasta luego")
                self.txt()
                break

    #Carga del apis en los objetos
    def API(self):
        self.API_Equipos()
        self.API_Estadios()
        self.API_Partidos()

    #Carga del apis Teams en los objetos
    def API_Equipos(self):
        #Accede al api y descarga la informacion con el requests y la transforma en un json con el .json()
        api_equipos = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
        
        #agarra cada diccionario del apis y la convierte en objeto por medio del constructor
        for team in api_equipos:
            nuevo = Equipo(team["id"], team["code"], team["name"], team["group"])
            self.Lista_Equipo.append(nuevo)
    #Carga del apis estadios en los objetos
    def API_Estadios(self):
        #Accede al api y descarga la informacion con el requests y la transforma en un json con el .json()
        api_estadios = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()

        #Recorrer Lista de estadios y guardar su informacion
        for estadio in api_estadios:
            nuevo_estadio = Estadio(estadio['id'], estadio['name'], estadio['city'], estadio['capacity'], estadio['restaurants'])
            
            #Recorrer Lista de restaurantes y guardar su informacion dentro de su estadio pertinente
            restaurantes = []
            for restaurante in estadio['restaurants']:
                nuevo_restaurante = Restaurante(restaurante['name'], restaurante['products'])


                #Recorrer Lista de productos y guardar su informacion dentro de su restaurantes pertinente
                productos = []
                for producto in restaurante['products']:
                    nuevo_producto = Producto(producto['name'], producto['quantity'], producto['price'], producto['adicional'], producto['stock'])
                    productos.append(nuevo_producto)
                    self.Lista_Producto.append(nuevo_producto)
                #Guardamos lista de productos dentro del restaurantes
                nuevo_estadio.restaurantes = restaurantes



                restaurantes.append(nuevo_restaurante)
                self.Lista_Restaurante.append(nuevo_restaurante)
            #Guardamos lista de restaurantes dentro del estadio
            nuevo_estadio.restaurantes = restaurantes



            self.Lista_Estadio.append(nuevo_estadio)
    #Carga del apis Stadiums en los objetos
    def API_Partidos(self):
        #Accede al api y descarga la informacion con el requests y la transforma en un json con el .json()
        api_partidos = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()

        for partido in api_partidos:
            #sustituimos los diccionarios de equipo que ya existen como objetos para tener todo a base de objeto 
            for equipo in self.Lista_Equipo:
                if partido["home"]["id"] == equipo.id:
                    local = equipo
                if partido["away"]["id"] == equipo.id:
                    away = equipo

            #Busca un stadium que comparti id y lo intercambia en la variable
            for estadio in self.Lista_Estadio:
                if estadio.id == partido["stadium_id"]:
                    estadio_partido = estadio
            
            #agarra cada diccionario del apis y la convierte en objeto por medio del constructor
            nuevo = Partido(partido["id"], partido["number"], local, away, partido["date"], partido["group"], estadio_partido)

            self.Lista_Partido.append(nuevo)

    #Gestión de partidos y estadios
    def modulo_1(self):
        opciones = ["Buscar todos los partidos de un país", "Buscar todos los partidos que se jugarán en un estadio específico", "Buscar todos los partidos que se jugarán en una fecha determinada"]
        opcion = self.menu(opciones)

        if opcion == 0:
            self.buscar_partido_pais()
        elif opcion == 1:
            self.buscar_partido_estadios()
        elif opcion == 2:
            self.buscar_partido_fecha()
    #Busqueda de los partidos por el nombre de los paises que juegan
    def buscar_partido_pais(self):
        #Con el dato ingresado recorre la lista y compara en elm atriburo home y away
        partido_buscar =input("Ingresa el pais por el que desea buscar el partido: ").lower()
        encontrar = False
        for partido in self.Lista_Partido:
            if partido_buscar in partido.home.nombre.lower() or partido_buscar in partido.away.nombre.lower():
                encontrar = True
                print(partido.show())
        
        if not encontrar:
            print("No se encontraron resultados")
    #Busqueda de los partidos por el estadio donde se juega      
    def buscar_partido_estadios(self):
        #Con el dato ingresado recorre la lista y compara en el atributo estadio
        partido_buscar =input("Ingresa el estadio por el que desea buscar el partido: ").lower()
        encontrar = False
        for partido in self.Lista_Partido:
            if partido_buscar in partido.estadio.nombre.lower():
                encontrar = True
                print(partido.show())
        
        if not encontrar:
            print("No se encontraron resultados")
    #Busqueda de los partidos por la fecha
    def buscar_partido_fecha(self):
        #Con el dato ingresado recorre la lista y compara en el atributo fecha
        partido_buscar=input("Ingresa la fecha por el que desea buscar el partido (Ej: 2024-06-14): ").lower()
        encontrar = False
        for partido in self.Lista_Partido:
            if partido_buscar == partido.fecha.lower():
                encontrar = True
                print(partido.show())
        
        if not encontrar:
            print("No se encontraron resultados")


    #Gestión de venta de entradas
    def modulo_2(self):
        #Pide la cedula al clientee y la verifica
        cedula = input("Ingresa tu cedula (sin puntos): ")
        while not cedula.replace(".", "").isnumeric() or 7 > len(cedula.replace(".", "")) > 8:
            cedula = input("Error, Ingresa la cedula: ")
        cedula = int(cedula.replace(".", ""))
        
        #Verifica si el clientee ya existe, de ser asi, busca su informacvion de no ser asi le pide los datos por primera vez
        dato_cliente = self.valifecha_cedula(cedula)
        if dato_cliente == False:
            nombre = input("Ingresa tu nombre: ")
            while not nombre.isalpha():
                nombre = input("Error, Ingresa el nombre: ")

            edad = input("Ingresa tu edad: ")
            while not edad.isnumeric() or int(edad) < 1:
                edad = input("Error, Ingresa la edad: ")
            edad = int(edad)

            dato_cliente = Clientee(nombre, edad, cedula)
            self.Lista_Cliente.append(dato_cliente)
        
        #Muestra todos los juegos para que el usuario escoja uno
        for index, partido in enumerate(self.Lista_Partido):
            print(f"        ----------{index+1}----------")
            print(partido.show())
        
        partido_numero = input("Ingrese el numero del partido que desea escoger: ")
        while not partido_numero.isnumeric() or not int(partido_numero) in range(1, len(self.Lista_Partido)+1):
            partido_numero = input("Ingrese el numero del partido que desea escoger: ")
        
        #Ingerso del tipo de ticket
        tipo_ticket = input("Ingrese el numero del tipo de entrada que desea: \n1. General \n2. VIP \n")
        while not tipo_ticket.isnumeric() or not int(tipo_ticket) in range(1, 3):
            tipo_ticket = input("Ingrese el numero del tipo de entrada que desea: \n1. General \n2. VIP \n")

        #Consigue el partido, junto a el se busca la capacidad del estadio para usar luego
        partido = self.Lista_Partido[int(partido_numero)-1]
        partido_capacidad = partido.estadio.capacidad
        precio = 0 
        if tipo_ticket == "1":
            partido_capacidad = partido_capacidad[0]
            precio = 35
        else:
            partido_capacidad = partido_capacidad[1]
            precio = 75
        
        #Cantidad de filas segun su capacidad
        row = partido_capacidad//10
        
        #Mapa del estadio, es una matriz
        asientos = []
        for i in range(1, row+1):
            row_asientos = []
            for j in range(1, 11):
                if len(str(i)) == 1:
                    i = "0"+str(i)
                asiento = f"{i}-{j}"
                row_asientos.append(asiento)
            asientos.append(row_asientos)
        
        for asiento in asientos:
            asiento = " | ".join(asiento)
            print(asiento)


        if tipo_ticket == "1":
            ticket_comprado = partido.tickets_general
        else:
            ticket_comprado = partido.tickets_vip

        #Pide los datos del puesto del ticket
        print("formato del codigo fila-columna")
        asiento_row = input("Ingresa la fila del asiento: ")
        while not asiento_row.isnumeric() or not int(asiento_row) in range(1, row+1):
            asiento_row = input("Ingresa la fila del asiento: ")

        print("formato del codigo fila-columnaa")
        asiento_columna = input("Ingresa la columnaa del asiento: ")
        while not asiento_columna.isnumeric() or not int(asiento_columna) in range(1, 11):
            asiento_columna = input("Ingresa la columnaa del asiento: ")
        
        asiento = f"{asiento_columna}-{asiento_columna}"

        #Verifica la disponibilidad
        while asiento in ticket_comprado:
            print("Ticket ocupado ingrese otro")

            print("formato del codigo fila-columnaa")
            asiento_row = input("Ingresa la fila del asiento: ")
            while not asiento_row.isnumeric() or not int(asiento_row) in range(1, row+1):
                asiento_row = input("Ingresa la fila del asiento: ")

            print("formato del codigo fila-columnaa")
            asiento_columna = input("Ingresa la columnaa del asiento: ")
            while not asiento_columna.isnumeric() or not int(asiento_columna) in range(1, 11):
                asiento_columna = input("Ingresa la columnaa del asiento: ")
            
            asiento = f"{asiento_columna}-{asiento_columna}"

        #Claculos de la factura
        subtotal = precio
        descuento = 0
        if self.vampiro(cedula):
            descuento = subtotal*0.5
        IVA = subtotal*0.16
        total = subtotal - descuento + IVA
        
        #factura
        print("-------Resumen-------")
        print("---------------------------")
        print(f"-Asiento: {asiento}")
        print(f"-Subtotal: {subtotal}")
        print(f"-descuento {descuento}")
        print(f"-IVA: {IVA}")
        print(f"-total: {total}")


        compras = input("Desea comprar la entrada? \n1. si\n2. no \n>")
        while not compras.isnumeric() or not int(compras) in range(1,3):
            compras = input("Desea comprar la entrada? \n1. si\n2. no \n>")
        
        #guarda la informacion en las clases pertinentes para ser usadas mas adeolante
        if compras == "1":
            id_unico = uuid.uuid4()
            print(f"Gracias por su compra, este el codig de tu entrada: {id_unico}")
            dato_cliente.balance += total
            dato_cliente.tipo_ticket = tipo_ticket
            if tipo_ticket == "1":
                partido.tickets_general.append(asiento)
            else:
                partido.tickets_vip.append(asiento)
            nuevo_ticket = Ticket(id_unico, cedula, tipo_ticket, asiento, partido)
            self.Lista_Ticket.append(nuevo_ticket)

        else:
            print("Hasta luego")
    
    #Verifica si un numero es vampiro o no
    def vampiro(self, numero):
        digitos = list(str(numero))
        num_digitos = len(digitos)

        # Comprobación de los factores
        for i in range(1, int(numero**0.5)+1):
            if numero % i == 0:
                factor1 = str(i)
                factor2 = str(numero // i)
                factores = factor1 + factor2

                # Comprobación de la permutación
                if sorted(digitos) == sorted(factores) and len(factor1) == len(factor2):
                    return True

        return False

    #Te valida si la cedula existe para algun clientee anterior
    def valifecha_cedula(self, cedula):
        for cliente in self.Lista_Cliente:
            if int(cliente.cedula) == int(cedula):
                return cliente
        
        return False

    #Gestión de asistencia a partidos
    def modulo_3(self):
        
        codigo = input("Ingrese el numero del codigo que desea revisar: ")
        if self.valifecha_ticket(codigo):
            print("Entrada Valida")
        else:
            print("Esta entrada no es valida")
    #Verifica si el ticket existe o si ya fue usado, de no ser asi lo verifica
    def valifecha_ticket(self, codigo):
        for ticket in self.Lista_Ticket:
            if str(ticket.id) == codigo and ticket.attendance == False:
                ticket.attendance = True
                #partido.attendance +=1
                return True
        
        return False

    #Gestión de restaurantes
    def modulo_4(self):
        opciones = ["Buscar productos por nombre", "Buscar productos por tipo", "Buscar productos por rango"]
        opcion = self.menu(opciones)

        if opcion == 0:
            self.buscar_producto_nombre()
        elif opcion == 1:
            self.buscar_producto_tipo()
        elif opcion == 2:
            self.buscar_producto_rango()
    #Busca el productos por medio del nombre
    def buscar_producto_nombre(self):
        producto_buscar =input("Ingresa el nombre del productos que desea buscar: ").lower()
        encontrar = False
        for product in self.Lista_Product:
            if producto_buscar in product.nombre.lower():
                encontrar = True
                print(product.show())
        
        if not encontrar:
            print("No se encontraron resultados")
    #Busca el productos por medio del tipo
    def buscar_producto_tipo(self):
        producto_buscar =input("Ingresa el numero de la opcion que desee buscar: \n1. De Paquete \n2. De Plato \n3. Con Alcohol: \n4. Sin Alcohol: ")
        encontrar = True
        for product in self.Lista_Product:
            if producto_buscar == "1" and product.adicional == "packedad":
                print(product.show())
            elif producto_buscar == "2" and product.adicional == "plate":
                print(product.show())
            elif producto_buscar == "3" and product.adicional == "alcoholic":
                print(product.show())
            elif producto_buscar == "4" and product.adicional == "non-alcoholic":
                print(product.show())
            elif not producto_buscar in "1234":
                encontrar = False

        if encontrar:
            print("Dato invalido")
    #Busca el productos por medio del rango
    def buscar_producto_rango(self):
        producto_buscar_min =input("Ingresa el numero minimo del precio: ")
        while not producto_buscar_min.isnumeric():
            producto_buscar_min =input("Ingresa el numero minimo del precio: ")
        
        producto_buscar_max =input("Ingresa el numero maximo del pecio: ")
        while not producto_buscar_max.isnumeric() and float(producto_buscar_max) < float(producto_buscar_min):
            producto_buscar_max =input("Ingresa el numero maximo del precio: ")
        
        encontrar = False
        for producto in self.Lista_Producto:
            if float(producto_buscar_min) < float(producto.precio) < float(producto_buscar_max):
                encontrar = True
                print(producto.show())
        
        if not encontrar:
            print("No hay resultados en este rango")

    #Gestión de venta de restaurantes
    def modulo_5(self):
        #pide la cedula y verifica si existe luego se valida
        cedula = input("Ingresa tu cedula (sin puntos): ")
        while not cedula.replace(".", "").isnumeric() or 7 > len(cedula.replace(".", "")) > 8:
            cedula = input("Error, Ingresa la cedula: ")
        cedula = int(cedula.replace(".", ""))

        data_cliente = self.valifecha_cedula(cedula)

        if data_cliente == False:
            print("Usted no es clientee")
        else:
            #DE ser un clientee verifica si es vIP o no
            if data_cliente != 2:
                print("Usted no es clientee VIP")
            else:
                #busca en que estadios estas ubicado para darte los restaurantes de ese
                estadio = data_cliente.tickets[-1].partido.estadio
                restaurantes = estadio.restaurantes

                for index, restaurante in enumerate(restaurantes):
                    print(f"        ----------{index+1}----------")
                    print(restaurante.show())
                
                opcion = input("Ingrese el numero del restaurante que desea escoger: ")
                while not opcion.isnumeric() or not int(opcion) in range(1, len(restaurantes)+1):
                    opcion = input("Ingrese el numero del restaurante que desea escoger: ")
                
                #Consigue la lista de productoss y te la muestra para ser seleccionada
                restaurante = restaurantes[int(opcion)-1]
                productos = restaurante.productos

                for index, producto in enumerate(productos):
                    print(f"        ----------{index+1}----------")
                    print(producto.show())
                
                opcion = input("Ingrese el numero del productos que desea comprar: ")
                while (not opcion.isnumeric() or not int(opcion) in range(1, len(productos)+1)) or (data_cliente.edad < 18):
                    opcion = input("Ingrese el numero del productos que desea comprar, recuerda que si eres menor no puede comprar alcohol: ")
                
                producto = productos[int(opcion)]

                cantidad = input("Ingresa la cantidad de productoss que desea comprar")
                while not cantidad.isnumeric():
                    cantidad = input("Ingresa la cantidad de productoss que desea comprar")
                
                #CAlculos factura
                subtotal = producto.precio* int(cantidad)
                descuento = 0
                if self.perfecto(data_cliente.cedula):
                    descuento = subtotal*0.15
                IVA = subtotal*0.16
                total = subtotal - descuento + IVA

                #Resumen
                print("-------Resumen-------")
                print("---------------------------")
                print(f"-productos: {producto.nombre}")
                print(f"-Cantidad: {cantidad}")
                print(f"-Subtotal: {subtotal}")
                print(f"-descuento {descuento}")
                print(f"-IVA: {IVA}")
                print(f"-total: {total}")

                compras = input("Desea realizar la compra? \n1. si\n2. no \n>")
                while not compras.isnumeric() or not int(compras) in range(1,3):
                    compras = input("Desea realizar la compra? \n1. si\n2. no \n>")
                
                #Guarda los datos dnecesario para usarlo luego 
                if compras == "1":
                    print("compra exitosa")
                    data_cliente.balance += total
                    producto.cantidad -= cantidad
                    producto.sold += cantidad
                else:
                    print("Gracias por visitar")
    
    #Te verifica si tu cedula es un numero perfecto
    def perfecto(self, numero):
        suma_divisores = 0
        for i in range(1, numero):
            if numero % i == 0:
                suma_divisores += i
        return suma_divisores == numero

    #Indicadores de gestión (estadísticas)
    def modulo_6(self):
        opciones = ["promedio de gasto de un clientee VIP en un partido", "tabla con la asistencia a los partidos de mejor a peor", "partido con mayor asistencia", "el partido con mayor boletos vendidos", "Top 3 productoss más vendidos en el restaurante.", "Top 3 de clientees (clientees que más compraron boletos)"]
        opcion = self.menu(opciones)

        if opcion == 0:
            print("promedio de gasto de un clientee VIP en un partido")

            balance = 0
            aux = 0
            for cliente in self.Lista_Cliente:
                if cliente.type_ticket == "2":
                    balance += cliente.balance
                    aux += 1
            if balance == 0 and aux == 0:
                print("No hay datos")
            else:
                print(f"El promedio de gasto de un clientee VIP es de: {balance/aux}$")
        elif opcion == 1:
            print("tabla con la asistencia a los partidos de mejor a peor")
            print("local, estadio, boletos vendidos, personas que asistieron, la relación asistencia/venta")
            
            partidos = []
            for partido in self.Lista_Partido:
                total = len(partido.tickets_general)+len(partido.tickets_vip)
                relacion = total-partido.attendance
                partidos.append([partido.home, partido.away, total,partido.attendance, relacion])
            lista_ordenada = sorted(partidos, key=self.comparar_por_total, reverse=True)

            for partido in partidos:
                print(partido)

        elif opcion == 2:
            print("partido con mayor asistencia")

            partido_max = self.Lista_Partido[0]
            for partido in range(1, len(self.Lista_Partido)):
                if partido_max.attendance < partido.attendance:
                    partido_max = partido

            partido_max.show()

        elif opcion == 3:
            print("el partido con mayor boletos vendidos")
            partido_max = self.Lista_Partido[0]
            for partido in range(1, len(self.Lista_Partido)):
                boletos_max = len(partido_max.tickets_vip) + len(partido_max.tickets_general)
                boletos = len(partido.tickets_vip) + len(partido.tickets_general)
                
                if boletos_max < boletos:
                    partido_max = partido

            partido_max.show()
            
        elif opcion == 4:
            print("Top 3 productoss más vendidos en el restaurante.")
            productoss_ordenados = sorted(self.Lista_Product, key=self.ordenar_por_vendidos, reverse=True)
            tres_productoss_con_mayor_vendidos = productoss_ordenados[:3]

            for productos in tres_productoss_con_mayor_vendidos:
                print(f"productos: {productos.nombre} - vendidos: {productos.sold}")

    

        elif opcion == 5:
            print("Top 3 de clientees (clientees que más compraron boletos)")
            clientees_ordenados = sorted(self.Lista_Cliente, key=self.ordenar_por_entradas, reverse=True)
            tres_clientees_con_mayor_entradas = clientees_ordenados[:3]

            for clientee in tres_clientees_con_mayor_entradas:
                print(f"Clientee: {clientee.nombre} - cantidad: {len(clientee.tickets)}")
    
    def ordenar_por_vendidos(clientee):
        
        return len(clientee.tickets)

    def comparar_por_total(lista1, lista2):
        print(lista1, lista2)
        if lista1[2] > lista2[2]:
            return 1
        elif lista1[2] < lista2[2]:
            return -1
        else:
            return 0        


    #Guardar informacion en Archivo.txt
    def txt(self):
        #Cada uno de estos With open, abre un archivo que esta en la carpeta txt (si no existe o crea) 
        #y luego transofrma los objetos en diccionarios para guardarlos en los txt, hace esto con cada clase que existe
        with open('TXT/Cliente.txt', 'a') as a:
            for cliente in self.Lista_Cliente:
                dicc = {'nombre': cliente.nombre,
                        'edad': cliente.edad,
                        'cedula': cliente.cedula,
                        'balance': cliente.balance,
                        'type_tickets': cliente.type_tickets,
                        'tickets': cliente.tickets}

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')
        with open('TXT/Partido.txt', 'a') as a:
            for partido in self.Lista_Partido:
                dicc = {
                        'id': partido.id,
                        'numero': partido.numero,
                        'home': partido.home.nombre,
                        'away': partido.away.nombre,
                        'fecha': partido.fecha,
                        'grupo': partido.grupo,
                        'estadio': partido.estadio.nombre,
                        'tickets_vip': partido.tickets_vip,
                        'tickets_general': partido.tickets_general,
                        'attendance': partido.attendance
                        
                        }

                json_data = json.dumps(dicc)
                a.write(json_data + '\n')

        with open('TXT/Product.txt', 'a') as a:
            for product in self.Lista_Product:
                dicc = {
                        'nombre': product.nombre,
                        'cantidad': product.cantidad,
                        'precio': product.precio,
                        'adicional': product.adicional,
                        'stock': product.stock,
                        'sold': product.sold
                }

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')
        with open('TXT/Restaurant.txt', 'a') as a:
            for restaurant in self.Lista_Restaurante:
                dicc = {
                    'nombre': restaurant.nombre,
                    'productos': []
                }

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')
        with open('TXT/estadio.txt', 'a') as a:
            for estadio in self.Lista_Estadio:
                dicc = {
                    'id': estadio.id,
                    'nombre': estadio.nombre,
                    'ciudad': estadio.ciudad,
                    'capacidad': estadio.capacidad,
                    'restaurantes': []
                }

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')
        with open('TXT/Team.txt', 'a') as a:
            for team in self.Lista_Equipo:
                dicc = {
                    'id': team.id,
                    'codigo': team.codigo,
                    'nombre': team.nombre,
                    'grupo': team.grupo,
                }

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')

        with open('TXT/Ticket.txt', 'a') as a:
            for ticket in self.Lista_Ticket:
                dicc = {
                    'id': ticket.id,
                    'cedula': ticket.cedula,
                    'tipo_boleto': ticket.tipo_boleto,
                    'asiento': ticket.asiento,
                    'partido': ticket.partido,
                    'attendance': ticket.attendance
                }

                json_data = json.dumps(dicc)
                # Write the string to the file with a newline character
                a.write(json_data + '\n')



