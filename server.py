from flask import Flask, render_template, redirect, request, url_for
import os
from dotenv import load_dotenv
import requests
import json

#Variables de entorno
load_dotenv()

SERVER_ADD = os.getenv('SERVER_ADD')
SERVER_PORT = os.getenv('SERVER_PORT')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')

    if username == None and email == None and password == None:
        return redirect('/login')
    
    else:
        return render_template('dashboard.html', username=username, email=email, password=password)

@app.route('/about')
def about():

    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')

    return render_template('conocenos.html',username=username, email=email,password=password)
    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/account')
def account():
    return render_template('registro.html', SERVER_ADD=SERVER_ADD, SERVER_PORT=SERVER_PORT)

@app.route('/token')
def token():
    email = request.args.get('email')
    password = request.args.get('password')

    url = f'http://{SERVER_ADD}:{SERVER_PORT}/api/token'
    myobj = {'email': email, 'password': password}

    req = requests.post(url, data = myobj)

    data= json.loads(req.text)
    print(data)

    if data['error']:
        return 'Error. No estas iniciado en sesion'

    else:
        return render_template('token.html', nombre=data['nombre'], apellido=data['apellido'], email=data['email'], company=data['company'], address=data['address'], token=data['token'], password=data['password'])

@app.route('/gentoken')
def gentoken():
    email = request.args.get('email')
    password = request.args.get('password')

    print(email, password)

    url = f'http://{SERVER_ADD}:{SERVER_PORT}/api/gentoken'
    myobj = {'email': email, 'password': password}

    req = requests.post(url, data=myobj)

    data= json.loads(req.text)
    print(data)

    if data['error']:
        return {'error': 'No estas iniciado en sesion', 'message': data['message']}

    else:
        return redirect(f'token?email={email}&password={password}')

@app.route('/inventory')
def inventory(): 

    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')

    data = requests.get(f'http://{SERVER_ADD}:{SERVER_PORT}/api/inventario/hosts/admin/admin')
   # return render_template('inventario_host.html', data= data.text)

    return render_template('inventario_host.html', data = json.loads(data.text),username=username, password=password, email=email)

@app.route('/devices')
def net_devices():
    data = requests.get(f'http://{SERVER_ADD}:{SERVER_PORT}/api/inventario/dispositivos-de-red/admin/admin')

    return render_template('inventario_dispositivos_red.html', data = json.loads(data.text))

@app.route('/tracer')
def tracer():
    return render_template('formulario.html')

@app.route('/tracer_search', methods = ['POST'])
def tracer_search():
    source_node = request.form.get('source_node')
    destination_node = request.form.get('destination_node') 
    print(destination_node)
    print(source_node)

    url = f'http://{SERVER_ADD}:{SERVER_PORT}/api/trazar-post'
    myobj = {'source_node': source_node, 'destination_node': destination_node}

    req = requests.post(url, data = myobj)

    data = json.loads(req.text)
    print(data)

    if data['success']:
        return render_template('rutas.html', data=data)
    
    else:
        return 'Error. Ja!'

@app.route('/auth/', methods=['POST'])
def auth():
    email = request.form.get('email')
    password = request.form.get('password')

    url = f'http://{SERVER_ADD}:{SERVER_PORT}/api/login'
    myobj = {'email': email, 'password': password}
    print(myobj)

    req = requests.post(url, data = myobj)

    data = json.loads(req.text)
    print(data)
    
    if data['exito']:
        username = data['username']
        email = data['email']
        password = data['password']

        return redirect(url_for('dashboard', username=username, email=email, password=password)) 
    
    else:
        return redirect('/login')


@app.route('/signup', methods=['POST'])
def signup():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    password = request.form.get('password')
    company = request.form.get('company')
    Address = request.form.get('Address')

    url = f'http://{SERVER_ADD}:{SERVER_PORT}/api/signup'
    myobj = {'nombre': nombre, 'apellido': apellido, 'email': email, 'password': password, 'company': company, 'Address': Address}

    req = requests.post(url, data = myobj)

    data = json.loads(req.text)

    if data['success']:
        return redirect('/dashboard')

    else:
        return redirect('/login')
    

    


if __name__ == '__name__':
    app.run()
