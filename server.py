from flask import Flask, request, redirect, render_template
from mysqlconnection import connectToMySQL
app = Flask (__name__)

@app.route('/dojos')
def index():
    dojos_db = connectToMySQL('dojos_and_ninja').query_db('SELECT dojos.name as dojo, dojos.id as dojo_id FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id;')
    return render_template('index.html', dojo_template=dojos_db)

@app.route('/ninjas')
def new_ninja():
    dojos_db = connectToMySQL('dojos_and_ninja').query_db('SELECT dojos.name as dojo, dojos.id as dojo_id FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id;')
    return render_template('new_ninja.html', dojo_template=dojos_db)

@app.route('/dojos/<dojo_id>')
def dojo(dojo_id):
    query = 'SELECT ninjas.first_name as first,ninjas.last_name as last,ninjas.age as age,dojos.name as name FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id=%(dojo_id)s;'
    data = {
        'dojo_id': dojo_id
    }
    dojo_db = connectToMySQL('dojos_and_ninja').query_db(query,data)
    dojo_db_name = dojo_db[0]['name']
    return render_template('dojo.html', dojo_template=dojo_db, dojo_name=dojo_db_name)

@app.route('/dojos/add', methods=['POST'])
def new_dojo():
    query = 'INSERT INTO dojos(name) VALUES(%(dojo_name)s);'
    data = {
        'dojo_name': request.form['dojo_name']
    }
    connectToMySQL('dojos_and_ninja').query_db(query,data)
    return redirect('/dojos')

@app.route('/dojos/add/ninja', methods=['POST'])
def add_new_ninja():
    query = 'INSERT INTO ninjas(first_name,last_name,age,dojo_id) VALUES(%(first_name)s,%(last_name)s,%(age)s,%(dojo_id)s);'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age'],
        'dojo_id': request.form['dojo']
    }
    connectToMySQL('dojos_and_ninja').query_db(query,data)
    return redirect('/dojos/'+request.form['dojo'])

if __name__ == '__main__':
    app.run(debug=True)