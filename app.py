
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='consultas'
    )

# Settings
app.secret_key = 'mysecretkey'
app.static_folder = 'static'

# Rutas

# Página de home
@app.route('/')
def Index():
    return render_template('index.html')

# Página de destinos
@app.route('/destinos')
def destinos():
    return render_template('destinos.html')

# Página de galería de fotos
@app.route('/galeria')
def galeria():
    return render_template('galeria1.html')

# Página de inicio de sesión
@app.route('/inisesion')
def inisesion():
    return render_template('inicioSesion.html')

# Página de quienes somos
@app.route('/quienessomos')
def quienessomos():
    return render_template('quienesSomos.html')

# Página de tipos de viajes
@app.route('/tiposdeviajes')
def tiposdeviajes():
    return render_template('tiposdeviajes.html')

# Página de vuelos
@app.route('/vuelos')
def vuelos():
    return render_template('vuelos.html')

# Página de envío exitoso
@app.route('/envioExitoso')
def envio_exitoso():
    return render_template('envioExitoso.html')

# Formulario de consultas
@app.route('/formularioConsultas')
def formularioConsultas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM consultas')
        data = cur.fetchall()
        cur.close()
        conn.close()
    except Error as e:
        flash(f"Error al conectar a la base de datos: {e}")
        data = []
    return render_template('formularioConsultas.html', consultas=data)

@app.route('/consultas', methods=['POST'])
def add_consultas():
    if request.method == 'POST':
        firstname = request.form['nombre']
        lastname = request.form['apellido']
        email = request.form['email']
        cellphone = request.form['phone']
        travelDate = request.form['travelDate']
        passengers = request.form['passengers']
        message = request.form['message']
        recomendacion = request.form['howDidYouFindUs']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO consultas (nombre, apellido, email, phone, date, pax, consulta, recomendacion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                        (firstname, lastname, email, cellphone, travelDate, passengers, message, recomendacion))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("envio_exitoso"))
        except Error as e:
            flash(f"Error al conectar a la base de datos: {e}")
            return redirect(url_for("formularioConsultas"))

# Página de la lista de consultas
@app.route('/list_consultas')
def list_consultas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM consultas')
        data = cur.fetchall()
        cur.close()
        conn.close()
    except Error as e:
        flash(f"Error al conectar a la base de datos: {e}")
        data = []
    return render_template('list_consultas.html', consultas=data)

# Página de editar consulta
@app.route('/edit/<id>')
def get_consulta(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM consultas WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('edit_consultas.html', consulta=data[0])
    except Error as e:
        flash(f"Error al conectar a la base de datos: {e}")
        return redirect(url_for("list_consultas"))

@app.route('/update/<id>', methods=['POST'])
def update_consulta(id):
    if request.method == 'POST':
        firstname = request.form['nombre']
        lastname = request.form['apellido']
        email = request.form['email']
        cellphone = request.form['phone']
        travelDate = request.form['travelDate']
        passengers = request.form['passengers']
        message = request.form['message']
        recomendacion = request.form['howDidYouFindUs']
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
            UPDATE consultas
            SET nombre = %s,
                apellido = %s,
                email = %s,
                phone = %s,
                date = %s,
                pax = %s,
                consulta = %s,
                recomendacion = %s
            WHERE id = %s""", (firstname, lastname, email, cellphone, travelDate, passengers, message, recomendacion, id))
            conn.commit()
            cur.close()
            conn.close()
            flash('Consulta editada satisfactoriamente')
        except Error as e:
            flash(f"Error al conectar a la base de datos: {e}")
        return redirect(url_for('list_consultas'))

@app.route('/delete/<string:id>')
def delete_consulta(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM consultas WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Consulta eliminada satisfactoriamente")
    except Error as e:
        flash(f"Error al conectar a la base de datos: {e}")
    return redirect(url_for('list_consultas'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True) #el debug sirve para que se actualice el servidor

