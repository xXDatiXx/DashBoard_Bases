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
        resizePequeño = 220

        #Leer consulta de la base de datos
        con = sql.connect("cleanwalkers.db")
        cursor = con.cursor()


        #------------------------
        #clientes_graphicsView_1
        #------------------------
        #grafica de pastel
        cursor.execute("SELECT Sexo, COUNT(*) FROM cliente GROUP BY Sexo")
        result = cursor.fetchall() #fetchall() -> lista de tuplas
        #seaborn pieplot
        df = pd.DataFrame(result) #convertir lista de tuplas a dataframe
        df.columns = ["Sexo", "Cantidad"] #asignar nombres a las columnas
        plt.figure(figsize=(5,5))
        plt.pie(df["Cantidad"], labels=df["Sexo"], autopct='%1.1f%%', shadow=False, startangle=90)
        #download image
        plt.savefig("graficas/clientes1.png")
        #resize image with PIL
        img = Image.open("graficas/clientes1.png")
        img = img.resize((resizePequeño,resizePequeño), Image.ANTIALIAS) #antialias para que no se pixele
        img.save("graficas/clientes1.png")
        self.clientes_graphicsView_1.setStyleSheet("background-image: url(graficas/clientes1.png);")
        #limpiar variables
        plt.close()
        

        #------------------------
        #clientes_graphicsView_2
        #------------------------
        cursor.execute("SELECT Sexo, TotalServicios FROM cliente")
        result = cursor.fetchall() #fetchall() -> lista de tuplas
        #seaborn barplot
        df = pd.DataFrame(result) #convertir lista de tuplas a dataframe
        df.columns = ["Sexo", "Cantidad"] #asignar nombres a las columnas
        sns.barplot(x="Sexo", y="Cantidad", data=df, palette="rocket")
        #download image
        plt.savefig("graficas/clientes2.png")
        #resize image with PIL
        img = Image.open("graficas/clientes2.png")
        img = img.resize((resizePequeño,resizePequeño), Image.ANTIALIAS)
        img.save("graficas/clientes2.png")
        self.clientes_graphicsView_3.setStyleSheet("background-image: url(graficas/clientes2.png);")
        #limpiar variables
        plt.close()


        #------------------------
        #clientes_graphicsView_3
        #------------------------
        cursor.execute("SELECT Sexo, TotalServicios FROM cliente")
        result = cursor.fetchall() #fetchall() -> lista de tuplas
        #seaborn barplot
        df = pd.DataFrame(result) #convertir lista de tuplas a dataframe
        df.columns = ["Sexo", "Cantidad"] #asignar nombres a las columnas
        sns.barplot(x="Sexo", y="Cantidad", data=df, palette="rocket")
        #download image
        plt.savefig("graficas/clientes3.png")
        #resize image with PIL
        img = Image.open("graficas/clientes3.png")
        img = img.resize((511,291), Image.ANTIALIAS)
        img.save("graficas/clientes3.png")
        self.clientes_graphicsView_3.setStyleSheet("background-image: url(graficas/clientes3.png);")
        #limpiar variables
        plt.close()

        #------------------------
        #clientes_graphicsView_4
        #------------------------
        #Gráfica de barras Horizontal bar plots
        #De los clientes que tengan mas TotalServicios, mostrar los 10 primeros con nombre
        cursor.execute("SELECT NombreCliente, ApellidoCLiente, TotalServicios FROM cliente ORDER BY TotalServicios DESC LIMIT 10")
        result = cursor.fetchall()
        df = pd.DataFrame(result) 
        df.columns = ["Nombre", "Apellido", "TotalServicios"] 
        df["Nombre"] = df["Nombre"] + " " + df["Apellido"]
        df = df.drop(["Apellido"], axis=1) #eliminar columna Apellido 
        sns.barplot(x="TotalServicios", y="Nombre", data=df, palette="rocket")
        plt.savefig("graficas/clientes4.png")
        img = Image.open("graficas/clientes4.png")
        img = img.resize((320,580), Image.ANTIALIAS)
        img.save("graficas/clientes4.png")
        self.clientes_graphicsView_4.setStyleSheet("background-image: url(graficas/clientes4.png);")
        plt.close()

        #------------------------
        #clientes_graphicsView_7
        #------------------------
        #Gráfica de barras
        cursor.execute("SELECT TotalServicios FROM cliente")
        result = cursor.fetchall() #fetchall() -> lista de tuplas
        df = pd.DataFrame(result)
        df.columns = ["Cantidad"]
        sns.barplot(x=df.index, y="Cantidad", data=df, palette="Blues_d")
        plt.savefig("graficas/clientes7.png")
        W = 511
        H = 291
        img = Image.open("graficas/clientes7.png")
        img = img.resize((W,H), Image.ANTIALIAS)
        img.save("graficas/clientes7.png")
        self.clientes_graphicsView_7.setStyleSheet("background-image: url(graficas/clientes7.png);")
        plt.close()

        
        self.calzado_graphicsView.setStyleSheet("background-image: url(graficas/logo.png);")
        self.empleados_graphicsView.setStyleSheet("background-image: url(graficas/logo.png);")
        self.servicios_graphicsView.setStyleSheet("background-image: url(graficas/logo.png);")
        self.clientes_graphicsView_4.setStyleSheet("background-image: url(graficas/logo.png);")
        self.clientes_graphicsView_5.setStyleSheet("background-image: url(graficas/logo.png);")
        self.clientes_graphicsView_6.setStyleSheet("background-image: url(graficas/logo.png);")


    #Funciones
    def gotoMain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

