# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'cadastro.db'),
    SECRET_KEY='senha-secreta',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#########################################


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        db = get_db()
        db.execute('insert into membro (nome, matricula, telefone, email, senha) values (?, ?, ?, ?, ?)', 
                    [request.form['nome'], request.form['matricula'], request.form['telefone'], request.form['email'], request.form['senha']])
        db.commit()
    db.close()           
    flash('New entry was successfully posted')
    return redirect(url_for('list'))

@app.route('/list')
def list():
    db = get_db()
    cur = db.execute('select * from membro order by id asc')
    rows = cur.fetchall()
    return render_template('lista_cadastrados.html', rows=rows)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')