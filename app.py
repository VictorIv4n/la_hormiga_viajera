from flask import Flask , render_template,request,redirect,url_for, flash

from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql Connection
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='1234'
app.config['MYSQL_DB'] ='consultas'
mysql = MySQL(app)
#settings

app.secret_key = 'mysecretkey'

app.static_folder = 'static'

#rutas

#pagina de home
@app.route('/')
def Index():
    return render_template('index.html')

#pagina de destinos
@app.route('/destinos')
def destinos():
    return render_template('destinos.html')

#pagina de galeria de fotos
@app.route('/galeria')
def galeria():
    return render_template('galeria1.html')

#pagina de inicio de sesion
@app.route('/inisesion')
def inisesion():
    return render_template('inicioSesion.html')

#pagina de quienes somos
@app.route('/quienessomos')
def quienessomos():
    return render_template('quienesSomos.html')

#pagina de tipos de viajes
@app.route('/tiposdeviajes')
def tiposdeviajes():
    return render_template('tiposdeviajes.html')

#pagina de vuelos
@app.route('/vuelos')
def vuelos():
    return render_template('vuelos.html')

# pagina de envio exitoso
@app.route('/envioExitoso')
def envio_exitoso():
        return render_template('envioExitoso.html')



@app.route('/formularioConsultas')
def formularioConsultas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM consultas')
    data = cur.fetchall()
    return render_template('formularioConsultas.html',consultas = data)

@app.route('/consultas', methods=['POST'])
def add_consultas():
    if request.method == 'POST':
        firstname =request.form['nombre']
        lastname =request.form['apellido']
        email =request.form['email']
        cellphone =request.form['phone']
        travelDate =request.form['travelDate']
        passengers =request.form['passengers']
        message = request.form['message']
        recomendacion = request.form['howDidYouFindUs']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO consultas (nombre, apellido, email, phone, date, pax, consulta, recomendacion ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (firstname, lastname, email, cellphone, travelDate, passengers, message,recomendacion))
        mysql.connection.commit()
        return redirect (url_for("envio_exitoso"))
    
#pagina de la lista de consultas
    
@app.route('/list_consultas')
def list_consultas():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM consultas ')
        data = cur.fetchall()
        return render_template('list_consultas.html', consultas = data)

#pagina de editar consulta
    
@app.route('/edit/<id>')
def get_consulta(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM consultas WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_consultas.html', consulta = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_consulta(id):
    if request.method == 'POST':
        firstname = request.form['nombre']
        lastname = request.form['apellido']
        email = request.form['email']
        cellphone = request.form['phone']
        travelDate =request.form['travelDate']
        passengers =request.form['passengers']
        message = request.form['message']
        recomendacion = request.form['howDidYouFindUs']
        cur =   mysql.connection.cursor()
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
        WHERE id = %s """, (firstname, lastname, email, cellphone, travelDate, passengers, message, recomendacion, id))
        mysql.connection.commit()
    flash('Consulta editada satisfactoriamente')
    return redirect(url_for('list_consultas'))     

@app.route('/delete/<string:id>')
def delete_consulta(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM consultas WHERE id = %s', (id,))
    mysql.connection.commit()
    flash("Consulta eliminada satisfatoriamente")
    return redirect(url_for('list_consultas'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True) #el debug sirve para que se actualice el servidor