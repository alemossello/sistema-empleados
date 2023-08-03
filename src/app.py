from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()


#CONFIGURACION PARA CONECTAR LA BASE DE DATOS.
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados'
app.config['MYSQL_DATABASE_PORT'] = 3307

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS #Guardamos la ruta como un valor en la app

mysql.init_app(app)


@app.route('/')
def index():
    
    conn = mysql.connect()
    cursor = conn.cursor()

    # sql = "Insert into empleados (nombre, correo, foto) values ('Camila','cami@email.com','foto.jpge');"

    sql = "SELECT * from empleados"
    cursor.execute(sql)

    empleados = cursor.fetchall() #Me trae todos los registros.

    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)

@app.route("/create")
def create():
    return render_template('empleados/create.html')

@app.route("/store", methods=["POST"])
def store():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    now = datetime.now() #Fecha actual
    tiempo = now.strftime("%Y%H%M%S") #Convertimos la fecha en string

    #Guardamos la foto en la carpeta 'uploads0
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '-' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s)"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route("/delete/<int:id>")
def delete (id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = f"SELECT foto FROM empleados where id='{id}'"
    cursor.execute(sql)
    nombreFoto = cursor.fetchone()[0]

    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
    except:
        pass

    sql = "DELETE FROM empleados WHERE id=%s" #O podemos usar fstrings
    cursor.execute(sql, id)

    conn.commit()

    return redirect("/")

@app.route("/modify/<int:id>")
def modify (id):
    sql =  f"SELECT * from empleados where id = {id}"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    empleado = cursor.fetchone() #NOS GUARDAMOS EL EMPLEADO

    conn.commit()

    return render_template("empleados/edit.html", empleado = empleado)


@app.route("/update", methods=["POST"])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    id = request.form["txtId"]

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != "":
        now = datetime.now() #Fecha actual
        tiempo = now.strftime("%Y%H%M%S") #Convertimos la fecha en string
        nuevoNombreFoto = tiempo + '-' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)

        sql =  f"SELECT foto FROM empleados WHERE id = {id}"
        cursor.execute(sql)
        conn.commit()

        nombreFoto = cursor.fetchone()[0]
        # borrarEstaFoto = os.path.join(app.config["UPLOADS"], nombreFoto)

        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

        sql = f"UPDATE empleados set foto = '{nuevoNombreFoto}' WHERE id = '{id}'"
        cursor.execute(sql)
        conn.commit()

    sql = f"UPDATE empleados set nombre = '{_nombre}', correo = '{_correo}' WHERE id = '{id}'"
    cursor.execute(sql)
    conn.commit()

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)