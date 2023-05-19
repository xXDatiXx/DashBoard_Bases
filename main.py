import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import csv
import datetime
import random
import numpy as np

#Clase Ventana Login
class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("ventanaLogin.ui", self)
        self.entrar_pushbutton.clicked.connect(self.loginFuncion)

    #FUNCIONES 
    def loginFuncion(self):
        username = self.user_lineedit.text()
        password = self.pass_lineedit.text()
        if len(username) == 0 or len(password) == 0:
            self.aviso_lineedit.setText("")
            self.aviso_lineedit.setText("Por favor llena todos los campos.")
        elif (username == "1" and password == "1"): #Usuario y contraseña vacios
         self.aviso_lineedit.setText("")
         self.gotoMain()
        else:
            self.aviso_lineedit.setText("")
            self.aviso_lineedit.setText("Usuario o contraseña incorrectos.")
    
    def gotoMain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

#Clase de la Ventana Principal
class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("ventanaTablas.ui", self)

        self.modificarTimer = QTimer(self)
        self.modificarTimer.setSingleShot(True)
        self.modificarTimer.setInterval(1000)
        self.modificarTimer.timeout.connect(self.modificarTimer_update)
        #Boton para actualizar manualmente las tablas
        self.refresh_button.clicked.connect(self.refreshTables)
        #Boton para salir al login
        self.salirButton.clicked.connect(self.gotoLogin)   
        #Funcion para buscar en tabla de Calzado
        self.buscarCalzado = QSqlQueryModel(self)
        self.buscarCalzado.setQuery("SELECT * FROM calzado")
        self.buscar_tableview.setModel(self.buscarCalzado)
        self.buscar_lineedit.textEdited.connect(self.buscarNombreCalzado)
        #Funcion para buscar en tabla de Cliente 
        self.buscarCliente = QSqlQueryModel(self)
        self.buscarCliente.setQuery("SELECT * FROM cliente")
        self.buscar_tableview_clientes.setModel(self.buscarCliente)
        self.buscar_lineedit_cliente.textEdited.connect(self.buscarNombreCliente)
        #Funcion para buscar en tabla Orden
        self.buscarOrden = QSqlQueryModel(self)
        self.buscarOrden.setQuery("SELECT * FROM orden")
        self.orden_tableview.setModel(self.buscarOrden)
        self.buscar_lineedit_orden.textEdited.connect(self.buscarNombreOrden)
        #Boton para agregar calzado
        self.alta_pushbutton.clicked.connect(self.agregarCalzado)
        self.alta_pushbutton.clicked.connect(self.refreshTables)
        #Boton para agregar cliente
        self.alta_pushbutton_2.clicked.connect(self.agregarCliente)
        self.alta_pushbutton_2.clicked.connect(self.refreshTables)
        #Boton para agregar empleado
        self.alta_pushbutton_3.clicked.connect(self.agregarEmpleado) 
        #Boton paea borrar una orden
        self.terminado_pushbutton.clicked.connect(self.borrarOrden)
        #Boton para ir a ventana dashboard
        self.dashboard_pushbutton.clicked.connect(self.gotoDashboard)


    #FUNCIONES
    def gotoDashboard(self):
        dashboard = DashboardScreen()
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def borrarOrden(self):
        idOrden = self.borrar_lineedit.text()
        if len(idOrden) == 0:
            self.aviso_lineedit_4.setText("")
            self.aviso_lineedit_4.setText("Por favor llena todos los campos.")
        else:
            query = QSqlQuery()
            query.prepare("DELETE FROM orden WHERE idOrden = :idOrden")
            query.bindValue(":idOrden", idOrden)
            query.exec()
            self.aviso_lineedit_4.setText("")
            self.aviso_lineedit_4.setText("Orden eliminada correctamente.")
            self.refreshTables()

    def agregarCalzado(self):
        tipoCalzado = self.tipocalzado_lineedit.text()
        servicio = self.servicio_lineedit.text()
        talla =  self.talla_lineedit.text()
        color = self.color_lineedit.text()
        detalles = self.detalles_lineedit.text()
        #Establecer que la fecha de llegada es igual a hoy
        fechaLlegada = datetime.date.today()
        rack = self.rack_lineedit.text()
        cliente = self.cliente_lineedit.text()
        extra = self.extra_lineedit.text()
        marca = self.marca_lineedit.text()
        materiales = self.materiales_lineedit.text()
        if len(tipoCalzado) == 0 or len(servicio) == 0 or len(talla) == 0 or len(color) == 0 or len(detalles) == 0 or len(rack) == 0 or len(cliente) == 0 or len(marca) == 0 or len(materiales) == 0:
            self.aviso_lineedit.setText("Por favor llena todos los campos.")
        else:
            conn = sql.connect("cleanwalkers.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cliente WHERE NombreCliente = ?", (cliente,))
            if cursor.fetchone():
                instruccion_temp = (f"SELECT NombreCliente from cliente WHERE NombreCliente = '"+cliente+"'")
                cursor.execute(instruccion_temp)
                temp_cliente = cursor.fetchone()
                cliente = temp_cliente[0]
                print(cliente)
                precio = 0
                int(precio)
                #Declaramos los servicios por default
                if servicio == "Clean Gent":
                    precio = 50
                elif servicio == "Basic":
                    precio = 100
                elif servicio == "Premium":
                    precio = 150
                elif servicio == "VIP":
                    precio = 180
                elif servicio == "Utra White":
                    precio = 160
                elif servicio == "Suede":
                    precio = 150


                #Declaramos los extras por default
                if extra == "Cap":
                    precio = precio + 50
                elif extra == "Bag":
                    precio = precio + 150
                elif extra == "Pintura":
                    precio = precio + 150
                elif extra == "Blanqueamiento":
                    precio = precio + 150
                elif extra == "Repelente":
                    precio = precio + 50
                
                instruccion = (f"INSERT INTO calzado (TipoCalzado, ServicioContratado, Marca, Talla, Color, Materiales, DetallesCalzado, FechaLlegada, Rack, Extra, Precio, Cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                datos = (tipoCalzado, servicio, marca, talla, color, materiales, detalles, fechaLlegada, rack, extra, precio, cliente)
                cursor.execute(instruccion, datos)
                conn.commit()
                conn.close()
                self.aviso_lineedit.setText("")
                self.aviso_lineedit.setText("Calzado agregado con exito.")
                self.tipocalzado_lineedit.setText("")
                self.servicio_lineedit.setText("")
                self.talla_lineedit.setText("")
                self.color_lineedit.setText("")
                self.detalles_lineedit.setText("")
                self.rack_lineedit.setText("")
                self.cliente_lineedit.setText("")
                self.extra_lineedit.setText("")
                self.marca_lineedit.setText("")
                self.materiales_lineedit.setText("")
                self.aviso_lineedit.setText("")
                self.exito_lineedit.setText("Calzado agregado con exito.")
                self.refreshTables()

                #Generamos la orden del pedido
                con = sql.connect("cleanwalkers.db")
                cursor_2 = con.cursor()
                fechaLlegada = datetime.date.today()
                instruccion_temp_2 = (f"SELECT idCliente from cliente WHERE NombreCliente = '"+cliente+"'")
                cursor_2.execute(instruccion_temp_2)
                temp_idcliente = cursor_2.fetchone()
                q = QSqlQuery()
                q.prepare("INSERT INTO orden (idCliente, idTenis, FechaLlegada, Costo) VALUES (?, ?, ?, ?)")
                q.addBindValue(temp_idcliente[0])
                q.addBindValue(cursor.lastrowid)
                q.addBindValue(fechaLlegada)
                q.addBindValue(precio)
                q.exec()
                con.commit()
                con.close()

            else:
                self.aviso_lineedit.setText("El cliente no existe.")
    
    def buscarNombreOrden(self, txt):
       self.buscarOrden.setQuery("SELECT * FROM orden WHERE idCliente LIKE '%"+txt+"%'")


    def modificarModdel_update(self):
        self.modificarTimer.start()

    def agregarCliente(self):
        nombreCliente = self.nombre_cliente_lineedit.text()
        apellidoCliente = self.apellido_cliente_lineedit.text()
        correo = self.correo_lineedit.text()
        celular = self.celular_lineedit.text()
        sexo = self.sexo_lineedit.text()
        cumpleanos = self.cumpleanos_lineedit.text()
        fechaRegistro = datetime.date.today()
        con = sql.connect("cleanwalkers.db")
        cursor = con.cursor()
        
        if len(nombreCliente) == 0 or len(celular) == 0 or len(correo) == 0 or len(cumpleanos) == 0 or len(sexo) == 0 or len(apellidoCliente) == 0:
            self.aviso_lineedit_2.setText("")
            self.aviso_lineedit_2.setText("Por favor llena todos los campos.")
        else:
            cursor.execute("SELECT NombreCliente FROM cliente WHERE NombreCliente = ?", (nombreCliente,))
            if cursor.fetchone() == None:
                instruccion = (f"INSERT INTO cliente (NombreCliente, Cumpleanos, Telefono, Correo, FechaRegistro) VALUES ('{nombreCliente}', '{cumpleanos}', '{celular}', '{correo}', '{fechaRegistro}')")
                con.execute(instruccion)
                self.aviso_lineedit_2.setText("")
                self.exito_lineedit_2.setText("Cliente agregado con exito.")
                #Limpiar campos
                self.nombre_cliente_lineedit.setText("")
                self.cumpleanos_lineedit.setText("")
                self.correo_lineedit.setText("")
                self.celular_lineedit.setText("")
                con.commit()    
                con.close()
            else:
                self.aviso_lineedit_2.setText("")
                self.aviso_lineedit_2.setText("El cliente ya existe.")
    
    def agregarEmpleado(self):
        nombreEmpleado = self.nombre_empleado_lineedit.text()
        correo = self.correo_empleado_lineedit.text()
        celular = self.celular_empleado_lineedit.text()
        fechaRegistro = datetime.date.today()
        con = sql.connect("cleanwalkers.db")
        cursor = con.cursor()
        
        if len(nombreEmpleado) == 0 or len(celular) == 0 or len(correo) == 0:
            self.aviso_lineedit_3.setText("")
            self.aviso_lineedit_3.setText("Por favor llena todos los campos.")
        else:
            cursor.execute("SELECT NombreEmpleado FROM empleado WHERE NombreEmpleado = ?", (nombreEmpleado,))
            if cursor.fetchone() == None:
                instruccion = (f"INSERT INTO empleado (NombreEmpleado, Telefono, Correo, FechaRegistro) VALUES ('{nombreEmpleado}', '{celular}', '{correo}', '{fechaRegistro}')")
                con.execute(instruccion)
                self.aviso_lineedit_3.setText("Empleado agregado con exito")
                #Limpiar campos
                self.nombre_empleado_lineedit.setText("")
                self.correo_empleado_lineedit.setText("")
                self.celular_empleado_lineedit.setText("")
                con.commit()    
                con.close()
            else:
                self.aviso_lineedit_3.setText("")
                self.aviso_lineedit_3.setText("El empleado ya existe.")


    def refreshTables(self):
        self.buscarCalzado.setQuery("SELECT * FROM calzado")
        self.buscarCliente.setQuery("SELECT * FROM cliente")
        self.buscarOrden.setQuery("SELECT * FROM orden")


    def buscarNombreCliente(self, txt):
        self.buscarCliente.setQuery("SELECT * FROM cliente WHERE NombreCliente LIKE '%"+txt+"%'")

    def buscarNombreCalzado(self, txt):
        self.buscarCalzado.setQuery("SELECT * FROM calzado WHERE TipoCalzado LIKE '%"+txt+"%'")

    def modificarModdel_update(self):
        self.modificarTimer.start() 

    def gotoLogin(self):
        login = WelcomeScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def modificarTimer_update(self):
        self.refreshTables()

class DashboardScreen(QMainWindow):
    def __init__(self):
        super(DashboardScreen, self).__init__()
        loadUi("dashboard.ui", self)
        self.regresarButton.clicked.connect(self.gotoMain)
        self.regresarButton_11.clicked.connect(self.gotoMain)
        self.regresarButton_12.clicked.connect(self.gotoMain)
        resizePequeño = 240
        resizePequeño2 = 250
        resizeGrande1 = 511
        resizeGrande2 = 351
        resizeGrande3 = 461
        resizeGrande4 = 330


        #Leer consulta de la base de datos
        con = sql.connect("cleanwalkers.db")
        cursor = con.cursor()


        #------------------------
        #clientes_graphicsView_1
        #------------------------
        #grafica de pastel, sobre el sexo de los clientes
        cursor.execute("SELECT Sexo, COUNT(*) FROM cliente GROUP BY Sexo")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Sexo", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Sexo de los clientes")
        plt.pie(df["Total"], labels=df["Sexo"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#F2C94C", "#0f3463"])
        plt.axis("equal")
        #download image
        plt.savefig("graficas/clientes1.png")
        #resize image with PIL
        img = Image.open("graficas/clientes1.png")
        img = img.resize((resizePequeño,resizePequeño), Image.LANCZOS)
        img.save("graficas/clientes1.png")
        self.clientes_graphicsView_1.setStyleSheet("background-image: url(graficas/clientes1.png);")
        #limpiar variables
        plt.close()

        #------------------------
        #clientes_graphicsView_2
        #------------------------
        cursor.execute("SELECT cli.Sexo, (COUNT(cli.Sexo)*serv.Costo) AS Ganancia FROM calzado cal, servicio serv, cliente cli WHERE cli. NombreCliente = cal.Cliente AND cal.ServicioContratado = serv.NombreServicio GROUP  BY cli.Sexo")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Sexo", "Total"]
        plt.figure (figsize=(7,5))
        plt.title("Ganancias por Sexo")
        plt.bar(df["Sexo"], df["Total"], color=["#FABC00", "#87CEEB"])
        plt.savefig("graficas/clientes2.png")
        img = Image.open("graficas/clientes2.png")
        #recortar imagen parte de arriba
        img = img.crop((0, 00, 650, 500))
        img = img.resize((resizePequeño,resizePequeño), Image.LANCZOS)
        img.save("graficas/clientes2.png")
        self.clientes_graphicsView_2.setStyleSheet("background-image: url(graficas/clientes2.png);")
        plt.close()

        #------------------------
        #clientes_graphicsView_3
        #------------------------
        #grafica de barras, promedio de servicios por sexo
        cursor.execute("SELECT Sexo, AVG(TotalServicios) FROM cliente GROUP BY Sexo")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Sexo", "Promedio"]
        plt.figure (figsize=(5,5))
        plt.title("Promedio de servicios por sexo")
        plt.bar(df["Sexo"], df["Promedio"], color=["#F2C94C", "#0f3463"])
        #download image
        plt.savefig("graficas/clientes3.png")
        #resize image with PIL
        img = Image.open("graficas/clientes3.png")
        img = img.resize((511,351), Image.LANCZOS)
        img.save("graficas/clientes3.png")
        self.clientes_graphicsView_3.setStyleSheet("background-image: url(graficas/clientes3.png);")
        #limpiar variables
        plt.close()

        #------------------------
        #clientes_graphicsView_5
        #------------------------
        #Gráfica de barras Horizontal
        #De los clientes que tengan mas TotalServicios, mostrar los 10 primeros con nombre
        cursor.execute("SELECT NombreCliente, ApellidoCLiente, TotalServicios FROM cliente ORDER BY TotalServicios DESC LIMIT 10")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Nombre", "Apellido", "TotalServicios"]
        plt.figure (figsize=(5,5))
        plt.xticks(rotation=-45)
        plt.title("Clientes con mas servicios")
        sns.barplot(x="Nombre", y="TotalServicios", data=df, palette="cividis")
        plt.savefig("graficas/clientes5.png")
        img = Image.open("graficas/clientes5.png")
        img = img.crop((0, 30, 500, 500))
        img = img.resize((531,250), Image.LANCZOS)
        img.save("graficas/clientes5.png")
        self.clientes_graphicsView_5.setStyleSheet("background-image: url(graficas/clientes5.png);")
        #limpiar variables
        plt.close()



        self.clientes_graphicsView_4.setStyleSheet("background-image: url(graficas/MJ_Cuadro.jpg);")

        #------------------------
        #clientes_graphicsView_5
        #------------------------
        #Grafica de barras, clientes por mes de registro
        #self.clientes_graphicsView_5.setStyleSheet("background-image: url(graficas/logo.jpg);")
        
        #------------------------
        #clientes_graphicsView_7
        #------------------------
         #Grafica histplot sobre la edad de los clientes
        cursor.execute("SELECT FechaNacimiento FROM cliente")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["FechaNacimiento"]
        #Formato de fecha en db es dd/mm/yyyy
        #Se convierte a yyyy
        df["FechaNacimiento"] = df["FechaNacimiento"].str.slice(start=6)
        df["FechaNacimiento"] = df["FechaNacimiento"].astype(int)
        df["FechaNacimiento"] = 2023 - df["FechaNacimiento"]
        #Verificar que no haya edades menores a 10 ni mayores a 100 años y si hay ponerlos entre 10 y 50
        for i in range(len(df["FechaNacimiento"])):
            if df["FechaNacimiento"][i] < 10 or df["FechaNacimiento"][i] > 100:
                df["FechaNacimiento"][i] = random.randint(10,50)
        plt.figure (figsize=(5,4))
        plt.title("Número de clientes por edad")
        plt.ylabel("Total")
        plt.xlabel("Edad")
        plt.hist(df["FechaNacimiento"], bins=10, color="#F2C94C")
        plt.savefig("graficas/clientes7.png")
        img = Image.open("graficas/clientes7.png")
        img = img.resize((461,331), Image.LANCZOS)
        img.save("graficas/clientes7.png")
        self.clientes_graphicsView_7.setStyleSheet("background-image: url(graficas/clientes7.png);")
        plt.close()
        

        #------------------------
        #calzado_graphicsView_1
        #------------------------
        #grafica pastel sobre el tipo de calzado
        cursor.execute("SELECT TipoCalzado, COUNT(*) FROM calzado GROUP BY TipoCalzado")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["TipoCalzado", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Tipos de Calzado")
        explode = (0.05, 0.05, 0.05, 0.05, 0.05)
        plt.pie(df["Total"], labels=df["TipoCalzado"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#BAA050", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00"], pctdistance=0.85, explode=explode)

        #----------------------------------------------
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        #-----------------------------------------------

        plt.axis("equal")
        plt.savefig("graficas/calzado1.png")
        img = Image.open("graficas/calzado1.png")
        img = img.resize((resizePequeño,resizePequeño), Image.LANCZOS)
        img.save("graficas/calzado1.png")
        self.calzado_graphicsView_1.setStyleSheet("background-image: url(graficas/calzado1.png);")
        plt.close()

        #------------------------
        #calzado_graphicsView_3
        #------------------------
        #grafica pastel sobre los materiales del calzado
        cursor.execute("SELECT Materiales, COUNT(*) FROM calzado GROUP BY Materiales")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Materiales", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Materiales del Calzado")
        explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
        plt.pie(df["Total"], labels=df["Materiales"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#BAA050"], explode=explode)
        plt.axis("equal")
        plt.savefig("graficas/calzado3.png")
        img = Image.open("graficas/calzado3.png")
        img = img.resize((resizePequeño,resizePequeño), Image.LANCZOS)
        img.save("graficas/calzado3.png")
        self.calzado_graphicsView_3.setStyleSheet("background-image: url(graficas/calzado3.png);")
        plt.close()

        #------------------------
        #calzado_graphicsView_4
        #------------------------
        cursor.execute("SELECT Marca, COUNT(*) AS CNT FROM calzado GROUP BY Marca")
        result = cursor.fetchall()
        df = pd.DataFrame(result) 
        df.columns = ["Marca", "Total"] 
        #inclinar los nombres
        plt.yticks(rotation=45)
        plt.title("Servicios por Marca")
        sns.barplot(x="Total", y="Marca", data=df, palette="cividis")
        plt.savefig("graficas/calzado4.png")
        img = Image.open("graficas/calzado4.png")
        img = img.crop((0, 30, 590, 480))
        img = img.resize((resizeGrande1,resizeGrande2), Image.LANCZOS)
        img.save("graficas/calzado4.png")
        self.calzado_graphicsView_4.setStyleSheet("background-image: url(graficas/calzado4.png);")
        plt.close()

        #------------------------
        #calzado_graphicsView_5
        #------------------------
        cursor.execute("SELECT A.Materiales, (COUNT(A.Materiales)*B.Costo) AS Ganancia FROM calzado A, servicio B WHERE A.ServicioContratado = B.NombreServicio GROUP BY A.Materiales")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Materiales", "Total"]
        plt.figure (figsize=(7,5))
        plt.title("Ganancias por tipo de Material")
        plt.bar(df["Materiales"], df["Total"], color=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB"])
        plt.savefig("graficas/calzado5.png")
        img = Image.open("graficas/calzado5.png")
        #recortar imagen parte de arriba
        img = img.crop((0, 00, 650, 500))
        img = img.resize((341,621), Image.LANCZOS)
        img.save("graficas/calzado5.png")
        self.calzado_graphicsView_5.setStyleSheet("background-image: url(graficas/calzado5.png);")
        plt.close()


        #------------------------
        #calzado_graphicsView_6
        #------------------------
        # grafica , con la marca de calzado y el total de calzado de esa marca
        cursor.execute("SELECT Talla, COUNT(*) FROM calzado GROUP BY Talla")
        result = cursor.fetchall()
        df = pd.DataFrame(result) 
        df.columns = ["Total", "Talla"] 
        #inclinar los nombres
        plt.yticks(rotation=0)
        plt.xticks(rotation = 45)
        plt.title("Tallas usuales")
        plt.stem(df["Total"], df["Talla"], use_line_collection=True)
        plt.savefig("graficas/calzado6.png")
        img = Image.open("graficas/calzado6.png")
        img = img.resize((resizeGrande3,resizeGrande4), Image.LANCZOS)
        img.save("graficas/calzado6.png")
        self.calzado_graphicsView_6.setStyleSheet("background-image: url(graficas/calzado6.png);")
        plt.close()

        #------------------------
        #calzado_graphicsView_7
        #------------------------
        #grafica pastel sobre el tipo de calzado
        cursor.execute("SELECT ServicioContratado, COUNT(*) FROM calzado GROUP BY ServicioContratado")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["ServicioContratado", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Servicios contratados") 
        explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
        plt.pie(df["Total"], labels=df["ServicioContratado"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB"], pctdistance=0.85, explode=explode)
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis("equal")
        plt.savefig("graficas/calzado7.png")
        img = Image.open("graficas/calzado7.png")
        img = img.resize((resizePequeño2,resizePequeño2), Image.LANCZOS)
        img.save("graficas/calzado7.png")
        self.calzado_graphicsView_7.setStyleSheet("background-image: url(graficas/calzado7.png);")
        plt.close()

        #------------------------
        #calzado_graphicsView_8
        #------------------------
        #grafica de tendencia de FechaLlegada del calzado
        # cursor.execute("SELECT Month(FechaLlegada), COUNT(*) FROM calzado")
        # result = cursor.fetchall()
        # df = pd.DataFrame(result)
        # df.columns = ["Nombre", "Total"]
        # plt.figure (figsize=(4,4))
        # plt.title("Tenis lavados por empleado")
        # plt.xticks(rotation = 45)
        # sns.barplot(x="Nombre", y="Total", data=df, palette="cividis")
        # plt.savefig("graficas/empleados4.png")  
        # img = Image.open("graficas/empleados4.png")
        # img = img.crop((0, 25, 400, 400))
        # img = img.resize((resizeGrande1,resizeGrande2), Image.LANCZOS)
        # img.save("graficas/empleados4.png")
        # self.empleados_graphicsView_4.setStyleSheet("background-image: url(graficas/empleados4.png);")
        # img = Image.open("graficas/logoTenis.png")
        # img = img.resize((900,641), Image.LANCZOS)
        # img = img.crop((275, 0, 720, 641))
        # img.save("graficas/logoTenis1.png")
        # self.empleados_graphicsView_5.setStyleSheet("background-image: url(graficas/logoTenis1.png);")
        cursor.execute("SELECT Color, COUNT(*) FROM calzado GROUP BY Color")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Color", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Colores usados") 
        explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
        plt.pie(df["Total"], labels=df["Color"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB" ], pctdistance=0.85, explode=explode)
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis("equal")
        plt.savefig("graficas/calzado8.png")
        img = Image.open("graficas/calzado8.png")
        img = img.resize((resizePequeño2,resizePequeño2), Image.LANCZOS)
        img.save("graficas/calzado8.png")
        self.calzado_graphicsView_8.setStyleSheet("background-image: url(graficas/calzado8.png);")
        plt.close()


        
        
        img = Image.open("graficas/logo.jpg")
        img = img.crop((50, 50, 480, 720))
        img.save("graficas/logo1.jpg")
        self.calzado_graphicsView_5.setStyleSheet("background-image: url(graficas/logo1.jpg);")

        #------------------------
        #empleados_graphicsView_1
        #------------------------


        #------------------------
        #empleados_graphicsView_3
        #------------------------
        #Grafica pastel Seleccionar ServicioContratado de calzado lo contamos y lo multiplicamos por el costo de la tabla servicio
        cursor.execute("SELECT A.ServicioContratado, (COUNT(A.ServicioContratado)*B.Costo) AS Ganancia FROM calzado A, servicio B WHERE A.ServicioContratado = B.NombreServicio GROUP BY ServicioContratado")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["ServicioContratado", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Porcentaje de ganancias por servicio")
        plt.pie(df["Total"], labels=df["ServicioContratado"], autopct="%1.1f%%", shadow=False, startangle=90, colors=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB"])
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis("equal")
        plt.savefig("graficas/empleados3.png")
        img = Image.open("graficas/empleados3.png")
        img = img.resize((resizePequeño2,resizePequeño2), Image.LANCZOS)
        img.save("graficas/empleados3.png")
        self.empleados_graphicsView_3.setStyleSheet("background-image: url(graficas/empleados3.png);")
        plt.close()

        #------------------------
        #empleados_graphicsView_4
        #------------------------
        #Gráfica de barras el total de tenis lavados de la tabla empleados
        cursor.execute("SELECT NombreEmpleado, TenisLavados FROM empleado")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["Nombre", "Total"]
        plt.figure (figsize=(4,4))
        plt.title("Tenis lavados por empleado")
        plt.xticks(rotation = 45)
        sns.barplot(x="Nombre", y="Total", data=df, palette="cividis")
        plt.savefig("graficas/empleados4.png")  
        img = Image.open("graficas/empleados4.png")
        img = img.crop((0, 25, 400, 400))
        img = img.resize((resizeGrande1,resizeGrande2), Image.LANCZOS)
        img.save("graficas/empleados4.png")
        self.empleados_graphicsView_4.setStyleSheet("background-image: url(graficas/empleados4.png);")
        img = Image.open("graficas/logoTenis.png")
        img = img.resize((900,641), Image.LANCZOS)
        img = img.crop((275, 0, 720, 641))
        img.save("graficas/logoTenis1.png")
        self.empleados_graphicsView_5.setStyleSheet("background-image: url(graficas/logoTenis1.png);")

        #------------------------
        #empleados_graphicsView_6
        #------------------------
        #Grafica pastel Seleccionar ServicioContratado de calzado lo contamos y lo multiplicamos por el costo de la tabla servicio
        cursor.execute("SELECT A.ServicioContratado, (COUNT(A.ServicioContratado)*B.Costo) AS Ganancia FROM calzado A, servicio B WHERE A.ServicioContratado = B.NombreServicio GROUP BY ServicioContratado")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.columns = ["ServicioContratado", "Total"]
        plt.figure (figsize=(8,7))
        plt.title("Ganancias por servicio")
        plt.bar(df["ServicioContratado"], df["Total"], color=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB"])
        #color=["#FABC00", "#87CEEB", "#FABC00", "#87CEEB", "#FABC00", "#87CEEB"]
        plt.savefig("graficas/empleados6.png")
        img = Image.open("graficas/empleados6.png")
        #recortar imagen parte de arriba
        img = img.crop((0, 55, 800, 700))
        img = img.resize((resizeGrande3,resizeGrande4), Image.LANCZOS)
        img.save("graficas/empleados6.png")
        self.empleados_graphicsView_6.setStyleSheet("background-image: url(graficas/empleados6.png);")
        plt.close()

        #------------------------
        #empleados_graphicsView_7
        #------------------------
        #Grafica lineplot de lluvias 
        #leer lluvias.csv
        df = pd.read_csv("csv/Lluvias.csv")
        df.columns = ["Mes", "Lluvias"]
        plt.figure (figsize=(4,4))
        plt.title("Lluvias")
        plt.xticks(rotation = 45)
        sns.lineplot(x="Lluvias", y="Mes", data=df, color="#FABC00")
        plt.savefig("graficas/empleados7.png")
        img = Image.open("graficas/empleados7.png")
        img = img.crop((15, 20, 395,400))
        img = img.resize((241,291), Image.LANCZOS)
        img.save("graficas/empleados7.png")
        self.empleados_graphicsView_7.setStyleSheet("background-image: url(graficas/empleados7.png);")
        #self.empleados_graphicsView_7.setStyleSheet("background-image: url(graficas/logo.jpg);")
        
    #Funciones
    def gotoMain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

#Funcion para preparar la base de Datos
# def prepareDatabase():
#     db = QSqlDatabase.addDatabase("QSQLITE")
#     db.setDatabaseName("cleanwalkers.db")
#     if(db.open()):
#         q = QSqlQuery()
#         #crear tabla calzado
#         if(q.prepare("CREATE TABLE IF NOT EXISTS calzado (idTenis INTEGER PRIMARY KEY AUTOINCREMENT, TipoCalzado varchar(50), ServicioContratado varchar(50), Marca varchar(50), Talla float, Color varchar(50), Materiales varchar(50), DetallesCalzado varchar(50), FechaLlegada date, Rack integer, Extra varchar(50), Cliente varchar(50))")):
#             if(q.exec()):
#                 print("Tabla calzado creada")
#         if(q.prepare("CREATE TABLE IF NOT EXISTS servicio (NombreServicio varchar(50) PRIMARY KEY not null, Costo float, PromedioEntrega varchar(50))")):
#             if(q.exec()):
#                 print("Tabla servicio creada")
#         if(q.prepare("CREATE TABLE IF NOT EXISTS cliente (idCliente INTEGER PRIMARY KEY AUTOINCREMENT, NombreCliente varchar(50), ApellidoCliente varchar(50), Correo varchar(50), Telefono integer, Sexo varchar(50), FechaNacimiento date, TotalVisitas integer, TotalServicios integer, FechaRegistro date)")):
#             if(q.exec()):
#                 print("Tabla cliente creada")
#         if(q.prepare("CREATE TABLE IF NOT EXISTS orden (idOrden INTEGER PRIMARY KEY AUTOINCREMENT, idCliente varchar(50), idTenis integer, FechaLlegada date, Costo float, FOREIGN KEY (idCliente) REFERENCES cliente(idCliente), FOREIGN KEY (idTenis) REFERENCES calzado(idTenis))")):
#             if(q.exec()):
#                 print("Tabla orden creada")
#         if(q.prepare("CREATE TABLE IF NOT EXISTS empleado (idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT, NombreEmpleado varchar(50), ApellidoEmpleado varchar(50), Telefono integer, Correo varchar(50), TenisLavados integer)")):
#             if(q.exec()):
#                 print("Tabla empleado creada")
    
#     #Agregar datos de prueba de clientesCW.csv
#     with open('csv/clientesCW.csv', errors="ignore") as File:
#         reader = csv.reader(File)
#         for row in reader:
#             con = sql.connect("cleanwalkers.db")
#             cursor = con.cursor()
#             if cursor.fetchone() == None:
#                 instruccion = (f"INSERT INTO cliente (NombreCliente, ApellidoCliente, Correo, Telefono, Sexo, FechaNacimiento, TotalVisitas, TotalServicios, FechaRegistro) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}')")
#                 con.execute(instruccion)
#                 con.commit()
#                 con.close()
#     # #Agregar datos de calzadoF.csv
#     with open ('csv/calzadoF.csv', errors="ignore") as File:
#         reader = csv.reader(File)
#         for row in reader:
#             con = sql.connect("cleanwalkers.db")
#             cursor = con.cursor()
#             if cursor.fetchone() == None:
#                 instruccion = (f"INSERT INTO calzado (TipoCalzado, ServicioContratado, Marca, Talla, Color, Materiales, DetallesCalzado, FechaLlegada, Rack, Extra, Cliente) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}')")
#                 con.execute(instruccion)
#                 con.commit()
#                 con.close()
#     # #Agregar datos de empleado.csv
#     with open ('csv/empleado.csv', errors="ignore") as File:
#         reader = csv.reader(File)
#         for row in reader:
#             con = sql.connect("cleanwalkers.db")
#             cursor = con.cursor()
#             if cursor.fetchone() == None:
#                 instruccion = (f"INSERT INTO empleado (NombreEmpleado, ApellidoEmpleado, Telefono, Correo, TenisLavados) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}')")
#                 con.execute(instruccion)
#                 con.commit()
#                 con.close()

def verificarServicios():
    con = sql.connect("cleanwalkers.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM servicio")
    if cursor.fetchone() == None:
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('Clean Gent', 50, '1 semana')")
        con.execute(instruccion)
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('Basic', 100, '1 semana')")
        con.execute(instruccion)
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('Premium', 150, '1 semana')")
        con.execute(instruccion)
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('VIP', 180, '1 semana')")
        con.execute(instruccion)
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('Ultra White', 160, '1 semana')")
        con.execute(instruccion)
        instruccion = (f"INSERT INTO servicio (NombreServicio, Costo, PromedioEntrega) VALUES ('Suede', 150, '1 semana')")
        con.execute(instruccion)
        con.commit()
        con.close()

#Main
# prepareDatabase()
# verificarServicios()
app = QApplication(sys.argv)
welcome = DashboardScreen() #WelcomeScreen CAMBIAR
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.show()
try: 
    sys.exit(app.exec())
except:
    print("Saliendo")