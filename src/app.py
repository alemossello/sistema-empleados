from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
mysql = MySQL()


#CONFIGURACION PARA CONECTAR LA BASE DE DATOS.
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados'
app.config['MYSQL_DATABASE_PORT'] = 3307

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
    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route("/delete/<int:id>", methods=["DELETE"])

if __name__ == '__main__':
    app.run(debug=True)