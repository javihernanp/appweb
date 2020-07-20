from flask import Flask,  render_template, request, redirect, url_for, flash,session, logging, json, jsonify
from flask_mysqldb import MySQL

import os
from functools import wraps


app = Flask(__name__)
  
app.secret_key = os.urandom(24)
  
# MySQL configurations
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='tienda'

mysql = MySQL(app)

'''Decoradores para comprobar si estan logueados'''
def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap
'''Raiz Index.html'''

@app.route('/')
def index():
    return render_template('index.html')

'''Página de registro'''    
@app.route('/register')
@not_logged_in
def register():
    return render_template('register2.html')
    

'''Registro commit usuario'''
@app.route('/process', methods=['POST'])
def process():
    # connect
 
    cursor=mysql.connection.cursor()
    msg = ''
    name = request.form['name']
    apellido = request.form['apellido']
    dni = request.form['dni']
    direccion = request.form['direccion']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    
    if name and apellido and dni and email and password:
        try:
            cursor.execute('INSERT INTO clientes VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)', (name, apellido, dni, direccion,phone,email,password)) 
            mysql.connection.commit()
            cursor.close()
        except:
            return jsonify({'error' : 'Revisa el DNI o ese correo no esta disponible'})
        msg = 'Registrado ahora puedes hacer login'
        return jsonify({'name' : msg})
    
    return jsonify({'error' : 'Error al enviar los datos!'})

'''login''' 
@app.route('/login',methods=['GET','POST'])
@not_logged_in
def login():
    cursor=mysql.connection.cursor()
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        resultado=cursor.execute("SELECT * FROM clientes WHERE email=%s and password=%s", (email,password))
        if resultado > 0:
            datos = cursor.fetchall()
            session['logged_in'] = True
            for campo in datos:
                session['uid']=campo[0]
                session['s_name']=campo[6]
            
            return redirect(url_for('index'))
        
        else:
            cursor.close()
            return jsonify({'error' : 'Correo o Contraseña incorrectos'})
        
    return render_template('login.html')
    
