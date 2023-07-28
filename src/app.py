from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

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
    sql = "Insert into empleados (nombre, correo, foto) values ('Camila','cami@email.com','foto.jpge');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    conn.commit()

    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)