#Funcion para preparar la base de Datos
def prepareDatabase():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("cleanwalkers.db")
    if(db.open()):
        q = QSqlQuery()
        if(q.prepare("CREATE TABLE IF NOT EXISTS calzado (idTenis INTEGER PRIMARY KEY AUTOINCREMENT, TipoCalzado varchar(50), ServicioContratado varchar(50), Marca varchar(50), Talla float, Color varchar(50), Materiales varchar(50), DetallesCalzado varchar(50), FechaLlegada date, Rack integer, Extra varchar(50), Cliente varchar(50), FOREIGN KEY (Cliente) REFERENCES cliente(NombreCliente))")):
            if(q.exec()):
                print("Tabla calzado creada")
        if(q.prepare("CREATE TABLE IF NOT EXISTS servicio (NombreServicio varchar(50) PRIMARY KEY not null, Costo float, PromedioEntrega varchar(50))")):
            if(q.exec()):
                print("Tabla servicio creada")
        if(q.prepare("CREATE TABLE IF NOT EXISTS cliente (idCliente INTEGER PRIMARY KEY AUTOINCREMENT, NombreCliente varchar(50), ApellidoCliente varchar(50), Correo varchar(50), Telefono integer, Sexo varchar(50), FechaNacimineto date, TotalVisitas integer, TotalServicios integer, FechaRegistro date)")):
            if(q.exec()):
                print("Tabla cliente creada")
        if(q.prepare("CREATE TABLE IF NOT EXISTS orden (idOrden INTEGER PRIMARY KEY AUTOINCREMENT, idCliente varchar(50), idTenis integer, FechaLlegada date, Costo float, FOREIGN KEY (idCliente) REFERENCES cliente(idCliente), FOREIGN KEY (idTenis) REFERENCES calzado(idTenis))")):
            if(q.exec()):
                print("Tabla orden creada")
        if(q.prepare("CREATE TABLE IF NOT EXISTS empleado (idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT, NombreEmpleado varchar(50), ApellidoEmpleado varchar(50), Telefono integer, Correo varchar(50), idTenisLavados integer)")):
            if(q.exec()):
                print("Tabla empleado creada")
    #Agregar datos de prueba de clientesCW.csv
    # with open('clientesCW.csv', errors="ignore") as File:
    #     reader = csv.reader(File)
    #     for row in reader:
    #         con = sql.connect("cleanwalkers.db")
    #         cursor = con.cursor()
    #         if cursor.fetchone() == None:
    #             instruccion = (f"INSERT INTO cliente (NombreCliente, ApellidoCliente, Correo, Telefono, Sexo, FechaNacimineto, TotalVisitas, TotalServicios) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}')")
    #             con.execute(instruccion)
    #             con.commit()
    #             con.close()
  
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
prepareDatabase()
verificarServicios()
app = QApplication(sys.argv)
welcome = DashboardScreen() #WelcomeScreen CAMBIAR
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.show()
try: 
    sys.exit(app.exec())
except:
    print("Saliendo")