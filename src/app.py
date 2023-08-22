from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory, flash #mensajes de error
from flaskext.mysql import MySQL
from datetime import datetime
import os
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL()


#CONFIGURACION PARA CONECTAR LA BASE DE DATOS.
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados'
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['SECRET_KEY'] = 'codoacodo' #para los FLASHES... token de cookie

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS #Guardamos la ruta como un valor en la app

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(cursor = DictCursor) #El parametro se lo pasamos para que nos devuelva la información como un dictionary (Corresponde a la libreria PyMiSql)

#Funcion para las consultas a la base de datos.

def queryMySql(query, data = ()):
    if len(data) > 0:
        cursor.execute(query, data)
    else:
        cursor.execute(query)

    conn.commit()


#Muestro la foto en la tabla
@app.route('/fotodeusuario/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('UPLOADS'), nombreFoto)

@app.route('/')
def index():

    sql = "SELECT * from empleados"
    cursor.execute(sql)

    empleados = cursor.fetchall() #Me trae todos los registros.

    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)

@app.route("/empleado/crear", methods = ["GET","POST"])
def alta_empleado():
    if request.method == "GET":
        return render_template('empleados/create.html')
    elif request.method == "POST":
        _nombre = request.form["txtNombre"]
        _correo = request.form["txtCorreo"]
        _foto = request.files["txtFoto"]

        if _nombre == "" or _correo == "":
            flash("El nombre o el correo no pueden estar vacíos.")
            return redirect(url_for('alta_empleado'))
        else:
            now = datetime.now() #Fecha actual
            tiempo = now.strftime("%Y%H%M%S") #Convertimos la fecha en string

            #Guardamos la foto en la carpeta 'uploads0
            if _foto.filename != '':
                nuevoNombreFoto = tiempo + '-' + _foto.filename
                _foto.save("src/uploads/" + nuevoNombreFoto)

            sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s)"
            datos = (_nombre, _correo, nuevoNombreFoto)

            #Utilizamos la funcion creada en el inicio.
            queryMySql(sql, datos)

            return redirect('/')


@app.route("/delete/<int:id>")
def delete (id):

    sql = f"SELECT foto FROM empleados where id='{id}'"
    # cursor.execute(sql)
    queryMySql(sql)
    nombreFoto = cursor.fetchone()['foto']

    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
    except:
        pass

    sql = f"DELETE FROM empleados WHERE id={id}"
    queryMySql(sql)

    return redirect("/")

@app.route("/modify/<int:id>")
def modify (id):
    sql =  f"SELECT * from empleados where id = {id}"
    queryMySql(sql)

    empleado = cursor.fetchone() #NOS GUARDAMOS EL EMPLEADO

    return render_template("empleados/edit.html", empleado = empleado)


@app.route("/update", methods=["POST"])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    id = request.form["txtId"]

    if _foto.filename != "":
        now = datetime.now() #Fecha actual
        tiempo = now.strftime("%Y%H%M%S") #Convertimos la fecha en string
        nuevoNombreFoto = tiempo + '-' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)

        sql =  f"SELECT foto FROM empleados WHERE id = {id}"
        queryMySql(sql)

        nombreFoto = cursor.fetchone()[0]
        # borrarEstaFoto = os.path.join(app.config["UPLOADS"], nombreFoto)
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        except:
            pass

        sql = f"UPDATE empleados set foto = '{nuevoNombreFoto}' WHERE id = '{id}'"
        queryMySql(sql)

    sql = f"UPDATE empleados set nombre = '{_nombre}', correo = '{_correo}' WHERE id = '{id}'"
    queryMySql(sql)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)