'''Página de usuario'''
@app.route('/profile/<id>')
@is_logged_in
def profile(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM clientes where id=%s',(session['uid'],))
    datos = cursor.fetchall()
    cursor.close()
    return render_template('profile.html', contacts = datos)

'''editar datos usuario'''
@app.route('/edit/<id>')
@is_logged_in
def edit(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT * FROM clientes where id=%s',(session['uid'],))
        datos = cursor.fetchall()
        cursor.close()
        return render_template('edit.html', valores = datos)
    except:
        return redirect(url_for('login'))
'''actualizar datos usuario en la base de datos'''
@app.route('/update/<id>', methods=['POST'])
def update(id):
    cursor = mysql.connection.cursor()
    msg=''
    if request.method == 'POST':
        name = request.form['name']
        apellido = request.form['apellido']
        dni = request.form['dni']
        direccion = request.form['direccion']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        try:
            cursor.execute('UPDATE clientes SET nombre=%s, apellido=%s,dni=%s,direccion=%s,telefono=%s,email=%s,password=%s where id=%s',(name, apellido, dni, direccion,phone,email,password,(session['uid'])))
            mysql.connection.commit()
            msg = 'Datos actualizados correctamente'
            return jsonify({'name' : msg})
            
        except:
            return jsonify({'error' : 'No se han podido actualizar los datos, correo no disponible'})
            
'''Borrar usuario'''       
@app.route('/delete/<id>', methods=['POST','GET'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=%s',(session['uid'],))
    mysql.connection.commit()
    session.clear()
    cursor.close()
    return redirect(url_for('login'))

'''cerrar sesion'''

@app.route('/out')
def logout():
    if 'uid' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('login'))
'''Página de productos'''    
@app.route('/products')
def products():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos')
    datos = cursor.fetchall()
    
    cursor.close()
    return render_template('products.html', products = datos)
'''detalles productos'''
@app.route('/detalles/<id>')
def detalles(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos where id=%s', (id))
    datos = cursor.fetchall()
    cursor.close()
    return render_template('detalles.html', producto = datos)
'''comprar usuario'''
@app.route('/comprar/<id>',methods=['POST','GET'])

def comprar(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE id=%s", [id])
        comp = cursor.fetchall()  
        for campo in comp:
            idp = campo[0]
            pnombre = campo[1]
            cantidad = campo[5]
        cursor.execute('INSERT INTO pedidos VALUES (NULL, %s, %s,%s,NULL)',(session['s_name'],id,pnombre))
        mysql.connection.commit()
        cantidad -= 1
        cursor.execute('UPDATE productos SET cantidad=%s where id=%s and nombre=%s',(cantidad,idp,pnombre))
        mysql.connection.commit()
    return redirect(url_for('products'))
'''delete producto'''
@app.route('/deleteproduct/<id>',methods=['POST','GET'])

def deleteproduct(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", [id])
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('products'))
''' editar producto'''
@app.route('/editproduct/<id>',methods=['POST','GET'])
def editproduct(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('SELECT * FROM productos where id=%s',[id])
            datos = cursor.fetchall()
            cursor.close()
            for campo in datos:
                session['p_name']=campo[1]
            return render_template('editproduct.html', valores = datos)
        except:
            return redirect(url_for('products'))
    return redirect(url_for('products'))

@app.route('/updateproducto',methods=['POST','GET'])
def updateproducto():
    cursor = mysql.connection.cursor()
    msg=''
    if request.method == 'POST':
        name = request.form['name']
        precio = request.form['precio']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        try:
            cursor.execute('UPDATE productos SET nombre=%s, precio=%s,tipo=%s,descripcion=%s,cantidad=%s where nombre=%s',(name,precio,tipo,descripcion,cantidad,session['p_name']))
            mysql.connection.commit()
            msg = 'Datos actualizados correctamente'
            session.pop('p_name',None)
            return jsonify({'name' : msg})   
        except:
            return jsonify({'error' : 'No se han podido actualizar los datos, revisa que no hay otro producto con el mismo nombre'})    
'''carrito usuario'''
@app.route('/carrito/<id>')

def carrito(id):
    correo=session['s_name']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE emailcliente=%s", [correo])
    datos = cursor.fetchall()
    cursor.close()
    return render_template('carrito.html', pedidos = datos)
'''borrar pedido'''
@app.route('/DeletePedido/<id>')

def DeletePedido(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE id=%s',[id])
    datos = cursor.fetchall()
    for campo in datos:
        idp=campo[2]
        pnombre=campo[3]
        
    cursor.execute('DELETE FROM pedidos WHERE id=%s',[id])
    mysql.connection.commit()
    cursor.execute('SELECT * FROM productos WHERE id=%s and nombre=%s',(idp, pnombre))
    datosP = cursor.fetchall()
    for dato in datosP:
        cantidad=dato[5]
    cantidad+=1             
    cursor.execute('UPDATE productos SET cantidad=%s where id=%s and nombre=%s',(cantidad,idp,pnombre))
    mysql.connection.commit()
    if session['uid'] == 1:
        return redirect(url_for('admincarrito'))
    else:
        return redirect(url_for('carrito', id=session['uid']))
'''carrito admin'''
@app.route('/admincarrito')

def admincarrito():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pedidos")
    datos = cursor.fetchall()
    cursor.close()
    return render_template('carrito.html', pedidos = datos)
'''actualizar tabla productos admin'''

@app.route('/productupdate')
def productupdate():
    file = "C:\\json\\productos.json"
    json_data=open(file).read()
    json_obj = json.loads(json_data)
    cursor = mysql.connection.cursor()
    def validate_string(val):
        if val != None:
            if type(val) is int:
                return str(val).encode('utf-8')
            else:
                return val
    cursor.execute("DELETE FROM productos")
    mysql.connection.commit()
    cursor.execute("ALTER TABLE productos AUTO_INCREMENT = 1;")
    mysql.connection.commit()
    for i, dato in enumerate(json_obj):
        
        nombre = validate_string(dato.get("nombre", None))
        precio = validate_string(dato.get("precio", None))
        tipo = validate_string(dato.get("tipo", None))
        descripcion = validate_string(dato.get("descripcion", None))
        cantidad = validate_string(dato.get("cantidad", None))

        cursor.execute("INSERT INTO productos (nombre,	precio, tipo,descripcion,cantidad) VALUES (%s,	%s,%s,%s,%s)", (nombre,	precio,tipo,descripcion,cantidad))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('profile', id=session['uid']))

'''añadir productos'''
@app.route('/addproduct')
@is_logged_in
def addproduct():
    return render_template('regisp.html')
@app.route('/pad', methods=['POST'])
def pad():
    cursor=mysql.connection.cursor()
    msg = ''
    name = request.form['name']
    precio = request.form['precio']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    if name and precio and tipo and descripcion and cantidad:
        try:
            cursor.execute('INSERT INTO productos VALUES (NULL, %s, %s, %s, %s, %s)', (name, precio, tipo, descripcion,cantidad)) 
            mysql.connection.commit()
            cursor.close()
        except:
            return jsonify({'error' : 'Revisa, nombre no esta disponible'})
        msg = 'Registrado el producto'
        return jsonify({'name' : msg})
    
    return jsonify({'error' : 'Error al enviar los datos!'})
'''filtro monitor'''
@app.route('/monitor')
def monitor():
    return render_template('filtrom.html')
@app.route('/mp', methods=['POST'])
def mp():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM monitor')
    filas=[x[0] for x in cursor.description] #this will extract row headers
    data = cursor.fetchall()
    json_data=[]
    for datos in data:
        json_data.append(dict(zip(filas,datos)))
    return (json.dumps(json_data))
'''filtro teclado'''
@app.route('/teclado')
def teclado():
    return render_template('filtrot.html')
@app.route('/tp', methods=['POST'])
def tp():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM teclado')
    filas=[x[0] for x in cursor.description] #this will extract row headers
    data = cursor.fetchall()
    json_data=[]
    for datos in data:
        json_data.append(dict(zip(filas,datos)))
    return (json.dumps(json_data))
'''filtro raton'''
@app.route('/raton')
def raton():
    return render_template('filtror.html')
@app.route('/rp', methods=['POST'])
def rp():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM raton')
    filas=[x[0] for x in cursor.description] #this will extract row headers
    data = cursor.fetchall()
    json_data=[]
    for datos in data:
        json_data.append(dict(zip(filas,datos)))
    return (json.dumps(json_data))
  


if __name__ == '__main__':
    app.run(port= 3000, debug= True)